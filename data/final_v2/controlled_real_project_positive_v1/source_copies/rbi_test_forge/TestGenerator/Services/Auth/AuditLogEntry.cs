namespace RBBH.TestAutomation.Api.Services.Auth;

/// <summary>
/// Jedan sigurnosni audit zapis.
/// Immutable record — bilježi se pri svakom login pokušaju.
/// </summary>
/// <param name="TimestampUtc">Vrijeme događaja (UTC).</param>
/// <param name="EventType">Tip događaja — koristiti konstante iz <see cref="AuditEventTypes"/>.</param>
/// <param name="Username">Korisničko ime iz pokušaja prijave.</param>
/// <param name="IpAddress">IP adresa klijenta; može biti null u interaktivnom Blazor Server modu.</param>
/// <param name="FailureReason">Razlog neuspjeha (null za uspješne prijave).</param>
public sealed record AuditLogEntry(
    DateTime TimestampUtc,
    string EventType,
    string Username,
    string? IpAddress,
    string? FailureReason);

/// <summary>
/// Tipovi sigurnosnih događaja koji se bilježe u audit log.
/// </summary>
public static class AuditEventTypes
{
    public const string LoginSuccess = "LoginSuccess";
    public const string LoginFailure = "LoginFailure";
    public const string AccountLocked = "AccountLocked";
    public const string Logout = "Logout";
}

/// <summary>
/// Razlozi neuspješne prijave (vrijednost <see cref="AuditLogEntry.FailureReason"/>).
/// Konstante umjesto magic stringova — konzistentnost u logu i lakši filter.
/// </summary>
public static class AuditFailureReasons
{
    public const string InvalidCredentials = "InvalidCredentials";
    public const string Locked = "Locked";
}
