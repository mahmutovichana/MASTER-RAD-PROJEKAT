using MediatR;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.AppraiserAssignment.Commands;

public sealed record ConfirmAdditionalPaymentCommand(int OrderId) : ICommand<SendToAppraiserResultDto>;

public sealed class ConfirmAdditionalPaymentCommandHandler
    : IRequestHandler<ConfirmAdditionalPaymentCommand, SendToAppraiserResultDto>
{
    private readonly IAppraiserAssignmentService _service;
    public ConfirmAdditionalPaymentCommandHandler(IAppraiserAssignmentService service) => _service = service;
    public Task<SendToAppraiserResultDto> Handle(ConfirmAdditionalPaymentCommand command, CancellationToken ct)
        => _service.ConfirmAdditionalPaymentAsync(command.OrderId, ct);
}
