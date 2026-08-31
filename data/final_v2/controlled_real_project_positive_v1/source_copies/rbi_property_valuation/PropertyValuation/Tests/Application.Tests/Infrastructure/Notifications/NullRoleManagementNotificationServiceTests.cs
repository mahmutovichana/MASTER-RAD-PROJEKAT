using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Notifications.Models;
using RBBH.CollateralAppraisal.Infrastructure.Notifications;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Notifications;

public sealed class NullRoleManagementNotificationServiceTests
{
    private readonly ILogger<NullRoleManagementNotificationService> _logger =
        Substitute.For<ILogger<NullRoleManagementNotificationService>>();

    private readonly NullRoleManagementNotificationService _sut;

    public NullRoleManagementNotificationServiceTests()
    {
        _sut = new NullRoleManagementNotificationService(_logger);
    }

    private static RoleManagementNotificationEvent MakeEvent(string eventType, string severity) =>
        new()
        {
            EventType     = eventType,
            ActorUserId   = "actor-1",
            TargetUserId  = "target-1",
            Role          = "AM",
            Severity      = severity,
            Message       = "Test message",
            OccurredAt    = DateTime.UtcNow,
            Reason        = "test reason",
            CorrelationId = "corr-1"
        };

    [Fact]
    public async Task NotifyRoleAssignedAsync_LogsInformationAndCompletes()
    {
        await _sut.NotifyRoleAssignedAsync(MakeEvent("ROLE_ASSIGNED", "Info"));

        var call = Assert.Single(_logger.ReceivedCalls());
        Assert.Equal(LogLevel.Information, call.GetArguments()[0]);
    }

    [Fact]
    public async Task NotifyRoleRemovedAsync_LogsInformationAndCompletes()
    {
        await _sut.NotifyRoleRemovedAsync(MakeEvent("ROLE_REMOVED", "Info"));

        var call = Assert.Single(_logger.ReceivedCalls());
        Assert.Equal(LogLevel.Information, call.GetArguments()[0]);
    }

    [Fact]
    public async Task NotifyAdminRoleTransferredAsync_LogsCriticalAndCompletes()
    {
        await _sut.NotifyAdminRoleTransferredAsync(MakeEvent("ADMIN_ROLE_TRANSFERRED", "Critical"));

        var call = Assert.Single(_logger.ReceivedCalls());
        Assert.Equal(LogLevel.Critical, call.GetArguments()[0]);
    }

    [Fact]
    public async Task NotifyRoleChangeBlockedAsync_LogsWarningAndCompletes()
    {
        await _sut.NotifyRoleChangeBlockedAsync(MakeEvent("ROLE_CHANGE_BLOCKED", "Warning"));

        var call = Assert.Single(_logger.ReceivedCalls());
        Assert.Equal(LogLevel.Warning, call.GetArguments()[0]);
    }
}
