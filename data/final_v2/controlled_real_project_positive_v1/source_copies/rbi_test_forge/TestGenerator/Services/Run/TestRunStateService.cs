using System.Diagnostics;
using RBBH.TestAutomation.Api.Services;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Domain.Enums;
using RBBH.TestAutomation.Core.Repositories;

namespace RBBH.TestAutomation.Api.Services.Run;

/// <summary>Agregatna faza zadnjeg pokretanja (za indikator u sidebaru).</summary>
public enum TestRunPhase { Idle, Running, AllPassed, SomeFailed }

/// <summary>
/// Dijeljeno stanje izvršavanja testova — jedna instanca po circuit-u (Scoped).
/// Header "Pokreni" i Scenariji stranica pokreću testove kroz ovaj servis, a
/// SideNav (indikator) i Scenariji (kolona Rezultat) osluškuju <see cref="Changed"/>.
/// Tako je stanje konzistentno bez obzira gdje je korisnik.
/// </summary>
public sealed class TestRunStateService(
    IScenarioService scenarios,
    IScenarioRunner runner,
    IServiceProvider sp,
    ILogger<TestRunStateService> logger)
{
    private readonly Dictionary<Guid, ScenarioRunResult> _results = new();

    /// <summary>Trenutna agregatna faza zadnjeg pokretanja.</summary>
    public TestRunPhase Phase { get; private set; } = TestRunPhase.Idle;

    public int PassedCount { get; private set; }
    public int FailedCount { get; private set; }
    public bool IsRunning => Phase == TestRunPhase.Running;

    /// <summary>Rezultati po scenariju (prazno ako scenarij još nije pokrenut).</summary>
    public IReadOnlyDictionary<Guid, ScenarioRunResult> Results => _results;

    /// <summary>Okida se na svaku promjenu stanja — komponente se pretplate i re-renderuju.</summary>
    public event Action? Changed;

    /// <summary>Pokreni sve scenarije (one iz Scenariji taba). Sigurno za višestruke pozive.</summary>
    public async Task RunAllAsync(CancellationToken ct = default)
    {
        if (IsRunning) return;
        var lista = await scenarios.GetAllAsync(ct);
        await RunManyAsync(lista.Select(i => i.Id).ToList(), ct);
    }

    /// <summary>Pokreni određeni skup scenarija (npr. svi scenariji jedne grupe).</summary>
    public async Task RunManyAsync(IReadOnlyList<Guid> scenarioIds, CancellationToken ct = default)
    {
        if (IsRunning || scenarioIds.Count == 0) return;

        Phase = TestRunPhase.Running;
        _results.Clear();
        Notify();

        try
        {
            var config = await scenarios.GetRunConfigAsync(ct);

            foreach (var id in scenarioIds)
            {
                var dto = await scenarios.GetByIdAsync(id, ct);
                if (dto is null) continue;

                _results[id] = Running(id, dto.Naziv);
                Notify();

                _results[id] = await runner.RunAsync(dto, config, ct);
                Notify();
            }

            Finish();
        }
        catch (OperationCanceledException)
        {
            Phase = TestRunPhase.Idle;
            Notify();
        }
        catch
        {
            Phase = TestRunPhase.SomeFailed;
            Notify();
        }
    }

    /// <summary>
    /// Pokreni sve scenarije jedne grupe i <b>upiši RunResult u bazu</b> (best-effort).
    /// Upis se preskače u mock modu (nema IRunRepository) ili se tiho ignoriše pri grešci.
    /// </summary>
    public async Task RunGroupAsync(Guid groupId, IReadOnlyList<Guid> scenarioIds, CancellationToken ct = default)
    {
        var startedAt = DateTime.UtcNow;
        var sw = Stopwatch.StartNew();

        await RunManyAsync(scenarioIds, ct);
        sw.Stop();

        // Ako ništa nije izvršeno (prazno / otkazano) — ne upisuj prazan run.
        if (Phase is TestRunPhase.Idle) return;

        await PersistAsync(groupId, startedAt, sw.Elapsed, ct);
    }

    private async Task PersistAsync(Guid groupId, DateTime startedAt, TimeSpan duration, CancellationToken ct)
    {
        // IRunRepository postoji samo u real modu (RegisterTestForge). U mock modu preskačemo.
        var repo = sp.GetService(typeof(IRunRepository)) as IRunRepository;
        if (repo is null) return;

        try
        {
            var executed = PassedCount + FailedCount;                 // Skipped (UI) se ne broji
            var passRate = executed > 0 ? (double)PassedCount / executed * 100 : 0;

            await repo.AddAsync(new RunResult
            {
                GroupId     = groupId,
                State       = FailedCount == 0 && PassedCount > 0 ? RunState.Passed : RunState.Failed,
                Duration    = duration,
                PassRate    = passRate,
                TriggerType = TriggerType.Manual,
                StartedAt   = startedAt,
                CompletedAt = DateTime.UtcNow,
            }, ct);
        }
        catch (Exception ex)
        {
            // Best-effort — neuspjeli upis ne smije srušiti pokretanje.
            logger.LogWarning(ex, "Nije moguće upisati RunResult za grupu {GroupId}", groupId);
        }
    }

    /// <summary>Pokreni jedan scenarij (play dugme u redu). Ažurira agregatnu fazu.</summary>
    public async Task RunOneAsync(Guid scenarioId, CancellationToken ct = default)
    {
        var dto = await scenarios.GetByIdAsync(scenarioId, ct);
        if (dto is null) return;

        _results[scenarioId] = Running(scenarioId, dto.Naziv);
        if (!IsRunning) Phase = TestRunPhase.Running;
        Notify();

        try
        {
            var config = await scenarios.GetRunConfigAsync(ct);
            _results[scenarioId] = await runner.RunAsync(dto, config, ct);
        }
        catch (OperationCanceledException) { return; }
        catch (Exception ex)
        {
            _results[scenarioId] = new ScenarioRunResult(
                scenarioId, dto.Naziv, ScenarioRunStatus.Failed, null, null, 0, ex.Message, null, null);
        }

        Finish();
    }

    /// <summary>Resetuje fazu na Idle (npr. pri otvaranju Scenariji taba bez prethodnog runa).</summary>
    public void Reset()
    {
        Phase = TestRunPhase.Idle;
        _results.Clear();
        Notify();
    }

    private void Finish()
    {
        PassedCount = _results.Values.Count(r => r.Status == ScenarioRunStatus.Passed);
        FailedCount = _results.Values.Count(r => r.Status == ScenarioRunStatus.Failed);
        Phase = FailedCount == 0 && PassedCount > 0 ? TestRunPhase.AllPassed
              : FailedCount > 0                      ? TestRunPhase.SomeFailed
              : TestRunPhase.Idle;
        Notify();
    }

    private static ScenarioRunResult Running(Guid id, string naziv) =>
        new(id, naziv, ScenarioRunStatus.Running, null, null, 0, null, null, null);

    private void Notify() => Changed?.Invoke();
}
