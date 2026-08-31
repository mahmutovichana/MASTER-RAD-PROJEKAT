using RBBH.TestAutomation.Api.DTO;

namespace RBBH.TestAutomation.Api.Services;

public sealed class MockRunHistoryService : IRunHistoryService
{
    private static readonly Guid _grpSmoke = Guid.Parse("10000000-0000-0000-0000-000000000001");
    private static readonly Guid _grpRegression = Guid.Parse("10000000-0000-0000-0000-000000000002");

    private readonly List<RunHistoryRow> _runs;

    public MockRunHistoryService()
    {
        var now = DateTime.UtcNow;
        var rng = new Random(42);
        _runs = [];

        var groups = new[]
        {
            (_grpSmoke, "Smoke", "#43a047", TestTag.Smoke),
            (_grpRegression, "Regression", "#1e88e5", TestTag.Regression),
        };

        for (var day = 29; day >= 0; day--)
        {
            foreach (var (gid, name, color, tag) in groups)
            {
                var passRate = 60 + rng.Next(40);
                var total = 5 + rng.Next(6);
                var passed = (int)(total * passRate / 100.0);
                var failed = total - passed;
                var status = failed == 0 ? "Passed" : "Failed";
                var trigger = day % 3 == 0 ? "Scheduled" : day % 5 == 0 ? "Pipeline" : "Manual";
                var duration = TimeSpan.FromSeconds(8 + rng.Next(120));
                var started = now.AddDays(-day).AddHours(-rng.Next(12));

                _runs.Add(new RunHistoryRow(
                    Guid.NewGuid(), gid, name, color, tag,
                    status, trigger, passRate, total, passed, failed,
                    duration, started, started + duration, null));
            }
        }
    }

    public Task<IReadOnlyList<RunHistoryRow>> GetHistoryAsync(RunHistoryFilter filter, CancellationToken ct = default)
    {
        var q = _runs.AsEnumerable();
        if (filter.GroupId is not null) q = q.Where(r => r.GroupId == filter.GroupId);
        if (filter.Tag is not null) q = q.Where(r => r.GroupTag == filter.Tag);
        if (filter.Status is not null) q = q.Where(r => r.Status == filter.Status);
        if (filter.TriggerType is not null) q = q.Where(r => r.TriggerType == filter.TriggerType);
        if (filter.DateFrom is not null) q = q.Where(r => r.StartedAt >= filter.DateFrom);
        if (filter.DateTo is not null) q = q.Where(r => r.StartedAt <= filter.DateTo.Value.AddDays(1));
        IReadOnlyList<RunHistoryRow> result = q.OrderByDescending(r => r.StartedAt).ToList();
        return Task.FromResult(result);
    }

    public Task<HistoryDashboard> GetDashboardAsync(CancellationToken ct = default)
    {
        var dashboard = new HistoryDashboard(
            TotalRuns: _runs.Count,
            AvgPassRate: _runs.Average(r => r.PassRate),
            AvgDuration: TimeSpan.FromMilliseconds(_runs.Average(r => r.Duration.TotalMilliseconds)),
            PassedRuns: _runs.Sum(r => r.PassedCount),
            FailedRuns: _runs.Sum(r => r.FailedCount));
        return Task.FromResult(dashboard);
    }

    public Task<IReadOnlyList<TrendPoint>> GetTrendAsync(int days = 30, CancellationToken ct = default)
    {
        var since = DateTime.UtcNow.AddDays(-days);
        IReadOnlyList<TrendPoint> trend = _runs
            .Where(r => r.StartedAt >= since)
            .OrderBy(r => r.StartedAt)
            .Select(r => new TrendPoint(r.StartedAt.Date, r.PassRate, r.GroupName))
            .ToList();
        return Task.FromResult(trend);
    }

    public Task<IReadOnlyList<FlakyTestInfo>> GetFlakyTestsAsync(int minRuns = 3, CancellationToken ct = default)
    {
        IReadOnlyList<FlakyTestInfo> flaky =
        [
            new("Health check", "Smoke", 15, 6, 42.9),
            new("Login korisnika", "Smoke", 12, 4, 36.4),
            new("Kreiranje korisnika", "Regression", 10, 3, 33.3),
        ];
        return Task.FromResult(flaky);
    }

    public Task<RunHistoryRow?> GetRunByIdAsync(Guid runId, CancellationToken ct = default)
    {
        return Task.FromResult(_runs.FirstOrDefault(r => r.Id == runId));
    }
}
