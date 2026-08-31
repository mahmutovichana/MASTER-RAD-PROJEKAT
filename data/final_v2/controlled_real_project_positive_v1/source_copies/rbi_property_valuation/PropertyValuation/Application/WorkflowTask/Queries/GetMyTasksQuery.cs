using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;

namespace RBBH.CollateralAppraisal.Application.WorkflowTask.Queries;

public sealed record GetMyTasksQuery(int Page = 1, int PageSize = 20) : IQuery<PagedResult<WorkflowTaskDto>>;

public sealed class GetMyTasksQueryHandler
    : IRequestHandler<GetMyTasksQuery, PagedResult<WorkflowTaskDto>>
{
    private readonly IWorkflowTaskService _service;
    public GetMyTasksQueryHandler(IWorkflowTaskService service) => _service = service;
    public Task<PagedResult<WorkflowTaskDto>> Handle(GetMyTasksQuery query, CancellationToken ct)
        => _service.GetMyTasksAsync(query.Page, query.PageSize, ct);
}
