using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Application.Orders;

/// <summary>
/// Kombinirani interfejs za odabir i lifecycle vještaka.
/// Extenduje tri fokusirana sub-interfejsa (I-2 refactoring):
///   - IFlAppraiserSelectionService   (FL automatski odabir)
///   - IPlAppraiserSelectionService   (PL ručni odabir)
///   - IAppraiserOrderLifecycleService (post-selekcijski lifecycle)
///
/// Handlers i servisi koji trebaju CIJELU funkcionalnost injectuju ovaj interfejs.
/// Oni koji trebaju samo podskup (npr. FL selekciju) mogu injectovati sub-interfejs.
/// </summary>
public interface IAppraiserAssignmentService
    : IFlAppraiserSelectionService,
      IPlAppraiserSelectionService,
      IAppraiserOrderLifecycleService
{
    // Sve metode su nasljeđene iz sub-interfejsa.
    // AppraiserAssignmentService implementira ovaj kombinirani interfejs.
}
