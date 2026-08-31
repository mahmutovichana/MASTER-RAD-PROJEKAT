using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.QuoteRequests.Commands;

public sealed record AcceptQuoteCommand(int OrderId, int QuoteRequestId) : ICommand<AcceptQuoteResult>;

public sealed class AcceptQuoteCommandHandler : IRequestHandler<AcceptQuoteCommand, AcceptQuoteResult>
{
    private readonly IQuoteRequestService _service;
    public AcceptQuoteCommandHandler(IQuoteRequestService service) => _service = service;
    public Task<AcceptQuoteResult> Handle(AcceptQuoteCommand command, CancellationToken ct)
        => _service.AcceptQuoteAsync(command.OrderId, command.QuoteRequestId, ct);
}
