﻿using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Appraisers;
using RBBH.CollateralAppraisal.Domain.Appraisers;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Appraisers;

/// <summary>
/// FL automatski odabir vještaka (Faza C).
/// Kandidati: aktivni, nisu na GO, nisu na blacklisti. Filter po gradu narudžbe —
/// ako 0 kandidata u gradu, proširi na sve gradove. Limit aktivnih procjena:
/// Firma &lt; 5, Individualni &lt; 2. Sortiranje: broj aktivnih procjena pa Id (deterministićko).
/// </summary>
[ExcludeFromCodeCoverage]
public sealed class AppraiserSelectionService : IAppraiserSelectionService
{
    private readonly ApplicationDbContext _db;

    public AppraiserSelectionService(ApplicationDbContext db)
    {
        _db = db;
    }

    public async Task<Appraiser?> SelectForOrderAsync(
        AppraisalOrder order,
        IReadOnlyList<int>? excludeAppraiserIds = null,
        CancellationToken ct = default)
    {
        var candidates = await _db.Appraisers
            .AsNoTracking()
            .Where(a => a.IsActive && !a.IsBlacklisted && !a.IsOnLeave)
            .ToListAsync(ct);

        // FL/PL matching — samo vještaci koji smiju procjenjivati vrstu klijenta narudžbe.
        candidates = candidates.Where(a => a.CanHandle(order.WorkflowType)).ToList();

        // Iskljući vještake koji su već odbili ili prekoraćili rok za ovu narudžbu.
        if (excludeAppraiserIds is { Count: > 0 })
            candidates = candidates.Where(a => !excludeAppraiserIds.Contains(a.Id)).ToList();

        if (candidates.Count == 0)
            return null;

        // Parametar 2 — tip nekretnine: vještak mora pokrivati tip kolaterala narudžbe.
        var propertyTypeCode = await ResolvePropertyTypeCodeAsync(order.CollateralTypeId, ct);
        if (!string.IsNullOrWhiteSpace(propertyTypeCode))
            candidates = candidates.Where(a => a.CanHandlePropertyType(propertyTypeCode)).ToList();

        if (candidates.Count == 0)
            return null;

        if (!string.IsNullOrWhiteSpace(order.City))
        {
            var inCity = candidates
                .Where(a => a.CanHandleCity(order.City))
                .ToList();

            if (inCity.Count > 0)
                candidates = inCity;
        }

        var activeCounts = await _db.AppraisalOrders
            .Where(o => o.AppraiserId != null && AppraisalOrderStatusGroups.ActiveAppraisalStatuses.Contains(o.Status))
            .GroupBy(o => o.AppraiserId!.Value)
            .Select(g => new { AppraiserId = g.Key, Count = g.Count() })
            .ToDictionaryAsync(x => x.AppraiserId, x => x.Count, ct);

        var eligible = candidates
            .Select(a => new
            {
                Appraiser = a,
                ActiveCount = activeCounts.TryGetValue(a.Id, out var c) ? c : 0
            })
            .Where(x => x.Appraiser.LegalForm == AppraiserLegalForm.Firm
                ? x.ActiveCount < 5
                : x.ActiveCount < 2)
            .OrderBy(x => x.ActiveCount)
            .ThenBy(x => x.Appraiser.Id)
            .ToList();

        return eligible.Count > 0 ? eligible[0].Appraiser : null;
    }

    private async Task<string?> ResolvePropertyTypeCodeAsync(int? collateralTypeId, CancellationToken ct)
    {
        if (collateralTypeId is null) return null;
        return await _db.CodebookValues
            .AsNoTracking()
            .Where(v => v.Id == collateralTypeId.Value)
            .Select(v => v.Code)
            .FirstOrDefaultAsync(ct);
    }
}
