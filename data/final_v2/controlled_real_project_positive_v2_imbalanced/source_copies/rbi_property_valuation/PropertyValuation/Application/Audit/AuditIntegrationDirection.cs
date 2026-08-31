namespace RBBH.CollateralAppraisal.Application.Audit;

/// <summary>
/// Smjer integracije — opisuje da li je akcija pokrenuta prema vanjskom sistemu,
/// od vanjskog sistema, ili je interno.
/// </summary>
public static class AuditIntegrationDirection
{
    /// <summary>Podaci dolaze IZ vanjskog sistema u naš sistem (import, sync pull).</summary>
    public const string Inbound  = "Inbound";

    /// <summary>Podaci idu IZ našeg sistema prema vanjskom sistemu (push, write-back).</summary>
    public const string Outbound = "Outbound";

    /// <summary>Akcija je potpuno interna — ne uključuje vanjski sistem.</summary>
    public const string Internal = "Internal";
}
