using RBBH.TestAutomation.Core.Domain.Enums;

namespace RBBH.TestAutomation.Core.Domain;

/// <summary>
/// Rezultat jednog pokretanja grupe testova.
/// </summary>
public class RunResult
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid GroupId { get; set; }
    public RunState State { get; set; } = RunState.Pending;
    public TimeSpan Duration { get; set; }
    public double PassRate { get; set; }
    public int TotalCount { get; set; }
    public int PassedCount { get; set; }
    public int FailedCount { get; set; }
    public double ThroughputPerSecond { get; set; }
    public TriggerType TriggerType { get; set; } = TriggerType.Manual;
    public DateTime StartedAt { get; set; } = DateTime.UtcNow;
    public DateTime? CompletedAt { get; set; }
    public string? OptionsJson { get; set; }
    public string? DetailsJson { get; set; }

    public TestGroup? Group { get; set; }
}
