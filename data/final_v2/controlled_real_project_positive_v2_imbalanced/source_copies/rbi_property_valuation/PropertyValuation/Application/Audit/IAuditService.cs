namespace RBBH.CollateralAppraisal.Application.Audit;

/// <summary>
/// Jedina tačka ulaza za bilježenje audit događaja u poslovnoj logici.
/// Implementacija (AuditService) brine o kontekstu korisnika, HTTP kontekstu,
/// serijalizaciji, sanitizaciji i distribuciji prema svim IAuditSink implementacijama.
///
/// Poslovna logika samo kreira AuditEvent i poziva RecordAsync — ne mora znati ništa
/// o načinu čuvanja, formatu ili broju odredišta.
/// </summary>
public interface IAuditService
{
    /// <summary>
    /// Asinkrono bilježi audit događaj.
    /// Ne baca izuzetak ako sink ne uspije — greška se loguje interno.
    /// </summary>
    Task RecordAsync(AuditEvent auditEvent, CancellationToken cancellationToken = default);
}
