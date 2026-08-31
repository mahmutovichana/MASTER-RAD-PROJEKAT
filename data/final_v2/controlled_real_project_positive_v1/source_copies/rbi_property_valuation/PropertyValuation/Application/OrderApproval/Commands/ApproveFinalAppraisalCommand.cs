using FluentValidation;
using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;

namespace RBBH.CollateralAppraisal.Application.OrderApproval.Commands;

public sealed record ApproveFinalAppraisalCommand(
    int OrderId,
    int? AppraiserRating = null) : ICommand<ApproveFinalAppraisalResultDto>;

public sealed class ApproveFinalAppraisalCommandHandler
    : IRequestHandler<ApproveFinalAppraisalCommand, ApproveFinalAppraisalResultDto>
{
    private readonly IOrderApprovalService _service;
    public ApproveFinalAppraisalCommandHandler(IOrderApprovalService service) => _service = service;
    public Task<ApproveFinalAppraisalResultDto> Handle(ApproveFinalAppraisalCommand command, CancellationToken ct)
        => _service.ApproveFinalAppraisalAsync(command.OrderId, command.AppraiserRating, ct);
}

public sealed class ApproveFinalAppraisalCommandValidator : AbstractValidator<ApproveFinalAppraisalCommand>
{
    public ApproveFinalAppraisalCommandValidator()
    {
        RuleFor(x => x.OrderId)
            .GreaterThan(0).WithMessage("ID narudžbe je nevažeći.");

        RuleFor(x => x.AppraiserRating)
            .InclusiveBetween(1, 5)
            .When(x => x.AppraiserRating.HasValue)
            .WithMessage("Ocjena vještaka mora biti između 1 i 5.");
    }
}
