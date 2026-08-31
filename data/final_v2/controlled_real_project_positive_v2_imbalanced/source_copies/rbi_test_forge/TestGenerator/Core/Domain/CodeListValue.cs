namespace RBBH.TestAutomation.Core.Domain;

public sealed class CodeListValue
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid CategoryId { get; set; }
    public CodeListCategory Category { get; set; } = null!;
    public required string Name { get; set; }
    public string? Code { get; set; }
    public int Order { get; set; }
    public bool Active { get; set; } = true;
    public string? CreatedBy { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public string? UpdatedBy { get; set; }
    public DateTime? UpdatedAt { get; set; }
}
