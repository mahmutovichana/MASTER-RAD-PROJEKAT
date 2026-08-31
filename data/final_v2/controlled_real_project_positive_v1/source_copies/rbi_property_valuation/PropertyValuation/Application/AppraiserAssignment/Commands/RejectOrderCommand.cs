using FluentValidation;
using MediatR;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.AppraiserAssignment.Commands;

public sealed record RejectOrderCommand(
    int     OrderId,
    string  RejectionReason,
    string? RejectionComment = null) : ICommand<SendToAppraiserResultDto>;

public sealed class RejectOrderCommandHandler
    : IRequestHandler<RejectOrderCommand, SendToAppraiserResultDto>
{
    private readonly IAppraiserAssignmentService _service;
    public RejectOrderCommandHandler(IAppraiserAssignmentService service) => _service = service;
    public Task<SendToAppraiserResultDto> Handle(RejectOrderCommand cmd, CancellationToken ct)
        => _service.RejectOrderAsync(cmd.OrderId, cmd.RejectionReason, cmd.RejectionComment, ct);
}

public sealed class RejectOrderCommandValidator : AbstractValidator<RejectOrderCommand>
{
    public RejectOrderCommandValidator()
    {
        RuleFor(x => x.OrderId).GreaterThan(0).WithMessage("ID narudžbe je nevažeći.");
        RuleFor(x => x.RejectionReason)
            .NotEmpty().WithMessage("Razlog odbijanja je obavezan.")
            .MaximumLength(500).WithMessage("Razlog odbijanja ne smije biti duži od 500 znakova.");
    }
}
