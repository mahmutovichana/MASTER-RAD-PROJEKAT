using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;

namespace RBBH.CollateralAppraisal.Application.Orders.Commands;

public sealed record CreateDraftOrderCommand(string? WorkflowType = null) : ICommand<AppraisalOrderDto>;

public sealed class CreateDraftOrderCommandHandler : IRequestHandler<CreateDraftOrderCommand, AppraisalOrderDto>
{
    private readonly IAppraisalOrderService _service;
    public CreateDraftOrderCommandHandler(IAppraisalOrderService service) => _service = service;
    public Task<AppraisalOrderDto> Handle(CreateDraftOrderCommand command, CancellationToken ct)
        => _service.CreateDraftAsync(command.WorkflowType, ct);
}
