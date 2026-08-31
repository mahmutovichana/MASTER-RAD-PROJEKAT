using FluentValidation;
using MediatR;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Models;
using ValidationException = RBBH.CollateralAppraisal.Application.Common.Exceptions.ValidationException;

namespace RBBH.CollateralAppraisal.Application.Common.Behaviors;

/// <summary>
/// Pipeline behavior koji pokreće sve FluentValidation validatore registrovane za dati request.
/// Baca ValidationException (400) ako validacija ne prođe — handler se ne poziva.
/// Registrovati kao PRVI behavior u lancu.
/// </summary>
public sealed class ValidationBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : notnull
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators)
        => _validators = validators;

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        if (!_validators.Any())
            return await next();

        var context = new ValidationContext<TRequest>(request);
        var results = await Task.WhenAll(
            _validators.Select(v => v.ValidateAsync(context, cancellationToken)));

        var failures = results
            .SelectMany(r => r.Errors)
            .Where(f => f is not null)
            .ToList();

        if (failures.Count == 0)
            return await next();

        var fieldErrors = failures
            .Select(f => new ValidationFieldError(f.PropertyName, f.ErrorCode, f.ErrorMessage))
            .ToList();

        throw new ValidationException(fieldErrors);
    }
}
