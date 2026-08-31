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
using RBBH.CollateralAppraisal.Application.Common.Validation;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Codebooks;

/// <summary>
/// Implementacija poslovnih pravila za upravljanje vrijednostima šifarnika.
/// Poslovna pravila su ovdje, ne u endpointima.
/// </summary>
public sealed class CodebookValueService : ICodebookValueService
{
    private readonly ApplicationDbContext      _db;
    private readonly ICurrentUserService       _currentUser;
    private readonly ICodebookUsageService     _usageService;
    private readonly ICodebookCacheInvalidator _cache;
    private readonly IAuditService             _auditService;
    private readonly ILogger<CodebookValueService> _logger;

    public CodebookValueService(
        ApplicationDbContext          db,
        ICurrentUserService           currentUser,
        ICodebookUsageService         usageService,
        ICodebookCacheInvalidator     cache,
        IAuditService                 auditService,
        ILogger<CodebookValueService> logger)
    {
        _db           = db;
        _currentUser  = currentUser;
        _usageService = usageService;
        _cache        = cache;
        _auditService = auditService;
        _logger       = logger;
    }

    // ── Kreiranje i uređivanje ────────────────────────────────────────────────

    public async Task<CodebookValueDto> CreateAsync(
        string codebookKey, CreateCodebookValueRequest request, CancellationToken ct = default)
    {
        var errors = ValidateCreateRequest(request);
        if (errors.Count > 0)
            throw new ValidationException(errors);

        var duplicate = await _db.CodebookValues
            .AnyAsync(x => x.CodebookKey == codebookKey && x.Code == request.Code, ct);
        if (duplicate)
            throw new ConflictException(
                $"Vrijednost s kodom '{request.Code}' već postoji u šifarniku '{codebookKey}'.",
                CodebookErrorCodes.DuplicateCode);

        var entity = CodebookValue.Create(
            codebookKey,
            request.Code,
            request.Label,
            request.Description,
            request.SortOrder,
            _currentUser.UserId);

        _db.CodebookValues.Add(entity);
        try
        {
            await _db.SaveChangesAsync(ct);
        }
        catch (DbUpdateException ex)
            when (ex.InnerException is Microsoft.Data.SqlClient.SqlException sql && sql.Number is 2601 or 2627)
        {
            // Souběžan zahtjev je uspio ubaciti isti Code između naše provjere i inserta
            throw new ConflictException(
                $"Vrijednost s kodom '{request.Code}' već postoji u šifarniku '{codebookKey}'.",
                CodebookErrorCodes.DuplicateCode);
        }

        await RecordAuditAsync(
            AuditActions.CodebookEntryCreated,
            AuditOperationTypes.Create, entity,
            newValues: new { entity.Code, entity.Label, entity.SortOrder },
            status: AuditStatuses.Success, ct: ct);

        await InvalidateCacheAsync(codebookKey, ct);

        return ToDto(entity);
    }

    public async Task<CodebookValueDto> UpdateAsync(
        string codebookKey, int id, UpdateCodebookValueRequest request, CancellationToken ct = default)
    {
        var errors = ValidateUpdateRequest(request);
        if (errors.Count > 0)
            throw new ValidationException(errors);

        var entity = await FindOrThrowAsync(codebookKey, id, ct);

        var oldValues = new { entity.Label, entity.Description, entity.SortOrder };
        var now = DateTime.UtcNow;
        entity.UpdateDetails(request.Label, request.Description, request.SortOrder, _currentUser.UserId, now);

        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(
            AuditActions.CodebookEntryUpdated,
            AuditOperationTypes.Update, entity,
            oldValues: oldValues,
            newValues: new { request.Label, request.Description, request.SortOrder },
            status: AuditStatuses.Success, ct: ct);

        await InvalidateCacheAsync(codebookKey, ct);

        return ToDto(entity);
    }

    // ── Čitanje ───────────────────────────────────────────────────────────────

    public async Task<IReadOnlyList<CodebookOptionDto>> GetActiveAsync(
        string codebookKey, CancellationToken ct = default)
    {
        // Dropdown: samo aktivne, neobrisane vrijednosti — globalni query filter isključuje deleted
        return await _db.CodebookValues
            .AsNoTracking()
            .Where(x => x.CodebookKey == codebookKey && x.IsActive)
            .OrderBy(x => x.SortOrder).ThenBy(x => x.Label)
            .Select(x => new CodebookOptionDto(x.Id, x.Code, x.Label, x.SortOrder, x.Description))
            .ToListAsync(ct);
    }

