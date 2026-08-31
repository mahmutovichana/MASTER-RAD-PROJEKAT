using RBBH.CollateralAppraisal.Application.Notifications.Models;

namespace RBBH.CollateralAppraisal.Application.Notifications;

/// <summary>
/// Servis za slanje notifikacija vezanih za promjene rola.
///
/// Pravila:
/// - Ako notification servis ne uspije, promjena role može ostati uspješna.
///   Greška se mora logovati. Koristiti try/catch po uzoru na IAuditService pattern u projektu.
/// - Ne slati duple notifikacije za isti CorrelationId ako sistem podržava deduplikaciju.
/// - Ne slati osjetljive interne podatke u porukama.
/// - Critical eventi (admin transfer, posljednji admin blokiran) trebaju fallback/retry logiku.
///
/// MVP implementacija: NullRoleManagementNotificationService (ne radi ništa, samo loguje).
/// Zamjeniti stvarnom implementacijom kada se doda notification infrastruktura.
///
/// TODO (Hamza): Implementirati NullRoleManagementNotificationService u Infrastructure/Notifications/
///              Registrovati u Infrastructure/DependencyInjection.cs:
///              services.AddScoped&lt;IRoleManagementNotificationService, NullRoleManagementNotificationService&gt;();
/// </summary>
public interface IRoleManagementNotificationService
{
    /// <summary>Notifikacija pri uspješnoj dodjeli role (Severity: Info).</summary>
    Task NotifyRoleAssignedAsync(
        RoleManagementNotificationEvent notificationEvent,
        CancellationToken cancellationToken = default);

    /// <summary>Notifikacija pri uspješnom uklanjanju role (Severity: Info).</summary>
    Task NotifyRoleRemovedAsync(
        RoleManagementNotificationEvent notificationEvent,
        CancellationToken cancellationToken = default);

    /// <summary>Notifikacija pri transferu admin role (Severity: Critical).</summary>
    Task NotifyAdminRoleTransferredAsync(
        RoleManagementNotificationEvent notificationEvent,
        CancellationToken cancellationToken = default);

    /// <summary>Notifikacija kada je promjena role blokirana ili nije uspjela (Severity: Warning/Critical).</summary>
    Task NotifyRoleChangeBlockedAsync(
        RoleManagementNotificationEvent notificationEvent,
        CancellationToken cancellationToken = default);
}
