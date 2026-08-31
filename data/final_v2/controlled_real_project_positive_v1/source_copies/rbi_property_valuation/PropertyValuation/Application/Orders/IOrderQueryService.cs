using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Requests;

namespace RBBH.CollateralAppraisal.Application.Orders;

public interface IOrderQueryService
{
    /// <summary>Vraća detalje narudžbe, s Capabilities izračunatim za trenutnog korisnika.</summary>
    Task<AppraisalOrderDetailDto> GetByIdAsync(int orderId, CancellationToken ct = default);

    /// <summary>Straničena lista narudžbi s filterima i sortiranjem.</summary>
    Task<PagedResult<AppraisalOrderListItemDto>> GetListAsync(OrderListRequest request, CancellationToken ct = default);

    /// <summary>KPI summary za dashboard — ukupan broj, drafts, u toku, završeni, otkazani.</summary>
    Task<OrderSummaryDto> GetSummaryAsync(CancellationToken ct = default);
}
