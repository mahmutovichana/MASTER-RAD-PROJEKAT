using System.Net.Http.Headers;
using System.Text.Json;

namespace RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;

/// <summary>
/// Dohvata JWT access token iz Keycloaka koristeći ROPC (Resource Owner Password Credentials) grant.
/// Tokeni se keširaju po ulozi dok ne isteknu.
///
/// Preduslov: Keycloak klijent mora imati "Direct Access Grants" (ROPC) uključen.
/// </summary>
public sealed class JwtTokenHelper : IDisposable
{
    private readonly HttpClient _http = new();
    private readonly string     _tokenUrl;
    private readonly string     _clientId;

    private readonly Dictionary<string, (string Token, DateTime ExpiresAt)> _cache = [];

    public JwtTokenHelper(E2EConfig config)
    {
        _tokenUrl = $"{config.KeycloakUrl}/realms/{config.KeycloakRealm}/protocol/openid-connect/token";
        _clientId = config.KeycloakClientId;
    }

    /// <summary>
    /// Vraća validan JWT token za zadanog korisnika.
    /// Kešira token i automatski ga osvježava kada istekne.
    /// </summary>
    public async Task<string> GetTokenAsync(UserCredentials user, CancellationToken ct = default)
    {
        if (_cache.TryGetValue(user.Role, out var cached) &&
            cached.ExpiresAt > DateTime.UtcNow.AddSeconds(30))
            return cached.Token;

        var body = new FormUrlEncodedContent(new Dictionary<string, string>
        {
            ["grant_type"] = "password",
            ["client_id"]  = _clientId,
            ["username"]   = user.Username,
            ["password"]   = user.Password
        });

        var response = await _http.PostAsync(_tokenUrl, body, ct);

        if (!response.IsSuccessStatusCode)
        {
            var error = await response.Content.ReadAsStringAsync(ct);
            throw new InvalidOperationException(
                $"Keycloak ROPC token za korisnika '{user.Username}' nije uspješan. " +
                $"Status: {response.StatusCode}. " +
                $"Provjeri da klijent '{_clientId}' ima Direct Access Grants uključen. " +
                $"Greška: {error}");
        }

        var json       = await response.Content.ReadAsStringAsync(ct);
        using var doc  = JsonDocument.Parse(json);
        var root       = doc.RootElement;
        var token      = root.GetProperty("access_token").GetString()!;
        var expiresIn  = root.GetProperty("expires_in").GetInt32();

        _cache[user.Role] = (token, DateTime.UtcNow.AddSeconds(expiresIn));
        return token;
    }

    public void Dispose() => _http.Dispose();
}
