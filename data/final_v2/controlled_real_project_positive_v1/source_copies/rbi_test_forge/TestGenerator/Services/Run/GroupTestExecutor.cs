using System.Diagnostics;
using System.Text.Json;
using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Api.Services;
using RBBH.TestAutomation.Api.Services.Notifications;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Domain.Enums;
using RBBH.TestAutomation.Core.Repositories;

namespace RBBH.TestAutomation.Api.Services.Run;

public sealed record RunOptions(
    bool RunInParallel = false,
    bool StopOnFirstFailure = false,
    int MaxParallelThreads = RunConfiguration.DefaultMaxParallelThreads);

public sealed record RunConfiguration(
    bool RunInParallel = false,
    int MaxParallelThreads = RunConfiguration.DefaultMaxParallelThreads)
{
    public const int DefaultMaxParallelThreads = 4;
}

public sealed record GroupRunProgress(
    Guid RunId,
    Guid GroupId,
    int Total,
    int Passed,
    int Failed,
    double ThroughputPerSecond,
    IReadOnlyList<ScenarioRunResult> Results)
{
    public int Completed => Passed + Failed;
}

public interface IGroupTestExecutor
{
    event Action<GroupRunProgress>? ProgressChanged;
    Task<GroupRunProgress> ExecuteGroupAsync(Guid groupId, RunOptions options, CancellationToken ct = default);
}

