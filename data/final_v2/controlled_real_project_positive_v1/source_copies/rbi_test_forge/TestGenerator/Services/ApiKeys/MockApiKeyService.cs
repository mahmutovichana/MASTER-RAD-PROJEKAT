using System.Security.Cryptography;
using System.Text;
using RBBH.TestAutomation.Api.DTO;

namespace RBBH.TestAutomation.Api.Services.ApiKeys;

public sealed class MockApiKeyService : IApiKeyService
{
    private readonly List<(ApiKeyDto Dto, string Hash)> _keys = [];
    private readonly Lock _lock = new();

    public Task<(ApiKeyDto Key, string RawKey)> GenerateAsync(
        string name, DateTime? expiresAt, string createdBy, CancellationToken ct = default)
    {
        lock (_lock)
        {
            var rawKey = $"tag_{Convert.ToBase64String(RandomNumberGenerator.GetBytes(32)).Replace("+", "").Replace("/", "").Replace("=", "")}";
            var hash = HashKey(rawKey);
            var dto = new ApiKeyDto(Guid.NewGuid(), name, rawKey[..8], expiresAt, false,
                DateTime.UtcNow, createdBy, null);
            _keys.Add((dto, hash));
            return Task.FromResult((dto, rawKey));
        }
    }

    public Task<IReadOnlyList<ApiKeyDto>> GetAllAsync(CancellationToken ct = default)
    {
        lock (_lock)
        {
            IReadOnlyList<ApiKeyDto> result = _keys.Select(k => k.Dto).Reverse().ToList();
            return Task.FromResult(result);
        }
    }

    public Task RevokeAsync(Guid id, CancellationToken ct = default)
    {
        lock (_lock)
        {
            for (var i = 0; i < _keys.Count; i++)
            {
                if (_keys[i].Dto.Id == id)
                {
                    var old = _keys[i].Dto;
                    _keys[i] = (old with { IsRevoked = true }, _keys[i].Hash);
                    break;
                }
            }
            return Task.CompletedTask;
        }
    }

    public Task<ApiKeyValidationResult> ValidateAsync(string rawKey, CancellationToken ct = default)
    {
        lock (_lock)
        {
            var hash = HashKey(rawKey);
            var match = _keys.FirstOrDefault(k => k.Hash == hash);
            if (match.Dto is null) return Task.FromResult(new ApiKeyValidationResult(false));
            if (match.Dto.IsRevoked) return Task.FromResult(new ApiKeyValidationResult(false));
            if (match.Dto.ExpiresAt.HasValue && match.Dto.ExpiresAt < DateTime.UtcNow)
                return Task.FromResult(new ApiKeyValidationResult(false));
            return Task.FromResult(new ApiKeyValidationResult(true, match.Dto.Id, match.Dto.Name));
        }
    }

    private static string HashKey(string key)
    {
        var bytes = SHA256.HashData(Encoding.UTF8.GetBytes(key));
        return Convert.ToHexStringLower(bytes);
    }
}
