using System.Text.Json;
using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Core.Repositories;
using RBBH.TestAutomation.Core.Domain;

namespace RBBH.TestAutomation.Api.Services;

/// <summary>
/// EF Core implementacija <see cref="IGroupService"/> — koristi repozitorije iz RBBH.TestAutomation.Core.
/// Aktivan kad je <c>MockGroups:Enabled=false</c> (produkcija).
/// </summary>
public class GroupService(IGroupRepository groups, IScenarioRepository scenarios, ITestForgeAuditWriter audit) : IGroupService
{
    public async Task<IReadOnlyList<GroupTreeNodeDto>> GetGroupsTreeAsync(CancellationToken ct = default)
    {
        var all = await groups.GetAllAsync(ct);
        var roots = all.Where(g => g.ParentGroupId == null).ToList();
        var result = new List<GroupTreeNodeDto>();
        foreach (var root in roots)
        {
            var summary = await groups.GetSummaryAsync(root.Id, ct);
            var children = new List<GroupTreeNodeDto>();
            foreach (var child in root.ChildGroups)
            {
                var cs = await groups.GetSummaryAsync(child.Id, ct);
                children.Add(new GroupTreeNodeDto(ToDto(child), ToSummaryDto(cs), []));
            }
            result.Add(new GroupTreeNodeDto(ToDto(root), ToSummaryDto(summary), children));
        }
        return result;
    }

    public async Task<GroupDto?> GetByIdAsync(Guid id, CancellationToken ct = default)
    {
        var g = await groups.GetByIdAsync(id, ct);
        return g is null ? null : ToDto(g);
    }

    public async Task<IReadOnlyList<GroupDto>> GetRootGroupsAsync(CancellationToken ct = default)
    {
        var roots = await groups.GetRootGroupsAsync(ct);
        return roots.Select(ToDto).ToList();
    }

    public async Task<Guid> CreateAsync(CreateGroupRequest r, string actorId, string actorName, CancellationToken ct = default)
    {
        var g = new TestGroup
        {
            Naziv = r.Naziv, Opis = r.Opis, Boja = r.Boja,
            Tag = MapTag(r.Tag), Prioritet = r.Prioritet, ParentGroupId = r.ParentGroupId,
        };
        return await groups.AddAsync(g, actorId, actorName, ct);
    }

    public async Task UpdateAsync(Guid id, UpdateGroupRequest r, string actorId, string actorName, CancellationToken ct = default)
    {
        var g = await groups.GetByIdAsync(id, ct)
            ?? throw new InvalidOperationException($"Grupa {id} ne postoji.");
        g.Naziv = r.Naziv; g.Opis = r.Opis; g.Boja = r.Boja;
        g.Tag = MapTag(r.Tag); g.Prioritet = r.Prioritet;
        await groups.UpdateAsync(g, actorId, actorName, ct);
    }

    public Task DeleteAsync(Guid id, string actorId, string actorName, CancellationToken ct = default) =>
        groups.DeleteAsync(id, actorId, actorName, ct);

    public async Task<IReadOnlyList<ScenarioListItemDto>> GetScenariosAsync(Guid groupId, CancellationToken ct = default)
    {
        var list = await scenarios.GetByGroupAsync(groupId, ct);
        return list.Select(ToListItem).ToList();
    }

    public Task ReorderScenariosAsync(Guid groupId, IReadOnlyList<Guid> orderedIds, CancellationToken ct = default) =>
        groups.ReorderScenariosAsync(groupId, orderedIds, ct);

    public async Task<ScenarioListItemDto> CopyScenarioAsync(Guid scenarioId, Guid targetGroupId, string actorId, string actorName, CancellationToken ct = default)
    {
        var copy = await scenarios.CloneAsync(scenarioId, targetGroupId, ct);
        await audit.WriteAsync(TestForgeAuditEntities.Scenario, copy.Id, TestForgeAuditActions.Create,
            actorId, actorName, oldValues: null,
            newValues: new { copy.Id, copy.GroupId, copy.Naziv, copy.Tip, copy.Redoslijed, ClonedFrom = scenarioId }, ct);
        return ToListItem(copy);
    }

    public Task SetScheduleActiveAsync(Guid groupId, bool isActive, CancellationToken ct = default) =>
        groups.SetScheduleActiveAsync(groupId, isActive, ct);

    private static readonly JsonSerializerOptions JsonOpts = new(JsonSerializerDefaults.Web);

    public async Task<NotificationConfig?> GetNotificationConfigAsync(Guid groupId, CancellationToken ct = default)
    {
        var g = await groups.GetByIdAsync(groupId, ct);
        if (g?.NotificationConfigJson is null) return null;
        try { return JsonSerializer.Deserialize<NotificationConfig>(g.NotificationConfigJson, JsonOpts); }
        catch { return null; }
    }

    public async Task SaveNotificationConfigAsync(Guid groupId, NotificationConfig config, CancellationToken ct = default)
    {
        var g = await groups.GetByIdAsync(groupId, ct)
            ?? throw new InvalidOperationException($"Grupa {groupId} ne postoji.");
        g.NotificationConfigJson = JsonSerializer.Serialize(config, JsonOpts);
        await groups.UpdateAsync(g, g.IzmjenjenOd ?? "", "", ct);
    }

    private static GroupDto ToDto(TestGroup g) => new(
        g.Id, g.Naziv, g.Opis, g.Boja, MapTagDto(g.Tag), g.Prioritet,
        g.ParentGroupId, g.KreiranOd, g.KreiranAt, g.IzmjenjenOd, g.IzmjenjenAt);

    private static GroupSummaryDto ToSummaryDto(RBBH.TestAutomation.Core.Repositories.GroupSummary s) =>
        new(s.ScenarioCount, s.LastRunAt, s.LastPassRate, s.ActiveScheduleCount);

    private static ScenarioListItemDto ToListItem(TestScenario s) =>
        new(s.Id, s.GroupId, s.Naziv, s.Tip, s.Redoslijed)
        {
            RunSequentially = s.RunSequentially,
        };

    private static RBBH.TestAutomation.Core.Domain.Enums.TestTag MapTag(RBBH.TestAutomation.Api.DTO.TestTag t) => t switch
    {
        RBBH.TestAutomation.Api.DTO.TestTag.Smoke => RBBH.TestAutomation.Core.Domain.Enums.TestTag.Smoke,
        RBBH.TestAutomation.Api.DTO.TestTag.Regression => RBBH.TestAutomation.Core.Domain.Enums.TestTag.Regression,
        RBBH.TestAutomation.Api.DTO.TestTag.Full => RBBH.TestAutomation.Core.Domain.Enums.TestTag.Full,
        _ => RBBH.TestAutomation.Core.Domain.Enums.TestTag.Smoke,
    };

    private static RBBH.TestAutomation.Api.DTO.TestTag MapTagDto(RBBH.TestAutomation.Core.Domain.Enums.TestTag t) => t switch
    {
        RBBH.TestAutomation.Core.Domain.Enums.TestTag.Smoke => RBBH.TestAutomation.Api.DTO.TestTag.Smoke,
        RBBH.TestAutomation.Core.Domain.Enums.TestTag.Regression => RBBH.TestAutomation.Api.DTO.TestTag.Regression,
        RBBH.TestAutomation.Core.Domain.Enums.TestTag.Full => RBBH.TestAutomation.Api.DTO.TestTag.Full,
        _ => RBBH.TestAutomation.Api.DTO.TestTag.Smoke,
    };
}
