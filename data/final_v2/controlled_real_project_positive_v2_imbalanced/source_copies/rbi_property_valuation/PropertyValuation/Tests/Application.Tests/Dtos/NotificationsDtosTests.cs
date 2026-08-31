using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Notifications.Models;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Dtos;

public sealed class NotificationsDtosTests
{
    [Fact]
    public void RoleManagementNotificationEvent_DefaultsSeverityToInfo()
    {
        var ev = new RoleManagementNotificationEvent
        {
            EventType    = "ROLE_ASSIGNED",
            ActorUserId  = "admin-1",
            TargetUserId = "user-1",
            Role         = "AM",
            Message      = "Rola AM dodijeljena korisniku user-1",
            OccurredAt   = new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc)
        };

        Assert.Equal("Info", ev.Severity);
        Assert.Equal("ROLE_ASSIGNED", ev.EventType);
        Assert.Equal("AM", ev.Role);
        Assert.Null(ev.Reason);
        Assert.Null(ev.CorrelationId);
    }

    [Fact]
    public void RoleManagementNotificationEvent_AllowsCriticalSeverityWithReason()
    {
        var ev = new RoleManagementNotificationEvent
        {
            EventType    = "ADMIN_ROLE_TRANSFERRED",
            ActorUserId  = "admin-1",
            TargetUserId = "user-2",
            Severity     = "Critical",
            Message      = "Administrator rola prenesena",
            OccurredAt   = new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc),
            Reason       = "Predaja administracije",
            CorrelationId = "corr-1"
        };

        Assert.Equal("Critical", ev.Severity);
        Assert.Equal("Predaja administracije", ev.Reason);
        Assert.Equal("corr-1", ev.CorrelationId);
    }

    [Fact]
    public void OrderNotificationsOptions_DefaultsCaInboxEmailToEmpty()
    {
        var options = new OrderNotificationsOptions();

        Assert.Equal("", options.CaInboxEmail);
        Assert.Equal("OrderNotifications", OrderNotificationsOptions.SectionName);
    }

    [Fact]
    public void NotificationRequest_StoresAllProperties()
    {
        var request = new NotificationRequest(
            RecipientUserId: "user-1",
            RecipientRole: null,
            Channel: NotificationChannel.InApp,
            Subject: "Naslov",
            Message: "Poruka",
            RelatedEntityType: "AppraisalOrder",
            RelatedEntityId: "5");

        Assert.Equal(NotificationChannel.InApp, request.Channel);
        Assert.Equal("user-1", request.RecipientUserId);
        Assert.Equal("AppraisalOrder", request.RelatedEntityType);
        Assert.Null(request.RecipientEmail);
    }

    [Fact]
    public void NotificationItem_StoresAllProperties()
    {
        var item = new NotificationItem(
            Id: 1,
            Subject: "Naslov",
            Message: "Poruka",
            IsRead: false,
            CreatedAt: new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc),
            RelatedEntityType: "AppraisalOrder",
            RelatedEntityId: "5");

        Assert.False(item.IsRead);
        Assert.Equal("Naslov", item.Subject);
    }

    [Fact]
    public void NotificationDto_StoresAllProperties()
    {
        var now = new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc);

        var dto = new NotificationDto(
            Id: 1,
            Subject: "Naslov",
            Message: "Poruka",
            IsRead: false,
            CreatedAt: now,
            RelatedEntityType: "AppraisalOrder",
            RelatedEntityId: "10");

        Assert.Equal(1, dto.Id);
        Assert.Equal("Naslov", dto.Subject);
        Assert.Equal("Poruka", dto.Message);
        Assert.False(dto.IsRead);
        Assert.Equal(now, dto.CreatedAt);
        Assert.Equal("AppraisalOrder", dto.RelatedEntityType);
        Assert.Equal("10", dto.RelatedEntityId);
    }

    [Fact]
    public void NotificationInboxResult_StoresAllProperties()
    {
        var item = new NotificationDto(1, "Naslov", "Poruka", true,
            new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc), null, null);

        var result = new NotificationInboxResult(
            Items: [item],
            TotalCount: 1,
            Page: 1,
            PageSize: 20,
            UnreadCount: 0);

        Assert.Single(result.Items);
        Assert.Equal(1, result.TotalCount);
        Assert.Equal(1, result.Page);
        Assert.Equal(20, result.PageSize);
        Assert.Equal(0, result.UnreadCount);
    }
}
