using RBBH.TestAutomation.Core.Repositories;

namespace RBBH.TestAutomation.Api.Services;

/// <summary>
/// Development fallback za audit događaje kada SQL Server nije konfigurisan.
/// Poslovni upis se ne blokira, a događaji ostaju dostupni dok proces radi.
/// </summary>
public sealed class InMemoryTestForgeAuditWriter : ITestForgeAuditWriter
{
    private readonly List<AuditEntry> _entries = [];
    private readonly object _sync = new();

    public Task WriteAsync(
        string entityType, Guid entityId, string action, string actorId,
        string actorName, object? oldValues, object? newValues,
        CancellationToken ct = default)
    {
        lock (_sync)
            _entries.Add(new(entityType, entityId, action, actorId, actorName, DateTimeOffset.UtcNow));
        return Task.CompletedTask;
    }

    private sealed record AuditEntry(
        string EntityType, Guid EntityId, string Action,
        string ActorId, string ActorName, DateTimeOffset CreatedAt);
}
