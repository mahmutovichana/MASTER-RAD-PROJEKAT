using FluentValidation;
using FluentValidation.Results;
using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Validation;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Application.Orders.Requests;

namespace RBBH.CollateralAppraisal.Application.Orders.Commands;

public sealed record UpdateDraftOrderCommand(
    int OrderId,
    UpdateOrderRequest Request,
    bool IsAutosave = false) : ICommand<AppraisalOrderDto>;

public sealed class UpdateDraftOrderCommandHandler : IRequestHandler<UpdateDraftOrderCommand, AppraisalOrderDto>
{
    private readonly IAppraisalOrderService _service;
    public UpdateDraftOrderCommandHandler(IAppraisalOrderService service) => _service = service;
    public Task<AppraisalOrderDto> Handle(UpdateDraftOrderCommand command, CancellationToken ct)
        => _service.UpdateDraftAsync(command.OrderId, command.Request, command.IsAutosave, ct);
}

/// <summary>
/// Delegira validaciju na OrderRequestValidator.ValidateUpdate — Single Source of Truth.
/// effectiveClientType je null pri validaciji jer UpdateDraftOrderCommand ne zna order context.
/// </summary>
public sealed class UpdateDraftOrderCommandValidator : AbstractValidator<UpdateDraftOrderCommand>
{
    public UpdateDraftOrderCommandValidator()
    {
        RuleFor(x => x.OrderId)
            .GreaterThan(0).WithMessage("ID narudžbe je nevažeći.");

        RuleFor(x => x.Request)
            .Custom((r, ctx) =>
            {
                try
                {
                    OrderRequestValidator.ValidateUpdate(r, r.ClientType);
                }
                catch (RBBH.CollateralAppraisal.Application.Common.Exceptions.ValidationException ex)
                {
                    if (ex.FieldErrors is not null)
                        foreach (var e in ex.FieldErrors)
                            ctx.AddFailure(new ValidationFailure(e.Field, e.Message));
                    else
                        foreach (var (field, msgs) in ex.Errors)
                            foreach (var msg in msgs)
                                ctx.AddFailure(new ValidationFailure(field, msg));
                }
            });
    }
}
