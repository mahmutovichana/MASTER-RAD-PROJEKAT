using MediatR;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.AppraiserAssignment.Commands;

public sealed record SendToAppraiserCommand(int OrderId) : ICommand<SendToAppraiserResultDto>;

public sealed class SendToAppraiserCommandHandler
    : IRequestHandler<SendToAppraiserCommand, SendToAppraiserResultDto>
{
    private readonly IAppraiserAssignmentService _service;
    public SendToAppraiserCommandHandler(IAppraiserAssignmentService service) => _service = service;
    public Task<SendToAppraiserResultDto> Handle(SendToAppraiserCommand command, CancellationToken ct)
        => _service.SendToAppraiserAsync(command.OrderId, ct);
}
