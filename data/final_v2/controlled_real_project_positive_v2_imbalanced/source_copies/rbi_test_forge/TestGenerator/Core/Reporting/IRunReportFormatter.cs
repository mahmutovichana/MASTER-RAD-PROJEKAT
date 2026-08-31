namespace RBBH.TestAutomation.Core.Reporting;

/// <summary>
/// Pretvara <see cref="RunReport"/> u tekstualni izvještaj određenog formata
/// (JUnit XML, TRX, HTML ili JSON). Implementacije su stateless i thread-safe —
/// registruju se kao Singleton (isti obrazac kao generatori testova).
/// </summary>
public interface IRunReportFormatter
{
    /// <summary>Format koji ovaj formatter proizvodi.</summary>
    RunReportFormat Format { get; }

    /// <summary>MIME tip za HTTP <c>Content-Type</c> (npr. <c>application/xml</c>).</summary>
    string ContentType { get; }

    /// <summary>Predloženo ime fajla za download (npr. <c>run-{jobId}.xml</c>).</summary>
    string FileName(Guid jobId);

    /// <summary>Renderuje izvještaj u tekstualni sadržaj datog formata.</summary>
    string Render(RunReport report);
}
