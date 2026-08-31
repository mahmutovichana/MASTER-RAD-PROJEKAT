using System.Text.Json;
using System.Text.Json.Serialization;

namespace RBBH.TestAutomation.Core.Reporting;

/// <summary>
/// JSON formatter izvještaja — za custom integracije. Emituje stabilan, čitljiv objekat
/// (summary + lista testova) umjesto direktne serializacije recorda, da format ostane
/// nezavisan od internih tipova i da enumi budu stringovi.
/// </summary>
public sealed class JsonReportFormatter : IRunReportFormatter
{
    private static readonly JsonSerializerOptions Options = new()
    {
        WriteIndented = true,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
    };

    public RunReportFormat Format => RunReportFormat.Json;
    public string ContentType => "application/json";
    public string FileName(Guid jobId) => $"run-{jobId:N}.json";

    public string Render(RunReport report)
    {
        var dto = new
        {
            jobId = report.JobId,
            runName = report.RunName,
            startedAt = report.StartedAt,
            completedAt = report.CompletedAt,
            summary = new
            {
                total = report.Total,
                passed = report.Passed,
                failed = report.Failed,
                skipped = report.Skipped,
                passRate = report.PassRate,
                durationSeconds = Math.Round(report.DurationSeconds, 3),
            },
            tests = report.Tests.Select(t => new
            {
                name = t.Name,
                suite = t.Suite,
                status = t.Status.ToString(),
                durationSeconds = Math.Round(t.DurationSeconds, 3),
                errorMessage = t.ErrorMessage,
                errorDetails = t.ErrorDetails,
            }),
        };

        return JsonSerializer.Serialize(dto, Options);
    }
}
