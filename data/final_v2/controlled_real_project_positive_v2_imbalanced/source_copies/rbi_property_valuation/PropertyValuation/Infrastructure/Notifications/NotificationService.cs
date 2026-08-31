using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Domain.Notifications;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Notifications;

/// <summary>
/// Implementacija <see cref="INotificationService"/> — sprema in-app notifikacije u
/// <c>notifications</c> tabelu i po potrebi šalje email kopiju preko <see cref="IEmailProvider"/>.
/// </summary>
public sealed class NotificationService : INotificationService
{
    private readonly ApplicationDbContext _db;
    private readonly IEmailProvider _emailProvider;
    private readonly ILogger<NotificationService> _logger;

    public NotificationService(
        ApplicationDbContext db,
        IEmailProvider emailProvider,
        ILogger<NotificationService> logger)
    {
        _db            = db;
        _emailProvider = emailProvider;
        _logger        = logger;
    }

    public async Task NotifyUserAsync(
        string  userId,
        string  subject,
        string  message,
        string? relatedEntityType = null,
        string? relatedEntityId   = null,
        bool    sendEmail         = false,
        string? emailAddress      = null,
        CancellationToken ct      = default)
    {
        var now = DateTime.UtcNow;

        var inApp = Notification.CreateInApp(userId, subject, message, relatedEntityType, relatedEntityId);
        inApp.MarkSent(now);
        _db.Notifications.Add(inApp);

        if (sendEmail && !string.IsNullOrWhiteSpace(emailAddress))
        {
            var email = Notification.CreateEmail(userId, null, subject, message, relatedEntityType, relatedEntityId);

            try
            {
                await _emailProvider.SendAsync(new EmailMessage(emailAddress, subject, message), ct);
                email.MarkSent(now);
            }
            catch (Exception ex)
            {
                email.MarkFailed(ex.Message, now);
                _logger.LogWarning(ex, "Slanje email notifikacije korisniku {UserId} nije uspjelo.", userId);
            }

            _db.Notifications.Add(email);
        }

        await _db.SaveChangesAsync(ct);
    }

    public async Task NotifyUsersAsync(
        IEnumerable<string> userIds,
        string  subject,
        string  message,
        string? relatedEntityType = null,
        string? relatedEntityId   = null,
        CancellationToken ct      = default)
    {
        var now = DateTime.UtcNow;

        foreach (var userId in userIds.Distinct())
        {
            var inApp = Notification.CreateInApp(userId, subject, message, relatedEntityType, relatedEntityId);
            inApp.MarkSent(now);
            _db.Notifications.Add(inApp);
        }

        await _db.SaveChangesAsync(ct);
    }

    public async Task<NotificationInboxResult> GetInboxAsync(
        string userId,
        int    page       = 1,
        int    pageSize   = 20,
        bool   unreadOnly = false,
        CancellationToken ct = default)
    {
        page     = Math.Max(page, 1);
        pageSize = Math.Clamp(pageSize, 1, 100);

        var baseQuery = _db.Notifications.AsNoTracking()
            .Where(n => n.RecipientUserId == userId && n.Channel == RBBH.CollateralAppraisal.Domain.Notifications.NotificationChannel.InApp);

        var query = unreadOnly ? baseQuery.Where(n => !n.IsRead) : baseQuery;

        var totalCount  = await query.CountAsync(ct);
        var unreadCount = await baseQuery.CountAsync(n => !n.IsRead, ct);

        var items = await query
            .OrderByDescending(n => n.CreatedAt)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Select(n => new NotificationDto(
                n.Id, n.Subject, n.Message, n.IsRead, n.CreatedAt, n.RelatedEntityType, n.RelatedEntityId))
            .ToListAsync(ct);

        return new NotificationInboxResult(items, totalCount, page, pageSize, unreadCount);
    }

    public Task<int> GetUnreadCountAsync(string userId, CancellationToken ct = default) =>
        _db.Notifications.AsNoTracking()
            .CountAsync(n => n.RecipientUserId == userId
                          && n.Channel == RBBH.CollateralAppraisal.Domain.Notifications.NotificationChannel.InApp
                          && !n.IsRead, ct);

    public async Task<bool> MarkReadAsync(int notificationId, string userId, CancellationToken ct = default)
    {
        var notification = await _db.Notifications
            .FirstOrDefaultAsync(n => n.Id == notificationId && n.RecipientUserId == userId, ct);

        if (notification is null)
            return false;

        if (!notification.IsRead)
        {
            notification.MarkRead(DateTime.UtcNow);
            await _db.SaveChangesAsync(ct);
        }

        return true;
    }
}
