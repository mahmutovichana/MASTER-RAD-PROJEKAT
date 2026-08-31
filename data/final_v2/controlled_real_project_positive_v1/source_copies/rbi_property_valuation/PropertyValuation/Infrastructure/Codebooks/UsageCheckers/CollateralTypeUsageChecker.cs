using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Codebooks.Interfaces;
using RBBH.CollateralAppraisal.Application.Codebooks.Models;
using RBBH.CollateralAppraisal.Application.Common.Constants;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Codebooks.UsageCheckers;

public sealed class CollateralTypeUsageChecker : ICodebookUsageChecker
{
    private readonly ApplicationDbContext _db;
    public CollateralTypeUsageChecker(ApplicationDbContext db) => _db = db;

    public string CodebookKey => CodebookKeys.CollateralTypes;

    public async Task<CodebookUsageLocation?> CheckAsync(int valueId, CancellationToken ct = default)
    {
        var count = await _db.AppraisalOrders
            .IgnoreQueryFilters()
            .CountAsync(o => o.CollateralTypeId == valueId || o.CombinedCollateralTypeId == valueId, ct);

        return count > 0
            ? new CodebookUsageLocation { Module = "Narudžbe", EntityName = "AppraisalOrder", Count = count }
            : null;
    }
}
