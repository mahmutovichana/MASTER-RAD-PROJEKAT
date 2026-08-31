using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Common.Validation;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Notifications.Models;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Security.DTOs;
using RBBH.CollateralAppraisal.Application.Security.Interfaces;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Auth;

/// <summary>
/// Implementacija upravljanja rolama putem Keycloak Admin REST API.
///
/// Poslovnih pravila:
/// BR-ROLE-02: Samo Administrator može dodjeljivati i uklanjati role.
/// BR-ROLE-04: Sistem ne smije ostati bez najmanje jednog aktivnog Administratora.
/// BR-ROLE-11: Sve izmjene rola moraju biti auditirane.
/// BR-ROLE-12: Pokušaj uklanjanja posljednjeg Administratora mora biti blokiran i auditiran.
/// </summary>
[ExcludeFromCodeCoverage]
public sealed class RoleManagementService : IRoleManagementService
{
    private readonly IHttpClientFactory                   _httpClientFactory;
    private readonly KeycloakAdminOptions                 _options;
    private readonly IUserRoleProvider                    _userRoleProvider;
    private readonly ICurrentUserService                  _currentUser;
    private readonly IAuditService                        _auditService;
    private readonly IRoleManagementNotificationService   _notificationService;
    private readonly ApplicationDbContext                 _db;
    private readonly ILogger<RoleManagementService>       _logger;

    // CamelCase je obavezan: Keycloak role-mappings API oćekuje { "id", "name" } (mala slova).
    // PropertyNameCaseInsensitive pokriva deserializaciju, CamelCase policy serializaciju.
    private static readonly JsonSerializerOptions _json = new()
    {
        PropertyNameCaseInsensitive = true,
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
    };

    private record KeycloakRole(string Id, string Name);
    private record KeycloakUserInfo(string Id, string Username);
    private record TokenResponse([property: JsonPropertyName("access_token")] string AccessToken);

    public RoleManagementService(
        IHttpClientFactory                 httpClientFactory,
        IOptions<KeycloakAdminOptions>     options,
        IUserRoleProvider                  userRoleProvider,
        ICurrentUserService                currentUser,
        IAuditService                      auditService,
        IRoleManagementNotificationService notificationService,
        ApplicationDbContext               db,
        ILogger<RoleManagementService>     logger)
    {
        _httpClientFactory   = httpClientFactory;
        _options             = options.Value;
        _userRoleProvider    = userRoleProvider;
        _currentUser         = currentUser;
        _auditService        = auditService;
        _notificationService = notificationService;
        _db                  = db;
        _logger              = logger;
    }

    public async Task AssignRoleAsync(AssignRoleRequest request, CancellationToken ct = default)
    {
        await ValidateRoleExistsAndActiveAsync(request.RoleName, ct);

        var user = await _userRoleProvider.GetUserWithRolesAsync(request.UserId, ct)
            ?? throw new NotFoundException(
                $"Korisnik s ID-em '{request.UserId}' nije pronaÄ‘en.", "USER_NOT_FOUND");

        if (user.Roles.Contains(request.RoleName))
            throw new ConflictException(
                $"Korisnik već ima rolu '{request.RoleName}'.",
                "ROLE_USER_ALREADY_HAS_ROLE");

        var token  = await GetAdminTokenAsync(ct);
        var client = CreateAuthorizedClient(token);
        var role   = await GetKeycloakRoleAsync(client, request.RoleName, ct);

        await AssignRoleToUserAsync(client, request.UserId, role, ct);

        await NotifySafeAsync(() => _notificationService.NotifyRoleAssignedAsync(
            BuildEvent("ROLE_ASSIGNED", request.UserId, request.RoleName, "Info"), ct));

        await RecordAuditAsync(AuditActions.UserRoleAssigned, request.UserId,
            new { request.RoleName }, ct, operationType: AuditOperationTypes.Assign);
    }

    public async Task RemoveRoleAsync(RemoveRoleRequest request, CancellationToken ct = default)
    {
        await ValidateRoleExistsAndActiveAsync(request.RoleName, ct);

        var user = await _userRoleProvider.GetUserWithRolesAsync(request.UserId, ct)
            ?? throw new NotFoundException(
                $"Korisnik s ID-em '{request.UserId}' nije pronaÄ‘en.", "USER_NOT_FOUND");

        if (!user.Roles.Contains(request.RoleName))
            throw new ConflictException(
                $"Korisnik nema rolu '{request.RoleName}'.",
                "ROLE_USER_DOES_NOT_HAVE_ROLE");

        if (request.RoleName == AppRoles.Administrator)
            await EnsureNotLastAdminAsync(request.UserId, ct);

        var token  = await GetAdminTokenAsync(ct);
        var client = CreateAuthorizedClient(token);
        var role   = await GetKeycloakRoleAsync(client, request.RoleName, ct);

        await RemoveRoleFromUserAsync(client, request.UserId, role, ct);

        await NotifySafeAsync(() => _notificationService.NotifyRoleRemovedAsync(
            BuildEvent("ROLE_REMOVED", request.UserId, request.RoleName, "Info"), ct));

        await RecordAuditAsync(AuditActions.UserRoleRemoved, request.UserId,
            new { request.RoleName }, ct, operationType: AuditOperationTypes.Remove);
    }

