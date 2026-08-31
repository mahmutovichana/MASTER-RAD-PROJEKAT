using System.Net.Http.Json;
using System.Text.Json.Serialization;
using Microsoft.Extensions.Caching.Memory;

namespace RBBH.TestAutomation.Api.Services;

/// <summary>
/// Production implementacija — poziva Keycloak Admin REST API.
/// Token se kešira u IMemoryCache kako bi se izbjeglo učestalo dobavljanje.
/// </summary>
public sealed class KeycloakAdminService : IKeycloakAdminService
{
    private readonly HttpClient _http;
    private readonly IMemoryCache _cache;
    private readonly string _tokenUrl;
    private readonly string _adminBaseUrl;
    private readonly string _clientId;
    private readonly string _clientSecret;

    public KeycloakAdminService(
        IHttpClientFactory factory,
        IMemoryCache cache,
        IConfiguration config)
    {
        _http = factory.CreateClient("KeycloakAdmin");
        _cache = cache;
        _clientId = config["KeycloakAdmin:ClientId"]
            ?? config["OpenIDConnectSettings:ClientId"]
            ?? string.Empty;
        _clientSecret = config["KeycloakAdmin:ClientSecret"]
            ?? config["OpenIDConnectSettings:ClientSecret"]
            ?? string.Empty;

        // Authority format: "http://keycloak:8080/realms/rbbh"
        var authority = config["OpenIDConnectSettings:Authority"]
                        ?? "http://keycloak:8080/realms/rbbh";
        _tokenUrl = $"{authority}/protocol/openid-connect/token";

        var slashRealms = authority.LastIndexOf("/realms/", StringComparison.Ordinal);
        var kcBase = slashRealms > 0 ? authority[..slashRealms] : authority;
        var realm  = slashRealms > 0 ? authority[(slashRealms + 8)..] : "rbbh";
        _adminBaseUrl = $"{kcBase}/admin/realms/{realm}";
    }

    public async Task<IReadOnlyList<UserWithRolesDto>> GetUsersWithRolesAsync(CancellationToken ct = default)
    {
        var token = await GetAccessTokenAsync(ct);
        using var req = new HttpRequestMessage(HttpMethod.Get, $"{_adminBaseUrl}/users?max=200");
        req.Headers.Authorization = new("Bearer", token);
        var res = await _http.SendAsync(req, ct);
        res.EnsureSuccessStatusCode();

        var kcUsers = await res.Content.ReadFromJsonAsync<List<KcUser>>(cancellationToken: ct) ?? [];

        var usersWithRoles = await Task.WhenAll(kcUsers.Select(async u =>
        {
            var roles = await GetUserRolesAsync(u.Id, token, ct);
            var dto = new KeycloakUserDto(
                u.Id,
                u.Username ?? string.Empty,
                $"{u.FirstName} {u.LastName}".Trim(),
                u.Email ?? string.Empty,
                u.Enabled);
            return new UserWithRolesDto(dto, roles);
        }));

        return usersWithRoles;
    }

    public async Task AssignRoleAsync(string userId, string roleName, CancellationToken ct = default)
    {
        var token = await GetAccessTokenAsync(ct);
        var roleRep = await GetRealmRoleAsync(roleName, token, ct);

        using var req = new HttpRequestMessage(
            HttpMethod.Post,
            $"{_adminBaseUrl}/users/{userId}/role-mappings/realm");
        req.Headers.Authorization = new("Bearer", token);
        req.Content = JsonContent.Create(new[] { roleRep });
        (await _http.SendAsync(req, ct)).EnsureSuccessStatusCode();
    }

    public async Task RemoveRoleAsync(string userId, string roleName, CancellationToken ct = default)
    {
        var token = await GetAccessTokenAsync(ct);
        var roleRep = await GetRealmRoleAsync(roleName, token, ct);

        using var req = new HttpRequestMessage(
            HttpMethod.Delete,
            $"{_adminBaseUrl}/users/{userId}/role-mappings/realm");
        req.Headers.Authorization = new("Bearer", token);
        req.Content = JsonContent.Create(new[] { roleRep });
        (await _http.SendAsync(req, ct)).EnsureSuccessStatusCode();
    }

    // ── Helpers ──────────────────────────────────────────────────────────────

    private async Task<string> GetAccessTokenAsync(CancellationToken ct)
    {
        return await _cache.GetOrCreateAsync("kc_admin_token", async entry =>
        {
            var form = new FormUrlEncodedContent(new Dictionary<string, string>
            {
                ["grant_type"]    = "client_credentials",
                ["client_id"]     = _clientId,
                ["client_secret"] = _clientSecret,
            });
            var res = await _http.PostAsync(_tokenUrl, form, ct);
            res.EnsureSuccessStatusCode();
            var tokenRes = await res.Content.ReadFromJsonAsync<KcTokenResponse>(cancellationToken: ct);
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromSeconds(
                Math.Max(30, (tokenRes?.ExpiresIn ?? 60) - 30));
            return tokenRes!.AccessToken;
        }) ?? throw new InvalidOperationException("Keycloak token nije dostupan.");
    }

    private async Task<List<string>> GetUserRolesAsync(string userId, string token, CancellationToken ct)
    {
        using var req = new HttpRequestMessage(
            HttpMethod.Get,
            $"{_adminBaseUrl}/users/{userId}/role-mappings/realm");
        req.Headers.Authorization = new("Bearer", token);
        var res = await _http.SendAsync(req, ct);
        if (!res.IsSuccessStatusCode) return [];
        var roles = await res.Content.ReadFromJsonAsync<List<KcRole>>(cancellationToken: ct) ?? [];
        return roles.Select(r => r.Name).ToList();
    }

    private async Task<KcRole> GetRealmRoleAsync(string roleName, string token, CancellationToken ct)
    {
        var cacheKey = $"kc_role_{roleName}";
        return await _cache.GetOrCreateAsync(cacheKey, async entry =>
        {
            using var req = new HttpRequestMessage(
                HttpMethod.Get,
                $"{_adminBaseUrl}/roles/{Uri.EscapeDataString(roleName)}");
            req.Headers.Authorization = new("Bearer", token);
            var res = await _http.SendAsync(req, ct);
            res.EnsureSuccessStatusCode();
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1);
            return (await res.Content.ReadFromJsonAsync<KcRole>(cancellationToken: ct))!;
        }) ?? throw new InvalidOperationException($"Rola '{roleName}' nije pronađena u Keycloak-u.");
    }

    // ── Keycloak JSON modeli ──────────────────────────────────────────────────

    private sealed record KcUser(
        string Id,
        string? Username,
        [property: JsonPropertyName("firstName")] string? FirstName,
        [property: JsonPropertyName("lastName")]  string? LastName,
        string? Email,
        bool Enabled);

    private sealed record KcRole(string Id, string Name);

    private sealed record KcTokenResponse(
        [property: JsonPropertyName("access_token")] string AccessToken,
        [property: JsonPropertyName("expires_in")]   int ExpiresIn);
}
