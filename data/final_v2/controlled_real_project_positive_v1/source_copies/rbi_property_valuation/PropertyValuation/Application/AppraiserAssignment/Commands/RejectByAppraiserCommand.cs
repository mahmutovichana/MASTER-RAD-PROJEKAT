using FluentValidation;
using MediatR;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Application.AppraiserAssignment.Commands;

public sealed record RejectByAppraiserCommand(
    int OrderId,
    AppraiserDeclineReason Reason,
    string? FreeText = null) : ICommand<SendToAppraiserResultDto>;

public sealed class RejectByAppraiserCommandHandler
    : IRequestHandler<RejectByAppraiserCommand, SendToAppraiserResultDto>
{
    private readonly IAppraiserAssignmentService _service;
    public RejectByAppraiserCommandHandler(IAppraiserAssignmentService service) => _service = service;
    public Task<SendToAppraiserResultDto> Handle(RejectByAppraiserCommand command, CancellationToken ct)
        => _service.RejectByAppraiserAsync(command.OrderId, command.Reason, command.FreeText, ct);
}

public sealed class RejectByAppraiserCommandValidator : AbstractValidator<RejectByAppraiserCommand>
{
    public RejectByAppraiserCommandValidator()
    {
        RuleFor(x => x.OrderId).GreaterThan(0).WithMessage("ID narudžbe je nevažeći.");
        RuleFor(x => x.Reason).IsInEnum().WithMessage("Razlog odbijanja je nevažeći.");
    }
}
