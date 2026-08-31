namespace RBBH.TestAutomation.Core.Domain;

public sealed class CodeListCategory
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public required string Name { get; set; }
    public required string Slug { get; set; }
    public string? Description { get; set; }
    public bool Active { get; set; } = true;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public ICollection<CodeListValue> Values { get; set; } = [];
}
