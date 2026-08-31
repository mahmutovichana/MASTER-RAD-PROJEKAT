using FluentValidation;
using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.OrderApproval.Commands;

public sealed record ReturnForReworkCommand(
    int OrderId,
    string Category,
    string Comment) : ICommand<ReturnForReworkResultDto>;

public sealed class ReturnForReworkCommandHandler
    : IRequestHandler<ReturnForReworkCommand, ReturnForReworkResultDto>
{
    private readonly IOrderApprovalService _service;
    public ReturnForReworkCommandHandler(IOrderApprovalService service) => _service = service;
    public Task<ReturnForReworkResultDto> Handle(ReturnForReworkCommand command, CancellationToken ct)
        => _service.ReturnForReworkAsync(command.OrderId, command.Category, command.Comment, ct);
}

public sealed class ReturnForReworkCommandValidator : AbstractValidator<ReturnForReworkCommand>
{
    public ReturnForReworkCommandValidator()
    {
        RuleFor(x => x.OrderId).GreaterThan(0).WithMessage("ID narudžbe je nevažeći.");
        RuleFor(x => x.Category).NotEmpty().WithMessage("Kategorija povrata je obavezna.");
        RuleFor(x => x.Comment).NotEmpty().WithMessage("Komentar je obavezan pri povratu na doradu.")
            .MaximumLength(2000).WithMessage("Komentar ne smije prelaziti 2000 znakova.");
    }
}
