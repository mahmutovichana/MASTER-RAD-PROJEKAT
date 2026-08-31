using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;

namespace RBBH.CollateralAppraisal.Application.OrderApproval.Queries;

public sealed record GetFinalAppraisalQuery(int OrderId) : IQuery<FinalAppraisalDto>;

public sealed class GetFinalAppraisalQueryHandler : IRequestHandler<GetFinalAppraisalQuery, FinalAppraisalDto>
{
    private readonly IOrderApprovalService _service;
    public GetFinalAppraisalQueryHandler(IOrderApprovalService service) => _service = service;
    public Task<FinalAppraisalDto> Handle(GetFinalAppraisalQuery query, CancellationToken ct)
        => _service.GetFinalAppraisalAsync(query.OrderId, ct);
}
