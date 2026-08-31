namespace RBBH.CollateralAppraisal.Application.Notifications;

/// <summary>
/// Adapter contract za slanje notifikacija.
/// Application sloj definiše interfejs — Infrastructure implementira konkretne providere.
///
/// Aktivni provider:
/// - EmailNotificationProvider — šalje Email kanal preko SMTP-a (MailKit); ako SMTP host
///   nije konfigurisan, samo loguje. InApp kanal (GetForUserAsync/MarkReadAsync) trenutno
///   nije DB-backed (vraća praznu listu / no-op) — eventualni DatabaseNotificationProvider
///   za in-app notifikacije je van obima.
/// </summary>
public interface INotificationProvider
{
    Task SendAsync(NotificationRequest request, CancellationToken ct = default);
    Task<IReadOnlyList<NotificationItem>> GetForUserAsync(string userId, int page = 1, int pageSize = 20, CancellationToken ct = default);
    Task MarkReadAsync(int notificationId, string userId, CancellationToken ct = default);
}

public sealed record NotificationRequest(
    string?              RecipientUserId,
    string?              RecipientRole,
    NotificationChannel  Channel,
    string               Subject,
    string               Message,
    string?              RelatedEntityType = null,
    string?              RelatedEntityId   = null,
    string?              RecipientEmail    = null);

public sealed record NotificationItem(
    int      Id,
    string   Subject,
    string   Message,
    bool     IsRead,
    DateTime CreatedAt,
    string?  RelatedEntityType,
    string?  RelatedEntityId);

public enum NotificationChannel { InApp = 0, Email = 1 }
