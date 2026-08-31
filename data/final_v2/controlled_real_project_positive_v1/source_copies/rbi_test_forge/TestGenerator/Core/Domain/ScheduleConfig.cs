namespace RBBH.TestAutomation.Core.Domain;

/// <summary>
/// Cron raspored za automatsko pokretanje grupe testova.
/// Engine (Hangfire) dolazi u Sprintu 3.
/// </summary>
public class ScheduleConfig
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid GroupId { get; set; }
    public string CronExpression { get; set; } = "0 8 * * 1-5";
    public bool IsActive { get; set; } = true;
    public string Timezone { get; set; } = "Europe/Sarajevo";
    public string? NotificationConfig { get; set; }

    public TestGroup? Group { get; set; }
}