    public async Task TransferAdminRoleAsync(TransferAdminRoleRequest request, CancellationToken ct = default)
    {
        if (string.IsNullOrWhiteSpace(request.Reason))
            throw new ValidationException([
                new ValidationFieldError(
                    "reason",
                    ValidationErrorCodes.RequiredField,
                    "Razlog prenosa administratorske role je obavezan.")
            ]);

        if (request.SourceUserId == request.TargetUserId)
            throw new ConflictException(
                "Nije moguće prenijeti administratorsku rolu na istog korisnika.",
                "ROLE_SELF_TRANSFER");

        var source = await _userRoleProvider.GetUserWithRolesAsync(request.SourceUserId, ct)
            ?? throw new NotFoundException(
                $"Izvorni korisnik '{request.SourceUserId}' nije pronaÄ‘en.", "USER_NOT_FOUND");

        _ = await _userRoleProvider.GetUserWithRolesAsync(request.TargetUserId, ct)
            ?? throw new NotFoundException(
                $"Ciljni korisnik '{request.TargetUserId}' nije pronaÄ‘en.", "USER_NOT_FOUND");

        if (!source.Roles.Contains(AppRoles.Administrator))
            throw new ConflictException(
                "Izvorni korisnik nema Administrator rolu i ne može je prenijeti.",
                "ROLE_SOURCE_USER_NOT_ADMIN");

        var token     = await GetAdminTokenAsync(ct);
        var client    = CreateAuthorizedClient(token);
        var adminRole = await GetKeycloakRoleAsync(client, AppRoles.Administrator, ct);

        // Siguran redoslijed (EC-ROLE-24): najprije dodaj ciljnom, pa ukloni izvornom
        await AssignRoleToUserAsync(client, request.TargetUserId, adminRole, ct);
        await RemoveRoleFromUserAsync(client, request.SourceUserId, adminRole, ct);

        await NotifySafeAsync(() => _notificationService.NotifyAdminRoleTransferredAsync(
            BuildEvent("ADMIN_ROLE_TRANSFERRED", request.TargetUserId, AppRoles.Administrator, "Critical",
                request.Reason), ct));

        await RecordAuditAsync(AuditActions.AdminRoleTransferred, request.SourceUserId,
            new { request.SourceUserId, request.TargetUserId, request.Reason }, ct,
            operationType: AuditOperationTypes.Assign, severity: AuditSeverity.Critical);
    }

    // â”€â”€ Private helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    private async Task ValidateRoleExistsAndActiveAsync(string roleName, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(roleName))
            throw new ValidationException([
                new ValidationFieldError("roleName", ValidationErrorCodes.RequiredField, "Naziv role je obavezan.")
            ]);

