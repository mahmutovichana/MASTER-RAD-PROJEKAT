using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Api.Services;

namespace UnitTests.Grupe;

/// <summary>
/// Unit testovi za <see cref="MockGroupService"/>.
///
/// Pokriva data-sloj acceptance kriterija US #5:
///   AC2 — reorder scenarija (ReorderScenariosAsync)
///   AC3 — kopiranje scenarija u drugu grupu (CopyScenarioAsync)
///   AC4 — hijerarhija ≤2 nivoa (depth guard u CreateAsync, blokada brisanja grupe s podgrupama)
///   AC5 — summary kartica (count, zadnji run, pass rate, null-state)
///   AC6 — pauziranje rasporeda (SetScheduleActiveAsync)
///
/// Svaki test kreira svoju instancu servisa → potpuna izolacija stanja.
/// </summary>
public class MockGroupServiceTests
{
    private const string ActorId   = "test-actor-001";
    private const string ActorName = "Test Korisnik";

    private static MockGroupService CreateSvc() => new();

    // ── Helpers za navigaciju kroz stablo ─────────────────────────────────────

    private static IEnumerable<GroupTreeNodeDto> Flatten(IEnumerable<GroupTreeNodeDto> nodes)
    {
        foreach (var n in nodes)
        {
            yield return n;
            foreach (var c in Flatten(n.Children))
                yield return c;
        }
    }

    private static async Task<GroupTreeNodeDto> NodeByNazivAsync(MockGroupService svc, string naziv)
    {
        var tree = await svc.GetGroupsTreeAsync();
        return Flatten(tree).First(n => n.Group.Naziv == naziv);
    }

    private static async Task<Guid> IdByNazivAsync(MockGroupService svc, string naziv)
        => (await NodeByNazivAsync(svc, naziv)).Group.Id;

    // ═══════════════════════════════════════════════════════════════════════════
    // GetGroupsTreeAsync — seed, nesting, summary  [AC4, AC5]
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetGroupsTreeAsync_WhenSeeded_ReturnsThreeRootsWithOneChild()
    {
        var svc = CreateSvc();
        var tree = await svc.GetGroupsTreeAsync();

        Assert.Equal(3, tree.Count);
        var totalChildren = tree.Sum(n => n.Children.Count);
        Assert.Equal(1, totalChildren);
    }

    [Fact]
    public async Task GetGroupsTreeAsync_WhenSeeded_RootsSortedByPrioritetDesc()
    {
        var svc = CreateSvc();
        var tree = await svc.GetGroupsTreeAsync();

        // Smoke (100) → Regression (50) → Full Suite (10)
        Assert.Equal(["Smoke", "Regression", "Full Suite"], tree.Select(n => n.Group.Naziv).ToList());
    }

    [Fact]
    public async Task GetGroupsTreeAsync_WhenSeeded_ChildNestsUnderRegression()
    {
        var svc = CreateSvc();
        var tree = await svc.GetGroupsTreeAsync();

        var regression = tree.First(n => n.Group.Naziv == "Regression");
        var child = Assert.Single(regression.Children);
        Assert.Equal("Regresija - API", child.Group.Naziv);
        Assert.Equal(regression.Group.Id, child.Group.ParentGroupId);
    }

    [Fact]
    public async Task GetGroupsTreeAsync_SummaryCountsMatchSeed()
    {
        var svc = CreateSvc();

        Assert.Equal(2, (await NodeByNazivAsync(svc, "Smoke")).Summary.ScenarioCount);
        Assert.Equal(3, (await NodeByNazivAsync(svc, "Regression")).Summary.ScenarioCount);
        Assert.Equal(2, (await NodeByNazivAsync(svc, "Regresija - API")).Summary.ScenarioCount);
        Assert.Equal(1, (await NodeByNazivAsync(svc, "Full Suite")).Summary.ScenarioCount);
    }

    [Fact]
    public async Task GetGroupsTreeAsync_SummaryPassRateMatchesLastRun()
    {
        var svc = CreateSvc();
        Assert.Equal(92.0, (await NodeByNazivAsync(svc, "Smoke")).Summary.LastPassRate);
        Assert.Equal(68.0, (await NodeByNazivAsync(svc, "Regression")).Summary.LastPassRate);
    }

    [Fact]
    public async Task GetGroupsTreeAsync_WhenGroupNeverRun_SummaryLastRunIsNull()
    {
        // AC5 null-state — Full Suite nema run.
        var svc = CreateSvc();
        var full = await NodeByNazivAsync(svc, "Full Suite");

        Assert.Null(full.Summary.LastRunAt);
        Assert.Null(full.Summary.LastPassRate);
    }

