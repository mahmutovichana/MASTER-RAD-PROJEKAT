using System.Text.Json;
using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Repositories;

namespace RBBH.TestAutomation.Api.Services.Scenarios;

/// <summary>
/// EF Core / SQL Server implementacija servisa scenarija.
/// REST i UI detalji se serializuju kao JSON u polje <c>Act</c> doменskog entiteta.
/// </summary>
public sealed class ScenarioService(IGroupRepository groups, IScenarioRepository scenarios) : IScenarioService
{
    private static readonly JsonSerializerOptions _json = new()
    {
        PropertyNameCaseInsensitive = true,
    };

    // ── Čitanje ───────────────────────────────────────────────────────────────

    public async Task<IReadOnlyList<ScenarioListItemDto>> GetAllAsync(CancellationToken ct = default)
    {
        var allGroups = await groups.GetAllAsync(ct);
        return allGroups
            .SelectMany(g => g.Scenarios.Select((s, i) => ToListItem(s, i)))
            .OrderBy(s => s.Naziv, StringComparer.OrdinalIgnoreCase)
            .ToList();
    }

    public async Task<ScenarioDto?> GetByIdAsync(Guid id, CancellationToken ct = default)
    {
        var s = await scenarios.GetByIdAsync(id, ct);
        return s is null ? null : ToDto(s);
    }

    // ── Mutacije ──────────────────────────────────────────────────────────────

    public async Task<Guid> CreateAsync(CreateScenarioRequest r, string actorId, string actorName, CancellationToken ct = default)
    {
        if (r.GroupId is null)
            throw new InvalidOperationException("Scenarij mora biti dodijeljen grupi.");

        var entity = new TestScenario
        {
            GroupId    = r.GroupId.Value,
            Naziv      = r.Naziv,
            Tip        = r.Tip.ToString(),
            Target     = r.Rest?.Url ?? r.Ui?.UrlStranice ?? r.Blazor?.ComponentName ?? "",
            Act        = SerializeDetails(r.Tip, r.Rest, r.Ui, r.Blazor),
            RunSequentially = r.RunSequentially,
            KreiranOd  = actorId,
            KreiranAt  = DateTime.UtcNow,
        };
        return await scenarios.AddAsync(entity, ct);
    }

    public async Task UpdateAsync(Guid id, UpdateScenarioRequest r, string actorId, string actorName, CancellationToken ct = default)
    {
        if (r.GroupId is null)
            throw new InvalidOperationException("Scenarij mora biti dodijeljen grupi.");

        var entity = await scenarios.GetByIdAsync(id, ct)
            ?? throw new InvalidOperationException($"Scenarij s ID {id} ne postoji.");

        entity.GroupId = r.GroupId.Value;
        entity.Naziv   = r.Naziv;
        entity.Tip     = r.Tip.ToString();
        entity.Target  = r.Rest?.Url ?? r.Ui?.UrlStranice ?? r.Blazor?.ComponentName ?? "";
        entity.Act     = SerializeDetails(r.Tip, r.Rest, r.Ui, r.Blazor);
        entity.RunSequentially = r.RunSequentially;

        await scenarios.UpdateAsync(entity, ct);
    }

    public async Task DeleteAsync(Guid id, string actorId, string actorName, CancellationToken ct = default)
    {
        try { await scenarios.DeleteAsync(id, ct); }
        catch (InvalidOperationException) { /* idempotentna operacija */ }
    }

    public async Task<ScenarioDto> CloneAsync(Guid id, string actorId, string actorName, CancellationToken ct = default)
    {
        var source = await scenarios.GetByIdAsync(id, ct)
            ?? throw new InvalidOperationException($"Scenarij s ID {id} ne postoji.");

        var kopija = new TestScenario
        {
            GroupId   = source.GroupId,
            Naziv     = $"{source.Naziv} (kopija)",
            Tip       = source.Tip,
            Target    = source.Target,
            Act       = source.Act,
            RunSequentially = source.RunSequentially,
            KreiranOd = actorId,
            KreiranAt = DateTime.UtcNow,
        };
        await scenarios.AddAsync(kopija, ct);
        return ToDto(kopija);
    }

    public Task<RunConfigDto> GetRunConfigAsync(CancellationToken ct = default)
        => Task.FromResult(new RunConfigDto(
        [
            new RunVariableDto("baseUrl", "https://api.dev.local"),
            new RunVariableDto("token",   ""),
        ]));

    // ── Mapiranje ─────────────────────────────────────────────────────────────

    private static ScenarioListItemDto ToListItem(TestScenario s, int index) =>
        new(s.Id, s.GroupId, s.Naziv, s.Tip, index)
        {
            RunSequentially = s.RunSequentially,
        };

    private static ScenarioDto ToDto(TestScenario s)
    {
        var tip = Enum.TryParse<TipScenarija>(s.Tip, ignoreCase: true, out var t) ? t : TipScenarija.Rest;
        RestScenarioDto?   rest   = null;
        UiScenarioDto?     ui     = null;
        BlazorScenarioDto? blazor = null;

        if (!string.IsNullOrWhiteSpace(s.Act))
        {
            if (tip == TipScenarija.Rest)
                rest   = JsonSerializer.Deserialize<RestScenarioDto>(s.Act, _json);
            else if (tip == TipScenarija.Ui)
                ui     = JsonSerializer.Deserialize<UiScenarioDto>(s.Act, _json);
            else if (tip == TipScenarija.Blazor)
                blazor = JsonSerializer.Deserialize<BlazorScenarioDto>(s.Act, _json);
        }

        return new ScenarioDto(
            Id:          s.Id,
            GroupId:     s.GroupId == Guid.Empty ? null : s.GroupId,
            Naziv:       s.Naziv,
            Opis:        null,
            Tip:         tip,
            Rest:        rest,
            Ui:          ui,
            Blazor:      blazor,
            KreiranOd:   s.KreiranOd,
            KreiranAt:   s.KreiranAt,
            IzmjenjenOd: null,
            IzmjenjenAt: null,
            RunSequentially: s.RunSequentially);
    }

    private static string? SerializeDetails(
        TipScenarija tip, RestScenarioDto? rest, UiScenarioDto? ui, BlazorScenarioDto? blazor = null) =>
        tip == TipScenarija.Rest   && rest   is not null ? JsonSerializer.Serialize(rest)   :
        tip == TipScenarija.Ui     && ui     is not null ? JsonSerializer.Serialize(ui)     :
        tip == TipScenarija.Blazor && blazor is not null ? JsonSerializer.Serialize(blazor) :
        null;
}
