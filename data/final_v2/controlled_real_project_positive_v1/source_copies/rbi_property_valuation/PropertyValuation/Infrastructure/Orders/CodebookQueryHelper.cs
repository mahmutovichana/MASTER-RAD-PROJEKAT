using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

internal static class CodebookQueryHelper
{
    public static async Task<string> GetLabelAsync(ApplicationDbContext db, int id, CancellationToken ct)
    {
        var value = await db.CodebookValues.FindAsync([id], ct);
        return value?.Label ?? string.Empty;
    }
}
