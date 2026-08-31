namespace RBBH.TestAutomation.Core.Domain;

public sealed class ApplicationAuditEntry
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public required string EntityType { get; set; }
    public Guid? EntityId { get; set; }
    public required string Action { get; set; }
    public required string ChangedBy { get; set; }
    public string? ChangedByName { get; set; }
    public DateTime ChangedAt { get; set; } = DateTime.UtcNow;
    public string? OldValues { get; set; }
    public string? NewValues { get; set; }
}
