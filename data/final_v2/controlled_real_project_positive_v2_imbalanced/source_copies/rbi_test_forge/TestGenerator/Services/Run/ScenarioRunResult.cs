namespace RBBH.TestAutomation.Api.Services.Run;

/// <summary>Status izvršavanja jednog scenarija u live runneru.</summary>
public enum ScenarioRunStatus
{
    /// <summary>Još nije pokrenut.</summary>
    NotRun,

    /// <summary>Izvršavanje u toku.</summary>
    Running,

    /// <summary>Status i svi assert-i prošli.</summary>
    Passed,

    /// <summary>Status ili neki assert nije zadovoljen (vidi <see cref="ScenarioRunResult.FailReason"/>).</summary>
    Failed,

    /// <summary>Tip scenarija se još ne izvršava (npr. UI scenariji u Sprintu 2).</summary>
    Skipped,
}

/// <summary>
/// Rezultat jednog izvršavanja REST scenarija — koristi se za prikaz u UI-ju
/// i (kasnije) agregaciju u <c>RunResult</c> po grupi.
/// </summary>
public sealed record ScenarioRunResult(
    Guid              ScenarioId,
    string            Naziv,
    ScenarioRunStatus Status,
    int?              ActualStatus,
    int?              ExpectedStatus,
    long              DurationMs,
    string?           FailReason,
    string?           RequestDetails,
    string?           ResponseDetails);
