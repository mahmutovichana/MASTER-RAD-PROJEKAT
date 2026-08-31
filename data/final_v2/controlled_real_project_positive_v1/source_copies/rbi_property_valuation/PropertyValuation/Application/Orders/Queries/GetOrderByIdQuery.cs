using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;

namespace RBBH.CollateralAppraisal.Application.Orders.Queries;

public sealed record GetOrderByIdQuery(int OrderId) : IQuery<AppraisalOrderDto>;

public sealed class GetOrderByIdQueryHandler : IRequestHandler<GetOrderByIdQuery, AppraisalOrderDto>
{
    private readonly IAppraisalOrderService _service;
    public GetOrderByIdQueryHandler(IAppraisalOrderService service) => _service = service;
    public Task<AppraisalOrderDto> Handle(GetOrderByIdQuery query, CancellationToken ct)
        => _service.GetByIdAsync(query.OrderId, ct);
}
