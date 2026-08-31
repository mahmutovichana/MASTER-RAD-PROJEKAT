using RBBH.TestAutomation.Core.Domain.Enums;

namespace RBBH.TestAutomation.Core.Domain;

/// <summary>
/// Grupa testova (suite). Podržava ≤2 nivoa hijerarhije — pravilo se provodi u repozitoriju.
/// </summary>
public class TestGroup
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string Naziv { get; set; } = "";
    public string? Opis { get; set; }
    public string? Boja { get; set; }
    public TestTag Tag { get; set; }
    public int Prioritet { get; set; }
    public string? RunConfiguration { get; set; }
    public Guid? ParentGroupId { get; set; }

    public string? NotificationConfigJson { get; set; }

    public string? KreiranOd { get; set; }
    public DateTime KreiranAt { get; set; } = DateTime.UtcNow;
    public string? IzmjenjenOd { get; set; }
    public DateTime? IzmjenjenAt { get; set; }

    public TestGroup? ParentGroup { get; set; }
    public ICollection<TestGroup> ChildGroups { get; set; } = [];
    public ICollection<TestScenario> Scenarios { get; set; } = [];
    public ICollection<ScheduleConfig> Schedules { get; set; } = [];
    public ICollection<RunResult> RunResults { get; set; } = [];
}
