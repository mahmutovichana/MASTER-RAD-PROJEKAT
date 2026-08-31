using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Appraisers;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Domain.Appraisers;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Appraisers;

/// <summary>Master-data CRUD za vještake (Faza C) — koristi CA admin stranica "/sifarnici/vjestaci".</summary>
[ExcludeFromCodeCoverage]
public sealed class AppraiserService : IAppraiserService
{
    private readonly ApplicationDbContext _db;
    private readonly IAuditService        _audit;

    public AppraiserService(ApplicationDbContext db, IAuditService audit)
    {
        _db    = db;
        _audit = audit;
    }

    public async Task<PagedResult<AppraiserDto>> GetListAsync(
        int page, int pageSize, string? search = null, string? city = null,
        bool? onLeave = null, bool? blacklisted = null, bool? active = null,
        CancellationToken ct = default)
    {
        var query = _db.Appraisers.AsNoTracking().AsQueryable();

        if (!string.IsNullOrWhiteSpace(search))
        {
            var s = search.Trim().ToLower();
            query = query.Where(a => a.Name.ToLower().Contains(s)
                || (a.City != null && a.City.ToLower().Contains(s)));
        }

        if (!string.IsNullOrWhiteSpace(city))
            query = query.Where(a => a.City == city);

        if (onLeave.HasValue)
            query = query.Where(a => a.IsOnLeave == onLeave.Value);

        if (blacklisted.HasValue)
            query = query.Where(a => a.IsBlacklisted == blacklisted.Value);

        if (active.HasValue)
            query = query.Where(a => a.IsActive == active.Value);

        query = query.OrderBy(a => a.Name);

        var total = await query.CountAsync(ct);
        var pg    = Math.Max(1, page);
        var size  = Math.Clamp(pageSize, 1, 200);

        var appraisers = await query
            .Skip((pg - 1) * size)
            .Take(size)
            .ToListAsync(ct);

        var activeCounts = await GetActiveCountsAsync(ct);

        var items = appraisers
            .Select(a => ToDto(a, activeCounts.TryGetValue(a.Id, out var c) ? c : 0))
            .ToList();

        return new PagedResult<AppraiserDto>
        {
            Items      = items,
            TotalCount = total,
            Page       = pg,
            PageSize   = size
        };
    }

    public async Task<AppraiserDto> GetByIdAsync(int id, CancellationToken ct = default)
    {
        var appraiser = await FindAsync(id, ct);
        var activeCounts = await GetActiveCountsAsync(ct);

        return ToDto(appraiser, activeCounts.TryGetValue(appraiser.Id, out var c) ? c : 0);
    }

    public async Task<AppraiserDto> CreateAsync(CreateAppraiserRequest request, CancellationToken ct = default)
    {
        var legalForm = ParseLegalForm(request.LegalForm);

        var clientScope = ParseClientScope(request.ClientScope);
        var appraiser = Appraiser.Create(
            request.Name, request.City, legalForm,
            request.ContactEmail, request.ContactPhone, request.Notes,
            clientScope: clientScope,
            supportedPropertyTypes: request.SupportedPropertyTypes,
            supportedCities: request.SupportedCities);

        _db.Appraisers.Add(appraiser);
        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(AuditActions.AppraiserCreated, appraiser, ct);

        return ToDto(appraiser, 0);
    }

    public async Task<AppraiserDto> UpdateAsync(int id, UpdateAppraiserRequest request, CancellationToken ct = default)
    {
        var appraiser = await FindAsync(id, ct);
        var legalForm = ParseLegalForm(request.LegalForm);
        var now = DateTime.UtcNow;

        var clientScope = request.ClientScope is not null ? ParseClientScope(request.ClientScope) : (AppraiserClientScope?)null;
        appraiser.UpdateDetails(
            request.Name, request.City, legalForm,
            request.ContactEmail, request.ContactPhone, request.Notes, now,
            clientScope: clientScope,
            supportedPropertyTypes: request.SupportedPropertyTypes,
            supportedCities: request.SupportedCities);

        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(AuditActions.AppraiserUpdated, appraiser, ct);

        var activeCounts = await GetActiveCountsAsync(ct);
        return ToDto(appraiser, activeCounts.TryGetValue(appraiser.Id, out var c) ? c : 0);
    }

