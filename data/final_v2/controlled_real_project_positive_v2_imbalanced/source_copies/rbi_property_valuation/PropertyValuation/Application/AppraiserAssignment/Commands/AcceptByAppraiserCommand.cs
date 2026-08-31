using MediatR;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.AppraiserAssignment.Commands;

public sealed record AcceptByAppraiserCommand(int OrderId) : ICommand<SendToAppraiserResultDto>;

public sealed class AcceptByAppraiserCommandHandler
    : IRequestHandler<AcceptByAppraiserCommand, SendToAppraiserResultDto>
{
    private readonly IAppraiserAssignmentService _service;
    public AcceptByAppraiserCommandHandler(IAppraiserAssignmentService service) => _service = service;
    public Task<SendToAppraiserResultDto> Handle(AcceptByAppraiserCommand command, CancellationToken ct)
        => _service.AcceptByAppraiserAsync(command.OrderId, ct);
}
