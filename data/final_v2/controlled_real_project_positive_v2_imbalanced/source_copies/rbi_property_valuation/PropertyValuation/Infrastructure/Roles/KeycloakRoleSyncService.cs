﻿using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using RBBH.CollateralAppraisal.Application.Roles.Interfaces;
using RBBH.CollateralAppraisal.Infrastructure.Auth;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Roles;

/// <summary>
/// Implementacija <see cref="IKeycloakRoleSyncService"/> koja komunicira s Keycloak Admin REST API.
/// Koristi client_credentials grant (service account) za autentifikaciju.
///
/// Sve operacije su idempotentne:
/// - CreateRoleAsync: 409 Conflict se ignoriše
/// - DeleteRoleAsync: 404 Not Found se ignoriše
/// - AssignRoleToUserAsync: korisnik može već imati rolu
/// - RemoveRoleFromUserAsync: korisnik možda nema rolu
/// </summary>
[ExcludeFromCodeCoverage]
public sealed class KeycloakRoleSyncService : IKeycloakRoleSyncService
{
    private readonly IHttpClientFactory             _factory;
    private readonly KeycloakAdminOptions           _options;
    private readonly ILogger<KeycloakRoleSyncService> _logger;

    private static readonly JsonSerializerOptions _json = new()
    {
        PropertyNameCaseInsensitive = true,
        PropertyNamingPolicy        = JsonNamingPolicy.CamelCase
    };

    private record TokenResponse([property: JsonPropertyName("access_token")] string AccessToken);
    private record KeycloakRole(string Id, string Name, string? Description);
    private record KeycloakUser(string Id, string Username);

    public KeycloakRoleSyncService(
        IHttpClientFactory             factory,
        IOptions<KeycloakAdminOptions> options,
        ILogger<KeycloakRoleSyncService> logger)
    {
        _factory = factory;
        _options = options.Value;
        _logger  = logger;
    }

    // â”€â”€ Role definicije â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    public async Task CreateRoleAsync(string roleName, string? description, CancellationToken ct = default)
    {
        var client = await GetAuthorizedClientAsync(ct);
        var body   = JsonSerializer.Serialize(new { name = roleName, description = description ?? "" }, _json);
        var resp   = await client.PostAsync(
            $"/admin/realms/{_options.Realm}/roles",
            new StringContent(body, Encoding.UTF8, "application/json"), ct);

        // 409 = rola već postoji â†’ idempotentno
        if (!resp.IsSuccessStatusCode && resp.StatusCode != System.Net.HttpStatusCode.Conflict)
        {
            var detail = await resp.Content.ReadAsStringAsync(ct);
            _logger.LogError("Keycloak CreateRole failed {Status}: {Detail}", resp.StatusCode, detail);
            resp.EnsureSuccessStatusCode();
        }
    }

    public async Task UpdateRoleAsync(string roleName, string? description, CancellationToken ct = default)
    {
        var client = await GetAuthorizedClientAsync(ct);
        var body   = JsonSerializer.Serialize(new { name = roleName, description = description ?? "" }, _json);
        var resp   = await client.PutAsync(
            $"/admin/realms/{_options.Realm}/roles/{Uri.EscapeDataString(roleName)}",
            new StringContent(body, Encoding.UTF8, "application/json"), ct);

        if (!resp.IsSuccessStatusCode && resp.StatusCode != System.Net.HttpStatusCode.NotFound)
            resp.EnsureSuccessStatusCode();
    }

    public async Task DeleteRoleAsync(string roleName, CancellationToken ct = default)
    {
        var client = await GetAuthorizedClientAsync(ct);
        var resp   = await client.DeleteAsync(
            $"/admin/realms/{_options.Realm}/roles/{Uri.EscapeDataString(roleName)}", ct);

        // 404 = rola ne postoji â†’ idempotentno
        if (resp.StatusCode != System.Net.HttpStatusCode.NotFound)
            resp.EnsureSuccessStatusCode();
    }

