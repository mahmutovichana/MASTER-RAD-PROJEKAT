namespace RBBH.CollateralAppraisal.Application.Notifications;

/// <summary>
/// Konfiguracija notifikacija vezanih za narudžbe procjene.
/// Vrijednosti se učitavaju iz sekcije "OrderNotifications" (appsettings).
/// </summary>
public sealed class OrderNotificationsOptions
{
    public const string SectionName = "OrderNotifications";

    /// <summary>Email adresa CA tima na koju se šalje obavještenje o novoj narudžbi.</summary>
    public string CaInboxEmail { get; set; } = "";
}
