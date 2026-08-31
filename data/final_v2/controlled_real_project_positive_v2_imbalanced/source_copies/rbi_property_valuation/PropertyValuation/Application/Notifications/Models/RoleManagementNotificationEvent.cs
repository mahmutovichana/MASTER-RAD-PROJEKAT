namespace RBBH.CollateralAppraisal.Application.Notifications.Models;

/// <summary>
/// Event model za notifikacije vezane za role management promjene.
///
/// Severity:
/// - Info    : normalna dodjela/uklanjanje role
/// - Warning : blokirana akcija (npr. pokušaj uklanjanja posljednjeg admina)
/// - Critical: transfer admin role, pokušaj uklanjanja posljednjeg Administratora
///
/// EventType konstante:
/// - "ROLE_ASSIGNED"
/// - "ROLE_REMOVED"
/// - "ADMIN_ROLE_TRANSFERRED"
/// - "LAST_ADMIN_REMOVAL_BLOCKED"
/// - "ROLE_CHANGE_BLOCKED"
/// - "ROLE_CHANGE_FAILED"
///
/// Napomena: Audit i Notification su različiti sistemi.
/// Audit bilježi interni trag za forenziku. Notification informiše korisnike/admine.
/// </summary>
public sealed class RoleManagementNotificationEvent
{
    public string EventType { get; init; } = string.Empty;
    public string ActorUserId { get; init; } = string.Empty;
    public string TargetUserId { get; init; } = string.Empty;
    public string? Role { get; init; }
    public string Severity { get; init; } = "Info";
    public string Message { get; init; } = string.Empty;
    public DateTime OccurredAt { get; init; }
    public string? Reason { get; init; }
    public string? CorrelationId { get; init; }
}
