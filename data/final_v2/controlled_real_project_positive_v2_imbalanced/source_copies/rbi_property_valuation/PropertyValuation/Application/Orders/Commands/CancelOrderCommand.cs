using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;

namespace RBBH.CollateralAppraisal.Application.Orders.Commands;

public sealed record CancelOrderCommand(int OrderId) : ICommand;

public sealed class CancelOrderCommandHandler : IRequestHandler<CancelOrderCommand>
{
    private readonly IAppraisalOrderService _service;
    public CancelOrderCommandHandler(IAppraisalOrderService service) => _service = service;
    public Task Handle(CancelOrderCommand command, CancellationToken ct)
        => _service.CancelAsync(command.OrderId, ct);
}
