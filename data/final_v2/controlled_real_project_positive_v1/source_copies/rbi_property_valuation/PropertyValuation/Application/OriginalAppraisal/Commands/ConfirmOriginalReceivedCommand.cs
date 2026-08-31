using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;

namespace RBBH.CollateralAppraisal.Application.OriginalAppraisal.Commands;

public sealed record ConfirmOriginalReceivedCommand(int OrderId) : ICommand<OriginalReceivedResultDto>;

public sealed class ConfirmOriginalReceivedCommandHandler
    : IRequestHandler<ConfirmOriginalReceivedCommand, OriginalReceivedResultDto>
{
    private readonly IOriginalAppraisalService _service;
    public ConfirmOriginalReceivedCommandHandler(IOriginalAppraisalService service) => _service = service;
    public Task<OriginalReceivedResultDto> Handle(ConfirmOriginalReceivedCommand command, CancellationToken ct)
        => _service.ConfirmOriginalReceivedAsync(command.OrderId, ct);
}