    public async Task<IReadOnlyList<CodebookValueDto>> GetAllAsync(
        string codebookKey, CancellationToken ct = default)
    {
        // Admin: aktivne + neaktivne, bez soft-deleted (globalni query filter)
        // Inline projekcija — EF Core prevodi direktno u SQL bez materijalizacije entiteta
        return await _db.CodebookValues
            .AsNoTracking()
            .Where(x => x.CodebookKey == codebookKey)
            .OrderBy(x => x.SortOrder).ThenBy(x => x.Label)
            .Select(x => new CodebookValueDto(
                x.Id, x.CodebookKey, x.Code, x.Label, x.Description, x.SortOrder,
                x.IsActive, x.IsSystem, x.IsCritical,
                x.CreatedAt, x.CreatedByUserId, x.UpdatedAt, x.UpdatedByUserId,
                x.DeactivatedAt, x.DeactivatedByUserId, x.DeactivationReason))
            .ToListAsync(ct);
    }

    public async Task<CodebookValueDto> GetByIdAsync(
        string codebookKey, int id, CancellationToken ct = default)
    {
        var entity = await FindOrThrowAsync(codebookKey, id, ct);
        return ToDto(entity);
    }

    // ── Usage check ───────────────────────────────────────────────────────────

    public async Task<CodebookUsageResult> CheckUsageAsync(
        string codebookKey, int id, CancellationToken ct = default)
    {
        // Validirati da vrijednost postoji prije usage checka
        _ = await FindOrThrowAsync(codebookKey, id, ct);
        return await _usageService.CheckUsageAsync(codebookKey, id, ct);
    }

    // ── Mutacije ──────────────────────────────────────────────────────────────

    public async Task<CodebookValueDto> DeactivateAsync(
        string codebookKey, int id, DeactivateCodebookValueRequest request, CancellationToken ct = default)
    {
        var entity = await FindOrThrowAsync(codebookKey, id, ct);

        // Vrijednost je već neaktivna — jasna greška radi transparentnosti
        if (!entity.IsActive)
            throw new ConflictException(
                "Vrijednost šifarnika je već neaktivna.",
                CodebookErrorCodes.ValueAlreadyInactive);

        // Kritična sistemska vrijednost ne smije biti deaktivirana
        if (entity.IsCritical)
        {
            await RecordAuditAsync(
                AuditActions.CodebookValueCriticalDeactivationBlocked,
                AuditOperationTypes.Update, entity,
                status: AuditStatuses.Conflict, severity: AuditSeverity.Warning, ct: ct);

            throw new ConflictException(
                "Kritična sistemska vrijednost ne smije biti deaktivirana.",
                CodebookErrorCodes.CriticalLocked);
        }

        var now = DateTime.UtcNow;
        entity.Deactivate(now, _currentUser.UserId, request.Reason);

        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(
            AuditActions.CodebookEntryDeactivated,
            AuditOperationTypes.Update, entity,
            oldValues: new { IsActive = true },
            newValues: new { IsActive = false, DeactivatedAt = now, Reason = request.Reason },
            status: AuditStatuses.Success, ct: ct);

        await InvalidateCacheAsync(codebookKey, ct);

        return ToDto(entity);
    }

    public async Task<CodebookValueDto> ActivateAsync(
        string codebookKey, int id, CancellationToken ct = default)
    {
        var entity = await FindOrThrowAsync(codebookKey, id, ct);

        // Vrijednost je već aktivna
        if (entity.IsActive)
            throw new ConflictException(
                "Vrijednost šifarnika je već aktivna.",
                CodebookErrorCodes.ValueAlreadyActive);

        var now = DateTime.UtcNow;
        entity.Activate(now, _currentUser.UserId);

        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(
            AuditActions.CodebookValueActivated,
            AuditOperationTypes.Update, entity,
            oldValues: new { IsActive = false },
            newValues: new { IsActive = true },
            status: AuditStatuses.Success, ct: ct);

        await InvalidateCacheAsync(codebookKey, ct);

        return ToDto(entity);
    }

