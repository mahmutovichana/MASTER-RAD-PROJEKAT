using RBBH.TestAutomation.Core.Domain;

namespace RBBH.TestAutomation.Api.DTO;

/// <summary>
/// YAML/JSON dokument za dijeljenje jedne TestForge grupe i njenih scenarija.
/// </summary>
public sealed class ScenarioExportDocument
{
    public string FormatVersion { get; set; } = "1.0";
    public DateTimeOffset ExportedAt { get; set; } = DateTimeOffset.UtcNow;
    public TestGroup Group { get; set; } = new();
    public List<TestScenario> Scenarios { get; set; } = [];
}

public enum ScenarioImportMergeStrategy
{
    OverwriteExisting,
    AddOnlyNew,
}

public sealed class ScenarioImportPreview
{
    public string FileName { get; set; } = string.Empty;
    public ScenarioExportDocument? Document { get; set; }
    public bool IsValid => Errors.Count == 0 && Document is not null;
    public bool WillUpdateExisting { get; set; }
    public int NewScenarioCount { get; set; }
    public int ExistingScenarioCount { get; set; }
    public List<string> Errors { get; set; } = [];
    public List<string> Warnings { get; set; } = [];
}

public sealed class ScenarioImportResult
{
    public int ImportedGroups { get; set; }
    public int UpdatedGroups { get; set; }
    public int ImportedScenarios { get; set; }
    public int SkippedScenarios { get; set; }
    public List<string> Messages { get; set; } = [];
}
