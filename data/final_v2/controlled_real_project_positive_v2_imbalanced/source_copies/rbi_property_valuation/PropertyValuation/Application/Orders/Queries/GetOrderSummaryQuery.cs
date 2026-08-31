using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
namespace RBBH.CollateralAppraisal.Application.Orders.Queries;

public sealed record GetOrderSummaryQuery : IQuery<OrderSummaryDto>;

public sealed class GetOrderSummaryQueryHandler : IRequestHandler<GetOrderSummaryQuery, OrderSummaryDto>
{
    private readonly IOrderQueryService _service;
    public GetOrderSummaryQueryHandler(IOrderQueryService service) => _service = service;
    public Task<OrderSummaryDto> Handle(GetOrderSummaryQuery query, CancellationToken ct)
        => _service.GetSummaryAsync(ct);
}
