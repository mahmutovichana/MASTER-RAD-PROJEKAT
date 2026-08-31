namespace RBBH.CollateralAppraisal.Infrastructure.Notifications;

/// <summary>
/// SMTP konfiguracija za slanje email notifikacija.
/// Vrijednosti se učitavaju iz sekcije "Smtp" (appsettings).
/// Ako <see cref="Host"/> nije postavljen, slanje emaila se preskače (loguje se umjesto).
/// </summary>
[System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage]
public sealed class SmtpOptions
{
    public const string SectionName = "Smtp";

    public string Host { get; set; } = "";
    public int Port { get; set; } = 587;
    public bool UseSsl { get; set; }
    public string Username { get; set; } = "";
    public string Password { get; set; } = "";
    public string FromAddress { get; set; } = "";
    public string FromName { get; set; } = "RBI BH — Procjene";
    public string AppBaseUrl { get; set; } = "";
}
