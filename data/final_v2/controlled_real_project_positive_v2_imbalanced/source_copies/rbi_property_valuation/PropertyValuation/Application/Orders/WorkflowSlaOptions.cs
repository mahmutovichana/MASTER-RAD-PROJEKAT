namespace RBBH.CollateralAppraisal.Application.Orders;

/// <summary>
/// SLA rokovi za workflow taskove — konfigurabilno po okruženju.
/// Promjena roka ne zahtijeva redeploy aplikacije.
///
/// Sve vrijednosti su u danima ako nije drugačije naznačeno.
/// </summary>
public sealed class WorkflowSlaOptions
{
    public const string SectionName = "WorkflowSla";

    /// <summary>Rok za CA da prihvati narudžbu (kreiran pri Submit). Podrazumijevano: 2 dana.</summary>
    public int CaAcceptDueDays { get; init; } = 2;

    /// <summary>Rok za isporuku originala procjene vještaka (kreiran pri CO odobrenju). Podrazumijevano: 3 dana.</summary>
    public int OriginalReceivedDueDays { get; init; } = 3;

    /// <summary>Trajanje preview tokena za import šifarnika (u minutama). Podrazumijevano: 15.</summary>
    public int ImportPreviewExpiryMinutes { get; init; } = 15;

    /// <summary>Prozor za dedupliciranje email notifikacija (u minutama). Podrazumijevano: 5.</summary>
    public int EmailDeduplicationWindowMinutes { get; init; } = 5;

    /// <summary>Rok prihvatanja narudžbe od strane vještaka (u satima). Podrazumijevano: 24h.</summary>
    public int AppraiserTimeoutWindowHours { get; init; } = 24;

    /// <summary>Interval provjere isteklih narudžbi u AppraiserTimeoutService (u minutama). Podrazumijevano: 30.</summary>
    public int AppraiserTimeoutCheckIntervalMinutes { get; init; } = 30;
}
