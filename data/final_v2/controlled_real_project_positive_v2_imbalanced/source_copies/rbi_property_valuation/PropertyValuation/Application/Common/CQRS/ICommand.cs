using MediatR;

namespace RBBH.CollateralAppraisal.Application.Common.CQRS;

/// <summary>
/// Marker za operacije koje mijenjaju stanje (write).
/// Pipeline: ValidationBehavior → LoggingBehavior → handler.
/// </summary>
public interface ICommand<TResult> : IRequest<TResult> { }

/// <summary>Command koji ne vraća rezultat.</summary>
public interface ICommand : IRequest { }