    public async Task DeleteAsync(
        string codebookKey, int id, CancellationToken ct = default)
    {
        var entity = await FindOrThrowAsync(codebookKey, id, ct);

        await EnsureCanDeleteAsync(codebookKey, id, entity, ct);

        // Fizičko brisanje dozvoljavamo samo kada vrijednost nije referencirana,
        // kako postojeći zapisi ne bi izgubili značenje historijskih podataka.
        var now = DateTime.UtcNow;
        entity.SoftDelete(now, _currentUser.UserId);

        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(
            AuditActions.CodebookValueDeleted,
            AuditOperationTypes.Delete, entity,
            status: AuditStatuses.Success, ct: ct);

        await InvalidateCacheAsync(codebookKey, ct);
    }

    /// <summary>
    /// Provjerava sva poslovna pravila koja blokiraju brisanje.
    /// Baca ConflictException s odgovarajućim kodom ako brisanje nije dozvoljeno.
    /// </summary>
    private async Task EnsureCanDeleteAsync(
        string codebookKey, int id, CodebookValue entity, CancellationToken ct)
    {
        if (entity.IsSystem)
        {
            await RecordAuditAsync(
                AuditActions.CodebookValueSystemDeleteBlocked,
                AuditOperationTypes.Delete, entity,
                status: AuditStatuses.Conflict, severity: AuditSeverity.Warning, ct: ct);

            throw new ConflictException(
                "Sistemske vrijednosti šifarnika ne mogu se brisati.",
                CodebookErrorCodes.SystemLocked);
        }

        if (entity.IsCritical)
        {
            await RecordAuditAsync(
                AuditActions.CodebookValueCriticalDeleteBlocked,
                AuditOperationTypes.Delete, entity,
                status: AuditStatuses.Conflict, severity: AuditSeverity.Warning, ct: ct);

            throw new ConflictException(
                "Kritična vrijednost šifarnika ne može se brisati.",
                CodebookErrorCodes.CriticalLocked);
        }

        // Usage check ponavljamo ovdje jer se stanje moglo promijeniti
        // nakon što je frontend ranije pozvao GET /usage endpoint
        CodebookUsageResult usage;
        try
        {
            usage = await _usageService.CheckUsageAsync(codebookKey, id, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Usage check pao za CodebookValue {Id} ({Key}). Brisanje blokirano (fail-safe).",
                id, codebookKey);

            await RecordAuditAsync(
                AuditActions.CodebookValueDeleteBlockedUsageCheckFailed,
                AuditOperationTypes.Delete, entity,
                status: AuditStatuses.Failed, severity: AuditSeverity.Warning, ct: ct);

            throw new ConflictException(
                "Provjera upotrebe nije uspjela. Brisanje je blokirano iz sigurnosnih razloga.",
                CodebookErrorCodes.UsageCheckFailed);
        }

        if (!usage.IsReliable)
        {
            await RecordAuditAsync(
                AuditActions.CodebookValueDeleteBlockedUsageCheckFailed,
                AuditOperationTypes.Delete, entity,
                status: AuditStatuses.Failed, severity: AuditSeverity.Warning, ct: ct);

            throw new ConflictException(
                "Provjera upotrebe nije bila pouzdana. Brisanje je blokirano.",
                CodebookErrorCodes.UsageCheckFailed);
        }

        if (usage.IsInUse)
        {
            await RecordAuditAsync(
                AuditActions.CodebookValueDeleteBlockedInUse,
                AuditOperationTypes.Delete, entity,
                newValues: new { usage.UsageCount, usage.Locations },
                status: AuditStatuses.Conflict, severity: AuditSeverity.Warning, ct: ct);

            throw new ConflictException(
                $"Vrijednost se koristi u {usage.UsageCount} zapisa i ne može se fizički obrisati. " +
                "Preporučena akcija: deaktivacija.",
                CodebookErrorCodes.ValueInUse);
        }
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    private async Task<CodebookValue> FindOrThrowAsync(string codebookKey, int id, CancellationToken ct)
    {
        // Globalni query filter automatski isključuje soft-deleted zapise
        // Provjera codebookKey-a je dio upita — pogrešan key tretiramo kao 404 (security)
        var entity = await _db.CodebookValues
            .FirstOrDefaultAsync(x => x.Id == id && x.CodebookKey == codebookKey, ct);

        if (entity is null)
            throw new NotFoundException(
                $"Vrijednost šifarnika ID={id} nije pronađena u šifarniku '{codebookKey}'.",
                CodebookErrorCodes.ValueNotFound);

        return entity;
    }

    private async Task RecordAuditAsync(
        string        action,
        string        operationType,
        CodebookValue entity,
        object?       oldValues  = null,
        object?       newValues  = null,
        string        status     = AuditStatuses.Success,
        string        severity   = AuditSeverity.Info,
        CancellationToken ct     = default)
    {
        try
        {
            await _auditService.RecordAsync(new AuditEvent
            {
                Action            = action,
                OperationType     = operationType,
                Module            = AuditModules.Codebooks,
                EntityType        = nameof(CodebookValue),
                EntityKey         = entity.Id.ToString(),
                EntityDisplayName = $"{entity.CodebookKey} / {entity.Code} — {entity.Label}",
                OldValues         = oldValues,
                NewValues         = newValues,
                Status            = status,
                Severity          = severity
            }, ct);
        }
        catch (Exception ex)
        {
            // Greška u audit logu ne smije srušiti poslovnu operaciju
            _logger.LogError(ex,
                "Audit log nije zapisan za akciju {Action} na CodebookValue {Id}.",
                action, entity.Id);
        }
    }

    private async Task InvalidateCacheAsync(string codebookKey, CancellationToken ct)
    {
        try
        {
            await _cache.InvalidateAsync(codebookKey, ct);
        }
        catch (Exception ex)
        {
            // Cache invalidacija ne smije se tiho ignorisati — dropdown može pokazivati stare podatke
            _logger.LogError(ex,
                "Cache invalidacija nije uspjela za codebookKey={Key}. " +
                "Dropdown može prikazivati zastarjele vrijednosti.",
                codebookKey);
        }
    }

    private static IReadOnlyList<ValidationFieldError> ValidateCreateRequest(CreateCodebookValueRequest req)
    {
        var errors = new List<ValidationFieldError>();

        if (string.IsNullOrWhiteSpace(req.Code))
            errors.Add(new ValidationFieldError("code", ValidationErrorCodes.RequiredField, "Kod je obavezan."));
        else if (req.Code.Length > 100)
            errors.Add(new ValidationFieldError("code", ValidationErrorCodes.MaxLengthExceeded, "Kod ne smije biti duži od 100 znakova."));
        else if (!req.Code.All(c => char.IsLetterOrDigit(c) || c == '_' || c == '-'))
            errors.Add(new ValidationFieldError("code", ValidationErrorCodes.InvalidCodeFormat, "Kod smije sadržavati samo slova, cifre, underscore (_) i crticu (-)."));

        if (string.IsNullOrWhiteSpace(req.Label))
            errors.Add(new ValidationFieldError("label", ValidationErrorCodes.RequiredField, "Naziv je obavezan."));
        else if (req.Label.Length > 300)
            errors.Add(new ValidationFieldError("label", ValidationErrorCodes.MaxLengthExceeded, "Naziv ne smije biti duži od 300 znakova."));

        if (req.Description?.Length > 1000)
            errors.Add(new ValidationFieldError("description", ValidationErrorCodes.MaxLengthExceeded, "Opis ne smije biti duži od 1000 znakova."));

        if (req.SortOrder < 0)
            errors.Add(new ValidationFieldError("sortOrder", ValidationErrorCodes.InvalidInput, "Redoslijed ne smije biti negativan."));

        return errors;
    }

    private static IReadOnlyList<ValidationFieldError> ValidateUpdateRequest(UpdateCodebookValueRequest req)
    {
        var errors = new List<ValidationFieldError>();

        if (string.IsNullOrWhiteSpace(req.Label))
            errors.Add(new ValidationFieldError("label", ValidationErrorCodes.RequiredField, "Naziv je obavezan."));
        else if (req.Label.Length > 300)
            errors.Add(new ValidationFieldError("label", ValidationErrorCodes.MaxLengthExceeded, "Naziv ne smije biti duži od 300 znakova."));

        if (req.Description?.Length > 1000)
            errors.Add(new ValidationFieldError("description", ValidationErrorCodes.MaxLengthExceeded, "Opis ne smije biti duži od 1000 znakova."));

        if (req.SortOrder < 0)
            errors.Add(new ValidationFieldError("sortOrder", ValidationErrorCodes.InvalidInput, "Redoslijed ne smije biti negativan."));

        return errors;
    }

    private static CodebookValueDto ToDto(CodebookValue x) => new(
        x.Id, x.CodebookKey, x.Code, x.Label, x.Description, x.SortOrder,
        x.IsActive, x.IsSystem, x.IsCritical,
        x.CreatedAt, x.CreatedByUserId, x.UpdatedAt, x.UpdatedByUserId,
        x.DeactivatedAt, x.DeactivatedByUserId, x.DeactivationReason);
}
