using FluentValidation;
using MediatR;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.AppraiserAssignment.Commands;

public sealed record ManualSelectAppraiserCommand(int OrderId, int AppraiserId)
    : ICommand<AppraiserAssignmentResultDto>;

public sealed class ManualSelectAppraiserCommandHandler
    : IRequestHandler<ManualSelectAppraiserCommand, AppraiserAssignmentResultDto>
{
    private readonly IAppraiserAssignmentService _service;
    public ManualSelectAppraiserCommandHandler(IAppraiserAssignmentService service) => _service = service;
    public Task<AppraiserAssignmentResultDto> Handle(ManualSelectAppraiserCommand command, CancellationToken ct)
        => _service.ManualSelectAppraiserAsync(command.OrderId, command.AppraiserId, ct);
}

public sealed class ManualSelectAppraiserCommandValidator : AbstractValidator<ManualSelectAppraiserCommand>
{
    public ManualSelectAppraiserCommandValidator()
    {
        RuleFor(x => x.OrderId).GreaterThan(0).WithMessage("ID narudžbe je nevažeći.");
        RuleFor(x => x.AppraiserId).GreaterThan(0).WithMessage("ID vještaka je nevažeći.");
    }
}
