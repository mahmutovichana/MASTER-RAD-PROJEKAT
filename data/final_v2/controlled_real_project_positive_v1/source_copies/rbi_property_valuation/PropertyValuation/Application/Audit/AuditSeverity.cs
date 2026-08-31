namespace RBBH.CollateralAppraisal.Application.Audit;

/// <summary>
/// Ozbiljnost audit eventa — za filtriranje, alerting i prioritizaciju.
/// </summary>
public static class AuditSeverity
{
    /// <summary>Rutinska operacija, nema posebnog značaja.</summary>
    public const string Info     = "Info";

    /// <summary>Neobična situacija koja zahtijeva pažnju, ali nije greška.</summary>
    public const string Warning  = "Warning";

    /// <summary>Sigurnosno relevantan događaj (neovlašteni pristup, promjena uloga...).</summary>
    public const string Security = "Security";

    /// <summary>Kritičan događaj koji zahtijeva hitnu reakciju.</summary>
    public const string Critical = "Critical";
}
