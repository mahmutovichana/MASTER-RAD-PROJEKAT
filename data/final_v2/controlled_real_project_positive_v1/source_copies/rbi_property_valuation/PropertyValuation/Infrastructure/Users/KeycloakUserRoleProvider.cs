﻿using System.Net.Http.Headers;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Application.Users.Models;
using RBBH.CollateralAppraisal.Infrastructure.Auth;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Users;

/// <summary>
/// Implementacija IUserRoleProvider koja dohvata korisnike i njihove role putem Keycloak Admin REST API.
/// Koristi service-account (client_credentials grant) za autentifikaciju prema admin API-ju.
/// </summary>
[ExcludeFromCodeCoverage]
public class KeycloakUserRoleProvider : IUserRoleProvider
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly KeycloakAdminOptions _options;
    private readonly ILogger<KeycloakUserRoleProvider> _logger;

    private static readonly JsonSerializerOptions _json = new() { PropertyNameCaseInsensitive = true };

    private record KeycloakUser(
        string Id,
        string Username,
        string? Email,
        string? FirstName,
        string? LastName,
        bool Enabled,
        string? ServiceAccountClientId = null);
    private record KeycloakRole(string Id, string Name);
    private record TokenResponse([property: JsonPropertyName("access_token")] string AccessToken);

    public KeycloakUserRoleProvider(
        IHttpClientFactory httpClientFactory,
        IOptions<KeycloakAdminOptions> options,
        ILogger<KeycloakUserRoleProvider> logger)
    {
        _httpClientFactory = httpClientFactory;
        _options = options.Value;
        _logger = logger;
    }

    public async Task<PagedResult<UserRoleSourceItem>> GetUsersWithRolesAsync(
        UserRoleListRequest request,
        CancellationToken cancellationToken = default)
    {
        var token = await GetAdminToken(cancellationToken);
        var client = CreateAuthorizedClient(token);

        if (!string.IsNullOrWhiteSpace(request.Role))
            return await GetUsersByRoleAsync(request, client, cancellationToken);

        var search = request.NormalizedSearch;
        var url = BuildUsersUrl(search);

        List<KeycloakUser> allUsers;
        try
        {
            var json = await client.GetStringAsync(url, cancellationToken);
            allUsers = JsonSerializer.Deserialize<List<KeycloakUser>>(json, _json) ?? [];
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Greška pri dohvatu korisnika iz Keycloaka.");
            throw;
        }

        // Bez `enabled` parametra Keycloak ne vraća service account korisnike,
        // pa je dovoljno filtrirati po IsActive na klijentu (vidi BuildUsersUrl).
        allUsers = allUsers.Where(u => u.ServiceAccountClientId is null).ToList();

        if (request.IsActive.HasValue)
            allUsers = allUsers.Where(u => u.Enabled == request.IsActive.Value).ToList();

        var totalCount = allUsers.Count;
        var page = request.ValidatedPage;
        var pageSize = request.ValidatedPageSize;
        var pageUsers = allUsers.Skip((page - 1) * pageSize).Take(pageSize).ToList();

        var items = await MapUsersToSourceItems(pageUsers, client, cancellationToken);

        return new PagedResult<UserRoleSourceItem>
        {
            Items = items,
            TotalCount = totalCount,
            Page = page,
            PageSize = pageSize
        };
    }

    private async Task<PagedResult<UserRoleSourceItem>> GetUsersByRoleAsync(
        UserRoleListRequest request,
        HttpClient client,
        CancellationToken cancellationToken)
    {
        var roleUrl = $"/admin/realms/{_options.Realm}/roles/{Uri.EscapeDataString(request.Role!)}/users?first=0&max=1000";

        List<KeycloakUser> allRoleUsers;
        try
        {
            var json = await client.GetStringAsync(roleUrl, cancellationToken);
            allRoleUsers = JsonSerializer.Deserialize<List<KeycloakUser>>(json, _json) ?? [];
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Greška pri dohvatu korisnika za rolu {Role}.", request.Role);
            throw;
        }

        allRoleUsers = allRoleUsers.Where(u => u.ServiceAccountClientId is null).ToList();

        if (request.IsActive.HasValue)
            allRoleUsers = allRoleUsers.Where(u => u.Enabled == request.IsActive.Value).ToList();

        var search = request.NormalizedSearch?.ToLower();
        if (!string.IsNullOrEmpty(search))
            allRoleUsers = allRoleUsers.Where(u =>
                (u.Username?.ToLower().Contains(search) ?? false) ||
                (u.Email?.ToLower().Contains(search) ?? false) ||
                ($"{u.FirstName} {u.LastName}".Trim().ToLower().Contains(search))).ToList();

        var totalCount = allRoleUsers.Count;
        var page = request.ValidatedPage;
        var pageSize = request.ValidatedPageSize;
        var pageUsers = allRoleUsers.Skip((page - 1) * pageSize).Take(pageSize).ToList();

        var items = await MapUsersToSourceItems(pageUsers, client, cancellationToken);

        return new PagedResult<UserRoleSourceItem>
        {
            Items = items,
            TotalCount = totalCount,
            Page = page,
            PageSize = pageSize
        };
    }

    public async Task<UserRoleSourceItem?> GetUserWithRolesAsync(
        string userId,
        CancellationToken cancellationToken = default)
    {
        var token = await GetAdminToken(cancellationToken);
        var client = CreateAuthorizedClient(token);

        KeycloakUser? user;
        try
        {
            var json = await client.GetStringAsync(
                $"/admin/realms/{_options.Realm}/users/{userId}", cancellationToken);
            user = JsonSerializer.Deserialize<KeycloakUser>(json, _json);
        }
        catch (HttpRequestException ex) when (ex.StatusCode == System.Net.HttpStatusCode.NotFound)
        {
            return null;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Greška pri dohvatu korisnika {UserId} iz Keycloaka.", userId);
            throw;
        }

        if (user is null) return null;

        var roles = await FetchUserRoles(client, user.Id, cancellationToken);
        return MapToSourceItem(user, roles);
    }

    private async Task<string> GetAdminToken(CancellationToken cancellationToken)
    {
        var client = _httpClientFactory.CreateClient("KeycloakAdmin");
        var form = new FormUrlEncodedContent(new Dictionary<string, string>
        {
            ["grant_type"] = "client_credentials",
            ["client_id"] = _options.ClientId,
            ["client_secret"] = _options.ClientSecret
        });

        HttpResponseMessage response;
        try
        {
            response = await client.PostAsync(
                $"/realms/{_options.Realm}/protocol/openid-connect/token", form, cancellationToken);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Keycloak Admin nije dostupan na {BaseUrl}.", _options.BaseUrl);
            throw new InvalidOperationException(
                "Keycloak Admin servis nije dostupan. Provjerite KeycloakAdmin konfiguraciju.", ex);
        }

        if (!response.IsSuccessStatusCode)
        {
            var body = await response.Content.ReadAsStringAsync(cancellationToken);
            _logger.LogError(
                "Keycloak Admin token: {Status} — {Body}. ClientId={ClientId} Realm={Realm}",
                response.StatusCode, body, _options.ClientId, _options.Realm);
            throw new InvalidOperationException(
                $"Keycloak Admin autentifikacija neuspješna ({response.StatusCode}). " +
                "Provjerite ClientSecret i service account role (view-users, manage-users).");
        }

        var json = await response.Content.ReadAsStringAsync(cancellationToken);
        var tokenResponse = JsonSerializer.Deserialize<TokenResponse>(json, _json);
        if (tokenResponse?.AccessToken is null)
            throw new InvalidOperationException("Keycloak token odgovor ne sadrži access_token.");

        return tokenResponse.AccessToken;
    }

    private HttpClient CreateAuthorizedClient(string token)
    {
        var client = _httpClientFactory.CreateClient("KeycloakAdmin");
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
        return client;
    }

    /// <summary>
    /// Vraća URL za dohvat svih korisnika (do 1000) iz Keycloaka.
    /// Bez `enabled` parametra — kad se on proslijedi, Keycloak nekonzistentno
    /// ukljućuje i service account korisnike u rezultat. Filtriranje po
    /// statusu (aktivan/neaktivan) i paginacija rade se na klijentu.
    /// </summary>
    private string BuildUsersUrl(string? search)
    {
        var url = $"/admin/realms/{_options.Realm}/users?first=0&max=1000";

        if (!string.IsNullOrEmpty(search))
            url += $"&search={Uri.EscapeDataString(search)}";

        return url;
    }

    private async Task<List<UserRoleSourceItem>> MapUsersToSourceItems(
        List<KeycloakUser> users,
        HttpClient client,
        CancellationToken cancellationToken)
    {
        var result = new List<UserRoleSourceItem>(users.Count);
        foreach (var user in users)
        {
            var roles = await FetchUserRoles(client, user.Id, cancellationToken);
            result.Add(MapToSourceItem(user, roles));
        }
        return result;
    }

    private async Task<List<string>> FetchUserRoles(HttpClient client, string userId, CancellationToken cancellationToken)
    {
        try
        {
            var json = await client.GetStringAsync(
                $"/admin/realms/{_options.Realm}/users/{userId}/role-mappings/realm", cancellationToken);
            var roles = JsonSerializer.Deserialize<List<KeycloakRole>>(json, _json) ?? [];
            return roles.Select(r => r.Name).ToList();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Greška pri dohvatu rola za korisnika {UserId}.", userId);
            return [];
        }
    }

    private static UserRoleSourceItem MapToSourceItem(KeycloakUser user, List<string> roles)
    {
        var displayName = $"{user.FirstName} {user.LastName}".Trim();
        return new()
        {
            UserId = user.Id,
            Username = user.Username,
            DisplayName = string.IsNullOrWhiteSpace(displayName) ? null : displayName,
            Email = user.Email,
            IsActive = user.Enabled,
            Roles = roles.AsReadOnly()
        };
    }
}
