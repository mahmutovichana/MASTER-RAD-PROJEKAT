using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging.Abstractions;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Domain.Notifications;
using RBBH.CollateralAppraisal.Infrastructure.Notifications;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Infrastructure.Tests.Notifications;

public sealed class NotificationServiceTests
{
    private static ApplicationDbContext CreateDb()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;

        return new ApplicationDbContext(options);
    }

    private static NotificationService CreateService(ApplicationDbContext db, IEmailProvider emailProvider) =>
        new(db, emailProvider, NullLogger<NotificationService>.Instance);

    [Fact]
    public async Task NotifyUserAsync_WithoutEmail_CreatesOnlyInAppNotification()
    {
        await using var db = CreateDb();
        var emailProvider = new FakeEmailProvider();
        var service = CreateService(db, emailProvider);

        await service.NotifyUserAsync("user-1", "Naslov", "Poruka");

        var saved = Assert.Single(db.Notifications);
        Assert.Equal(RBBH.CollateralAppraisal.Domain.Notifications.NotificationChannel.InApp, saved.Channel);
        Assert.Equal("user-1", saved.RecipientUserId);
        Assert.False(saved.IsRead);
        Assert.Empty(emailProvider.SentMessages);
    }

    [Fact]
    public async Task NotifyUserAsync_WithSendEmail_CreatesInAppAndEmailNotification()
    {
        await using var db = CreateDb();
        var emailProvider = new FakeEmailProvider();
        var service = CreateService(db, emailProvider);

        await service.NotifyUserAsync(
            "user-1", "Naslov", "Poruka",
            sendEmail: true, emailAddress: "user1@example.com");

        Assert.Equal(2, await db.Notifications.CountAsync());

        var emailNotification = await db.Notifications.SingleAsync(n => n.Channel == RBBH.CollateralAppraisal.Domain.Notifications.NotificationChannel.Email);
        Assert.Equal(NotificationStatus.Sent, emailNotification.Status);

        var sentMessage = Assert.Single(emailProvider.SentMessages);
        Assert.Equal("user1@example.com", sentMessage.ToAddress);
        Assert.Equal("Naslov", sentMessage.Subject);
    }

    [Fact]
    public async Task NotifyUserAsync_WhenEmailProviderThrows_MarksEmailNotificationAsFailed()
    {
        await using var db = CreateDb();
        var emailProvider = new FakeEmailProvider { ShouldThrow = true };
        var service = CreateService(db, emailProvider);

        await service.NotifyUserAsync(
            "user-1", "Naslov", "Poruka",
            sendEmail: true, emailAddress: "user1@example.com");

        var emailNotification = await db.Notifications.SingleAsync(n => n.Channel == RBBH.CollateralAppraisal.Domain.Notifications.NotificationChannel.Email);
        Assert.Equal(NotificationStatus.Failed, emailNotification.Status);
        Assert.NotNull(emailNotification.ErrorMessage);
    }

    [Fact]
    public async Task NotifyUserAsync_WithSendEmailButNoAddress_SkipsEmail()
    {
        await using var db = CreateDb();
        var emailProvider = new FakeEmailProvider();
        var service = CreateService(db, emailProvider);

        await service.NotifyUserAsync("user-1", "Naslov", "Poruka", sendEmail: true, emailAddress: null);

        var saved = Assert.Single(db.Notifications);
        Assert.Equal(RBBH.CollateralAppraisal.Domain.Notifications.NotificationChannel.InApp, saved.Channel);
    }

    [Fact]
    public async Task NotifyUsersAsync_CreatesOneInAppNotificationPerDistinctUser()
    {
        await using var db = CreateDb();
        var service = CreateService(db, new FakeEmailProvider());

        await service.NotifyUsersAsync(["user-1", "user-2", "user-1"], "CO obavještenje", "Poruka");

        var notifications = await db.Notifications.ToListAsync();
        Assert.Equal(2, notifications.Count);
        Assert.Contains(notifications, n => n.RecipientUserId == "user-1");
        Assert.Contains(notifications, n => n.RecipientUserId == "user-2");
    }

    [Fact]
    public async Task GetUnreadCountAsync_CountsOnlyUnreadInAppForUser()
    {
        await using var db = CreateDb();
        var service = CreateService(db, new FakeEmailProvider());

        await service.NotifyUserAsync("user-1", "A", "msg");
        await service.NotifyUserAsync("user-1", "B", "msg");
        await service.NotifyUserAsync("user-1", "C", "msg", sendEmail: true, emailAddress: "x@example.com");
        await service.NotifyUserAsync("user-2", "D", "msg");

        var firstId = (await db.Notifications.FirstAsync(n => n.Subject == "A" && n.RecipientUserId == "user-1")).Id;
        await service.MarkReadAsync(firstId, "user-1");

        var unread = await service.GetUnreadCountAsync("user-1");

        // "A" je pročitano. "B" i in-app dio "C" ostaju nepročitani — Email zapis "C" se ne broji.
        Assert.Equal(2, unread);
    }

    [Fact]
    public async Task GetInboxAsync_ReturnsPaginatedItemsNewestFirstWithUnreadCount()
    {
        await using var db = CreateDb();
        var service = CreateService(db, new FakeEmailProvider());

        await service.NotifyUserAsync("user-1", "Prva", "msg");
        await Task.Delay(5);
        await service.NotifyUserAsync("user-1", "Druga", "msg");
        await Task.Delay(5);
        await service.NotifyUserAsync("user-1", "Treca", "msg");

        var page1 = await service.GetInboxAsync("user-1", page: 1, pageSize: 2);

        Assert.Equal(3, page1.TotalCount);
        Assert.Equal(3, page1.UnreadCount);
        Assert.Equal(2, page1.Items.Count);
        Assert.Equal("Treca", page1.Items[0].Subject);
        Assert.Equal("Druga", page1.Items[1].Subject);

        var page2 = await service.GetInboxAsync("user-1", page: 2, pageSize: 2);
        Assert.Single(page2.Items);
        Assert.Equal("Prva", page2.Items[0].Subject);
    }

    [Fact]
    public async Task GetInboxAsync_UnreadOnly_FiltersOutReadNotifications()
    {
        await using var db = CreateDb();
        var service = CreateService(db, new FakeEmailProvider());

        await service.NotifyUserAsync("user-1", "Prva", "msg");
        await service.NotifyUserAsync("user-1", "Druga", "msg");

        var firstId = (await db.Notifications.FirstAsync(n => n.Subject == "Prva")).Id;
        await service.MarkReadAsync(firstId, "user-1");

        var inbox = await service.GetInboxAsync("user-1", unreadOnly: true);

        var item = Assert.Single(inbox.Items);
        Assert.Equal("Druga", item.Subject);
        Assert.Equal(1, inbox.UnreadCount);
        Assert.Equal(1, inbox.TotalCount);
    }

    [Fact]
    public async Task MarkReadAsync_ForOtherUsersNotification_ReturnsFalseAndDoesNotModify()
    {
        await using var db = CreateDb();
        var service = CreateService(db, new FakeEmailProvider());

        await service.NotifyUserAsync("user-1", "Naslov", "Poruka");
        var id = (await db.Notifications.FirstAsync()).Id;

        var found = await service.MarkReadAsync(id, "user-2");

        Assert.False(found);
        Assert.False((await db.Notifications.FirstAsync(n => n.Id == id)).IsRead);
    }

    [Fact]
    public async Task MarkReadAsync_ForNonExistentNotification_ReturnsFalse()
    {
        await using var db = CreateDb();
        var service = CreateService(db, new FakeEmailProvider());

        var found = await service.MarkReadAsync(999, "user-1");

        Assert.False(found);
    }

    [Fact]
    public async Task MarkReadAsync_IsIdempotent()
    {
        await using var db = CreateDb();
        var service = CreateService(db, new FakeEmailProvider());

        await service.NotifyUserAsync("user-1", "Naslov", "Poruka");
        var id = (await db.Notifications.FirstAsync()).Id;

        Assert.True(await service.MarkReadAsync(id, "user-1"));
        Assert.True(await service.MarkReadAsync(id, "user-1"));

        Assert.True((await db.Notifications.FirstAsync(n => n.Id == id)).IsRead);
    }

    private sealed class FakeEmailProvider : IEmailProvider
    {
        public List<EmailMessage> SentMessages { get; } = [];
        public bool ShouldThrow { get; set; }

        public Task SendAsync(EmailMessage message, CancellationToken ct = default)
        {
            if (ShouldThrow)
                throw new InvalidOperationException("SMTP nedostupan.");

            SentMessages.Add(message);
            return Task.CompletedTask;
        }
    }
}
