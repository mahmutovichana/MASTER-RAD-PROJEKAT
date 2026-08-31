using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Codebooks;
using RBBH.CollateralAppraisal.Application.Codebooks.Interfaces;
using RBBH.CollateralAppraisal.Application.Codebooks.Models;
using RBBH.CollateralAppraisal.Application.Codebooks.Requests;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Codebooks;

/// <summary>
/// Upravljanje šifarnicima (Codebook container) — kreiranje, ažuriranje, deaktivacija, soft delete.
/// Odvojeno od CodebookValueService koji upravlja vrijednostima unutar šifarnika.
///
/// Prava: samo Administrator (codebooks.manage permission).
/// Audit: svaka mutacija evidentira se putem IAuditService.
/// </summary>
public sealed class CodebookService : ICodebookService
{
    private readonly ApplicationDbContext    _db;
    private readonly ICurrentUserService    _currentUser;
    private readonly IAuditService          _auditService;
    private readonly ILogger<CodebookService> _logger;

    public CodebookService(
        ApplicationDbContext     db,
        ICurrentUserService     currentUser,
        IAuditService           auditService,
        ILogger<CodebookService> logger)
    {
        _db          = db;
        _currentUser = currentUser;
        _auditService = auditService;
        _logger       = logger;
    }

    // ── Čitanje ───────────────────────────────────────────────────────────────

    public async Task<PagedResult<CodebookListItemDto>> GetAllAsync(
        CodebookQueryRequest request, CancellationToken ct = default)
    {
        var query = _db.Codebooks.AsNoTracking().AsQueryable();

        // ── Filteri ───────────────────────────────────────────────────────────
        if (!string.IsNullOrWhiteSpace(request.Search))
        {
            var s = request.Search.Trim().ToLower();
            query = query.Where(c =>
                c.Code.ToLower().Contains(s) ||
                c.Name.ToLower().Contains(s) ||
                (c.Description != null && c.Description.ToLower().Contains(s)));
        }

        if (request.IsActive.HasValue)
            query = query.Where(c => c.IsActive == request.IsActive.Value);

        if (request.IsSystem.HasValue)
            query = query.Where(c => c.IsSystem == request.IsSystem.Value);

        if (!string.IsNullOrWhiteSpace(request.Category))
            query = query.Where(c => c.Category == request.Category);

        // ── Sortiranje ────────────────────────────────────────────────────────
        query = (request.SortBy?.ToLowerInvariant(), request.SortAsc) switch
        {
            ("code",      true)  => query.OrderBy(c => c.Code),
            ("code",      false) => query.OrderByDescending(c => c.Code),
            ("createdat", true)  => query.OrderBy(c => c.CreatedAt),
            ("createdat", false) => query.OrderByDescending(c => c.CreatedAt),
            ("updatedat", true)  => query.OrderBy(c => c.UpdatedAt),
            ("updatedat", false) => query.OrderByDescending(c => c.UpdatedAt),
            (_,           true)  => query.OrderBy(c => c.Name),
            (_,           false) => query.OrderByDescending(c => c.Name),
        };

        var total = await query.CountAsync(ct);
        var page  = Math.Max(1, request.Page);
        var size  = Math.Clamp(request.PageSize, 1, 200);

        // Broj vrijednosti — LEFT JOIN agregacija
        var codebookCodes = await query
            .Skip((page - 1) * size)
            .Take(size)
            .Select(c => c.Code)
            .ToListAsync(ct);

        // Dohvati broj vrijednosti za svaki šifarnik (ukupno i aktivnih)
        var valueCounts = await _db.CodebookValues
            .AsNoTracking()
            .Where(v => codebookCodes.Contains(v.CodebookKey))
            .GroupBy(v => v.CodebookKey)
            .Select(g => new
            {
                Key         = g.Key,
                Total       = g.Count(),
                ActiveCount = g.Count(v => v.IsActive)
            })
            .ToDictionaryAsync(x => x.Key, ct);

        var codebooks = await query
            .Skip((page - 1) * size)
            .Take(size)
            .ToListAsync(ct);

        var items = codebooks.Select(c =>
        {
            valueCounts.TryGetValue(c.Code, out var vc);
            return new CodebookListItemDto(
                c.Id,
                c.Code,
                c.Name,
                c.Description,
                c.Category,
                c.IsActive,
                c.IsSystem,
                vc?.Total ?? 0,
                vc?.ActiveCount ?? 0,
                c.CreatedAt,
                c.UpdatedAt,
                c.UpdatedByUserId);
        }).ToList();

        return new PagedResult<CodebookListItemDto>
        {
            Items      = items,
            TotalCount = total,
            Page       = page,
            PageSize   = size
        };
    }