    public async Task<bool> RoleExistsAsync(string roleName, CancellationToken ct = default)
    {
        try
        {
            var client = await GetAuthorizedClientAsync(ct);
            var resp   = await client.GetAsync(
                $"/admin/realms/{_options.Realm}/roles/{Uri.EscapeDataString(roleName)}", ct);
            return resp.IsSuccessStatusCode;
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "RoleExistsAsync check failed za rolu {Role}.", roleName);
            return false;
        }
    }

    public async Task<int> GetRoleUserCountAsync(string roleName, CancellationToken ct = default)
    {
        try
        {
            var client = await GetAuthorizedClientAsync(ct);
            var json   = await client.GetStringAsync(
                $"/admin/realms/{_options.Realm}/roles/{Uri.EscapeDataString(roleName)}/users?max=500", ct);
            var users  = JsonSerializer.Deserialize<List<KeycloakUser>>(json, _json) ?? [];
            return users.Count;
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "GetRoleUserCountAsync failed za rolu {Role}.", roleName);
            return 0;
        }
    }

    // â”€â”€ Korisnikâ€“rola mappinzi â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    public async Task AssignRoleToUserAsync(string userId, string roleName, CancellationToken ct = default)
    {
        var client = await GetAuthorizedClientAsync(ct);

        var role = await GetRoleObjectAsync(client, roleName, ct);
        if (role is null)
            throw new InvalidOperationException($"Rola '{roleName}' nije pronaÄ‘ena u Keycloak-u.");

        var body = JsonSerializer.Serialize(new[] { new { role.Id, role.Name } }, _json);
        var resp = await client.PostAsync(
            $"/admin/realms/{_options.Realm}/users/{userId}/role-mappings/realm",
            new StringContent(body, Encoding.UTF8, "application/json"), ct);

        resp.EnsureSuccessStatusCode();
    }

    public async Task RemoveRoleFromUserAsync(string userId, string roleName, CancellationToken ct = default)
    {
        var client = await GetAuthorizedClientAsync(ct);

        var role = await GetRoleObjectAsync(client, roleName, ct);
        if (role is null)
        {
            _logger.LogWarning("RemoveRoleFromUser: rola '{Role}' nije pronaÄ‘ena u Keycloak-u. Preskaćem.", roleName);
            return;
        }

        var body    = JsonSerializer.Serialize(new[] { new { role.Id, role.Name } }, _json);
        var request = new HttpRequestMessage(
            HttpMethod.Delete,
            $"/admin/realms/{_options.Realm}/users/{userId}/role-mappings/realm")
        {
            Content = new StringContent(body, Encoding.UTF8, "application/json")
        };
        var resp = await client.SendAsync(request, ct);

        // 404 = korisnik/rola ne postoji â†’ idempotentno
        if (resp.StatusCode != System.Net.HttpStatusCode.NotFound)
            resp.EnsureSuccessStatusCode();
    }

    public async Task<IReadOnlyList<string>> GetUserRealmRolesAsync(string userId, CancellationToken ct = default)
    {
        try
        {
            var client = await GetAuthorizedClientAsync(ct);
            var json   = await client.GetStringAsync(
                $"/admin/realms/{_options.Realm}/users/{userId}/role-mappings/realm", ct);
            var roles  = JsonSerializer.Deserialize<List<KeycloakRole>>(json, _json) ?? [];
            return roles.Select(r => r.Name).ToList().AsReadOnly();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "GetUserRealmRolesAsync failed za korisnika {UserId}.", userId);
            return [];
        }
    }

    // â”€â”€ Helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    private async Task<KeycloakRole?> GetRoleObjectAsync(HttpClient client, string roleName, CancellationToken ct)
    {
        try
        {
            var json = await client.GetStringAsync(
                $"/admin/realms/{_options.Realm}/roles/{Uri.EscapeDataString(roleName)}", ct);
            return JsonSerializer.Deserialize<KeycloakRole>(json, _json);
        }
        catch (HttpRequestException ex) when (ex.StatusCode == System.Net.HttpStatusCode.NotFound)
        {
            return null;
        }
    }

    private async Task<HttpClient> GetAuthorizedClientAsync(CancellationToken ct)
    {
        var client = _factory.CreateClient("KeycloakAdmin");

        var form = new FormUrlEncodedContent(new Dictionary<string, string>
        {
            ["grant_type"]    = "client_credentials",
            ["client_id"]     = _options.ClientId,
            ["client_secret"] = _options.ClientSecret
        });
        var tokenPath = $"/realms/{_options.Realm}/protocol/openid-connect/token";

        var resp = await client.PostAsync(tokenPath, form, ct);
        resp.EnsureSuccessStatusCode();

        var json  = await resp.Content.ReadAsStringAsync(ct);
        var token = (JsonSerializer.Deserialize<TokenResponse>(json, _json)
            ?? throw new InvalidOperationException("Keycloak token nije validan.")).AccessToken;

        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
        return client;
    }
}
