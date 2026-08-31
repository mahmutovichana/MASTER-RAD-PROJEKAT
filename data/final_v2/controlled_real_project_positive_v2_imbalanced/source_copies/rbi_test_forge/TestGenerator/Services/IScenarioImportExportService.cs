using RBBH.TestAutomation.Api.DTO;

namespace RBBH.TestAutomation.Api.Services;

public interface IScenarioImportExportService
{
    Task<string> ExportAllScenariosToYamlAsync(CancellationToken ct = default);

    Task<string> ExportAllScenariosToJsonAsync(CancellationToken ct = default);

    Task<ScenarioImportPreview> BuildPreviewAsync(string fileName, string content, CancellationToken ct = default);

    Task<ScenarioImportResult> ImportAsync(
        IEnumerable<ScenarioImportPreview> previews,
        ScenarioImportMergeStrategy strategy,
        string actorId,
        string actorName,
        CancellationToken ct = default);
}
