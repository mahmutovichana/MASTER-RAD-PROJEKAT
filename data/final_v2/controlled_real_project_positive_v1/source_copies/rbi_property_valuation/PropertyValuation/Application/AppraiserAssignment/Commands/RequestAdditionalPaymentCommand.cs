using MediatR;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.AppraiserAssignment.Commands;

public sealed record RequestAdditionalPaymentCommand(int OrderId) : ICommand<SendToAppraiserResultDto>;

public sealed class RequestAdditionalPaymentCommandHandler
    : IRequestHandler<RequestAdditionalPaymentCommand, SendToAppraiserResultDto>
{
    private readonly IAppraiserAssignmentService _service;
    public RequestAdditionalPaymentCommandHandler(IAppraiserAssignmentService service) => _service = service;
    public Task<SendToAppraiserResultDto> Handle(RequestAdditionalPaymentCommand command, CancellationToken ct)
        => _service.RequestAdditionalPaymentAsync(command.OrderId, ct);
}
