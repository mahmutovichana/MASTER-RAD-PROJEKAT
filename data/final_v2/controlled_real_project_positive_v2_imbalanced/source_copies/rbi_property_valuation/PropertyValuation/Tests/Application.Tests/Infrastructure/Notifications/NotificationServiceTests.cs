using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Domain.Notifications;
using RBBH.CollateralAppraisal.Infrastructure.Notifications;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;
using NotificationChannel = RBBH.CollateralAppraisal.Domain.Notifications.NotificationChannel;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Notifications;

public sealed class NotificationServiceTests : IDisposable
{
    private readonly ApplicationDbContext _db;
    private readonly IEmailProvider _emailProvider;
    private readonly NotificationService _sut;

    public NotificationServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db            = new ApplicationDbContext(options);
        _emailProvider = Substitute.For<IEmailProvider>();

        _sut = new NotificationService(_db, _emailProvider, Substitute.For<ILogger<NotificationService>>());
    }

    public void Dispose() => _db.Dispose();

    // ── NotifyUserAsync ─────────────────────────────────────────────────────

    [Fact]
    public async Task NotifyUserAsync_WithoutEmail_CreatesOnlyInAppNotification()
    {
        await _sut.NotifyUserAsync("user-1", "Naslov", "Poruka");

        var saved = await _db.Notifications.SingleAsync();
        Assert.Equal(NotificationChannel.InApp, saved.Channel);
        Assert.Equal("user-1", saved.RecipientUserId);
        Assert.Equal(NotificationStatus.Sent, saved.Status);

        await _emailProvider.DidNotReceive().SendAsync(Arg.Any<EmailMessage>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task NotifyUserAsync_SendEmailWithAddress_CreatesInAppAndEmailNotifications()
    {
        await _sut.NotifyUserAsync(
            "user-1", "Naslov", "Poruka", sendEmail: true, emailAddress: "user1@example.com");

        Assert.Equal(2, await _db.Notifications.CountAsync());

        var email = await _db.Notifications.SingleAsync(n => n.Channel == NotificationChannel.Email);
        Assert.Equal(NotificationStatus.Sent, email.Status);

        await _emailProvider.Received(1).SendAsync(
            Arg.Is<EmailMessage>(m => m.ToAddress == "user1@example.com" && m.Subject == "Naslov"),
            Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task NotifyUserAsync_SendEmailButNoAddress_OnlyCreatesInAppNotification()
    {
        await _sut.NotifyUserAsync("user-1", "Naslov", "Poruka", sendEmail: true, emailAddress: null);

        var saved = await _db.Notifications.SingleAsync();
        Assert.Equal(NotificationChannel.InApp, saved.Channel);

        await _emailProvider.DidNotReceive().SendAsync(Arg.Any<EmailMessage>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task NotifyUserAsync_EmailProviderThrows_MarksEmailNotificationFailed()
    {
        _emailProvider.SendAsync(Arg.Any<EmailMessage>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("SMTP down")));

        await _sut.NotifyUserAsync(
            "user-1", "Naslov", "Poruka", sendEmail: true, emailAddress: "user1@example.com");

        var email = await _db.Notifications.SingleAsync(n => n.Channel == NotificationChannel.Email);
        Assert.Equal(NotificationStatus.Failed, email.Status);
        Assert.Equal("SMTP down", email.ErrorMessage);
    }

    [Fact]
    public async Task NotifyUserAsync_WithRelatedEntity_PersistsRelatedEntityFields()
    {
        await _sut.NotifyUserAsync(
            "user-1", "Naslov", "Poruka", relatedEntityType: "AppraisalOrder", relatedEntityId: "42");

        var saved = await _db.Notifications.SingleAsync();
        Assert.Equal("AppraisalOrder", saved.RelatedEntityType);
        Assert.Equal("42", saved.RelatedEntityId);
    }

    // ── NotifyUsersAsync ────────────────────────────────────────────────────

    [Fact]
    public async Task NotifyUsersAsync_CreatesOneNotificationPerDistinctUser()
    {
        await _sut.NotifyUsersAsync(["user-1", "user-2", "user-1"], "Naslov", "Poruka");

        var notifications = await _db.Notifications.ToListAsync();
        Assert.Equal(2, notifications.Count);
        Assert.Contains(notifications, n => n.RecipientUserId == "user-1");
        Assert.Contains(notifications, n => n.RecipientUserId == "user-2");
        Assert.All(notifications, n => Assert.Equal(NotificationStatus.Sent, n.Status));
    }

    [Fact]
    public async Task NotifyUsersAsync_EmptyList_CreatesNoNotifications()
    {
        await _sut.NotifyUsersAsync([], "Naslov", "Poruka");

        Assert.Empty(await _db.Notifications.ToListAsync());
    }

    // ── GetInboxAsync ───────────────────────────────────────────────────────

    [Fact]
    public async Task GetInboxAsync_ReturnsNewestFirstWithTotalAndUnreadCounts()
    {
        await _sut.NotifyUserAsync("user-1", "Prva", "msg");
        await Task.Delay(5);
        await _sut.NotifyUserAsync("user-1", "Druga", "msg");
        await Task.Delay(5);
        await _sut.NotifyUserAsync("user-1", "Treca", "msg");

        var page1 = await _sut.GetInboxAsync("user-1", page: 1, pageSize: 2);

        Assert.Equal(3, page1.TotalCount);
        Assert.Equal(3, page1.UnreadCount);
        Assert.Equal(2, page1.Items.Count);
        Assert.Equal("Treca", page1.Items[0].Subject);
        Assert.Equal("Druga", page1.Items[1].Subject);

        var page2 = await _sut.GetInboxAsync("user-1", page: 2, pageSize: 2);
        Assert.Single(page2.Items);
        Assert.Equal("Prva", page2.Items[0].Subject);
    }

    [Fact]
    public async Task GetInboxAsync_UnreadOnly_FiltersOutReadNotifications()
    {
        await _sut.NotifyUserAsync("user-1", "Prva", "msg");
        await _sut.NotifyUserAsync("user-1", "Druga", "msg");

        var firstId = (await _db.Notifications.FirstAsync(n => n.Subject == "Prva")).Id;
        await _sut.MarkReadAsync(firstId, "user-1");

        var inbox = await _sut.GetInboxAsync("user-1", unreadOnly: true);

        var item = Assert.Single(inbox.Items);
        Assert.Equal("Druga", item.Subject);
        Assert.Equal(1, inbox.UnreadCount);
        Assert.Equal(1, inbox.TotalCount);
    }

    [Fact]
    public async Task GetInboxAsync_PageAndPageSizeBelowRange_AreClampedToOne()
    {
        await _sut.NotifyUserAsync("user-1", "Prva", "msg");

        var result = await _sut.GetInboxAsync("user-1", page: 0, pageSize: 0);

        Assert.Equal(1, result.Page);
        Assert.Equal(1, result.PageSize);
        Assert.Single(result.Items);
    }

    [Fact]
    public async Task GetInboxAsync_OnlyReturnsInAppChannelNotifications()
    {
        await _sut.NotifyUserAsync(
            "user-1", "Naslov", "Poruka", sendEmail: true, emailAddress: "user1@example.com");

        var inbox = await _sut.GetInboxAsync("user-1");

        var item = Assert.Single(inbox.Items);
        Assert.Equal("Naslov", item.Subject);
    }

    // ── GetUnreadCountAsync ─────────────────────────────────────────────────

    [Fact]
    public async Task GetUnreadCountAsync_CountsOnlyUnreadInAppForUser()
    {
        await _sut.NotifyUserAsync("user-1", "A", "msg");
        await _sut.NotifyUserAsync("user-1", "B", "msg", sendEmail: true, emailAddress: "x@example.com");
        await _sut.NotifyUserAsync("user-2", "C", "msg");

        var firstId = (await _db.Notifications.FirstAsync(n => n.Subject == "A")).Id;
        await _sut.MarkReadAsync(firstId, "user-1");

        var unread = await _sut.GetUnreadCountAsync("user-1");

        Assert.Equal(1, unread);
    }

    // ── MarkReadAsync ───────────────────────────────────────────────────────

    [Fact]
    public async Task MarkReadAsync_NotificationNotFound_ReturnsFalse()
    {
        Assert.False(await _sut.MarkReadAsync(999, "user-1"));
    }

    [Fact]
    public async Task MarkReadAsync_NotificationBelongsToOtherUser_ReturnsFalse()
    {
        await _sut.NotifyUserAsync("user-1", "Naslov", "Poruka");
        var id = (await _db.Notifications.FirstAsync()).Id;

        var found = await _sut.MarkReadAsync(id, "user-2");

        Assert.False(found);
        Assert.False((await _db.Notifications.FirstAsync(n => n.Id == id)).IsRead);
    }

    [Fact]
    public async Task MarkReadAsync_UnreadNotification_MarksReadAndReturnsTrue()
    {
        await _sut.NotifyUserAsync("user-1", "Naslov", "Poruka");
        var id = (await _db.Notifications.FirstAsync()).Id;

        var result = await _sut.MarkReadAsync(id, "user-1");

        Assert.True(result);
        var reloaded = await _db.Notifications.FirstAsync(n => n.Id == id);
        Assert.True(reloaded.IsRead);
        Assert.NotNull(reloaded.ReadAt);
    }

    [Fact]
    public async Task MarkReadAsync_AlreadyRead_ReturnsTrueWithoutChangingReadAt()
    {
        await _sut.NotifyUserAsync("user-1", "Naslov", "Poruka");
        var id = (await _db.Notifications.FirstAsync()).Id;
        await _sut.MarkReadAsync(id, "user-1");
        var firstReadAt = (await _db.Notifications.FirstAsync(n => n.Id == id)).ReadAt;

        var result = await _sut.MarkReadAsync(id, "user-1");

        Assert.True(result);
        Assert.Equal(firstReadAt, (await _db.Notifications.FirstAsync(n => n.Id == id)).ReadAt);
    }
}
