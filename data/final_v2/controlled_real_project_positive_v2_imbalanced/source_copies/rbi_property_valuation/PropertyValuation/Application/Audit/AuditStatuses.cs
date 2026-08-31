namespace RBBH.CollateralAppraisal.Application.Audit;

/// <summary>
/// Status izvršenja auditovane operacije — ishod akcije.
/// </summary>
public static class AuditStatuses
{
    /// <summary>Operacija uspješno izvršena.</summary>
    public const string Success          = "Success";

    /// <summary>Operacija nije uspjela zbog sistemske greške.</summary>
    public const string Failed           = "Failed";

    /// <summary>Pristup odbijen zbog nedovoljnih prava (403).</summary>
    public const string Forbidden        = "Forbidden";

    /// <summary>Podaci nisu prošli validaciju — operacija nije pokrenuta.</summary>
    public const string ValidationFailed = "ValidationFailed";

    /// <summary>Konflikt stanja — npr. optimistično zaključavanje, duplikat.</summary>
    public const string Conflict         = "Conflict";

    /// <summary>Neočekivana sistemska greška (unhandled exception).</summary>
    public const string SystemError      = "SystemError";
}
