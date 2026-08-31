﻿﻿﻿using System.Collections.Concurrent;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Codebooks.Import;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Infrastructure.Codebooks.Import.Mappers;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Codebooks.Import;

[ExcludeFromCodeCoverage]
public sealed class CodebookImportExportService : ICodebookImportExportService
{
    private readonly ApplicationDbContext _db;
    private readonly ICurrentUserService _currentUser;
    private readonly IAuditService _audit;
    private readonly ILogger<CodebookImportExportService> _logger;
    private readonly Dictionary<string, ICodebookMapper> _mappers;

    private static readonly ConcurrentDictionary<Guid, PendingImport> _pendingImports = new();
    // Legacy: _previewCache korišten u staroj implementaciji (bytes → confirm). Ostaje prazan.
    private static readonly ConcurrentDictionary<Guid, (string Type, byte[] Content, string FileName, ImportMode Mode)> _previewCache = new();
    // Novi dict: kešira završeni ImportResult za vještake (import se izvršava na preview koraku).
    // TTL = 30 minuta (korisnik potvrdi ili zatvori dijalog u tom periodu).
    private static readonly ConcurrentDictionary<Guid, ImportResult> _vjesticiResults = new();

    public CodebookImportExportService(
        ApplicationDbContext db,
        ICurrentUserService currentUser,
        IAuditService audit,
        IEnumerable<ICodebookMapper> mappers,
        ILogger<CodebookImportExportService> logger)
    {
        _db          = db;
        _currentUser = currentUser;
        _audit       = audit;
        _logger      = logger;
        _mappers     = mappers.ToDictionary(m => m.CodebookType, StringComparer.OrdinalIgnoreCase);
    }

    public IReadOnlyList<string> SupportedCodebookTypes => _mappers.Keys.ToList();

    // â"€â"€ Preview â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

    public async Task<ImportPreviewResult> PreviewImportAsync(
        ImportPreviewRequest request, CancellationToken ct = default)
    {
        var mapper = GetMapper(request.CodebookType);

        // Specijalni path za multi-sheet format (vještaci — svaki sheet = jedan vještak).
        //
        // DIZAJN: import se izvršava odmah pri PreviewImportAsync (ne čeka Confirm).
        // Razlog: _previewCache je in-memory static dict koji se gubi pri restartu servera
        // (hot-reload, docker restart). Za vještake nema smisla čuvati bajte do Confirma jer:
        //   1. Uvijek je upsert (idempotentno — ponovna primjena daje isti rezultat)
        //   2. Preview za vještake inače samo broji sheetove, ne validira podatke
        //   3. Gubitak tokena = "Preview token je istekao" greška za korisnika
        //
        // Na Confirm korak vraćamo keširan ImportResult (token = ključ u _previewCache).
        if (mapper.CodebookType == "vjestaci" && IsMultiSheetExcel(request.FileContent, request.FileName))
        {
            request.FileContent.Position = 0;
            using var ms = new MemoryStream();
            await request.FileContent.CopyToAsync(ms, ct);
            var bytes = ms.ToArray();

            // Pokreni import ODMAH (ne čeka Confirm)
            using var importStream = new MemoryStream(bytes);
            var (created, updated, skipped, errors) = await AppraiserMapper.ImportFromMultiSheetAsync(
                importStream, _db, _currentUser.UserId, ct);

            var resultMsg = $"Import završen: {created} kreirano, {updated} ažurirano, {skipped} preskoćeno.";
            if (errors.Count > 0)
            {
                resultMsg += $"\n\n{errors.Count} greška(e):\n"
                    + string.Join("\n", errors.Take(20).Select((e, i) => $"  {i + 1}. {e}"));
                if (errors.Count > 20) resultMsg += $"\n  ... i još {errors.Count - 20} grešaka.";
            }

            var importResult = new ImportResult("vjestaci", created, updated, skipped, 0, resultMsg);

            // Keširaj ImportResult (ne bytes) — na Confirm samo vraćamo ovaj rezultat
            var previewToken = Guid.NewGuid();
            _vjesticiResults[previewToken] = importResult;

            await RecordAuditAsync("CODEBOOK_IMPORTED", "vjestaci",
                new { Added = created, Updated = updated, Skipped = skipped, Errors = errors.Count }, ct);

            // Preview prikaz: koliko je obrađeno i koliko grešaka
            var totalSheets = created + updated + skipped;
            var errorEntries = errors.Take(50).Select((e, i) => new ImportRowError(i + 1, "Sheet", e)).ToList();
            return new ImportPreviewResult("vjestaci", request.FileName,
                totalSheets, created, updated, skipped, errors.Count, errorEntries, previewToken);
        }

        var (rows, parseErrors) = FileParser.Parse(request.FileContent, request.FileName, mapper.Columns);

        if (parseErrors.Count > 0)
            return new ImportPreviewResult(request.CodebookType, request.FileName,
                0, 0, 0, 0, parseErrors.Count, parseErrors, Guid.Empty);

        var ctx = BuildContext();
        var allErrors = new List<ImportRowError>();
        int newCount = 0, updateCount = 0, skipCount = 0;

        var dupKeyCol = mapper.DuplicateKeyColumn;
        var seenKeys = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var row in rows)
        {
            if (dupKeyCol is not null)
            {
                var key = row.Get(dupKeyCol) ?? "";
                if (!string.IsNullOrEmpty(key) && !seenKeys.Add(key))
                {
                    allErrors.Add(new(row.RowNumber, dupKeyCol, $"Duplikat u fajlu: '{key}'."));
                    continue;
                }
            }

            var rowErrors = await mapper.ValidateRowAsync(row, ctx, ct);
            if (rowErrors.Count > 0)
            {
                allErrors.AddRange(rowErrors);
                continue;
            }

            var action = await mapper.ClassifyRowAsync(row, ctx, ct);
            switch (request.Mode)
            {
                case ImportMode.AddNewOnly when action == RowAction.Update:
                    skipCount++;
                    break;
                case ImportMode.UpdateExistingOnly when action == RowAction.New:
                    skipCount++;
                    break;
                default:
                    if (action == RowAction.New) newCount++;
                    else updateCount++;
                    break;
            }
        }

