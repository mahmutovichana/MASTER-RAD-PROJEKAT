using System.Collections.Concurrent;

namespace RBBH.TestAutomation.Api.Services.Auth;

/// <summary>
/// In-memory ring buffer s zadnjih <see cref="Capacity"/> audit zapisa.
///
/// Registracija: Singleton — dijeli se kroz sve sesije jer adminu treba globalni
/// pregled svih login pokušaja, ne samo svoje sesije.
///
/// Ograničenja (prihvaćena za dev fazu):
/// - State se gubi pri restartu aplikacije.
/// - Cap od 1000 — stariji zapisi se odbacuju (FIFO).
/// Buduća verzija: zamijeniti s ApiAuditLogStore (SQL Server, bez gubitka pri restartu).
/// </summary>
public sealed class InMemoryAuditLogStore : IAuditLogStore
{
    private const int Capacity = 1000;

    private readonly ConcurrentQueue<AuditLogEntry> _entries = new();

    public void Add(AuditLogEntry entry)
    {
        _entries.Enqueue(entry);

        // Drži najviše Capacity zapisa — odbaci najstarije.
        while (_entries.Count > Capacity)
            _entries.TryDequeue(out _);
    }

    public IReadOnlyList<AuditLogEntry> GetRecent(int max = 100)
        => _entries.Reverse().Take(max).ToList();
}