public sealed class GroupTestExecutor(
    IGroupService groupSvc,
    IScenarioService scenarioSvc,
    IScenarioRunner runner,
    IServiceProvider sp,
    ILogger<GroupTestExecutor> logger) : IGroupTestExecutor
{
    private static readonly JsonSerializerOptions Json = new(JsonSerializerDefaults.Web);

    public event Action<GroupRunProgress>? ProgressChanged;

    public async Task<GroupRunProgress> ExecuteGroupAsync(Guid groupId, RunOptions options, CancellationToken ct = default)
    {
        var items = await groupSvc.GetScenariosAsync(groupId, ct);
        var orderedItems = items.OrderBy(i => i.Redoslijed).ToList();
        var run = await CreateRunAsync(groupId, orderedItems.Count, options, ct);
        var sw = Stopwatch.StartNew();
        var results = new List<ScenarioRunResult>();
        var config = await scenarioSvc.GetRunConfigAsync(ct);
        var maxParallelThreads = Math.Max(1, options.MaxParallelThreads);
        var resultsLock = new object();
        var persistLock = new SemaphoreSlim(1, 1);

        try
        {
            if (options.RunInParallel && !options.StopOnFirstFailure)
            {
                await ExecuteParallelRespectingSequentialMarkersAsync(
                    orderedItems, config, run, groupId, results, resultsLock, persistLock, sw, maxParallelThreads, ct);
            }
            else
            {
                foreach (var item in orderedItems)
                {
                    var result = await ExecuteScenarioAsync(item.Id, config, ct);
                    results.Add(result);
                    await PersistProgressAsync(run, results, orderedItems.Count, sw.Elapsed, completed: false, ct);
                    Notify(run.Id, groupId, orderedItems.Count, sw.Elapsed, results);

                    if (options.StopOnFirstFailure && result.Status == ScenarioRunStatus.Failed)
                        break;
                }
            }

            sw.Stop();
            await PersistProgressAsync(run, results, orderedItems.Count, sw.Elapsed, completed: true, ct);
            Notify(run.Id, groupId, orderedItems.Count, sw.Elapsed, results);
            await SendNotificationAsync(run, groupId, ct);
            return ToProgress(run.Id, groupId, orderedItems.Count, sw.Elapsed, results);
        }
        catch (OperationCanceledException)
        {
            sw.Stop();
            run.State = RunState.Cancelled;
            run.Duration = sw.Elapsed;
            run.CompletedAt = DateTime.UtcNow;
            await UpdateRunAsync(run, ct);
            throw;
        }
        catch (Exception ex)
        {
            // Bez ovoga bi run ostao zaglavljen u stanju Running i bio nevidljiv u
            // Historiji (koja filtrira Running/Pending). Bitno za Hangfire cron runove
            // gdje nema UI-ja da prikaze gresku — markiramo Failed pa je run vidljiv.
            sw.Stop();
            logger.LogError(ex, "Grupni run {RunId} (grupa {GroupId}) pao s greskom", run.Id, groupId);
            run.State = RunState.Failed;
            run.Duration = sw.Elapsed;
            run.CompletedAt = DateTime.UtcNow;
            await UpdateRunAsync(run, CancellationToken.None);
            throw;
        }
    }

    private async Task ExecuteParallelRespectingSequentialMarkersAsync(
        IReadOnlyList<ScenarioListItemDto> orderedItems,
        RunConfigDto config,
        RunResult run,
        Guid groupId,
        List<ScenarioRunResult> results,
        object resultsLock,
        SemaphoreSlim persistLock,
        Stopwatch sw,
        int maxParallelThreads,
        CancellationToken ct)
    {
        var batch = new List<ScenarioListItemDto>();

        foreach (var item in orderedItems)
        {
            if (item.RunSequentially)
            {
                await FlushParallelBatchAsync(batch, config, run, groupId, orderedItems.Count,
                    results, resultsLock, persistLock, sw, maxParallelThreads, ct);
                batch.Clear();

                var result = await ExecuteScenarioAsync(item.Id, config, ct);
                results.Add(result);
                await PersistProgressAsync(run, results, orderedItems.Count, sw.Elapsed, completed: false, ct);
                Notify(run.Id, groupId, orderedItems.Count, sw.Elapsed, results);
            }
            else
            {
                batch.Add(item);
            }
        }

        await FlushParallelBatchAsync(batch, config, run, groupId, orderedItems.Count,
            results, resultsLock, persistLock, sw, maxParallelThreads, ct);
    }

    private async Task FlushParallelBatchAsync(
        IReadOnlyList<ScenarioListItemDto> batch,
        RunConfigDto config,
        RunResult run,
        Guid groupId,
        int total,
        List<ScenarioRunResult> results,
        object resultsLock,
        SemaphoreSlim persistLock,
        Stopwatch sw,
        int maxParallelThreads,
        CancellationToken ct)
    {
        if (batch.Count == 0)
            return;

        using var throttle = new SemaphoreSlim(maxParallelThreads, maxParallelThreads);
        var tasks = batch.Select(async item =>
        {
            await throttle.WaitAsync(ct);
            try
            {
                var result = await ExecuteScenarioAsync(item.Id, config, ct);
                List<ScenarioRunResult> snapshot;
                lock (resultsLock)
                {
                    results.Add(result);
                    snapshot = results.ToList();
                }

                await persistLock.WaitAsync(ct);
                try
                {
                    await PersistProgressAsync(run, snapshot, total, sw.Elapsed, completed: false, ct);
                    Notify(run.Id, groupId, total, sw.Elapsed, snapshot);
                }
                finally
                {
                    persistLock.Release();
                }
            }
            finally
            {
                throttle.Release();
            }
        });

        await Task.WhenAll(tasks);
    }

    private async Task<ScenarioRunResult> ExecuteScenarioAsync(Guid id, RunConfigDto config, CancellationToken ct)
    {
        var dto = await scenarioSvc.GetByIdAsync(id, ct);
        if (dto is null)
            return new ScenarioRunResult(id, "Nepoznat scenarij", ScenarioRunStatus.Failed, null, null, 0,
                "Scenarij nije pronadjen.", null, null);

        return await runner.RunAsync(dto, config, ct);
    }

    private async Task<RunResult> CreateRunAsync(Guid groupId, int total, RunOptions options, CancellationToken ct)
    {
        var run = new RunResult
        {
            GroupId = groupId,
            State = RunState.Running,
            TotalCount = total,
            OptionsJson = JsonSerializer.Serialize(options, Json),
            DetailsJson = "[]",
            StartedAt = DateTime.UtcNow,
        };

        if (sp.GetService(typeof(IRunRepository)) is IRunRepository repo)
            run.Id = await repo.AddAsync(run, ct);

        return run;
    }

    private async Task PersistProgressAsync(
        RunResult run,
        IReadOnlyList<ScenarioRunResult> results,
        int total,
        TimeSpan duration,
        bool completed,
        CancellationToken ct)
    {
        run.TotalCount = total;
        run.PassedCount = results.Count(r => r.Status == ScenarioRunStatus.Passed);
        run.FailedCount = results.Count(r => r.Status == ScenarioRunStatus.Failed);
        run.PassRate = results.Count > 0 ? (double)run.PassedCount / results.Count * 100 : 0;
        run.ThroughputPerSecond = Throughput(results.Count, duration);
        run.Duration = duration;
        run.DetailsJson = JsonSerializer.Serialize(results, Json);

        if (completed)
        {
            run.State = run.FailedCount == 0 && run.PassedCount > 0 ? RunState.Passed : RunState.Failed;
            run.CompletedAt = DateTime.UtcNow;
        }

        await UpdateRunAsync(run, ct);
    }

    private async Task UpdateRunAsync(RunResult run, CancellationToken ct)
    {
        if (sp.GetService(typeof(IRunRepository)) is not IRunRepository repo)
            return;

        try
        {
            await repo.UpdateAsync(run, ct);
        }
        catch (Exception ex)
        {
            logger.LogWarning(ex, "Nije moguce azurirati RunResult {RunId}", run.Id);
        }
    }

    private async Task SendNotificationAsync(RunResult run, Guid groupId, CancellationToken ct)
    {
        try
        {
            if (sp.GetService(typeof(INotificationService)) is not INotificationService notif) return;
            if (sp.GetService(typeof(IGroupRepository)) is not IGroupRepository repo) return;
            var group = await repo.GetByIdAsync(groupId, ct);
            if (group is null) return;
            await notif.SendRunCompletionAsync(run, group, ct);
        }
        catch (Exception ex)
        {
            logger.LogWarning(ex, "Notifikacija nakon runa nije uspjela za grupu {GroupId}", groupId);
        }
    }

    private void Notify(Guid runId, Guid groupId, int total, TimeSpan duration, IReadOnlyList<ScenarioRunResult> results) =>
        ProgressChanged?.Invoke(ToProgress(runId, groupId, total, duration, results));

    private static GroupRunProgress ToProgress(
        Guid runId,
        Guid groupId,
        int total,
        TimeSpan duration,
        IReadOnlyList<ScenarioRunResult> results) =>
        new(
            runId,
            groupId,
            total,
            results.Count(r => r.Status == ScenarioRunStatus.Passed),
            results.Count(r => r.Status == ScenarioRunStatus.Failed),
            Throughput(results.Count, duration),
            results.ToList());

    private static double Throughput(int completed, TimeSpan duration) =>
        completed == 0 || duration.TotalSeconds <= 0 ? 0 : completed / duration.TotalSeconds;
}
