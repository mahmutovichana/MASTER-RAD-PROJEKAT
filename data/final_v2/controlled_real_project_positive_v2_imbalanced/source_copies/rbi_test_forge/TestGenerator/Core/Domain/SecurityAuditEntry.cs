namespace RBBH.TestAutomation.Core.Domain;

public sealed class SecurityAuditEntry
{
    public long Id { get; set; }
    public DateTime TimestampUtc { get; set; }
    public required string EventType { get; set; }
    public required string Username { get; set; }
    public string? IpAddress { get; set; }
    public string? FailureReason { get; set; }
}
