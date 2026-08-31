using RBBH.CollateralAppraisal.Domain.Common;

namespace RBBH.CollateralAppraisal.Domain.Notifications;

/// <summary>
/// In-app notifikacija za korisnika. Email notifikacije su odvojene (IEmailProvider).
/// ODLUKA POTREBNA (stakeholder): definisati po workflow koraku koje notifikacije idu email
/// a koje samo in-app. Dokumentovati u docs/notifications/notification-matrix.md.
/// </summary>
public sealed class Notification : BaseEntity
{
    public string? RecipientUserId { get; private set; }
    public string? RecipientRole { get; private set; }     // Notifikacija za cijelu rolu
    public NotificationChannel Channel { get; private set; }
    public string Subject { get; private set; } = null!;
    public string Message { get; private set; } = null!;
    public NotificationStatus Status { get; private set; }

    public DateTime? SentAt { get; private set; }
    public int RetryCount { get; private set; }
    public string? ErrorMessage { get; private set; }

    // ── Kontekst ───────────────────────────────────────────────────────────
    public string? RelatedEntityType { get; private set; }
    public string? RelatedEntityId { get; private set; }

    // ── Pročitanost (za in-app) ────────────────────────────────────────────
    public bool IsRead { get; private set; }
    public DateTime? ReadAt { get; private set; }

    /// <summary>
    /// Ključ za deduplikaciju — sprečava slanje identičnih notifikacija unutar 5-minutnog prozora.
    /// Format: "{channel}:{userId}:{entityType}:{entityId}:{subject}".
    /// </summary>
    public string? DeduplicationKey { get; private set; }

    private Notification() { }

    public static Notification CreateInApp(
        string recipientUserId,
        string subject,
        string message,
        string? relatedEntityType = null,
        string? relatedEntityId   = null)
    {
        var n = new Notification
        {
            RecipientUserId   = recipientUserId,
            Channel           = NotificationChannel.InApp,
            Subject           = subject,
            Message           = message,
            Status            = NotificationStatus.Pending,
            RelatedEntityType = relatedEntityType,
            RelatedEntityId   = relatedEntityId
        };
        n.DeduplicationKey = $"InApp:{recipientUserId}:{relatedEntityType}:{relatedEntityId}:{subject}";
        return n;
    }

    public static Notification CreateEmail(
        string? recipientUserId,
        string? recipientRole,
        string subject,
        string message,
        string? relatedEntityType = null,
        string? relatedEntityId   = null)
    {
        return new Notification
        {
            RecipientUserId   = recipientUserId,
            RecipientRole     = recipientRole,
            Channel           = NotificationChannel.Email,
            Subject           = subject,
            Message           = message,
            Status            = NotificationStatus.Pending,
            RelatedEntityType = relatedEntityType,
            RelatedEntityId   = relatedEntityId
        };
    }

    public void MarkSent(DateTime now)
    {
        Status = NotificationStatus.Sent;
        SentAt = now;
        SetUpdatedAt(now);
    }

    public void MarkFailed(string errorMessage, DateTime now)
    {
        Status       = NotificationStatus.Failed;
        ErrorMessage = errorMessage;
        RetryCount++;
        SetUpdatedAt(now);
    }

    public void MarkRead(DateTime now)
    {
        IsRead = true;
        ReadAt = now;
        SetUpdatedAt(now);
    }
}

public enum NotificationChannel { InApp = 0, Email = 1 }

public enum NotificationStatus
{
    Pending   = 0,
    Sent      = 1,
    Failed    = 2,
    Retrying  = 3,
    Cancelled = 4
}
