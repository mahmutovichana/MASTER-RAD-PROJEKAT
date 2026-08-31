namespace RBBH.TestAutomation.Core.Repositories;

/// <summary>Agregirani sažetak grupe — broj scenarija, zadnji run, pass rate.</summary>
public sealed record GroupSummary(
    int ScenarioCount,
    DateTime? LastRunAt,
    double? LastPassRate,
    int ActiveScheduleCount
);
