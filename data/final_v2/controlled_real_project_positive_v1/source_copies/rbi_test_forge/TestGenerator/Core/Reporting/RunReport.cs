namespace RBBH.TestAutomation.Core.Reporting;

/// <summary>Status jednog testa u izvještaju — format-neutralan (mapira se po formatu).</summary>
public enum RunReportStatus
{
    Passed,
    Failed,
    Skipped,
}

/// <summary>Podržani formati izvoza izvještaja run joba.</summary>
public enum RunReportFormat
{
    /// <summary>JUnit XML — kompatibilan sa Jenkins i GitLab CI.</summary>
    Junit,

    /// <summary>TRX (Visual Studio Test Results) — kompatibilan sa Azure DevOps.</summary>
    Trx,

    /// <summary>Samostalni HTML izvještaj za dijeljenje.</summary>
    Html,

    /// <summary>JSON format za custom integracije.</summary>
    Json,
}

/// <summary>
/// Jedan test u izvještaju. Mapira se iz rezultata izvršavanja scenarija
/// (naziv, pripadnost grupi/suite-u, status, trajanje, poruka i detalji greške).
/// </summary>
/// <param name="Name">Naziv testa/scenarija.</param>
/// <param name="Suite">Naziv grupe — koristi se kao <c>testsuite</c> / <c>className</c>.</param>
/// <param name="Status">Ishod testa.</param>
/// <param name="DurationSeconds">Trajanje izvršavanja u sekundama.</param>
/// <param name="ErrorMessage">Kratka poruka greške (null ako test nije pao).</param>
/// <param name="ErrorDetails">Dodatni detalji greške (očekivano/dobijeno, isječak odgovora...).</param>
public sealed record RunReportTest(
    string Name,
    string Suite,
    RunReportStatus Status,
    double DurationSeconds,
    string? ErrorMessage,
    string? ErrorDetails);

/// <summary>
/// Kompletan izvještaj jednog run joba — metapodaci + svi izvršeni testovi.
/// Agregatni brojači se izvode iz <see cref="Tests"/>, pa su uvijek konzistentni.
/// </summary>
/// <param name="JobId">Identifikator run joba.</param>
/// <param name="RunName">Čitljiv naziv run-a (npr. "TestForge CI Run abcdef...").</param>
/// <param name="StartedAt">Vrijeme početka (UTC).</param>
/// <param name="CompletedAt">Vrijeme završetka (UTC), null ako run još traje.</param>
/// <param name="Tests">Svi testovi obuhvaćeni izvještajem.</param>
public sealed record RunReport(
    Guid JobId,
    string RunName,
    DateTime StartedAt,
    DateTime? CompletedAt,
    IReadOnlyList<RunReportTest> Tests)
{
    /// <summary>Ukupan broj testova.</summary>
    public int Total => Tests.Count;

    /// <summary>Broj prošlih testova.</summary>
    public int Passed => Tests.Count(t => t.Status == RunReportStatus.Passed);

    /// <summary>Broj palih testova.</summary>
    public int Failed => Tests.Count(t => t.Status == RunReportStatus.Failed);

    /// <summary>Broj preskočenih testova.</summary>
    public int Skipped => Tests.Count(t => t.Status == RunReportStatus.Skipped);

    /// <summary>Broj stvarno izvršenih testova (prošli + pali).</summary>
    public int Executed => Passed + Failed;

    /// <summary>Ukupno trajanje (zbir trajanja svih testova) u sekundama.</summary>
    public double DurationSeconds => Tests.Sum(t => t.DurationSeconds);

    /// <summary>Postotak prolaznosti (0–100, zaokruženo na jednu decimalu).</summary>
    public double PassRate => Total > 0 ? Math.Round((double)Passed / Total * 100, 1) : 0;
}