    public async Task<CodebookDto?> GetByCodeAsync(string code, CancellationToken ct = default)
    {
        var c = await _db.Codebooks.AsNoTracking()
            .FirstOrDefaultAsync(x => x.Code == code, ct);

        if (c is null) return null;

        var valueCount = await _db.CodebookValues.AsNoTracking()
            .CountAsync(v => v.CodebookKey == code, ct);

        return ToDto(c, valueCount);
    }

    // ── Kreiranje ─────────────────────────────────────────────────────────────

    public async Task<CodebookDto> CreateAsync(
        CreateCodebookRequest request, CancellationToken ct = default)
    {
        ValidateCode(request.Code);
        ValidateName(request.Name);

        var duplicate = await _db.Codebooks
            .AnyAsync(c => c.Code == request.Code.Trim(), ct);
        if (duplicate)
            throw new ConflictException(
                $"Šifarnik s kodom '{request.Code}' već postoji.",
                CodebookErrorCodes.CodebookDuplicateCode);

        var entity = Codebook.CreateCustom(
            code:            request.Code.Trim().ToLowerInvariant(),
            name:            request.Name.Trim(),
            description:     request.Description?.Trim(),
            category:        request.Category?.Trim(),
            createdByUserId: _currentUser.UserId);

        _db.Codebooks.Add(entity);
        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(AuditActions.CodebookCreated, entity,
            AuditOperationTypes.Create, null,
            new { entity.Code, entity.Name, entity.Category },
            AuditStatuses.Success, AuditSeverity.Info, ct);

        return ToDto(entity, 0);
    }

    // ── Ažuriranje ────────────────────────────────────────────────────────────

    public async Task<CodebookDto> UpdateAsync(
        string code, UpdateCodebookRequest request, CancellationToken ct = default)
    {
        ValidateName(request.Name);

        var entity = await FindOrThrowAsync(code, ct);
        var oldValues = new { entity.Name, entity.Description, entity.Category };
        var now = DateTime.UtcNow;

        entity.Update(request.Name.Trim(), request.Description?.Trim(), request.Category?.Trim(),
            _currentUser.UserId, now);

        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(AuditActions.CodebookUpdated, entity,
            AuditOperationTypes.Update, oldValues,
            new { entity.Name, entity.Description, entity.Category },
            AuditStatuses.Success, AuditSeverity.Info, ct);

        var valueCount = await _db.CodebookValues.AsNoTracking()
            .CountAsync(v => v.CodebookKey == code, ct);
        return ToDto(entity, valueCount);
    }

    // ── Deaktivacija / Aktivacija ─────────────────────────────────────────────

    public async Task<CodebookDto> DeactivateAsync(string code, CancellationToken ct = default)
    {
        var entity = await FindOrThrowAsync(code, ct);

        if (!entity.IsActive)
            throw new ConflictException(
                "Šifarnik je već neaktivan.", CodebookErrorCodes.CodebookAlreadyInactive);

        var now = DateTime.UtcNow;
        entity.Deactivate(_currentUser.UserId, now);
        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(AuditActions.CodebookDeactivated, entity,
            AuditOperationTypes.Update,
            new { IsActive = true }, new { IsActive = false },
            AuditStatuses.Success, AuditSeverity.Warning, ct);

        var valueCount = await _db.CodebookValues.AsNoTracking()
            .CountAsync(v => v.CodebookKey == code, ct);
        return ToDto(entity, valueCount);
    }

    public async Task<CodebookDto> ActivateAsync(string code, CancellationToken ct = default)
    {
        var entity = await FindOrThrowAsync(code, ct);

        if (entity.IsActive)
            throw new ConflictException(
                "Šifarnik je već aktivan.", CodebookErrorCodes.CodebookAlreadyActive);

        entity.Activate(_currentUser.UserId, DateTime.UtcNow);
        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(AuditActions.CodebookActivated, entity,
            AuditOperationTypes.Update,
            new { IsActive = false }, new { IsActive = true },
            AuditStatuses.Success, AuditSeverity.Info, ct);

        var valueCount = await _db.CodebookValues.AsNoTracking()
            .CountAsync(v => v.CodebookKey == code, ct);
        return ToDto(entity, valueCount);
    }

    // ── Brisanje (soft delete) ────────────────────────────────────────────────

