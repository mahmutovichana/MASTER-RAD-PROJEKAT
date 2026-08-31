using FluentValidation;
using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.QuoteRequests.Commands;

public sealed record SendQuoteRequestsCommand(
    int OrderId,
    IReadOnlyList<int> AppraiserIds,
    DateTime Deadline) : ICommand<SendQuoteRequestsResult>;

public sealed class SendQuoteRequestsCommandHandler
    : IRequestHandler<SendQuoteRequestsCommand, SendQuoteRequestsResult>
{
    private readonly IQuoteRequestService _service;
    public SendQuoteRequestsCommandHandler(IQuoteRequestService service) => _service = service;
    public Task<SendQuoteRequestsResult> Handle(SendQuoteRequestsCommand command, CancellationToken ct)
        => _service.SendQuoteRequestsAsync(
            command.OrderId,
            new SendQuoteRequestsInput(command.AppraiserIds, command.Deadline),
            ct);
}

public sealed class SendQuoteRequestsCommandValidator
    : AbstractValidator<SendQuoteRequestsCommand>
{
    public SendQuoteRequestsCommandValidator()
    {
        RuleFor(x => x.OrderId).GreaterThan(0).WithMessage("ID narudžbe je nevažeći.");
        RuleFor(x => x.AppraiserIds)
            .NotEmpty().WithMessage("Potrebno je odabrati barem jednog vještaka.")
            .Must(ids => ids.All(id => id > 0)).WithMessage("Svi ID-evi vještaka moraju biti važeći.");
        RuleFor(x => x.Deadline)
            .GreaterThan(DateTime.UtcNow).WithMessage("Rok mora biti u budućnosti.");
    }
}
