using System.Collections.Concurrent;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;

namespace RBBH.CollateralAppraisal.Infrastructure.Common;

/// <summary>Procesni lock za lokalni razvoj s in-memory bazom.</summary>
public sealed class InMemoryJobLock : IDistributedJobLock
{
    private static readonly ConcurrentDictionary<long, byte> Locks = new();

    public Task<bool> TryAcquireAsync(long lockKey, CancellationToken ct = default) =>
        Task.FromResult(Locks.TryAdd(lockKey, 0));

    public Task ReleaseAsync(long lockKey, CancellationToken ct = default)
    {
        Locks.TryRemove(lockKey, out _);
        return Task.CompletedTask;
    }
}
