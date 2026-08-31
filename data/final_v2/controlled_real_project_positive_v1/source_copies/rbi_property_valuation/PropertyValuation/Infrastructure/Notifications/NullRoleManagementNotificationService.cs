using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Notifications.Models;

namespace RBBH.CollateralAppraisal.Infrastructure.Notifications;

/// <summary>
/// MVP implementacija koja ne šalje stvarne notifikacije — samo loguje svaki event.
/// Zamijeniti kada se doda notification infrastruktura (email, webhook, push).
/// </summary>
public sealed class NullRoleManagementNotificationService : IRoleManagementNotificationService
{
    private readonly ILogger<NullRoleManagementNotificationService> _logger;

    public NullRoleManagementNotificationService(ILogger<NullRoleManagementNotificationService> logger)
    {
        _logger = logger;
    }

    public Task NotifyRoleAssignedAsync(RoleManagementNotificationEvent e, CancellationToken cancellationToken = default)
    {
        _logger.LogInformation(
            "[Notification] {EventType} — actor={ActorUserId} target={TargetUserId} role={Role}",
            e.EventType, e.ActorUserId, e.TargetUserId, e.Role);
        return Task.CompletedTask;
    }

    public Task NotifyRoleRemovedAsync(RoleManagementNotificationEvent e, CancellationToken cancellationToken = default)
    {
        _logger.LogInformation(
            "[Notification] {EventType} — actor={ActorUserId} target={TargetUserId} role={Role}",
            e.EventType, e.ActorUserId, e.TargetUserId, e.Role);
        return Task.CompletedTask;
    }

    public Task NotifyAdminRoleTransferredAsync(RoleManagementNotificationEvent e, CancellationToken cancellationToken = default)
    {
        _logger.LogCritical(
            "[Notification] {EventType} — actor={ActorUserId} target={TargetUserId} reason={Reason}",
            e.EventType, e.ActorUserId, e.TargetUserId, e.Reason);
        return Task.CompletedTask;
    }

    public Task NotifyRoleChangeBlockedAsync(RoleManagementNotificationEvent e, CancellationToken cancellationToken = default)
    {
        _logger.LogWarning(
            "[Notification] {EventType} — actor={ActorUserId} target={TargetUserId} reason={Reason}",
            e.EventType, e.ActorUserId, e.TargetUserId, e.Reason);
        return Task.CompletedTask;
    }
}
