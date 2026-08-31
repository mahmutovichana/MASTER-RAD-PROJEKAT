namespace RBBH.TestAutomation.Core.Domain;

public class ApiKey
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string Name { get; set; } = "";
    public string KeyHash { get; set; } = "";
    public string Prefix { get; set; } = "";
    public DateTime? ExpiresAt { get; set; }
    public bool IsRevoked { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public string? CreatedBy { get; set; }
    public DateTime? LastUsedAt { get; set; }
}