        var token = Guid.NewGuid();
        if (allErrors.Count == 0)
        {
            _pendingImports[token] = new PendingImport(request.CodebookType, request.Mode, rows,
                DateTime.UtcNow.AddMinutes(15));
        }

        await RecordAuditAsync("CODEBOOK_IMPORT_PREVIEWED", request.CodebookType,
            new { request.FileName, TotalRows = rows.Count, newCount, updateCount, skipCount, ErrorCount = allErrors.Count }, ct);

        return new ImportPreviewResult(request.CodebookType, request.FileName,
            rows.Count, newCount, updateCount, skipCount, allErrors.Count, allErrors, token);
    }

    // â"€â"€ Confirm â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

    public async Task<ImportResult> ConfirmImportAsync(
        ImportConfirmRequest request, CancellationToken ct = default)
    {
        // Vještaci: import je već izvršen pri Preview — samo vrati keširan rezultat.
        if (_vjesticiResults.TryRemove(request.PreviewToken, out var cached))
            return cached;

        // Legacy path: _previewCache (bytes čuvani za confirm) — može biti prazan.
        // Ostaje radi kompatibilnosti s eventualnim starim tokenom u sesiji.
        if (_previewCache.TryRemove(request.PreviewToken, out var oldCached))
        {
            using var ms = new MemoryStream(oldCached.Content);
            var (created, updated, skipped, errors) = await AppraiserMapper.ImportFromMultiSheetAsync(
                ms, _db, _currentUser.UserId, ct);
            var msg = $"Import završen: {created} kreirano, {updated} ažurirano, {skipped} preskoćeno.";
            if (errors.Count > 0)
            {
                msg += $"\n\n{errors.Count} greška(e):\n"
                    + string.Join("\n", errors.Take(20).Select((e, i) => $"  {i + 1}. {e}"));
                if (errors.Count > 20)
                    msg += $"\n  ... i još {errors.Count - 20} grešaka.";
            }
            return new ImportResult(oldCached.Type, created, updated, skipped, 0, msg);
        }

        if (!_pendingImports.TryRemove(request.PreviewToken, out var pending))
            throw new ConflictException(
                "Preview token je istekao ili nije validan. Ponovite preview.",
                "IMPORT_TOKEN_INVALID");

        if (pending.ExpiresAt < DateTime.UtcNow)
            throw new ConflictException("Preview je istekao (15 min). Ponovite upload.", "IMPORT_TOKEN_EXPIRED");

        var mapper = GetMapper(pending.CodebookType);
        var ctx = BuildContext();

        await using var tx = await _db.Database.BeginTransactionAsync(ct);
        try
        {
            int added = 0, updated = 0, skipped = 0;

            foreach (var row in pending.Rows)
            {
                var action = await mapper.ClassifyRowAsync(row, ctx, ct);

                var shouldSkip = pending.Mode switch
                {
                    ImportMode.AddNewOnly => action == RowAction.Update,
                    ImportMode.UpdateExistingOnly => action == RowAction.New,
                    _ => false
                };

                if (shouldSkip) { skipped++; continue; }

                await mapper.ApplyRowAsync(row, action, ctx, ct);
                if (action == RowAction.New) added++; else updated++;
            }

            // Flush remaining batch items (ProtocolOrderMapper)
            if (ctx.Cache.TryGetValue("_pendingProtocols", out var pendingProto)
                && pendingProto is List<(Domain.Orders.AppraisalOrder, int, int)> protoList && protoList.Count > 0)
            {
                await ProtocolOrderMapper.FlushBatchAsync(_db, protoList, ctx.UserId, DateTime.UtcNow, ct);
            }

            int deactivated = 0;
            if (pending.Mode == ImportMode.DeactivateMissing)
                deactivated = await mapper.DeactivateMissingAsync(pending.Rows, ctx, ct);

            await _db.SaveChangesAsync(ct);
            await tx.CommitAsync(ct);

            await RecordAuditAsync("CODEBOOK_IMPORTED", pending.CodebookType,
                new { Added = added, Updated = updated, Skipped = skipped, Deactivated = deactivated }, ct);

            return new ImportResult(pending.CodebookType, added, updated, skipped, deactivated,
                $"Import završen: {added} dodano, {updated} ažurirano, {skipped} preskoćeno, {deactivated} deaktivirano.");
        }
        catch (Exception ex)
        {
            await tx.RollbackAsync(ct);
            _logger.LogError(ex, "Import sifarnika {Type} nije uspio - rollback.", pending.CodebookType);

            await RecordAuditAsync("CODEBOOK_IMPORT_FAILED", pending.CodebookType,
                new { Error = ex.Message }, ct);

            throw new ConflictException(
                "Import nije uspio. Sve promjene su poništene (rollback).",
                "IMPORT_FAILED");
        }
    }

    // â"€â"€ Export â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

    public async Task<ExportResult> ExportAsync(ExportRequest request, CancellationToken ct = default)
    {
        var mapper = GetMapper(request.CodebookType);
        var ctx = BuildContext();
        var rows = await mapper.ExportRowsAsync(request.IncludeInactive, ctx, ct);
        var result = FileExporter.Export(mapper.Columns, rows, request.CodebookType, request.Format);

        await RecordAuditAsync("CODEBOOK_EXPORTED", request.CodebookType,
            new { Format = request.Format.ToString(), RowCount = rows.Count, request.IncludeInactive }, ct);

        return result;
    }

    // â"€â"€ Helpers â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

    private ICodebookMapper GetMapper(string codebookType) =>
        _mappers.GetValueOrDefault(codebookType)
        ?? throw new NotFoundException($"Šifarnik '{codebookType}' nije podržan za import/export.", "CODEBOOK_TYPE_NOT_FOUND");

    private ImportContext BuildContext() => new()
    {
        DbContext = _db,
        UserId = _currentUser.IsAuthenticated ? _currentUser.UserId : null
    };

    private async Task RecordAuditAsync(string action, string codebookType, object details, CancellationToken ct)
    {
        try
        {
            await _audit.RecordAsync(new AuditEvent
            {
                Action            = action,
                OperationType     = action.Contains("EXPORT") ? AuditOperationTypes.Read : AuditOperationTypes.Create,
                Module            = AuditModules.Codebooks,
                EntityType        = "Codebook",
                EntityKey         = codebookType,
                EntityDisplayName = codebookType,
                NewValues         = details,
                Status            = action.Contains("FAILED") ? AuditStatuses.Failed : AuditStatuses.Success,
                Severity          = action.Contains("FAILED") ? AuditSeverity.Warning : AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Audit za {Action} šifarnika {Type} nije zapisan.", action, codebookType);
        }
    }

    private static bool IsMultiSheetExcel(Stream content, string fileName)
    {
        var ext = Path.GetExtension(fileName).ToLowerInvariant();
        if (ext is not ".xlsx" and not ".xls") return false;
        try
        {
            content.Position = 0;
            using var wb = new ClosedXML.Excel.XLWorkbook(content);
            return wb.Worksheets.Count > 1;
        }
        catch { return false; }
        finally { content.Position = 0; }
    }

    private sealed record PendingImport(
        string CodebookType, ImportMode Mode, IReadOnlyList<ParsedRow> Rows, DateTime ExpiresAt);
}
