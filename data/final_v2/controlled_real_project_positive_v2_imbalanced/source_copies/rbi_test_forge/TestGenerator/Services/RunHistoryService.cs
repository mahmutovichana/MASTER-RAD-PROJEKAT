using System.Text.Json;
using System.Text.Json.Serialization;
using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Api.Services.Run;
using Microsoft.EntityFrameworkCore;
using RBBH.TestAutomation.Core.Domain.Enums;
using RBBH.TestAutomation.Core.Infrastructure;

namespace RBBH.TestAutomation.Api.Services;

public sealed class RunHistoryService(TestForgeDbContext db) : IRunHistoryService
{
    public async Task<IReadOnlyList<RunHistoryRow>> GetHistoryAsync(RunHistoryFilter filter, CancellationToken ct = default)
    {
        var q = db.RunResults
            .Include(r => r.Group)
            .Where(r => r.Group != null && r.State != RunState.Running && r.State != RunState.Pending)
            .AsQueryable();

        if (filter.GroupId is not null)
            q = q.Where(r => r.GroupId == filter.GroupId);
        if (filter.Status is not null)
            q = q.Where(r => r.State == Enum.Parse<RunState>(filter.Status));
        if (filter.TriggerType is not null)
            q = q.Where(r => r.TriggerType == Enum.Parse<TriggerType>(filter.TriggerType));
        if (filter.DateFrom is not null)
            q = q.Where(r => r.StartedAt >= filter.DateFrom);
        if (filter.DateTo is not null)
            q = q.Where(r => r.StartedAt <= filter.DateTo.Value.AddDays(1));

        var rows = await q.OrderByDescending(r => r.StartedAt).Take(500).ToListAsync(ct);

        var result = rows.Select(r => new RunHistoryRow(
            r.Id, r.GroupId, r.Group!.Naziv, r.Group.Boja,
            MapTag(r.Group.Tag), r.State.ToString(), r.TriggerType.ToString(),
            r.PassRate, r.TotalCount, r.PassedCount, r.FailedCount,
            r.Duration, r.StartedAt, r.CompletedAt, r.DetailsJson
        )).ToList();

        if (filter.Tag is not null)
            return result.Where(r => r.GroupTag == filter.Tag).ToList();

        return result;
    }

    public async Task<HistoryDashboard> GetDashboardAsync(CancellationToken ct = default)
    {
        var completed = await db.RunResults
            .Where(r => r.State == RunState.Passed || r.State == RunState.Failed)
            .ToListAsync(ct);

        if (completed.Count == 0)
            return new HistoryDashboard(0, 0, TimeSpan.Zero, 0, 0);

        return new HistoryDashboard(
            TotalRuns: completed.Count,
            AvgPassRate: completed.Average(r => r.PassRate),
            AvgDuration: TimeSpan.FromMilliseconds(completed.Average(r => r.Duration.TotalMilliseconds)),
            PassedRuns: completed.Sum(r => r.PassedCount),
            FailedRuns: completed.Sum(r => r.FailedCount));
    }

    public async Task<IReadOnlyList<TrendPoint>> GetTrendAsync(int days = 30, CancellationToken ct = default)
    {
        var since = DateTime.UtcNow.AddDays(-days);
        var runs = await db.RunResults
            .Include(r => r.Group)
            .Where(r => r.StartedAt >= since && r.Group != null &&
                        (r.State == RunState.Passed || r.State == RunState.Failed))
            .OrderBy(r => r.StartedAt)
            .ToListAsync(ct);

        return runs.Select(r => new TrendPoint(
            r.StartedAt.Date, r.PassRate, r.Group!.Naziv
        )).ToList();
    }

    public async Task<IReadOnlyList<FlakyTestInfo>> GetFlakyTestsAsync(int minRuns = 3, CancellationToken ct = default)
    {
        var since = DateTime.UtcNow.AddDays(-30);
        var runs = await db.RunResults
            .Include(r => r.Group)
            .Where(r => r.StartedAt >= since && r.DetailsJson != null &&
                        (r.State == RunState.Passed || r.State == RunState.Failed))
            .OrderBy(r => r.StartedAt)
            .ToListAsync(ct);

        var scenarioResults = new Dictionary<string, List<(string GroupName, bool Passed)>>();
        foreach (var run in runs)
        {
            if (run.DetailsJson is null || run.Group is null) continue;
            try
            {
                var details = JsonSerializer.Deserialize<List<ScenarioDetail>>(run.DetailsJson, JsonOpts);
                if (details is null) continue;
                foreach (var d in details)
                {
                    var key = $"{run.Group.Naziv}::{d.Naziv}";
                    if (!scenarioResults.ContainsKey(key))
                        scenarioResults[key] = [];
                    scenarioResults[key].Add((run.Group.Naziv, d.Status == ScenarioRunStatus.Passed));
                }
            }
            catch { /* ignore malformed JSON */ }
        }

        var flaky = new List<FlakyTestInfo>();
        foreach (var (key, results) in scenarioResults)
        {
            if (results.Count < minRuns) continue;
            var flips = 0;
            for (var i = 1; i < results.Count; i++)
                if (results[i].Passed != results[i - 1].Passed) flips++;

            if (flips >= 2)
            {
                var parts = key.Split("::", 2);
                flaky.Add(new FlakyTestInfo(
                    ScenarioName: parts.Length > 1 ? parts[1] : key,
                    GroupName: results[0].GroupName,
                    TotalRuns: results.Count,
                    Flips: flips,
                    FlakyRate: (double)flips / (results.Count - 1) * 100));
            }
        }

        return flaky.OrderByDescending(f => f.FlakyRate).ToList();
    }

    public async Task<RunHistoryRow?> GetRunByIdAsync(Guid runId, CancellationToken ct = default)
    {
        var r = await db.RunResults.Include(x => x.Group).FirstOrDefaultAsync(x => x.Id == runId, ct);
        if (r?.Group is null) return null;
        return new RunHistoryRow(
            r.Id, r.GroupId, r.Group.Naziv, r.Group.Boja,
            MapTag(r.Group.Tag), r.State.ToString(), r.TriggerType.ToString(),
            r.PassRate, r.TotalCount, r.PassedCount, r.FailedCount,
            r.Duration, r.StartedAt, r.CompletedAt, r.DetailsJson);
    }

    private sealed record ScenarioDetail(string Naziv, ScenarioRunStatus Status);
    private static readonly JsonSerializerOptions JsonOpts =
        new(JsonSerializerDefaults.Web) { Converters = { new JsonStringEnumConverter() } };

    private static DTO.TestTag MapTag(RBBH.TestAutomation.Core.Domain.Enums.TestTag t) => t switch
    {
        RBBH.TestAutomation.Core.Domain.Enums.TestTag.Smoke => DTO.TestTag.Smoke,
        RBBH.TestAutomation.Core.Domain.Enums.TestTag.Regression => DTO.TestTag.Regression,
        RBBH.TestAutomation.Core.Domain.Enums.TestTag.Full => DTO.TestTag.Full,
        _ => DTO.TestTag.Smoke,
    };
}
