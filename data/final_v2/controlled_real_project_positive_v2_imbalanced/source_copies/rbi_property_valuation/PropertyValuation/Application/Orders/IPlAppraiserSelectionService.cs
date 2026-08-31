using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;

namespace RBBH.CollateralAppraisal.Application.Orders;

/// <summary>
/// PL workflow: lista kandidata i ručni odabir vještaka.
/// Separiran iz IAppraiserAssignmentService (I-2 refactoring).
/// </summary>
public interface IPlAppraiserSelectionService
{
    /// <summary>Lista vještaka pogodnih za ručni odabir (PL narudžbe ili FL fallback).</summary>
    Task<IReadOnlyList<AppraiserDto>> GetCandidatesForOrderAsync(int orderId, CancellationToken ct = default);

    /// <summary>Ručni odabir vještaka — CA bira sa liste kandidata.</summary>
    Task<AppraiserAssignmentResultDto> ManualSelectAppraiserAsync(int orderId, int appraiserId, CancellationToken ct = default);
}
