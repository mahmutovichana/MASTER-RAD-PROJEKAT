namespace RBBH.TestAutomation.Api.DTO;

public sealed record RunHistoryFilter(
    Guid? GroupId = null,
    TestTag? Tag = null,
    string? TriggerType = null,
    string? Status = null,
    DateTime? DateFrom = null,
    DateTime? DateTo = null);

public sealed record RunHistoryRow(
    Guid Id,
    Guid GroupId,
    string GroupName,
    string? GroupBoja,
    TestTag GroupTag,
    string Status,
    string TriggerType,
    double PassRate,
    int TotalCount,
    int PassedCount,
    int FailedCount,
    TimeSpan Duration,
    DateTime StartedAt,
    DateTime? CompletedAt,
    string? DetailsJson);

public sealed record HistoryDashboard(
    int TotalRuns,
    double AvgPassRate,
    TimeSpan AvgDuration,
    int PassedRuns,
    int FailedRuns);

public sealed record TrendPoint(DateTime Date, double PassRate, string GroupName);

public sealed record FlakyTestInfo(
    string ScenarioName,
    string GroupName,
    int TotalRuns,
    int Flips,
    double FlakyRate);
