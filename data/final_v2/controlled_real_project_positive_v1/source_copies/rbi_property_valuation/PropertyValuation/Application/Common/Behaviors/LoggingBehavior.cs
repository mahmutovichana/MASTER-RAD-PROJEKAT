using System.Diagnostics;
using MediatR;
using Microsoft.Extensions.Logging;

namespace RBBH.CollateralAppraisal.Application.Common.Behaviors;

/// <summary>
/// Pipeline behavior koji loguje svaki MediatR request s imenom i trajanjem.
/// Osigurava uniforman structured logging za sve commands i queries bez boilerplate koda u handlerima.
/// </summary>
public sealed class LoggingBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : notnull
{
    private readonly ILogger<LoggingBehavior<TRequest, TResponse>> _logger;

    public LoggingBehavior(ILogger<LoggingBehavior<TRequest, TResponse>> logger)
        => _logger = logger;

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        var name = typeof(TRequest).Name;
        _logger.LogInformation("[{Request}] START", name);

        var sw = Stopwatch.StartNew();
        try
        {
            var result = await next();
            _logger.LogInformation("[{Request}] END {Elapsed}ms", name, sw.ElapsedMilliseconds);
            return result;
        }
        catch (Exception ex)
        {
            _logger.LogWarning("[{Request}] FAILED {Elapsed}ms — {Error}", name, sw.ElapsedMilliseconds, ex.Message);
            throw;
        }
    }
}
