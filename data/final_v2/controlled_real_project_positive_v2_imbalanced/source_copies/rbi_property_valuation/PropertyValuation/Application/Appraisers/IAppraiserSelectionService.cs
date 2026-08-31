using RBBH.CollateralAppraisal.Domain.Appraisers;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Application.Appraisers;

/// <summary>
/// FL automatski odabir vještaka (Faza C) — grad narudžbe (s fallbackom na sve gradove),
/// najmanji broj aktivnih procjena, limit Firma&lt;5 / Individualni&lt;2.
/// </summary>
public interface IAppraiserSelectionService
{
    /// <summary>
    /// Vraća najpogodnijeg vještaka za narudžbu, ili <c>null</c> ako niko ne ispunjava uslove.
    /// <paramref name="excludeAppraiserIds"/> — isključuje vještake koji su već odbili ili prekoračili rok za ovu narudžbu.
    /// </summary>
    Task<Appraiser?> SelectForOrderAsync(
        AppraisalOrder order,
        IReadOnlyList<int>? excludeAppraiserIds = null,
        CancellationToken ct = default);
}
