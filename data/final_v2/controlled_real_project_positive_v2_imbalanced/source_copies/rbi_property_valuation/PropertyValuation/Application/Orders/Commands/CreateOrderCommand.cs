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

public sealed record CreateOrderCommand(CreateOrderRequest Request) : ICommand<AppraisalOrderDto>;

public sealed class CreateOrderCommandHandler : IRequestHandler<CreateOrderCommand, AppraisalOrderDto>
{
    private readonly IAppraisalOrderService _service;
    public CreateOrderCommandHandler(IAppraisalOrderService service) => _service = service;
    public Task<AppraisalOrderDto> Handle(CreateOrderCommand command, CancellationToken ct)
        => _service.CreateAsync(command.Request, ct);
}

/// <summary>
/// Delegira kompletnu validaciju na OrderRequestValidator — Single Source of Truth.
/// Konvertuje ValidationException u FluentValidation ValidationResult.
/// </summary>
public sealed class CreateOrderCommandValidator : AbstractValidator<CreateOrderCommand>
{
    public CreateOrderCommandValidator()
    {
        RuleFor(x => x.Request)
            .Custom((r, ctx) =>
            {
                try
                {
                    OrderRequestValidator.ValidateCreate(r);
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
