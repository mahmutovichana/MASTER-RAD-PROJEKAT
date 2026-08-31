using RBBH.CollateralAppraisal.Domain.Audit;

namespace RBBH.CollateralAppraisal.Application.Audit;

/// <summary>
/// Odredište za audit zapis (baza, datoteka, message queue, SIEM...).
/// Implementira se u Infrastructure sloju.
///
/// Registrujte više implementacija za fan-out: jedan zapis ide u bazu i u Splunk.
/// AuditService poziva sve registrovane sinkove paralelno.
/// </summary>
public interface IAuditSink
{
    /// <summary>
    /// Upisuje audit zapis u konkretno odredište.
    /// AuditLog je već kompletno popunjen (CorrelationId, Actor, JSON vrijednosti...).
    /// </summary>
    Task WriteAsync(AuditLog auditLog, CancellationToken cancellationToken = default);
}
