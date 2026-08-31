using RBBH.TestAutomation.Api.Services.Run;
using Hangfire;
using Hangfire.Console;
using Hangfire.Server;

namespace RBBH.TestAutomation.Api.Jobs;

public class GroupTestJob(IGroupTestExecutor executor, ILogger<GroupTestJob> logger)
{
    [Queue("default")]
    [AutomaticRetry(Attempts = 2, DelaysInSeconds = [60, 300], OnAttemptsExceeded = AttemptsExceededAction.Fail)]
    public async Task ExecuteGroup(Guid groupId, RunOptions options, PerformContext? context = null)
    {
        logger.LogInformation("Hangfire: pokretanje testova za grupu {GroupId}", groupId);
        context?.WriteLine($"Pokretanje testova za grupu {groupId}");

        // Live log u Dashboard konzoli — pretplata na progres executora ispisuje
        // svaki novi rezultat (zelena za prolaz, crvena za pad) dok run traje.
        // Executor i dalje perzistira live progres u bazu (TAG-70/71).
        var logged = 0;
        void OnProgress(GroupRunProgress p)
        {
            for (var i = logged; i < p.Results.Count; i++)
            {
                var r = p.Results[i];
                context?.WriteLine(
                    r.Status == ScenarioRunStatus.Failed
                        ? ConsoleTextColor.Red
                        : ConsoleTextColor.Green,
                    $"  {r.Naziv}: {r.Status} ({r.DurationMs}ms)");
            }
            logged = p.Results.Count;
        }

        executor.ProgressChanged += OnProgress;
        try
        {
            var result = await executor.ExecuteGroupAsync(groupId, options);

            logger.LogInformation(
                "Hangfire: grupa {GroupId} zavrsena - {Passed} proslo, {Failed} palo, ukupno {Total}",
                groupId,
                result.Passed,
                result.Failed,
                result.Total);
            context?.WriteLine($"Zavrseno: {result.Passed} proslo, {result.Failed} palo, ukupno {result.Total}.");
        }
        finally
        {
            executor.ProgressChanged -= OnProgress;
        }
    }

    // Poziva ScheduleService (recurring) — default RunOptions.
    // PerformContext Hangfire injektuje u runtime-u (u izrazu se proslijedi null).
    public Task ExecuteAsync(Guid groupId, PerformContext? context = null) =>
        ExecuteGroup(groupId, new RunOptions(), context);
}
