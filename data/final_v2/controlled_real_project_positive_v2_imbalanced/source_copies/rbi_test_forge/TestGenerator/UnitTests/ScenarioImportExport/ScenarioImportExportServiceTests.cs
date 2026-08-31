using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Api.Services;
using Microsoft.Extensions.DependencyInjection;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Domain.Enums;

namespace UnitTests.ScenarioImportExport;

public class ScenarioImportExportServiceTests
{
    [Fact]
    public async Task ExportAllScenariosToYaml_IncludesTestForgeGroupAndScenarios()
    {
        var service = CreateService();

        var yaml = await service.ExportAllScenariosToYamlAsync();

        Assert.Contains("formatVersion:", yaml);
        Assert.Contains("group:", yaml);
        Assert.Contains("scenarios:", yaml);
        Assert.Contains("Health check", yaml);
    }

    [Fact]
    public async Task BuildPreview_ReturnsErrorsForInvalidSchema()
    {
        var service = CreateService();
        var yaml = """
formatVersion: "1.0"
group:
  naziv: ""
scenarios: []
""";

        var preview = await service.BuildPreviewAsync("bad.yaml", yaml);

        Assert.False(preview.IsValid);
        Assert.Contains(preview.Errors, e => e.Contains("group.naziv"));
        Assert.Contains(preview.Errors, e => e.Contains("scenarios"));
    }

    [Fact]
    public async Task BuildPreview_SupportsJsonFiles()
    {
        var service = CreateService();
        var json = await service.ExportAllScenariosToJsonAsync();

        var preview = await service.BuildPreviewAsync("scenariji.json", json);

        Assert.True(preview.IsValid);
        Assert.Equal("Svi scenariji", preview.Document!.Group.Naziv);
    }

    [Fact]
    public async Task Import_AddOnlyNew_SkipsExistingAndAddsNewScenario()
    {
        var scenarioService = new MockScenarioService();
        var service = CreateService(scenarioService);
        var document = NewDocument(
            NewScenario("Health check"),
            NewScenario("Novi import scenarij"));
        var preview = await service.BuildPreviewAsync("scenariji.yaml", ToYaml(document));

        var result = await service.ImportAsync(
            [preview],
            ScenarioImportMergeStrategy.AddOnlyNew,
            "tester",
            "Tester");

        Assert.Equal(1, result.SkippedScenarios);
        Assert.Equal(1, result.ImportedScenarios);
        Assert.Contains(await scenarioService.GetAllAsync(), s => s.Naziv == "Novi import scenarij");
    }

    [Fact]
    public async Task Import_OverwriteExisting_UpdatesScenarioByName()
    {
        var scenarioService = new MockScenarioService();
        var service = CreateService(scenarioService);
        var document = NewDocument(NewScenario("Health check", target: "/api/changed"));
        var preview = await service.BuildPreviewAsync("scenariji.yaml", ToYaml(document));

        await service.ImportAsync(
            [preview],
            ScenarioImportMergeStrategy.OverwriteExisting,
            "tester",
            "Tester");

        var updated = (await scenarioService.GetAllAsync()).Single(s => s.Naziv == "Health check");
        var details = await scenarioService.GetByIdAsync(updated.Id);
        Assert.Equal("/api/changed", details!.Rest!.Url);
    }

    private static ScenarioImportExportService CreateService(MockScenarioService? scenarioService = null)
    {
        var services = new ServiceCollection().BuildServiceProvider();
        return new ScenarioImportExportService(scenarioService ?? new MockScenarioService(), services);
    }

    private static ScenarioExportDocument NewDocument(params TestScenario[] scenarios) =>
        new()
        {
            Group = new TestGroup
            {
                Id = Guid.Empty,
                Naziv = "Import grupa",
                Tag = global::RBBH.TestAutomation.Core.Domain.Enums.TestTag.Smoke,
                Prioritet = 1,
            },
            Scenarios = scenarios.ToList(),
        };

    private static TestScenario NewScenario(string name, string target = "/api/test") =>
        new()
        {
            Id = Guid.NewGuid(),
            Naziv = name,
            Tip = "Rest",
            Target = target,
            Act = "Get",
            Arrange = "[]",
            Assert = "[]",
            Redoslijed = 1,
        };

    private static string ToYaml(ScenarioExportDocument document) =>
        new YamlDotNet.Serialization.SerializerBuilder()
            .WithNamingConvention(YamlDotNet.Serialization.NamingConventions.CamelCaseNamingConvention.Instance)
            .ConfigureDefaultValuesHandling(YamlDotNet.Serialization.DefaultValuesHandling.OmitNull)
            .Build()
            .Serialize(document);
}
