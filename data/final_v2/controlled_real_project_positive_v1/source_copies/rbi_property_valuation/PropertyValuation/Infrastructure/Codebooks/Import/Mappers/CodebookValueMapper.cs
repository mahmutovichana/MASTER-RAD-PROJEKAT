using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Codebooks.Import;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Codebooks.Import.Mappers;

/// <summary>
/// Generićki mapper za bilo koji CodebookValue šifarnik (gradovi, poslovnice, tipovi kolaterala, itd.).
/// Instancira se sa codebook key-em.
/// </summary>
[ExcludeFromCodeCoverage]
public sealed class CodebookValueMapper : ICodebookMapper
{
    private readonly string _codebookKey;

    public CodebookValueMapper(string codebookType, string codebookKey)
    {
        CodebookType = codebookType;
        _codebookKey = codebookKey;
    }

    public string CodebookType { get; }

    public IReadOnlyList<ColumnDef> Columns =>
    [
        new("Kod", "Kod", Required: true),
        new("Naziv", "Naziv", Required: true),
        new("Opis", "Opis", Required: false),
        new("Redoslijed", "Redoslijed", Required: false),
        new("Aktivan", "Aktivan (Da/Ne)", Required: false)
    ];

    public Task<IReadOnlyList<ImportRowError>> ValidateRowAsync(ParsedRow row, ImportContext ctx, CancellationToken ct)
    {
        var errors = new List<ImportRowError>();
        if (string.IsNullOrWhiteSpace(row.Get("Kod")))
            errors.Add(new(row.RowNumber, "Kod", "Kod je obavezan."));
        if (string.IsNullOrWhiteSpace(row.Get("Naziv")))
            errors.Add(new(row.RowNumber, "Naziv", "Naziv je obavezan."));

        var sortStr = row.Get("Redoslijed");
        if (!string.IsNullOrWhiteSpace(sortStr) && !int.TryParse(sortStr, out _))
            errors.Add(new(row.RowNumber, "Redoslijed", $"'{sortStr}' nije validan broj."));

        return Task.FromResult<IReadOnlyList<ImportRowError>>(errors);
    }

    public async Task<RowAction> ClassifyRowAsync(ParsedRow row, ImportContext ctx, CancellationToken ct)
    {
        var db = (ApplicationDbContext)ctx.DbContext;
        var code = row.Get("Kod")!;
        var exists = await db.CodebookValues.AsNoTracking()
            .AnyAsync(v => v.CodebookKey == _codebookKey && v.Code == code, ct);
        return exists ? RowAction.Update : RowAction.New;
    }

    public async Task ApplyRowAsync(ParsedRow row, RowAction action, ImportContext ctx, CancellationToken ct)
    {
        var db = (ApplicationDbContext)ctx.DbContext;
        var code = row.Get("Kod")!.Trim();
        var label = row.Get("Naziv")!.Trim();
        var desc = row.Get("Opis");
        var sort = int.TryParse(row.Get("Redoslijed"), out var s) ? s : 0;
        var now = DateTime.UtcNow;

        if (action == RowAction.New)
        {
            db.CodebookValues.Add(CodebookValue.Create(
                _codebookKey, code, label, desc, sort, ctx.UserId));
        }
        else
        {
            var existing = await db.CodebookValues
                .FirstAsync(v => v.CodebookKey == _codebookKey && v.Code == code, ct);
            existing.UpdateDetails(label, desc, sort, ctx.UserId, now);

            var isActive = ParseBool(row.Get("Aktivan"), defaultVal: true);
            if (!isActive && existing.IsActive) existing.Deactivate(now, ctx.UserId, "Import: deaktivirano");
            if (isActive && !existing.IsActive) existing.Activate(now, ctx.UserId);
        }
    }

    public async Task<int> DeactivateMissingAsync(IReadOnlyList<ParsedRow> importedRows, ImportContext ctx, CancellationToken ct)
    {
        var db = (ApplicationDbContext)ctx.DbContext;
        var importedCodes = importedRows.Select(r => r.Get("Kod")!).ToHashSet(StringComparer.OrdinalIgnoreCase);
        var toDeactivate = await db.CodebookValues
            .Where(v => v.CodebookKey == _codebookKey && v.IsActive && !importedCodes.Contains(v.Code))
            .ToListAsync(ct);
        var now = DateTime.UtcNow;
        foreach (var v in toDeactivate) v.Deactivate(now, ctx.UserId, "Import: nije u fajlu");
        return toDeactivate.Count;
    }

    public async Task<IReadOnlyList<Dictionary<string, string?>>> ExportRowsAsync(
        bool includeInactive, ImportContext ctx, CancellationToken ct)
    {
        var db = (ApplicationDbContext)ctx.DbContext;
        var query = db.CodebookValues.AsNoTracking()
            .Where(v => v.CodebookKey == _codebookKey);
        if (!includeInactive) query = query.Where(v => v.IsActive);

        var list = await query.OrderBy(v => v.SortOrder).ThenBy(v => v.Label).ToListAsync(ct);
        return list.Select(v => new Dictionary<string, string?>
        {
            ["Kod"] = v.Code,
            ["Naziv"] = v.Label,
            ["Opis"] = v.Description,
            ["Redoslijed"] = v.SortOrder.ToString(),
            ["Aktivan"] = v.IsActive ? "Da" : "Ne"
        }).ToList();
    }

    private static bool ParseBool(string? value, bool defaultVal = false) => value switch
    {
        null or "" => defaultVal,
        "Da" or "da" or "DA" or "Yes" or "yes" or "1" or "true" => true,
        _ => false
    };
}
