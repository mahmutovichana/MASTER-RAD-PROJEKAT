using RBBH.CollateralAppraisal.Application.Common;

namespace RBBH.CollateralAppraisal.Api.Middleware;

public class CorrelationIdMiddleware
{
    private const int MaxCorrelationIdLength = 64;

    private readonly RequestDelegate _next;

    public CorrelationIdMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var correlationId = ResolveCorrelationId(context);

        context.Items[HttpHeaders.CorrelationId]              = correlationId;
        context.Response.Headers[HttpHeaders.CorrelationId]   = correlationId;

        await _next(context);
    }

    private static string ResolveCorrelationId(HttpContext context)
    {
        if (!context.Request.Headers.TryGetValue(HttpHeaders.CorrelationId, out var headerValue))
            return Guid.NewGuid().ToString();

        var value = headerValue.ToString().Trim();

        if (string.IsNullOrEmpty(value))
            return Guid.NewGuid().ToString();

        // Ograničavamo dužinu da spriječimo zlouporabu — predugi ID se odbacuje i generiše novi
        if (value.Length > MaxCorrelationIdLength)
            return Guid.NewGuid().ToString();

        return value;
    }
}
