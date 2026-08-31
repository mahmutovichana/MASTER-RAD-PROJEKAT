using MediatR;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.AppraiserAssignment.Commands;

public sealed record SubmitAppraisalCommand(int OrderId, DateTime? VisitDate = null)
    : ICommand<SendToAppraiserResultDto>;

public sealed class SubmitAppraisalCommandHandler
    : IRequestHandler<SubmitAppraisalCommand, SendToAppraiserResultDto>
{
    private readonly IAppraiserAssignmentService _service;
    public SubmitAppraisalCommandHandler(IAppraiserAssignmentService service) => _service = service;
    public Task<SendToAppraiserResultDto> Handle(SubmitAppraisalCommand command, CancellationToken ct)
        => _service.SubmitAppraisalAsync(command.OrderId, command.VisitDate, ct);
}
