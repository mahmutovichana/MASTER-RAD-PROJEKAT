using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Requests;

namespace RBBH.CollateralAppraisal.Application.Orders.Queries;

public sealed record GetOrdersListQuery(OrderListRequest Request) : IQuery<PagedResult<AppraisalOrderListItemDto>>;

public sealed class GetOrdersListQueryHandler
    : IRequestHandler<GetOrdersListQuery, PagedResult<AppraisalOrderListItemDto>>
{
    private readonly IOrderQueryService _service;
    public GetOrdersListQueryHandler(IOrderQueryService service) => _service = service;
    public Task<PagedResult<AppraisalOrderListItemDto>> Handle(GetOrdersListQuery query, CancellationToken ct)
        => _service.GetListAsync(query.Request, ct);
}
