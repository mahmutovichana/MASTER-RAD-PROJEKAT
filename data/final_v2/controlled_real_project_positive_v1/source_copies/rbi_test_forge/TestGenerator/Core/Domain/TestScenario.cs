namespace RBBH.TestAutomation.Core.Domain;

/// <summary>
/// Jedan test scenarij unutar grupe. <c>Arrange/Act/Assert</c> su JSON stringovi
/// čija shema ovisi o tipu (REST vs Blazor).
/// </summary>
public class TestScenario
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid GroupId { get; set; }
    public string Naziv { get; set; } = "";
    public string Tip { get; set; } = "Rest";
    public string Target { get; set; } = "";
    public string? Arrange { get; set; }
    public string? Act { get; set; }
    public string? Assert { get; set; }
    public int Redoslijed { get; set; }
    public bool RunSequentially { get; set; }

    public string? KreiranOd { get; set; }
    public DateTime KreiranAt { get; set; } = DateTime.UtcNow;

    public TestGroup? Group { get; set; }
}
