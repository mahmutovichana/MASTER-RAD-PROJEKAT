namespace RBBH.TestAutomation.Api.Services.Auth;

/// <summary>
/// Centralno mjesto za bilježenje sigurnosnih događaja prijave.
///
/// Dual-write: svaki događaj ide u Serilog (strukturirani log → Elasticsearch
/// dashboard) i u <see cref="IAuditLogStore"/> (in-memory → admin UI pregled).
///
/// Uz Keycloak: isti pozivi se premještaju u OIDC events
/// (OnTokenValidated / OnRemoteFailure) — apstrakcija ostaje ista.
/// </summary>
public sealed class SecurityEventLogger(
    IAuditLogStore auditLogStore,
    ILogger<SecurityEventLogger> logger)
{
    /// <summary>Bilježi uspješnu prijavu.</summary>
    public void LogLoginSuccess(string username, string? ipAddress)
    {
        auditLogStore.Add(new AuditLogEntry(
            DateTime.UtcNow,
            AuditEventTypes.LoginSuccess,
            username,
            ipAddress,
            FailureReason: null));

        logger.LogInformation(
            "Successful login for {Username} from {IpAddress}",
            username, ipAddress ?? "unknown");
    }

    /// <summary>Bilježi neuspješnu prijavu (pogrešni kredencijali ili zaključan nalog).</summary>
    public void LogLoginFailure(string username, string? ipAddress, string failureReason)
    {
        auditLogStore.Add(new AuditLogEntry(
            DateTime.UtcNow,
            AuditEventTypes.LoginFailure,
            username,
            ipAddress,
            failureReason));

        logger.LogWarning(
            "Failed login for {Username} from {IpAddress}: {FailureReason}",
            username, ipAddress ?? "unknown", failureReason);
    }

    /// <summary>Bilježi odjavu korisnika.</summary>
    public void LogLogout(string username, string? ipAddress)
    {
        auditLogStore.Add(new AuditLogEntry(
            DateTime.UtcNow,
            AuditEventTypes.Logout,
            username,
            ipAddress,
            FailureReason: null));

        logger.LogInformation(
            "Logout for {Username} from {IpAddress}",
            username, ipAddress ?? "unknown");
    }
}
