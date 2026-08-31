using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Infrastructure.Auth;

namespace RBBH.CollateralAppraisal.Infrastructure.Users;

/// <summary>
/// Suspenzija i reaktivacija korisnika putem Keycloak Admin API.
/// Keycloak ostaje source of truth — baza ne drži lokalni status.
/// </summary>
public sealed class UserSuspensionService : IUserSuspensionService
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly KeycloakAdminOptions _options;
    private readonly ICurrentUserService _currentUser;
    private readonly IAuditService _audit;
    private readonly ILogger<UserSuspensionService> _logger;

    private static readonly JsonSerializerOptions _json = new() { PropertyNameCaseInsensitive = true };

    private record TokenResponse([property: JsonPropertyName("access_token")] string AccessToken);
    private record KeycloakUserInfo(string Id, string Username, bool Enabled);

    public UserSuspensionService(
        IHttpClientFactory httpClientFactory,
        IOptions<KeycloakAdminOptions> options,
        ICurrentUserService currentUser,
        IAuditService audit,
        ILogger<UserSuspensionService> logger)
    {
        _httpClientFactory = httpClientFactory;
        _options           = options.Value;
        _currentUser       = currentUser;
        _audit             = audit;
        _logger            = logger;
    }

    public async Task SuspendAsync(string userId, string? reason, CancellationToken ct = default)
    {
        if (userId == _currentUser.UserId)
            throw new ConflictException(
                "Ne možete suspendovati vlastiti nalog.", "SELF_SUSPENSION_BLOCKED");

        var client = await GetAuthorizedClientAsync(ct);

        var user = await GetUserAsync(client, userId, ct)
            ?? throw new NotFoundException("Korisnik nije pronađen.", "USER_NOT_FOUND");

        if (!user.Enabled)
            throw new ConflictException("Korisnik je već suspendovan.", "USER_ALREADY_SUSPENDED");

        await SetUserEnabledAsync(client, userId, false, ct);

        await RecordAuditSafeAsync(AuditActions.UserSuspended, userId, user.Username,
            new { Reason = reason }, ct);
    }

    public async Task ReactivateAsync(string userId, CancellationToken ct = default)
    {
        var client = await GetAuthorizedClientAsync(ct);

        var user = await GetUserAsync(client, userId, ct)
            ?? throw new NotFoundException("Korisnik nije pronađen.", "USER_NOT_FOUND");

        if (user.Enabled)
            throw new ConflictException("Korisnik je već aktivan.", "USER_ALREADY_ACTIVE");

        await SetUserEnabledAsync(client, userId, true, ct);

        await RecordAuditSafeAsync(AuditActions.UserReactivated, userId, user.Username, null, ct);
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    private async Task<KeycloakUserInfo?> GetUserAsync(HttpClient client, string userId, CancellationToken ct)
    {
        var response = await client.GetAsync(
            $"/admin/realms/{_options.Realm}/users/{userId}", ct);

        if (response.StatusCode == System.Net.HttpStatusCode.NotFound) return null;
        response.EnsureSuccessStatusCode();

        var json = await response.Content.ReadAsStringAsync(ct);
        return JsonSerializer.Deserialize<KeycloakUserInfo>(json, _json);
    }

    private async Task SetUserEnabledAsync(HttpClient client, string userId, bool enabled, CancellationToken ct)
    {
        var body     = JsonSerializer.Serialize(new { enabled });
        var response = await client.PutAsync(
            $"/admin/realms/{_options.Realm}/users/{userId}",
            new StringContent(body, Encoding.UTF8, "application/json"), ct);
        response.EnsureSuccessStatusCode();
    }

    private async Task<HttpClient> GetAuthorizedClientAsync(CancellationToken ct)
    {
        var client = _httpClientFactory.CreateClient("KeycloakAdmin");
        var form   = new FormUrlEncodedContent(new Dictionary<string, string>
        {
            ["grant_type"]    = "client_credentials",
            ["client_id"]     = _options.ClientId,
            ["client_secret"] = _options.ClientSecret
        });

        var resp  = await client.PostAsync($"/realms/{_options.Realm}/protocol/openid-connect/token", form, ct);
        resp.EnsureSuccessStatusCode();

        var json  = await resp.Content.ReadAsStringAsync(ct);
        var token = (JsonSerializer.Deserialize<TokenResponse>(json, _json)
            ?? throw new InvalidOperationException("Token nije validan.")).AccessToken;

        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
        return client;
    }

    private async Task RecordAuditSafeAsync(
        string action, string userId, string? username, object? details, CancellationToken ct)
    {
        try
        {
            await _audit.RecordAsync(new AuditEvent
            {
                Action            = action,
                OperationType     = AuditOperationTypes.Update,
                Module            = AuditModules.Users,
                EntityType        = "User",
                EntityKey         = userId,
                EntityDisplayName = username ?? userId,
                NewValues         = details,
                Status            = AuditStatuses.Success,
                Severity          = AuditSeverity.Security
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Audit nije zapisan za korisnika {UserId}.", userId);
        }
    }
}
