using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;

namespace RBBH.CollateralAppraisal.Application.WorkflowTask.Commands;

public sealed record CompleteTaskCommand(int TaskId, string? Comment) : ICommand<WorkflowTaskDto>;

public sealed class CompleteTaskCommandHandler : IRequestHandler<CompleteTaskCommand, WorkflowTaskDto>
{
    private readonly IWorkflowTaskService _service;
    public CompleteTaskCommandHandler(IWorkflowTaskService service) => _service = service;
    public Task<WorkflowTaskDto> Handle(CompleteTaskCommand command, CancellationToken ct)
        => _service.CompleteTaskAsync(command.TaskId, command.Comment, ct);
}
