namespace RBBH.CollateralAppraisal.Infrastructure.Audit;

/// <summary>
/// Transactional outbox zapis za audit log.
/// DbAuditLogQueue upisuje ovdje sinhrono s poslovnom transakcijom;
/// AuditLogQueueWorker čita i prosljeđuje sinkovima u pozadini.
/// </summary>
public sealed class AuditOutboxEntry
{
    public long      Id          { get; private set; }
    public string    Payload     { get; private set; } = null!;
    public DateTime  CreatedAt   { get; private set; }
    public DateTime? ProcessedAt { get; private set; }

    private AuditOutboxEntry() { }

    public static AuditOutboxEntry Create(string payload) => new()
    {
        Payload   = payload,
        CreatedAt = DateTime.UtcNow
    };

    public void MarkProcessed() => ProcessedAt = DateTime.UtcNow;
}
