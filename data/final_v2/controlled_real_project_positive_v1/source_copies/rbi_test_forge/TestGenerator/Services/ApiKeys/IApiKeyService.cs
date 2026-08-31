using RBBH.TestAutomation.Api.DTO;

namespace RBBH.TestAutomation.Api.Services.ApiKeys;

public interface IApiKeyService
{
    Task<(ApiKeyDto Key, string RawKey)> GenerateAsync(string name, DateTime? expiresAt, string createdBy, CancellationToken ct = default);
    Task<IReadOnlyList<ApiKeyDto>> GetAllAsync(CancellationToken ct = default);
    Task RevokeAsync(Guid id, CancellationToken ct = default);
    Task<ApiKeyValidationResult> ValidateAsync(string rawKey, CancellationToken ct = default);
}

public sealed record ApiKeyValidationResult(bool IsValid, Guid? KeyId = null, string? KeyName = null);
