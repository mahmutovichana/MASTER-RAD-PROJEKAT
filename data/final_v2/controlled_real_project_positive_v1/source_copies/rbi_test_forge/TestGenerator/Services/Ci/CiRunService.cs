using System.Collections.Concurrent;
using System.Text.Json;
using RBBH.TestAutomation.Api.Services.Run;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Domain.Enums;
using RBBH.TestAutomation.Core.Repositories;

namespace RBBH.TestAutomation.Api.Services.Ci;

/// <summary>Status CI/CD run joba.</summary>
public enum CiJobStatus { Running, Passed, Failed }

/// <summary>
/// Jedan izvršeni test unutar CI joba — izvor za izvještaje (JUnit/TRX/HTML/JSON).
/// Projekcija <see cref="ScenarioRunResult"/> obogaćena nazivom grupe (suite).
/// </summary>
public sealed record CiTestEntry(
    string              Name,
    string              GroupName,
    ScenarioRunStatus   Status,
    long                DurationMs,
    string?             FailReason,
    int?                ActualStatus,
    int?                ExpectedStatus,
    string?             ResponseDetails);

/// <summary>Nepromjenjivi snimak stanja CI joba za API odgovor.</summary>
public sealed record CiJobSnapshot(
    Guid                JobId,
    CiJobStatus         Status,
    int                 Total,
    int                 Completed,
    int                 Passed,
    int                 Failed,
    double              PassRate,
    IReadOnlyList<string> FailedTests,
    DateTime            StartedAt,
    DateTime?           CompletedAt,
    IReadOnlyList<CiTestEntry> Results);

public interface ICiRunService
{
    /// <summary>Pokreni grupu testova asinhrono; vrati jobId za polling.</summary>
    Guid StartGroupRun(Guid groupId);

    /// <summary>Pokreni sve grupe s datim tagom; null ako tag nije validan.</summary>
    Guid? StartTagRun(string tag);

    /// <summary>Trenutni snimak joba, ili null ako jobId ne postoji.</summary>
    CiJobSnapshot? GetStatus(Guid jobId);

    /// <summary>Sačekaj završetak joba do timeout-a; vrati zadnji snimak.</summary>
    Task<CiJobSnapshot?> WaitForCompletionAsync(Guid jobId, TimeSpan timeout, CancellationToken ct = default);
}

/// <summary>
/// In-process tracker CI/CD pokretanja. Singleton — drži stanje jobova u memoriji i
/// izvršava ih u pozadini koristeći zaseban DI scope (jer su runner i servisi Scoped).
/// Rezultat svake grupe se best-effort upisuje kao <see cref="RunResult"/> (TriggerType.Pipeline).
/// </summary>
public sealed class CiRunService(IServiceScopeFactory scopeFactory, ILogger<CiRunService> logger) : ICiRunService
{
    private sealed class CiJob
    {
        public required Guid Id;
        public CiJobStatus Status = CiJobStatus.Running;
        public int Total;
        public int Completed;
        public int Passed;
        public int Failed;
        public readonly List<string> FailedTests = [];
        public readonly List<CiTestEntry> Results = [];   // per-test rezultati za izvještaje
        public DateTime StartedAt = DateTime.UtcNow;
        public DateTime? CompletedAt;
        public readonly TaskCompletionSource Completion =
            new(TaskCreationOptions.RunContinuationsAsynchronously);
        public readonly Lock Sync = new();
    }

    private readonly ConcurrentDictionary<Guid, CiJob> _jobs = new();

    // Isti JSON režim koji GroupTestExecutor koristi za DetailsJson — garantuje round-trip.
    private static readonly JsonSerializerOptions WebJson = new(JsonSerializerDefaults.Web);

    public Guid StartGroupRun(Guid groupId)
    {
        var job = NewJob();
        _ = Task.Run(() => RunAsync(job, _ => Task.FromResult<IReadOnlyList<Guid>>([groupId])));
        return job.Id;
    }

    public Guid? StartTagRun(string tag)
    {
        if (!Enum.TryParse<TestTag>(tag, ignoreCase: true, out var parsed))
            return null;

        var job = NewJob();
        _ = Task.Run(() => RunAsync(job, sp => ResolveGroupsByTagAsync(sp, parsed)));
        return job.Id;
    }

    public CiJobSnapshot? GetStatus(Guid jobId) =>
        _jobs.TryGetValue(jobId, out var job) ? Snapshot(job) : null;

    public async Task<CiJobSnapshot?> WaitForCompletionAsync(Guid jobId, TimeSpan timeout, CancellationToken ct = default)
    {
        if (!_jobs.TryGetValue(jobId, out var job)) return null;

        using var cts = CancellationTokenSource.CreateLinkedTokenSource(ct);
        cts.CancelAfter(timeout);
        try
        {
            await job.Completion.Task.WaitAsync(cts.Token);
        }
        catch (OperationCanceledException)
        {
            // Timeout — vraćamo zadnje poznato stanje (još uvijek Running).
        }

        return Snapshot(job);
    }

    private CiJob NewJob()
    {
        var job = new CiJob { Id = Guid.NewGuid() };
        _jobs[job.Id] = job;
        return job;
    }

