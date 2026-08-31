using System.Collections.Concurrent;
using System.Diagnostics.CodeAnalysis;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;

namespace RBBH.CollateralAppraisal.Api.Middleware;

/// <summary>
/// In-memory rate limiter za kritične endpointe (upload, approval).
/// Ograničava broj zahtjeva po korisniku unutar vremenskog prozora.
/// Za multi-instance deployment zamijeniti sa Redis-based implementacijom.
/// </summary>
[ExcludeFromCodeCoverage]
public sealed class SimpleRateLimiter
{
    private readonly ConcurrentDictionary<string, RateLimitEntry> _entries = new();
    private readonly int _maxRequests;
    private readonly TimeSpan _window;

    public SimpleRateLimiter(int maxRequests, TimeSpan window)
    {
        _maxRequests = maxRequests;
        _window = window;
    }

    public bool IsAllowed(string key)
    {
        var now = DateTime.UtcNow;
        var entry = _entries.AddOrUpdate(
            key,
            _ => new RateLimitEntry(1, now),
            (_, existing) =>
            {
                if (now - existing.WindowStart > _window)
                    return new RateLimitEntry(1, now);

                return existing with { Count = existing.Count + 1 };
            });

        return entry.Count <= _maxRequests;
    }

    private sealed record RateLimitEntry(int Count, DateTime WindowStart);
}

/// <summary>
/// Endpoint filter za rate limiting — vraća 429 Too Many Requests.
/// Koristi injectovani IDistributedRateLimiter koji je po defaultu in-memory.
/// Za multi-instance deploy: registruj RedisDistributedRateLimiter umjesto InMemoryDistributedRateLimiter.
/// Registriraj kao: .AddEndpointFilter&lt;RateLimitEndpointFilter&gt;()
/// </summary>
[ExcludeFromCodeCoverage]
public sealed class RateLimitEndpointFilter : IEndpointFilter
{
    private readonly IDistributedRateLimiter _limiter;
    private const int UploadMaxPerMinute   = 20;
    private const int ApprovalMaxPerMinute = 10;

    public RateLimitEndpointFilter(IDistributedRateLimiter limiter) => _limiter = limiter;

    public async ValueTask<object?> InvokeAsync(
        EndpointFilterInvocationContext context,
        EndpointFilterDelegate next)
    {
        var httpContext = context.HttpContext;
        var userId = httpContext.User.FindFirst("sub")?.Value
                  ?? httpContext.Connection.RemoteIpAddress?.ToString()
                  ?? "unknown";
        var path = httpContext.Request.Path.Value ?? "";

        var isUploadPath = path.Contains("/documents", StringComparison.OrdinalIgnoreCase)
                        || path.Contains("/invoice", StringComparison.OrdinalIgnoreCase);

        var (maxRequests, action) = isUploadPath
            ? (UploadMaxPerMinute, "upload")
            : (ApprovalMaxPerMinute, "approval");

        if (!_limiter.IsAllowed($"{userId}:{action}", maxRequests, TimeSpan.FromMinutes(1)))
        {
            return Results.Problem(
                title: "Previše zahtjeva",
                detail: "Prekoračili ste dozvoljeni broj zahtjeva. Pokušajte ponovo za minutu.",
                statusCode: StatusCodes.Status429TooManyRequests);
        }

        return await next(context);
    }
}
