using MediatR;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.AppraiserAssignment.Queries;

public sealed record GetAppraiserPackageQuery(int OrderId) : IQuery<AppraiserPackageDto>;

public sealed class GetAppraiserPackageQueryHandler
    : IRequestHandler<GetAppraiserPackageQuery, AppraiserPackageDto>
{
    private readonly IAppraiserAssignmentService _service;
    public GetAppraiserPackageQueryHandler(IAppraiserAssignmentService service) => _service = service;
    public Task<AppraiserPackageDto> Handle(GetAppraiserPackageQuery query, CancellationToken ct)
        => _service.GetAppraiserPackageAsync(query.OrderId, ct);
}
