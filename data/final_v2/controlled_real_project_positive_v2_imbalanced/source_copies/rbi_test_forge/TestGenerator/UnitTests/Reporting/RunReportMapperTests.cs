using System.Text.Json;
using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Api.Services.Ci;
using RBBH.TestAutomation.Api.Services.Run;
using RBBH.TestAutomation.Core.Reporting;
using Xunit;

namespace UnitTests.Reporting;

/// <summary>
/// Testovi za <see cref="RunReportMapper"/> — gradi izvještaj iz persistiranog
/// <see cref="RunHistoryRow"/> (DetailsJson). Dokazuje da izvještaji rade i nakon restarta
/// (čitanjem iz baze) te da su otporni na prazne/nevalidne detalje.
/// </summary>
public class RunReportMapperTests
{
    private static readonly JsonSerializerOptions WebJson = new(JsonSerializerDefaults.Web);

    private static string SerializeDetails(params ScenarioRunResult[] results) =>
        JsonSerializer.Serialize(results.ToList(), WebJson);

    private static RunHistoryRow Row(string? detailsJson) => new(
        Id: Guid.NewGuid(),
        GroupId: Guid.NewGuid(),
        GroupName: "Smoke",
        GroupBoja: "#43a047",
        GroupTag: TestTag.Smoke,
        Status: "Failed",
        TriggerType: "Pipeline",
        PassRate: 50,
        TotalCount: 2,
        PassedCount: 1,
        FailedCount: 1,
        Duration: TimeSpan.FromSeconds(1),
        StartedAt: new DateTime(2026, 6, 28, 10, 0, 0, DateTimeKind.Utc),
        CompletedAt: new DateTime(2026, 6, 28, 10, 0, 1, DateTimeKind.Utc),
        DetailsJson: detailsJson);

    [Fact]
    public void FromHistoryRow_MapsTestsStatusesAndDurations()
    {
        var details = SerializeDetails(
            new ScenarioRunResult(Guid.NewGuid(), "Health check", ScenarioRunStatus.Passed, 200, 200, 120, null, null, null),
            new ScenarioRunResult(Guid.NewGuid(), "Login", ScenarioRunStatus.Failed, 500, 200, 450, "pao", null, "Internal Server Error"));

        var report = RunReportMapper.FromHistoryRow(Row(details));

        Assert.Equal(2, report.Total);
        Assert.Equal(1, report.Passed);
        Assert.Equal(1, report.Failed);

        var health = report.Tests.Single(t => t.Name == "Health check");
        Assert.Equal(RunReportStatus.Passed, health.Status);
        Assert.Equal(0.120, health.DurationSeconds, 3);
        Assert.Equal("Smoke", health.Suite); // suite = naziv grupe iz row-a

        var login = report.Tests.Single(t => t.Name == "Login");
        Assert.Equal(RunReportStatus.Failed, login.Status);
        Assert.Equal("pao", login.ErrorMessage);
        Assert.Contains("500", login.ErrorDetails);
    }

    [Fact]
    public void FromHistoryRow_UsesRunMetadataFromRow()
    {
        var row = Row(SerializeDetails(
            new ScenarioRunResult(Guid.NewGuid(), "X", ScenarioRunStatus.Passed, 200, 200, 10, null, null, null)));

        var report = RunReportMapper.FromHistoryRow(row);

        Assert.Equal(row.Id, report.JobId);
        Assert.Equal(row.StartedAt, report.StartedAt);
        Assert.Equal(row.CompletedAt, report.CompletedAt);
        Assert.Contains("Smoke", report.RunName);
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("[]")]
    [InlineData("{ nije validan json")]
    public void FromHistoryRow_EmptyOrInvalidDetails_ReturnsNoTestsWithoutThrowing(string? details)
    {
        var report = RunReportMapper.FromHistoryRow(Row(details));

        Assert.Empty(report.Tests);
        Assert.Equal(0, report.Total);
    }
}
