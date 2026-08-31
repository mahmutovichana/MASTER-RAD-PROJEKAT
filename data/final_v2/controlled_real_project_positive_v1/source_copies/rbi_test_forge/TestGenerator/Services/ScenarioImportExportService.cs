using System.Text.Json;
using System.Text.Json.Serialization;
using RBBH.TestAutomation.Api.DTO;
using Microsoft.Extensions.DependencyInjection;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Domain.Enums;
using RBBH.TestAutomation.Core.Repositories;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace RBBH.TestAutomation.Api.Services;

public sealed class ScenarioImportExportService(
    IScenarioService scenarioService,
    IServiceProvider services) : IScenarioImportExportService
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        WriteIndented = true,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
        ReferenceHandler = ReferenceHandler.IgnoreCycles,
    };

    private readonly ISerializer _yamlSerializer = new SerializerBuilder()
        .WithNamingConvention(CamelCaseNamingConvention.Instance)
        .ConfigureDefaultValuesHandling(DefaultValuesHandling.OmitNull)
        .Build();

    private readonly IDeserializer _yamlDeserializer = new DeserializerBuilder()
        .WithNamingConvention(CamelCaseNamingConvention.Instance)
        .IgnoreUnmatchedProperties()
        .Build();

    public async Task<string> ExportAllScenariosToYamlAsync(CancellationToken ct = default) =>
        _yamlSerializer.Serialize(await BuildExportDocumentAsync(ct));

    public async Task<string> ExportAllScenariosToJsonAsync(CancellationToken ct = default) =>
        JsonSerializer.Serialize(await BuildExportDocumentAsync(ct), JsonOptions);

    public async Task<ScenarioImportPreview> BuildPreviewAsync(string fileName, string content, CancellationToken ct = default)
    {
        var preview = new ScenarioImportPreview { FileName = fileName };

        if (string.IsNullOrWhiteSpace(content))
        {
            preview.Errors.Add("Fajl je prazan.");
            return preview;
        }

        try
        {
            preview.Document = IsJson(fileName)
                ? JsonSerializer.Deserialize<ScenarioExportDocument>(content, JsonOptions)
                : _yamlDeserializer.Deserialize<ScenarioExportDocument>(content);
        }
        catch (Exception ex) when (ex is JsonException or YamlDotNet.Core.YamlException or InvalidOperationException)
        {
            preview.Errors.Add($"Fajl nije ispravan YAML/JSON dokument: {ex.Message}");
            return preview;
        }

        Validate(preview);
        await CalculatePreviewMetadataAsync(preview, ct);
        return preview;
    }

    public async Task<ScenarioImportResult> ImportAsync(
        IEnumerable<ScenarioImportPreview> previews,
        ScenarioImportMergeStrategy strategy,
        string actorId,
        string actorName,
        CancellationToken ct = default)
    {
        var result = new ScenarioImportResult();

        foreach (var preview in previews.Where(p => p.IsValid && p.Document is not null))
        {
            var document = preview.Document!;
            var groupId = await EnsureGroupAsync(document.Group, strategy, actorId, actorName, ct);
            if (preview.WillUpdateExisting)
                result.UpdatedGroups++;
            else
                result.ImportedGroups++;

            foreach (var scenario in document.Scenarios.OrderBy(s => s.Redoslijed))
            {
                scenario.GroupId = groupId;
                var existing = await FindExistingScenarioAsync(scenario, ct);

                if (existing is null)
                {
                    await CreateScenarioAsync(scenario, actorId, actorName, ct);
                    result.ImportedScenarios++;
                    continue;
                }

                if (strategy == ScenarioImportMergeStrategy.AddOnlyNew)
                {
                    result.SkippedScenarios++;
                    continue;
                }

                await UpdateScenarioAsync(existing.Id, scenario, actorId, actorName, ct);
                result.ImportedScenarios++;
            }

            result.Messages.Add($"{preview.FileName}: import zavrsen.");
        }

        return result;
    }

    private async Task<ScenarioExportDocument> BuildExportDocumentAsync(CancellationToken ct)
    {
        var scenarios = new List<TestScenario>();
        foreach (var item in await scenarioService.GetAllAsync(ct))
        {
            var dto = await scenarioService.GetByIdAsync(item.Id, ct);
            if (dto is not null)
                scenarios.Add(ToDomain(dto, item.Redoslijed));
        }

        return new ScenarioExportDocument
        {
            FormatVersion = "1.0",
            ExportedAt = DateTimeOffset.UtcNow,
            Group = new TestGroup
            {
                Id = Guid.Empty,
                Naziv = "Svi scenariji",
                Opis = "Export svih scenarija iz ekrana Scenariji.",
                Tag = RBBH.TestAutomation.Core.Domain.Enums.TestTag.Full,
                Prioritet = 0,
            },
            Scenarios = scenarios,
        };
    }

    private async Task<Guid> EnsureGroupAsync(
        TestGroup incoming,
        ScenarioImportMergeStrategy strategy,
        string actorId,
        string actorName,
        CancellationToken ct)
    {
        var groups = services.GetService<IGroupRepository>();
        if (groups is null || incoming.Id == Guid.Empty)
            return incoming.Id;

        var existing = await groups.GetByIdAsync(incoming.Id, ct);
        if (existing is null)
        {
            incoming.ParentGroup = null;
            incoming.ChildGroups = [];
            incoming.Scenarios = [];
            incoming.Schedules = [];
            incoming.RunResults = [];
            return await groups.AddAsync(incoming, actorId, actorName, ct);
        }

        if (strategy == ScenarioImportMergeStrategy.OverwriteExisting)
        {
            existing.Naziv = incoming.Naziv;
            existing.Opis = incoming.Opis;
            existing.Boja = incoming.Boja;
            existing.Tag = incoming.Tag;
            existing.Prioritet = incoming.Prioritet;
            existing.RunConfiguration = incoming.RunConfiguration;
            await groups.UpdateAsync(existing, actorId, actorName, ct);
        }

        return existing.Id;
    }

    private async Task<TestScenario?> FindExistingScenarioAsync(TestScenario incoming, CancellationToken ct)
    {
        if (incoming.Id != Guid.Empty)
        {
            var fromRepo = services.GetService<IScenarioRepository>();
            if (fromRepo is not null)
            {
                var scenario = await fromRepo.GetByIdAsync(incoming.Id, ct);
                if (scenario is not null)
                    return scenario;
            }

            var dto = await scenarioService.GetByIdAsync(incoming.Id, ct);
            if (dto is not null)
                return ToDomain(dto, incoming.Redoslijed);
        }

        var all = await scenarioService.GetAllAsync(ct);
        var match = all.FirstOrDefault(s =>
            string.Equals(s.Naziv, incoming.Naziv, StringComparison.OrdinalIgnoreCase)
            && (incoming.GroupId == Guid.Empty || s.GroupId == incoming.GroupId));

        if (match is null)
            return null;

        var matchedDto = await scenarioService.GetByIdAsync(match.Id, ct);
        return matchedDto is null ? null : ToDomain(matchedDto, match.Redoslijed);
    }

    private async Task CalculatePreviewMetadataAsync(ScenarioImportPreview preview, CancellationToken ct)
    {
        if (preview.Document is null)
            return;

        var group = preview.Document.Group;
        if (group.Id != Guid.Empty && services.GetService<IGroupRepository>() is { } groups)
            preview.WillUpdateExisting = await groups.GetByIdAsync(group.Id, ct) is not null;

        foreach (var scenario in preview.Document.Scenarios)
        {
            if (await FindExistingScenarioAsync(scenario, ct) is null)
                preview.NewScenarioCount++;
            else
                preview.ExistingScenarioCount++;
        }

        if (preview.ExistingScenarioCount > 0)
            preview.Warnings.Add($"{preview.ExistingScenarioCount} scenarija vec postoji.");
    }

    private static void Validate(ScenarioImportPreview preview)
    {
        var document = preview.Document;
        if (document is null)
        {
            preview.Errors.Add("Dokument nema ispravnu strukturu.");
            return;
        }

        if (string.IsNullOrWhiteSpace(document.FormatVersion))
            preview.Errors.Add("formatVersion je obavezan.");
        if (string.IsNullOrWhiteSpace(document.Group.Naziv))
            preview.Errors.Add("group.naziv je obavezan.");
        if (document.Scenarios.Count == 0)
            preview.Errors.Add("scenarios mora imati barem jedan scenarij.");

        var names = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var scenario in document.Scenarios)
        {
            if (string.IsNullOrWhiteSpace(scenario.Naziv))
                preview.Errors.Add("scenario.naziv je obavezan.");
            else if (!names.Add(scenario.Naziv))
                preview.Errors.Add($"scenario '{scenario.Naziv}': naziv je dupliran u fajlu.");
            if (string.IsNullOrWhiteSpace(scenario.Tip))
                preview.Errors.Add($"scenario '{scenario.Naziv}': tip je obavezan.");
            if (string.IsNullOrWhiteSpace(scenario.Target))
                preview.Errors.Add($"scenario '{scenario.Naziv}': target je obavezan.");
            if (scenario.Redoslijed < 0)
                preview.Errors.Add($"scenario '{scenario.Naziv}': redoslijed ne moze biti negativan.");
        }
    }

    private async Task CreateScenarioAsync(TestScenario scenario, string actorId, string actorName, CancellationToken ct) =>
        await scenarioService.CreateAsync(ToCreateRequest(scenario), actorId, actorName, ct);

    private async Task UpdateScenarioAsync(Guid id, TestScenario scenario, string actorId, string actorName, CancellationToken ct) =>
        await scenarioService.UpdateAsync(id, ToUpdateRequest(scenario), actorId, actorName, ct);

    private static TestScenario ToDomain(ScenarioDto dto, int order) =>
        new()
        {
            Id = dto.Id,
            GroupId = dto.GroupId ?? Guid.Empty,
            Naziv = dto.Naziv,
            Tip = dto.Tip == TipScenarija.Ui ? "Ui" : "Rest",
            Target = dto.Tip == TipScenarija.Ui ? dto.Ui?.UrlStranice ?? "" : dto.Rest?.Url ?? "",
            Arrange = dto.Tip == TipScenarija.Ui ? JsonSerializer.Serialize(dto.Ui, JsonOptions) : JsonSerializer.Serialize(dto.Rest?.Headeri ?? [], JsonOptions),
            Act = dto.Tip == TipScenarija.Ui ? JsonSerializer.Serialize(dto.Ui?.Koraci ?? [], JsonOptions) : dto.Rest?.Metoda.ToString(),
            Assert = dto.Tip == TipScenarija.Ui ? null : JsonSerializer.Serialize(dto.Rest?.ResponseAsserti ?? [], JsonOptions),
            Redoslijed = order,
            KreiranOd = dto.KreiranOd,
            KreiranAt = dto.KreiranAt,
        };

    private static CreateScenarioRequest ToCreateRequest(TestScenario scenario)
    {
        var tip = ParseTip(scenario.Tip);
        return new CreateScenarioRequest(
            scenario.GroupId == Guid.Empty ? null : scenario.GroupId,
            scenario.Naziv,
            null,
            tip,
            tip == TipScenarija.Rest ? ToRest(scenario) : null,
            tip == TipScenarija.Ui ? ToUi(scenario) : null);
    }

    private static UpdateScenarioRequest ToUpdateRequest(TestScenario scenario)
    {
        var request = ToCreateRequest(scenario);
        return new UpdateScenarioRequest(request.GroupId, request.Naziv, request.Opis, request.Tip, request.Rest, request.Ui);
    }

    private static TipScenarija ParseTip(string tip) =>
        tip.Equals("Ui", StringComparison.OrdinalIgnoreCase) ? TipScenarija.Ui : TipScenarija.Rest;

    private static RestScenarioDto ToRest(TestScenario scenario) =>
        new(
            Enum.TryParse<HttpMetoda>(scenario.Act, true, out var metoda) ? metoda : HttpMetoda.Get,
            scenario.Target,
            TryDeserialize<IReadOnlyList<HeaderDto>>(scenario.Arrange) ?? [],
            null,
            200,
            TryDeserialize<IReadOnlyList<ResponseAssertDto>>(scenario.Assert) ?? []);

    private static UiScenarioDto ToUi(TestScenario scenario) =>
        TryDeserialize<UiScenarioDto>(scenario.Arrange)
        ?? new UiScenarioDto(scenario.Target, TryDeserialize<IReadOnlyList<UiKorakDto>>(scenario.Act) ?? []);

    private static T? TryDeserialize<T>(string? json)
    {
        if (string.IsNullOrWhiteSpace(json))
            return default;

        try { return JsonSerializer.Deserialize<T>(json, JsonOptions); }
        catch (JsonException) { return default; }
    }

    private static bool IsJson(string fileName) =>
        fileName.EndsWith(".json", StringComparison.OrdinalIgnoreCase);
}