    private async Task RunAsync(CiJob job, Func<IServiceProvider, Task<IReadOnlyList<Guid>>> groupResolver)
    {
        try
        {
            using var scope = scopeFactory.CreateScope();
            var sp          = scope.ServiceProvider;
            var groupSvc    = sp.GetRequiredService<IGroupService>();
            var scenarioSvc = sp.GetRequiredService<IScenarioService>();
            var runner      = sp.GetRequiredService<IScenarioRunner>();
            var runRepo     = sp.GetService(typeof(IRunRepository)) as IRunRepository;

            var groupIds = await groupResolver(sp);
            var config   = await scenarioSvc.GetRunConfigAsync();

            // Pred-učitaj scenarije po grupi (+ naziv grupe za suite u izvještajima) da znamo ukupan broj.
            var perGroup = new List<(Guid GroupId, string GroupName, IReadOnlyList<Guid> ScenarioIds)>();
            foreach (var gid in groupIds)
            {
                var ids = (await groupSvc.GetScenariosAsync(gid)).Select(s => s.Id).ToList();
                var groupName = (await groupSvc.GetByIdAsync(gid))?.Naziv ?? "Grupa";
                perGroup.Add((gid, groupName, ids));
            }

            lock (job.Sync) job.Total = perGroup.Sum(g => g.ScenarioIds.Count);

            foreach (var (gid, groupName, scenarioIds) in perGroup)
            {
                var startedAt = DateTime.UtcNow;
                var groupResults = new List<ScenarioRunResult>();   // sirovi rezultati grupe → DetailsJson

                foreach (var sid in scenarioIds)
                {
                    var dto = await scenarioSvc.GetByIdAsync(sid);
                    if (dto is null) { lock (job.Sync) job.Completed++; continue; }

                    var result = await runner.RunAsync(dto, config);
                    groupResults.Add(result);

                    lock (job.Sync)
                    {
                        job.Completed++;
                        if (result.Status == ScenarioRunStatus.Passed) job.Passed++;
                        else if (result.Status == ScenarioRunStatus.Failed)
                        {
                            job.Failed++;
                            job.FailedTests.Add(dto.Naziv);
                        }

                        // Per-test zapis za in-memory izvještaje (uključuje i Skipped — npr. UI scenariji).
                        job.Results.Add(new CiTestEntry(
                            result.Naziv, groupName, result.Status, result.DurationMs,
                            result.FailReason, result.ActualStatus, result.ExpectedStatus, result.ResponseDetails));
                    }
                }

                // Persistiraj grupu uz per-test detalje (preživljava restart; isti oblik kao executor).
                await PersistRunAsync(runRepo, gid, startedAt, groupResults);
            }

            Finish(job);
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "CI run job {JobId} pao s greškom", job.Id);
            lock (job.Sync)
            {
                job.Status = CiJobStatus.Failed;
                job.CompletedAt = DateTime.UtcNow;
            }
            job.Completion.TrySetResult();
        }
    }

    private static async Task<IReadOnlyList<Guid>> ResolveGroupsByTagAsync(IServiceProvider sp, TestTag tag)
    {
        var groupSvc = sp.GetRequiredService<IGroupService>();
        var tree     = await groupSvc.GetGroupsTreeAsync();

        var result = new List<Guid>();
        void Walk(IEnumerable<DTO.GroupTreeNodeDto> nodes)
        {
            foreach (var n in nodes)
            {
                if ((int)n.Group.Tag == (int)tag) result.Add(n.Group.Id);
                Walk(n.Children);
            }
        }
        Walk(tree);
        return result;
    }

    private async Task PersistRunAsync(
        IRunRepository? repo, Guid groupId, DateTime startedAt, IReadOnlyList<ScenarioRunResult> results)
    {
        if (repo is null) return;   // mock mod — nema baze

        try
        {
            var passed = results.Count(r => r.Status == ScenarioRunStatus.Passed);
            var failed = results.Count(r => r.Status == ScenarioRunStatus.Failed);
            var executed = passed + failed;
            await repo.AddAsync(new RunResult
            {
                GroupId     = groupId,
                State       = failed == 0 && passed > 0 ? RunState.Passed : RunState.Failed,
                Duration    = DateTime.UtcNow - startedAt,
                TotalCount  = results.Count,
                PassedCount = passed,
                FailedCount = failed,
                PassRate    = executed > 0 ? (double)passed / executed * 100 : 0,
                TriggerType = TriggerType.Pipeline,
                StartedAt   = startedAt,
                CompletedAt = DateTime.UtcNow,
                // Isti oblik (List<ScenarioRunResult>, web JSON) koji executor/Historija koriste.
                DetailsJson = JsonSerializer.Serialize(results, WebJson),
            });
        }
        catch (Exception ex)
        {
            logger.LogWarning(ex, "CI: neuspio upis RunResult za grupu {GroupId}", groupId);
        }
    }

    private static void Finish(CiJob job)
    {
        lock (job.Sync)
        {
            job.Status = job.Failed == 0 ? CiJobStatus.Passed : CiJobStatus.Failed;
            job.CompletedAt = DateTime.UtcNow;
        }
        job.Completion.TrySetResult();
    }

    private static CiJobSnapshot Snapshot(CiJob job)
    {
        lock (job.Sync)
        {
            var executed = job.Passed + job.Failed;
            var passRate = executed > 0 ? Math.Round((double)job.Passed / executed * 100, 1) : 0;
            return new CiJobSnapshot(
                job.Id, job.Status, job.Total, job.Completed, job.Passed, job.Failed,
                passRate, job.FailedTests.ToList(), job.StartedAt, job.CompletedAt,
                job.Results.ToList());
        }
    }
}
