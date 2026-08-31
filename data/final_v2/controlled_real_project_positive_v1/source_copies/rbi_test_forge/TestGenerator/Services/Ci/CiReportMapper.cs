using RBBH.TestAutomation.Api.Services.Run;
using RBBH.TestAutomation.Core.Reporting;

namespace RBBH.TestAutomation.Api.Services.Ci;

/// <summary>
/// Mapira in-memory <see cref="CiJobSnapshot"/> u format-neutralan <see cref="RunReport"/>
/// koji formatteri (JUnit/TRX/HTML/JSON) konzumiraju. Drži RBBH.TestAutomation.Api tipove izvan Core sloja.
/// Zajedničko mapiranje jednog testa (<see cref="MapTest"/>) dijeli i <see cref="RunReportMapper"/>.
/// </summary>
public static class CiReportMapper
{
    /// <summary>Maksimalna dužina isječka odgovora ugrađenog u detalje greške (izbjegava ogromne izvještaje).</summary>
    private const int MaxResponseSnippet = 500;

    public static RunReport ToReport(CiJobSnapshot snap)
    {
        var tests = snap.Results
            .Select(r => MapTest(
                r.Name, r.GroupName, r.Status, r.DurationMs,
                r.FailReason, r.ActualStatus, r.ExpectedStatus, r.ResponseDetails))
            .ToList();

        return new RunReport(
            JobId: snap.JobId,
            RunName: $"TestForge CI Run {snap.JobId:N}",
            StartedAt: snap.StartedAt,
            CompletedAt: snap.CompletedAt,
            Tests: tests);
    }

    /// <summary>
    /// Zajedničko mapiranje jednog rezultata u <see cref="RunReportTest"/> — koriste ga
    /// i CI snapshot (<see cref="CiTestEntry"/>) i persistirani run (<see cref="ScenarioRunResult"/>).
    /// </summary>
    internal static RunReportTest MapTest(
        string name, string suite, ScenarioRunStatus status, long durationMs,
        string? failReason, int? actualStatus, int? expectedStatus, string? responseDetails)
    {
        var failed = status == ScenarioRunStatus.Failed;
        return new RunReportTest(
            Name: name,
            Suite: string.IsNullOrWhiteSpace(suite) ? "TestForge" : suite,
            Status: MapStatus(status),
            DurationSeconds: durationMs / 1000.0,
            ErrorMessage: failed ? (failReason ?? "Test je pao.") : null,
            ErrorDetails: failed ? BuildDetails(actualStatus, expectedStatus, responseDetails) : null);
    }

    private static RunReportStatus MapStatus(ScenarioRunStatus status) => status switch
    {
        ScenarioRunStatus.Passed => RunReportStatus.Passed,
        ScenarioRunStatus.Failed => RunReportStatus.Failed,
        _ => RunReportStatus.Skipped,
    };

    private static string? BuildDetails(int? actualStatus, int? expectedStatus, string? responseDetails)
    {
        var parts = new List<string>();

        if (expectedStatus is { } expected && actualStatus is { } actual)
            parts.Add($"Očekivani status: {expected}, dobijeni: {actual}.");

        if (!string.IsNullOrWhiteSpace(responseDetails))
        {
            var snippet = responseDetails.Length > MaxResponseSnippet
                ? responseDetails[..MaxResponseSnippet] + "…"
                : responseDetails;
            parts.Add(snippet);
        }

        return parts.Count > 0 ? string.Join(Environment.NewLine, parts) : null;
    }
}