    public async Task<AppraiserDto> SetOnLeaveAsync(int id, bool value, CancellationToken ct = default)
    {
        var appraiser = await FindAsync(id, ct);
        appraiser.SetOnLeave(value, DateTime.UtcNow);
        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(AuditActions.AppraiserUpdated, appraiser, ct);

        var activeCounts = await GetActiveCountsAsync(ct);
        return ToDto(appraiser, activeCounts.TryGetValue(appraiser.Id, out var c) ? c : 0);
    }

    public async Task<AppraiserDto> SetBlacklistedAsync(int id, bool value, CancellationToken ct = default)
    {
        var appraiser = await FindAsync(id, ct);
        appraiser.SetBlacklisted(value, DateTime.UtcNow);
        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(AuditActions.AppraiserUpdated, appraiser, ct);

        var activeCounts = await GetActiveCountsAsync(ct);
        return ToDto(appraiser, activeCounts.TryGetValue(appraiser.Id, out var c) ? c : 0);
    }

    public async Task DeactivateAsync(int id, CancellationToken ct = default)
    {
        var appraiser = await FindAsync(id, ct);
        appraiser.Deactivate(DateTime.UtcNow);
        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(AuditActions.AppraiserUpdated, appraiser, ct);
    }

    // â”€â”€ Pomoćne metode â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    private async Task<Appraiser> FindAsync(int id, CancellationToken ct)
    {
        var appraiser = await _db.Appraisers.FirstOrDefaultAsync(x => x.Id == id, ct);

        if (appraiser is null)
            throw new NotFoundException($"Vještak ID={id} nije pronaÄ‘en.", "APPRAISER_NOT_FOUND");

        return appraiser;
    }

    private async Task<Dictionary<int, int>> GetActiveCountsAsync(CancellationToken ct) =>
        await _db.AppraisalOrders
            .Where(o => o.AppraiserId != null && AppraisalOrderStatusGroups.ActiveAppraisalStatuses.Contains(o.Status))
            .GroupBy(o => o.AppraiserId!.Value)
            .Select(g => new { AppraiserId = g.Key, Count = g.Count() })
            .ToDictionaryAsync(x => x.AppraiserId, x => x.Count, ct);

    private static AppraiserLegalForm ParseLegalForm(string value) =>
        Enum.TryParse<AppraiserLegalForm>(value, ignoreCase: true, out var parsed)
            ? parsed
            : throw new ValidationException("legalForm", $"Nepoznat pravni oblik vještaka: '{value}'.");

    private static AppraiserClientScope ParseClientScope(string? value) =>
        Enum.TryParse<AppraiserClientScope>(value, ignoreCase: true, out var parsed)
            ? parsed
            : AppraiserClientScope.Sve;

    private static AppraiserDto ToDto(Appraiser a, int activeCount) => new(
        a.Id, a.Name, a.City, a.LegalForm.ToString(), a.IsOnLeave, a.IsBlacklisted, a.IsActive,
        activeCount, a.ContactEmail, a.ContactPhone, a.Notes, a.SupportedPropertyTypes,
        a.CreatedAt, a.UpdatedAt,
        a.SupportedCities, a.ClientScope.ToString());

    private async Task RecordAuditAsync(string action, Appraiser appraiser, CancellationToken ct)
    {
        await _audit.RecordAsync(new AuditEvent
        {
            Action            = action,
            OperationType     = action == AuditActions.AppraiserCreated ? AuditOperationTypes.Create : AuditOperationTypes.Update,
            Module            = AuditModules.AppraisalOrders,
            EntityType        = "Appraiser",
            EntityKey         = appraiser.Id.ToString(),
            EntityDisplayName = appraiser.Name,
            NewValues         = new
            {
                appraiser.Name, appraiser.City, LegalForm = appraiser.LegalForm.ToString(),
                appraiser.IsOnLeave, appraiser.IsBlacklisted, appraiser.IsActive
            },
            Status            = AuditStatuses.Success,
            Severity          = AuditSeverity.Info
        }, ct);
    }
}
