using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.QuoteRequests.Commands;

public sealed record SendThankYouCommand(int OrderId) : ICommand<SendThankYouResult>;

public sealed class SendThankYouCommandHandler : IRequestHandler<SendThankYouCommand, SendThankYouResult>
{
    private readonly IQuoteRequestService _service;
    public SendThankYouCommandHandler(IQuoteRequestService service) => _service = service;
    public Task<SendThankYouResult> Handle(SendThankYouCommand command, CancellationToken ct)
        => _service.SendThankYouAsync(command.OrderId, ct);
}