        // Provjeri da rola postoji i da je aktivna u lokalnoj bazi.
        // Sistemske role (AppRoles.All) su uvijek poznate; custom role moraju biti u DB.
        var isKnownSystemRole = AppRoles.All.Contains(roleName);
        if (!isKnownSystemRole)
        {
            var roleExists = await _db.RoleDefinitions
                .AnyAsync(r => r.Name == roleName && r.IsActive, ct);

            if (!roleExists)
                throw new ValidationException([
                    new ValidationFieldError(
                        "roleName",
                        ValidationErrorCodes.ValueNotAllowed,
                        $"Rola '{roleName}' nije aktivna ili ne postoji u sistemu.")
                ]);
        }
    }

    private async Task EnsureNotLastAdminAsync(string userId, CancellationToken ct)
    {
        // BR-ROLE-04: Sistem mora imati minimalno 2 aktivna Administratora u svakom trenutku.
        // Dohvatamo max=3 da razlikujemo 1, 2 i 3+ administratora.
        var token  = await GetAdminTokenAsync(ct);
        var client = CreateAuthorizedClient(token);
        var json   = await client.GetStringAsync(
            $"/admin/realms/{_options.Realm}/roles/{AppRoles.Administrator}/users?max=3", ct);
        var admins = JsonSerializer.Deserialize<List<KeycloakUserInfo>>(json, _json) ?? [];

        if (admins.Count <= 2)
        {
            var reason = admins.Count <= 1
                ? "Sistem bi ostao bez Administratora."
                : "Sistem mora imati minimalno dva aktivna Administratora (BR-ROLE-04).";

            await NotifySafeAsync(() => _notificationService.NotifyRoleChangeBlockedAsync(
                BuildEvent("MINIMUM_ADMIN_COUNT_BLOCKED", userId, AppRoles.Administrator, "Critical",
                    reason), ct));

            await RecordAuditAsync(AuditActions.MinimumAdminCountBlocked, userId,
                new { Reason = reason, CurrentAdminCount = admins.Count, MinimumRequired = 2 }, ct,
                operationType: AuditOperationTypes.Remove, severity: AuditSeverity.Critical);

            throw new ConflictException(
                "Nije moguće ukloniti administratorsku rolu. " +
                "Sistem mora imati minimalno dva aktivna Administratora u svakom trenutku.",
                "ROLE_MINIMUM_ADMIN_COUNT_BLOCKED");
        }
    }

    private async Task<string> GetAdminTokenAsync(CancellationToken ct)
    {
        var client = _httpClientFactory.CreateClient("KeycloakAdmin");
        var form = new FormUrlEncodedContent(new Dictionary<string, string>
        {
            ["grant_type"]    = "client_credentials",
            ["client_id"]     = _options.ClientId,
            ["client_secret"] = _options.ClientSecret
        });

        var response = await client.PostAsync(
            $"/realms/{_options.Realm}/protocol/openid-connect/token", form, ct);
        response.EnsureSuccessStatusCode();

        var json = await response.Content.ReadAsStringAsync(ct);
        return (JsonSerializer.Deserialize<TokenResponse>(json, _json)
            ?? throw new InvalidOperationException("Keycloak token odgovor ne sadrži access_token."))
            .AccessToken;
    }

    private HttpClient CreateAuthorizedClient(string token)
    {
        var client = _httpClientFactory.CreateClient("KeycloakAdmin");
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
        return client;
    }

    private async Task<KeycloakRole> GetKeycloakRoleAsync(HttpClient client, string roleName, CancellationToken ct)
    {
        try
        {
            var json = await client.GetStringAsync(
                $"/admin/realms/{_options.Realm}/roles/{Uri.EscapeDataString(roleName)}", ct);
            return JsonSerializer.Deserialize<KeycloakRole>(json, _json)
                ?? throw new InvalidOperationException($"Rola '{roleName}' nije pronaÄ‘ena u Keycloaku.");
        }
        catch (HttpRequestException ex) when (ex.StatusCode == System.Net.HttpStatusCode.NotFound)
        {
            throw new NotFoundException($"Rola '{roleName}' nije pronaÄ‘ena u Keycloaku.", "ROLE_NOT_FOUND");
        }
    }

    private async Task AssignRoleToUserAsync(HttpClient client, string userId, KeycloakRole role, CancellationToken ct)
    {
        var body     = JsonSerializer.Serialize(new[] { role }, _json);
        var content  = new StringContent(body, Encoding.UTF8, "application/json");
        var response = await client.PostAsync(
            $"/admin/realms/{_options.Realm}/users/{userId}/role-mappings/realm", content, ct);
        response.EnsureSuccessStatusCode();
    }

    private async Task RemoveRoleFromUserAsync(HttpClient client, string userId, KeycloakRole role, CancellationToken ct)
    {
        var body    = JsonSerializer.Serialize(new[] { role }, _json);
        var request = new HttpRequestMessage(
            HttpMethod.Delete,
            $"/admin/realms/{_options.Realm}/users/{userId}/role-mappings/realm")
        {
            Content = new StringContent(body, Encoding.UTF8, "application/json")
        };
        var response = await client.SendAsync(request, ct);
        response.EnsureSuccessStatusCode();
    }

    private RoleManagementNotificationEvent BuildEvent(
        string eventType,
        string targetUserId,
        string roleName,
        string severity,
        string? reason = null) =>
        new()
        {
            EventType    = eventType,
            ActorUserId  = _currentUser.UserId ?? string.Empty,
            TargetUserId = targetUserId,
            Role         = roleName,
            Severity     = severity,
            OccurredAt   = DateTime.UtcNow,
            Reason       = reason
        };

    private async Task NotifySafeAsync(Func<Task> notify)
    {
        try   { await notify(); }
        catch (Exception ex) { _logger.LogError(ex, "Slanje notifikacije nije uspjelo."); }
    }

    private async Task RecordAuditAsync(
        string action, string targetUserId, object? details, CancellationToken ct,
        string operationType = AuditOperationTypes.Assign,
        string severity      = AuditSeverity.Security)
    {
        try
        {
            await _auditService.RecordAsync(new AuditEvent
            {
                Action            = action,
                OperationType     = operationType,
                Module            = AuditModules.Roles,
                EntityType        = "User",
                EntityKey         = targetUserId,
                EntityDisplayName = $"User:{targetUserId}",
                NewValues         = details,
                Status            = AuditStatuses.Success,
                Severity          = severity
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Audit log nije zapisan za akciju {Action} na korisniku {UserId}.", action, targetUserId);
        }
    }
}
