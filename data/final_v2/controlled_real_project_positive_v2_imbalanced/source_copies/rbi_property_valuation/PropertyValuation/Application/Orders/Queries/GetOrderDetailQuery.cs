using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;

namespace RBBH.CollateralAppraisal.Application.Orders.Queries;

public sealed record GetOrderDetailQuery(int OrderId) : IQuery<AppraisalOrderDetailDto>;

public sealed class GetOrderDetailQueryHandler : IRequestHandler<GetOrderDetailQuery, AppraisalOrderDetailDto>
{
    private readonly IOrderQueryService _service;
    public GetOrderDetailQueryHandler(IOrderQueryService service) => _service = service;
    public Task<AppraisalOrderDetailDto> Handle(GetOrderDetailQuery query, CancellationToken ct)
        => _service.GetByIdAsync(query.OrderId, ct);
}
