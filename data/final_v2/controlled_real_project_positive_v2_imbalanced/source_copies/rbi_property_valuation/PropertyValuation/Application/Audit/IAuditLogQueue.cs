using RBBH.CollateralAppraisal.Domain.Audit;

namespace RBBH.CollateralAppraisal.Application.Audit;

/// <summary>
/// In-process queue za asinhrono pisanje audit zapisa — odvaja "skupi" dio (DB/file
/// upis kroz IAuditSink) od request/response ciklusa. AuditService stavlja VEĆ izgrađen
/// AuditLog (sve iz HttpContext-a/ICurrentUserService je već pročitano i snimljeno u
/// objekat) u red, a pozadinski worker (vidi Infrastructure) ga prazni i upisuje.
///
/// Cilj: "Audit log ne smije usporavati download" — RecordAsync vraća kontrolu odmah
/// nakon enqueue-a (mikrosekunde), ne čekajući stvarni DB INSERT.
/// </summary>
public interface IAuditLogQueue
{
    /// <summary>Stavlja audit zapis u red za asinhronu obradu. Ne baca ako je red pun —
    /// vidi konkretnu implementaciju za ponašanje kod zasićenja (sigurnost > potpunost).</summary>
    ValueTask EnqueueAsync(AuditLog log, CancellationToken ct = default);
}
