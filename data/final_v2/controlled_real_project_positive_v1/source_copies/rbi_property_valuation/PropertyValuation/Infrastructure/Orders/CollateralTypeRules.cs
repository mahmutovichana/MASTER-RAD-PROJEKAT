using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

/// <summary>
/// Pravilo za grananje CA "Završi pregled" (US-93): ako je kolateral isključivo stan
/// (bez kombinacije sa garažom/ostavom), CO provjera pristupa se preskače.
/// </summary>
public static class CollateralTypeRules
{
    public const string ApartmentCode = Application.Common.Constants.CollateralTypeCodes.Apartment;
    public const string ApartmentLegacyCode = Application.Common.Constants.CollateralTypeCodes.ApartmentLegacy;

    public static async Task<bool> IsApartmentOnlyAsync(ApplicationDbContext db, AppraisalOrder order, CancellationToken ct)
    {
        if (order.CombinedCollateralTypeId is not null) return false;
        if (order.CollateralTypeId is null) return false;

        var code = await db.CodebookValues.AsNoTracking()
            .Where(x => x.Id == order.CollateralTypeId.Value)
            .Select(x => x.Code)
            .FirstOrDefaultAsync(ct);

        return code is ApartmentCode or ApartmentLegacyCode;
    }
}
