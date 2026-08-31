using MediatR;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.AppraiserAssignment.Queries;

public sealed record GetCandidatesForOrderQuery(int OrderId) : IQuery<IReadOnlyList<AppraiserDto>>;

public sealed class GetCandidatesForOrderQueryHandler
    : IRequestHandler<GetCandidatesForOrderQuery, IReadOnlyList<AppraiserDto>>
{
    private readonly IAppraiserAssignmentService _service;
    public GetCandidatesForOrderQueryHandler(IAppraiserAssignmentService service) => _service = service;
    public Task<IReadOnlyList<AppraiserDto>> Handle(GetCandidatesForOrderQuery query, CancellationToken ct)
        => _service.GetCandidatesForOrderAsync(query.OrderId, ct);
}
