using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;

namespace RBBH.CollateralAppraisal.Application.Orders.Commands;

public sealed record SubmitOrderCommand(int OrderId) : ICommand<AppraisalOrderDto>;

public sealed class SubmitOrderCommandHandler : IRequestHandler<SubmitOrderCommand, AppraisalOrderDto>
{
    private readonly IAppraisalOrderService _service;
    public SubmitOrderCommandHandler(IAppraisalOrderService service) => _service = service;
    public Task<AppraisalOrderDto> Handle(SubmitOrderCommand command, CancellationToken ct)
        => _service.SubmitAsync(command.OrderId, ct);
}
