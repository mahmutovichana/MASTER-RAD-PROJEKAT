using System.Security.Cryptography;
using System.Text;
using RBBH.TestAutomation.Api.DTO;
using Microsoft.EntityFrameworkCore;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Infrastructure;

namespace RBBH.TestAutomation.Api.Services.ApiKeys;

public sealed class ApiKeyService(TestForgeDbContext db, ILogger<ApiKeyService> logger) : IApiKeyService
{
    public async Task<(ApiKeyDto Key, string RawKey)> GenerateAsync(
        string name, DateTime? expiresAt, string createdBy, CancellationToken ct = default)
    {
        var rawKey = GenerateRawKey();
        var hash = HashKey(rawKey);
        var prefix = rawKey[..8];

        var entity = new ApiKey
        {
            Name = name,
            KeyHash = hash,
            Prefix = prefix,
            ExpiresAt = expiresAt.HasValue
                ? DateTime.SpecifyKind(expiresAt.Value, DateTimeKind.Utc)
                : null,
            CreatedBy = createdBy,
        };

        db.ApiKeys.Add(entity);
        await db.SaveChangesAsync(ct);

        logger.LogInformation("API ključ kreiran: {Prefix}... za {Name} od {CreatedBy}", prefix, name, createdBy);
        return (ToDto(entity), rawKey);
    }

    public async Task<IReadOnlyList<ApiKeyDto>> GetAllAsync(CancellationToken ct = default)
    {
        var keys = await db.ApiKeys.OrderByDescending(k => k.CreatedAt).ToListAsync(ct);
        return keys.Select(ToDto).ToList();
    }

    public async Task RevokeAsync(Guid id, CancellationToken ct = default)
    {
        var key = await db.ApiKeys.FindAsync([id], ct)
            ?? throw new InvalidOperationException("API ključ nije pronađen.");
        key.IsRevoked = true;
        await db.SaveChangesAsync(ct);
        logger.LogInformation("API ključ revociran: {Prefix}... ({Name})", key.Prefix, key.Name);
    }

    public async Task<ApiKeyValidationResult> ValidateAsync(string rawKey, CancellationToken ct = default)
    {
        var hash = HashKey(rawKey);
        var key = await db.ApiKeys.FirstOrDefaultAsync(k => k.KeyHash == hash, ct);

        if (key is null)
            return new ApiKeyValidationResult(false);

        if (key.IsRevoked)
            return new ApiKeyValidationResult(false);

        if (key.ExpiresAt.HasValue && key.ExpiresAt.Value < DateTime.UtcNow)
            return new ApiKeyValidationResult(false);

        key.LastUsedAt = DateTime.UtcNow;
        await db.SaveChangesAsync(ct);

        return new ApiKeyValidationResult(true, key.Id, key.Name);
    }

    private static string GenerateRawKey()
    {
        var bytes = RandomNumberGenerator.GetBytes(32);
        return $"tag_{Convert.ToBase64String(bytes).Replace("+", "").Replace("/", "").Replace("=", "")}";
    }

    private static string HashKey(string rawKey)
    {
        var bytes = SHA256.HashData(Encoding.UTF8.GetBytes(rawKey));
        return Convert.ToHexStringLower(bytes);
    }

    private static ApiKeyDto ToDto(ApiKey k) => new(
        k.Id, k.Name, k.Prefix, k.ExpiresAt, k.IsRevoked,
        k.CreatedAt, k.CreatedBy, k.LastUsedAt);
}
