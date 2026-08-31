namespace RBBH.CollateralAppraisal.Application.Notifications;

/// <summary>
/// Centralni servis za dispatch notifikacija — koriste ga svi feature moduli (T2-T8)
/// umjesto direktnog kreiranja <c>Notification</c> entiteta.
///
/// Odgovornosti:
/// - Kreira i sprema in-app notifikacije (vidljive u inboxu korisnika).
/// - Po potrebi šalje i email kopiju preko <see cref="IEmailProvider"/>.
/// - Pruža paginiran inbox i broj nepročitanih notifikacija za bell ikonu.
///
/// Implementacija: <c>NotificationService</c> (Infrastructure/Notifications).
/// </summary>
public interface INotificationService
{
    /// <summary>
    /// Šalje in-app notifikaciju jednom korisniku. Ako je <paramref name="sendEmail"/> true
    /// i <paramref name="emailAddress"/> je zadan, šalje i email kopiju preko <see cref="IEmailProvider"/>.
    /// </summary>
    Task NotifyUserAsync(
        string  userId,
        string  subject,
        string  message,
        string? relatedEntityType = null,
        string? relatedEntityId   = null,
        bool    sendEmail         = false,
        string? emailAddress      = null,
        CancellationToken ct      = default);

    /// <summary>Šalje istu in-app notifikaciju svakom korisniku iz liste (npr. svim CO).</summary>
    Task NotifyUsersAsync(
        IEnumerable<string> userIds,
        string  subject,
        string  message,
        string? relatedEntityType = null,
        string? relatedEntityId   = null,
        CancellationToken ct      = default);

    /// <summary>Paginirani inbox in-app notifikacija za korisnika (najnovije prve).</summary>
    Task<NotificationInboxResult> GetInboxAsync(
        string userId,
        int    page       = 1,
        int    pageSize   = 20,
        bool   unreadOnly = false,
        CancellationToken ct = default);

    /// <summary>Broj nepročitanih in-app notifikacija — za bell ikonu u headeru.</summary>
    Task<int> GetUnreadCountAsync(string userId, CancellationToken ct = default);

    /// <summary>
    /// Označava notifikaciju kao pročitanu. Vraća false ako notifikacija ne postoji
    /// ili ne pripada datom korisniku (endpoint to mapira na 404).
    /// </summary>
    Task<bool> MarkReadAsync(int notificationId, string userId, CancellationToken ct = default);
}

/// <summary>Stavka inboxa — DTO projekcija <c>Notification</c> entiteta.</summary>
public sealed record NotificationDto(
    int      Id,
    string   Subject,
    string   Message,
    bool     IsRead,
    DateTime CreatedAt,
    string?  RelatedEntityType,
    string?  RelatedEntityId);

/// <summary>Paginirana stranica inboxa + ukupan broj nepročitanih (za bell badge).</summary>
public sealed record NotificationInboxResult(
    IReadOnlyList<NotificationDto> Items,
    int TotalCount,
    int Page,
    int PageSize,
    int UnreadCount);
