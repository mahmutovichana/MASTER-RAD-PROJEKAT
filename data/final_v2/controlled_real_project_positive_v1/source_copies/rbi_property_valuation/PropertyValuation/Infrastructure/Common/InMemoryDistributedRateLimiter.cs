using System.Collections.Concurrent;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;

namespace RBBH.CollateralAppraisal.Infrastructure.Common;

/// <summary>
/// In-memory implementacija IDistributedRateLimiter.
/// OGRANIČENJE: stanje je per-process — nije efektivno u multi-instance deploymentu.
/// Za HA deploy zamijeniti sa RedisDistributedRateLimiter (StackExchange.Redis + INCR/EXPIRE).
/// </summary>
public sealed class InMemoryDistributedRateLimiter : IDistributedRateLimiter
{
    private readonly ConcurrentDictionary<string, RateLimitEntry> _entries = new();

    public bool IsAllowed(string key, int maxRequests, TimeSpan window)
    {
        var now = DateTime.UtcNow;
        var entry = _entries.AddOrUpdate(
            key,
            _ => new RateLimitEntry(1, now),
            (_, existing) =>
            {
                if (now - existing.WindowStart > window)
                    return new RateLimitEntry(1, now);
                return existing with { Count = existing.Count + 1 };
            });
        return entry.Count <= maxRequests;
    }

    private sealed record RateLimitEntry(int Count, DateTime WindowStart);
}