    public async Task DeleteAsync(string code, CancellationToken ct = default)
    {
        var entity = await FindOrThrowAsync(code, ct);

        if (entity.IsSystem)
        {
            await RecordAuditAsync(AuditActions.CodebookDeleteBlockedInUse, entity,
                AuditOperationTypes.Delete, null, null,
                AuditStatuses.Conflict, AuditSeverity.Warning, ct,
                reason: "Sistemski šifarnik ne može biti obrisan.");

            throw new ConflictException(
                "Sistemski šifarnici ne mogu biti fizički obrisani.",
                CodebookErrorCodes.CodebookSystemLocked);
        }

        // Provjeri da li šifarnik ima aktivne vrijednosti
        var activeValues = await _db.CodebookValues
            .CountAsync(v => v.CodebookKey == code && v.IsActive, ct);
        if (activeValues > 0)
        {
            await RecordAuditAsync(AuditActions.CodebookDeleteBlockedInUse, entity,
                AuditOperationTypes.Delete, null,
                new { ActiveValueCount = activeValues },
                AuditStatuses.Conflict, AuditSeverity.Warning, ct,
                reason: $"Šifarnik ima {activeValues} aktivnih vrijednosti.");

            throw new ConflictException(
                $"Nije moguće obrisati šifarnik koji ima {activeValues} aktivnih vrijednosti. Deaktivirajte ih prvo.",
                CodebookErrorCodes.CodebookHasActiveValues);
        }

        entity.SoftDelete(_currentUser.UserId, DateTime.UtcNow);
        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(AuditActions.CodebookDeleted, entity,
            AuditOperationTypes.Delete, null, null,
            AuditStatuses.Success, AuditSeverity.Warning, ct);
    }

    // ── Pomoćne metode ────────────────────────────────────────────────────────

    private async Task<Codebook> FindOrThrowAsync(string code, CancellationToken ct)
    {
        return await _db.Codebooks.FirstOrDefaultAsync(c => c.Code == code, ct)
            ?? throw new NotFoundException(
                $"Šifarnik s kodom '{code}' nije pronađen.",
                CodebookErrorCodes.CodebookNotFound);
    }

    private static CodebookDto ToDto(Codebook c, int valueCount) => new(
        c.Id, c.Code, c.Name, c.Description, c.Category,
        c.IsActive, c.IsSystem, valueCount,
        c.CreatedAt, c.CreatedByUserId, c.UpdatedAt, c.UpdatedByUserId);

    private static void ValidateCode(string code)
    {
        if (string.IsNullOrWhiteSpace(code))
            throw new Application.Common.Exceptions.ValidationException(
                [new Application.Common.Models.ValidationFieldError("code", "REQUIRED_FIELD", "Kod šifarnika je obavezan.")]);

        if (code.Length > 100)
            throw new Application.Common.Exceptions.ValidationException(
                [new Application.Common.Models.ValidationFieldError("code", "MAX_LENGTH_EXCEEDED", "Kod šifarnika ne smije biti duži od 100 znakova.")]);

        if (!System.Text.RegularExpressions.Regex.IsMatch(code, @"^[a-zA-Z0-9_\-]+$"))
            throw new Application.Common.Exceptions.ValidationException(
                [new Application.Common.Models.ValidationFieldError("code", "INVALID_FORMAT", "Kod može sadržavati samo slova, cifre, _ i -.")]);
    }

    private static void ValidateName(string name)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new Application.Common.Exceptions.ValidationException(
                [new Application.Common.Models.ValidationFieldError("name", "REQUIRED_FIELD", "Naziv šifarnika je obavezan.")]);

        if (name.Length > 250)
            throw new Application.Common.Exceptions.ValidationException(
                [new Application.Common.Models.ValidationFieldError("name", "MAX_LENGTH_EXCEEDED", "Naziv ne smije biti duži od 250 znakova.")]);
    }

    private async Task RecordAuditAsync(
        string action, Codebook entity, string operationType,
        object? oldValues, object? newValues,
        string status, string severity, CancellationToken ct,
        string? reason = null)
    {
        try
        {
            await _auditService.RecordAsync(new AuditEvent
            {
                Action            = action,
                OperationType     = operationType,
                Module            = AuditModules.Codebooks,
                EntityType        = "Codebook",
                EntityKey         = entity.Code,
                EntityDisplayName = entity.Name,
                OldValues         = oldValues,
                NewValues         = newValues,
                Status            = status,
                Severity          = severity,
                Reason            = reason
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Audit nije zapisan za akciju {Action} na šifarniku {Code}.", action, entity.Code);
        }
    }
}
