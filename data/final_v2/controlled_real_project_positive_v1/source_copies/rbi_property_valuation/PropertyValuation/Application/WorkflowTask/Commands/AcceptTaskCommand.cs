using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;

namespace RBBH.CollateralAppraisal.Application.WorkflowTask.Commands;

public sealed record AcceptTaskCommand(int TaskId) : ICommand<WorkflowTaskDto>;

public sealed class AcceptTaskCommandHandler : IRequestHandler<AcceptTaskCommand, WorkflowTaskDto>
{
    private readonly IWorkflowTaskService _service;
    public AcceptTaskCommandHandler(IWorkflowTaskService service) => _service = service;
    public Task<WorkflowTaskDto> Handle(AcceptTaskCommand command, CancellationToken ct)
        => _service.AcceptTaskAsync(command.TaskId, ct);
}