    [Fact]
    public async Task GetGroupsTreeAsync_ActiveScheduleCount_OnlyCountsActive()
    {
        var svc = CreateSvc();
        // Smoke ima aktivan raspored; Full Suite ima neaktivan.
        Assert.Equal(1, (await NodeByNazivAsync(svc, "Smoke")).Summary.ActiveScheduleCount);
        Assert.Equal(0, (await NodeByNazivAsync(svc, "Full Suite")).Summary.ActiveScheduleCount);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // GetRootGroupsAsync
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetRootGroupsAsync_ReturnsOnlyRoots()
    {
        var svc = CreateSvc();
        var roots = await svc.GetRootGroupsAsync();

        Assert.Equal(3, roots.Count);
        Assert.All(roots, g => Assert.Null(g.ParentGroupId));
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // CreateAsync — depth guard  [AC4]
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task CreateAsync_WhenParentIsRoot_AddsChild()
    {
        var svc = CreateSvc();
        var smokeId = await IdByNazivAsync(svc, "Smoke");

        var id = await svc.CreateAsync(
            new CreateGroupRequest("Smoke - Mobile", null, null, TestTag.Smoke, 10, smokeId),
            ActorId, ActorName);

        Assert.NotEqual(Guid.Empty, id);
        var created = await svc.GetByIdAsync(id);
        Assert.NotNull(created);
        Assert.Equal(smokeId, created.ParentGroupId);
    }

    [Fact]
    public async Task CreateAsync_WhenParentAlreadyChild_ThrowsInvalidOperation()
    {
        // Depth guard — "Regresija - API" je već child; podgrupa pod njom bi bila 3. nivo.
        var svc = CreateSvc();
        var childId = await IdByNazivAsync(svc, "Regresija - API");

        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            svc.CreateAsync(
                new CreateGroupRequest("3. nivo", null, null, TestTag.Regression, 10, childId),
                ActorId, ActorName));
    }

    [Fact]
    public async Task CreateAsync_WhenParentDoesNotExist_ThrowsInvalidOperation()
    {
        var svc = CreateSvc();
        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            svc.CreateAsync(
                new CreateGroupRequest("Sirota", null, null, TestTag.Smoke, 10, Guid.NewGuid()),
                ActorId, ActorName));
    }

    [Fact]
    public async Task CreateAsync_WhenRootGroup_SetsKreiranOdAndKreiranAt()
    {
        var svc = CreateSvc();
        var before = DateTime.UtcNow;

        var id = await svc.CreateAsync(
            new CreateGroupRequest("Nova root", null, "#000000", TestTag.Full, 5, null),
            ActorId, ActorName);

        var created = await svc.GetByIdAsync(id);
        Assert.NotNull(created);
        Assert.Equal(ActorId, created.KreiranOd);
        Assert.True(created.KreiranAt >= before);
        Assert.Null(created.IzmjenjenOd);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // UpdateAsync
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task UpdateAsync_WhenValid_ChangesFieldsAndSetsIzmjenjen()
    {
        var svc = CreateSvc();
        var smokeId = await IdByNazivAsync(svc, "Smoke");
        var before = DateTime.UtcNow;

        await svc.UpdateAsync(smokeId,
            new UpdateGroupRequest("Smoke v2", "novi opis", "#111111", TestTag.Smoke, 200),
            ActorId, ActorName);

        var updated = await svc.GetByIdAsync(smokeId);
        Assert.NotNull(updated);
        Assert.Equal("Smoke v2", updated.Naziv);
        Assert.Equal(200, updated.Prioritet);
        Assert.Equal(ActorId, updated.IzmjenjenOd);
        Assert.NotNull(updated.IzmjenjenAt);
        Assert.True(updated.IzmjenjenAt >= before);
    }

    [Fact]
    public async Task UpdateAsync_WhenGroupDoesNotExist_ThrowsInvalidOperation()
    {
        var svc = CreateSvc();
        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            svc.UpdateAsync(Guid.NewGuid(),
                new UpdateGroupRequest("X", null, null, TestTag.Smoke, 0),
                ActorId, ActorName));
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // DeleteAsync — block-on-children + cascade  [AC4]
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task DeleteAsync_WhenGroupHasChildren_ThrowsInvalidOperation()
    {
        var svc = CreateSvc();
        var regressionId = await IdByNazivAsync(svc, "Regression");

        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            svc.DeleteAsync(regressionId, ActorId, ActorName));
    }

    [Fact]
    public async Task DeleteAsync_WhenLeafGroup_RemovesGroupAndScenarios()
    {
        var svc = CreateSvc();
        var smokeId = await IdByNazivAsync(svc, "Smoke");

        await svc.DeleteAsync(smokeId, ActorId, ActorName);

        Assert.Null(await svc.GetByIdAsync(smokeId));
        Assert.Empty(await svc.GetScenariosAsync(smokeId));
    }

