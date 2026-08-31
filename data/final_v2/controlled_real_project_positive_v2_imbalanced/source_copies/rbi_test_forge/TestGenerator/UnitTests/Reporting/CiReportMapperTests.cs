using RBBH.TestAutomation.Api.Services.Ci;
using RBBH.TestAutomation.Api.Services.Run;
using RBBH.TestAutomation.Core.Reporting;
using Xunit;

namespace UnitTests.Reporting;

/// <summary>
/// Testovi za <see cref="CiReportMapper"/> — mapiranje in-memory snapshot-a u
/// format-neutralan <see cref="RunReport"/> (status, trajanje, detalji greške).
/// </summary>
public class CiReportMapperTests
{
    private static CiJobSnapshot Snapshot(params CiTestEntry[] results) => new(
        JobId: Guid.NewGuid(),
        Status: CiJobStatus.Failed,
        Total: results.Length,
        Completed: results.Length,
        Passed: results.Count(r => r.Status == ScenarioRunStatus.Passed),
        Failed: results.Count(r => r.Status == ScenarioRunStatus.Failed),
        PassRate: 50,
        FailedTests: results.Where(r => r.Status == ScenarioRunStatus.Failed).Select(r => r.Name).ToList(),
        StartedAt: DateTime.UtcNow,
        CompletedAt: DateTime.UtcNow,
        Results: results);

    [Fact]
    public void ToReport_MapsStatusesDurationsAndCounts()
    {
        var snap = Snapshot(
            new CiTestEntry("Test A", "Smoke", ScenarioRunStatus.Passed, 200, null, 200, 200, null),
            new CiTestEntry("Test B", "Smoke", ScenarioRunStatus.Failed, 500, "pao", 500, 200, "{\"error\":\"x\"}"),
            new CiTestEntry("UI", "Regression", ScenarioRunStatus.Skipped, 0, null, null, null, null));

        var report = CiReportMapper.ToReport(snap);

        Assert.Equal(3, report.Total);
        Assert.Equal(1, report.Passed);
        Assert.Equal(1, report.Failed);
        Assert.Equal(1, report.Skipped);

        var a = report.Tests.Single(t => t.Name == "Test A");
        Assert.Equal(RunReportStatus.Passed, a.Status);
        Assert.Equal(0.2, a.DurationSeconds, 3);
        Assert.Equal("Smoke", a.Suite);
        Assert.Null(a.ErrorMessage);
    }

    [Fact]
    public void ToReport_Failed_IncludesExpectedActualAndResponseInDetails()
    {
        var snap = Snapshot(
            new CiTestEntry("Test B", "Smoke", ScenarioRunStatus.Failed, 500, "pao", 500, 200, "{\"error\":\"x\"}"));

        var report = CiReportMapper.ToReport(snap);
        var b = report.Tests.Single();

        Assert.Equal("pao", b.ErrorMessage);
        Assert.Contains("200", b.ErrorDetails);          // očekivani status
        Assert.Contains("500", b.ErrorDetails);          // dobijeni status
        Assert.Contains("error", b.ErrorDetails);        // isječak odgovora
    }

    [Fact]
    public void ToReport_TruncatesLongResponseDetails()
    {
        var huge = new string('x', 2000);
        var snap = Snapshot(
            new CiTestEntry("Big", "Smoke", ScenarioRunStatus.Failed, 100, "pao", 500, 200, huge));

        var report = CiReportMapper.ToReport(snap);

        Assert.True(report.Tests.Single().ErrorDetails!.Length < 700); // 500 + prefiks + "…"
    }
}
