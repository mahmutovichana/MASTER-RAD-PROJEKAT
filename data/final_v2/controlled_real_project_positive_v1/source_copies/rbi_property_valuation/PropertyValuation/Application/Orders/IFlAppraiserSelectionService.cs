using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;

namespace RBBH.CollateralAppraisal.Application.Orders;

/// <summary>
/// FL workflow: automatski algoritamski odabir vještaka.
/// Separiran iz IAppraiserAssignmentService (I-2 refactoring) da bi
/// FlAppraiserAssignmentService mogao biti manja, fokusirana klasa.
/// </summary>
public interface IFlAppraiserSelectionService
{
    /// <summary>
    /// FL narudžba — automatski algoritamski odabir vještaka prema
    /// dostupnosti, blacklisti, aktivnim zadacima i gradu nekretnine.
    /// </summary>
    Task<AppraiserAssignmentResultDto> AutoSelectAppraiserAsync(int orderId, CancellationToken ct = default);
}