    [Fact]
    public async Task DeleteAsync_WhenGroupDoesNotExist_ThrowsInvalidOperation()
    {
        var svc = CreateSvc();
        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            svc.DeleteAsync(Guid.NewGuid(), ActorId, ActorName));
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // ReorderScenariosAsync  [AC2]
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task ReorderScenariosAsync_WhenGivenOrder_PersistsOrder()
    {
        var svc = CreateSvc();
        var smokeId = await IdByNazivAsync(svc, "Smoke");
        var scenariji = await svc.GetScenariosAsync(smokeId);
        var reversed = scenariji.Select(s => s.Id).Reverse().ToList();

        await svc.ReorderScenariosAsync(smokeId, reversed);

        var after = await svc.GetScenariosAsync(smokeId);
        Assert.Equal(reversed, after.Select(s => s.Id).ToList());
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // CopyScenarioAsync  [AC3]
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task CopyScenarioAsync_WhenCalled_CreatesNewIdInTargetGroupWithMaxOrderPlusOne()
    {
        var svc = CreateSvc();
        var smokeId = await IdByNazivAsync(svc, "Smoke");
        var fullId  = await IdByNazivAsync(svc, "Full Suite"); // ima 1 scenarij (Redoslijed 0)
        var source  = (await svc.GetScenariosAsync(smokeId)).First();

        var copy = await svc.CopyScenarioAsync(source.Id, fullId, ActorId, ActorName);

        Assert.NotEqual(source.Id, copy.Id);
        Assert.Equal(fullId, copy.GroupId);
        Assert.EndsWith("(kopija)", copy.Naziv);
        Assert.Equal(1, copy.Redoslijed); // max(0) + 1
    }

    [Fact]
    public async Task CopyScenarioAsync_WhenCalled_LeavesSourceGroupUnchanged()
    {
        var svc = CreateSvc();
        var smokeId = await IdByNazivAsync(svc, "Smoke");
        var fullId  = await IdByNazivAsync(svc, "Full Suite");
        var sourceCountBefore = (await svc.GetScenariosAsync(smokeId)).Count;
        var source = (await svc.GetScenariosAsync(smokeId)).First();

        await svc.CopyScenarioAsync(source.Id, fullId, ActorId, ActorName);

        Assert.Equal(sourceCountBefore, (await svc.GetScenariosAsync(smokeId)).Count);
        Assert.Equal(2, (await svc.GetScenariosAsync(fullId)).Count); // 1 seed + 1 kopija
    }

    [Fact]
    public async Task CopyScenarioAsync_WhenTargetAlreadyHasScenario_ThrowsInvalidOperation()
    {
        var svc = CreateSvc();
        var smokeId = await IdByNazivAsync(svc, "Smoke");
        var fullId  = await IdByNazivAsync(svc, "Full Suite");
        var source = (await svc.GetScenariosAsync(smokeId)).First();

        await svc.CopyScenarioAsync(source.Id, fullId, ActorId, ActorName);

        var ex = await Assert.ThrowsAsync<InvalidOperationException>(() =>
            svc.CopyScenarioAsync(source.Id, fullId, ActorId, ActorName));
        Assert.Equal("Scenarij je vec dodijeljen odabranoj grupi.", ex.Message);
    }

    [Fact]
    public async Task CopyScenarioAsync_WhenTargetIsSourceGroup_ThrowsInvalidOperation()
    {
        var svc = CreateSvc();
        var smokeId = await IdByNazivAsync(svc, "Smoke");
        var source = (await svc.GetScenariosAsync(smokeId)).First();

        var ex = await Assert.ThrowsAsync<InvalidOperationException>(() =>
            svc.CopyScenarioAsync(source.Id, smokeId, ActorId, ActorName));
        Assert.Equal("Scenarij je vec dodijeljen odabranoj grupi.", ex.Message);
    }

    [Fact]
    public async Task CopyScenarioAsync_WhenSourceMissing_ThrowsInvalidOperation()
    {
        var svc = CreateSvc();
        var fullId = await IdByNazivAsync(svc, "Full Suite");

        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            svc.CopyScenarioAsync(Guid.NewGuid(), fullId, ActorId, ActorName));
    }

    [Fact]
    public async Task CopyScenarioAsync_WhenTargetGroupMissing_ThrowsInvalidOperation()
    {
        var svc = CreateSvc();
        var smokeId = await IdByNazivAsync(svc, "Smoke");
        var source = (await svc.GetScenariosAsync(smokeId)).First();

        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            svc.CopyScenarioAsync(source.Id, Guid.NewGuid(), ActorId, ActorName));
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // SetScheduleActiveAsync  [AC6 pause stub]
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task SetScheduleActiveAsync_WhenPaused_SetsInactive()
    {
        var svc = CreateSvc();
        var smokeId = await IdByNazivAsync(svc, "Smoke");

        await svc.SetScheduleActiveAsync(smokeId, false);

        // Aktivni raspored Smoke-a sada je pauziran → ActiveScheduleCount pada na 0.
        Assert.Equal(0, (await NodeByNazivAsync(svc, "Smoke")).Summary.ActiveScheduleCount);
    }
}
