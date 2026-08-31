using RBBH.CollateralAppraisal.Domain.Notifications;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Domain;

public sealed class NotificationTests
{
    [Fact]
    public void CreateInApp_SetsChannelAndPendingStatus()
    {
        var notification = Notification.CreateInApp(
            recipientUserId: "user-1",
            subject: "Naslov",
            message: "Poruka",
            relatedEntityType: "AppraisalOrder",
            relatedEntityId: "123");

        Assert.Equal(NotificationChannel.InApp, notification.Channel);
        Assert.Equal(NotificationStatus.Pending, notification.Status);
        Assert.Equal("user-1", notification.RecipientUserId);
        Assert.Equal("Naslov", notification.Subject);
        Assert.Equal("Poruka", notification.Message);
        Assert.Equal("AppraisalOrder", notification.RelatedEntityType);
        Assert.Equal("123", notification.RelatedEntityId);
        Assert.Null(notification.RecipientRole);
        Assert.False(notification.IsRead);
    }

    [Fact]
    public void CreateEmail_AllowsRoleBasedRecipientWithoutUserId()
    {
        var notification = Notification.CreateEmail(
            recipientUserId: null,
            recipientRole: "CA",
            subject: "Naslov",
            message: "Poruka");

        Assert.Equal(NotificationChannel.Email, notification.Channel);
        Assert.Equal(NotificationStatus.Pending, notification.Status);
        Assert.Null(notification.RecipientUserId);
        Assert.Equal("CA", notification.RecipientRole);
    }

    [Fact]
    public void MarkSent_SetsStatusSentAtAndUpdatedAt()
    {
        var notification = Notification.CreateInApp("user-1", "S", "M");
        var now = DateTime.UtcNow;

        notification.MarkSent(now);

        Assert.Equal(NotificationStatus.Sent, notification.Status);
        Assert.Equal(now, notification.SentAt);
        Assert.Equal(now, notification.UpdatedAt);
    }

    [Fact]
    public void MarkFailed_SetsErrorMessageAndIncrementsRetryCount()
    {
        var notification = Notification.CreateInApp("user-1", "S", "M");
        var now = DateTime.UtcNow;

        notification.MarkFailed("SMTP timeout", now);

        Assert.Equal(NotificationStatus.Failed, notification.Status);
        Assert.Equal("SMTP timeout", notification.ErrorMessage);
        Assert.Equal(1, notification.RetryCount);
        Assert.Equal(now, notification.UpdatedAt);

        notification.MarkFailed("SMTP timeout again", now.AddMinutes(1));

        Assert.Equal(2, notification.RetryCount);
        Assert.Equal("SMTP timeout again", notification.ErrorMessage);
    }

    [Fact]
    public void MarkRead_SetsIsReadAndReadAt()
    {
        var notification = Notification.CreateInApp("user-1", "S", "M");
        var now = DateTime.UtcNow;

        notification.MarkRead(now);

        Assert.True(notification.IsRead);
        Assert.Equal(now, notification.ReadAt);
        Assert.Equal(now, notification.UpdatedAt);
    }
}
