using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Requests;

namespace RBBH.CollateralAppraisal.Application.Orders.Interfaces;

/// <summary>
/// Kreiranje novih narudžbi — puna narudžba i draft.
/// Sub-interfejs od IAppraisalOrderService (I-1 refactoring).
/// </summary>
public interface IOrderCreateService
{
    /// <summary>Kreira novu narudžbu direktno (Draft → odmah s podacima).</summary>
    Task<AppraisalOrderDto> CreateAsync(CreateOrderRequest request, CancellationToken ct = default);

    /// <summary>Kreira prazan draft koji se popunjava autosave-om iz UI-a.</summary>
    Task<AppraisalOrderDto> CreateDraftAsync(string? workflowType = null, CancellationToken ct = default);

    /// <summary>Ažurira draft narudžbu (parcijalni update, podržava autosave).</summary>
    Task<AppraisalOrderDto> UpdateDraftAsync(int id, UpdateOrderRequest request, bool isAutosave = false, CancellationToken ct = default);
}
