namespace RBBH.TestAutomation.Api.DTO;

public sealed record ApiKeyDto(
    Guid Id,
    string Name,
    string Prefix,
    DateTime? ExpiresAt,
    bool IsRevoked,
    DateTime CreatedAt,
    string? CreatedBy,
    DateTime? LastUsedAt);
