using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;

namespace RBBH.CollateralAppraisal.Application.OriginalAppraisal.Commands;

public sealed record SendAppraiserReminderCommand(int OrderId) : ICommand<AppraiserReminderResultDto>;

public sealed class SendAppraiserReminderCommandHandler
    : IRequestHandler<SendAppraiserReminderCommand, AppraiserReminderResultDto>
{
    private readonly IOriginalAppraisalService _service;
    public SendAppraiserReminderCommandHandler(IOriginalAppraisalService service) => _service = service;
    public Task<AppraiserReminderResultDto> Handle(SendAppraiserReminderCommand command, CancellationToken ct)
        => _service.SendAppraiserReminderAsync(command.OrderId, ct);
}
