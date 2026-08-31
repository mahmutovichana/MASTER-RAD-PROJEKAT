using System.Text.Json;
using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Api.Services.Run;
using RBBH.TestAutomation.Core.Reporting;

namespace RBBH.TestAutomation.Api.Services.Ci;

/// <summary>
/// Mapira persistirani run (<see cref="RunHistoryRow"/> iz baze/historije) u <see cref="RunReport"/>.
/// Per-test detalji se čitaju iz <c>DetailsJson</c> (serializovan <see cref="ScenarioRunResult"/>
/// list, isti oblik koji upisuju <see cref="CiRunService"/> i GroupTestExecutor). Omogućava
/// izvještaje koji preživljavaju restart aplikacije.
/// </summary>
public static class RunReportMapper
{
    // Isti JSON režim kojim su rezultati serializovani u DetailsJson — garantuje round-trip.
    private static readonly JsonSerializerOptions WebJson = new(JsonSerializerDefaults.Web);

    public static RunReport FromHistoryRow(RunHistoryRow row)
    {
        var tests = Deserialize(row.DetailsJson)
            .Select(r => CiReportMapper.MapTest(
                r.Naziv, row.GroupName, r.Status, r.DurationMs,
                r.FailReason, r.ActualStatus, r.ExpectedStatus, r.ResponseDetails))
            .ToList();

        return new RunReport(
            JobId: row.Id,   // runId služi kao identifikator izvještaja
            RunName: $"{row.GroupName} — {row.StartedAt:yyyy-MM-dd HH:mm} UTC",
            StartedAt: row.StartedAt,
            CompletedAt: row.CompletedAt,
            Tests: tests);
    }

    /// <summary>
    /// Deserializuje <c>DetailsJson</c>. Stari/agregatni run-ovi (null, "[]" ili nevalidan JSON)
    /// daju praznu listu umjesto greške.
    /// </summary>
    private static List<ScenarioRunResult> Deserialize(string? detailsJson)
    {
        if (string.IsNullOrWhiteSpace(detailsJson)) return [];

        try
        {
            return JsonSerializer.Deserialize<List<ScenarioRunResult>>(detailsJson, WebJson) ?? [];
        }
        catch (JsonException)
        {
            return [];
        }
    }
}
