using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Api.Services.Groups;

namespace UnitTests.Grupe;

/// <summary>
/// Unit testovi za <see cref="GroupTreeBuilder.Build"/> — čista izgradnja stabla (dubina, sort, siročad).
/// </summary>
public class GroupTreeBuilderTests
{
    private static GroupDto G(Guid id, string naziv, int prioritet, Guid? parent = null) =>
        new(id, naziv, null, null, TestTag.Smoke, prioritet, parent, null, DateTime.UtcNow, null, null);

    private static readonly Dictionary<Guid, GroupSummaryDto> NoSummaries = new();

    [Fact]
    public void Build_WhenEmpty_ReturnsEmpty()
    {
        var result = GroupTreeBuilder.Build([], NoSummaries);
        Assert.Empty(result);
    }

    [Fact]
    public void Build_WhenFlatRoots_SortsByPrioritetDescThenNaziv()
    {
        var a = G(Guid.NewGuid(), "Alfa", 10);
        var b = G(Guid.NewGuid(), "Beta", 50);
        var c = G(Guid.NewGuid(), "Gama", 50);

        var result = GroupTreeBuilder.Build([a, b, c], NoSummaries);

        // Prioritet desc (50 prije 10), pa Naziv asc (Beta prije Gama).
        Assert.Equal(["Beta", "Gama", "Alfa"], result.Select(n => n.Group.Naziv).ToList());
    }

    [Fact]
    public void Build_WhenChildHasParent_NestsUnderParent()
    {
        var parentId = Guid.NewGuid();
        var parent = G(parentId, "Root", 50);
        var child = G(Guid.NewGuid(), "Child", 50, parentId);

        var result = GroupTreeBuilder.Build([parent, child], NoSummaries);

        var root = Assert.Single(result);
        Assert.Equal("Root", root.Group.Naziv);
        var nested = Assert.Single(root.Children);
        Assert.Equal("Child", nested.Group.Naziv);
    }

    [Fact]
    public void Build_WhenOrphan_TreatedAsRoot()
    {
        // Parent ID koji ne postoji u listi → siroče se prikazuje kao root (ne nestaje).
        var orphan = G(Guid.NewGuid(), "Siroče", 50, Guid.NewGuid());

        var result = GroupTreeBuilder.Build([orphan], NoSummaries);

        var root = Assert.Single(result);
        Assert.Equal("Siroče", root.Group.Naziv);
        Assert.Empty(root.Children);
    }

    [Fact]
    public void Build_WhenSummaryMissing_UsesEmptySummary()
    {
        var g = G(Guid.NewGuid(), "Bez sažetka", 50);

        var result = GroupTreeBuilder.Build([g], NoSummaries);

        var node = Assert.Single(result);
        Assert.Equal(0, node.Summary.ScenarioCount);
        Assert.Null(node.Summary.LastRunAt);
        Assert.Null(node.Summary.LastPassRate);
        Assert.Equal(0, node.Summary.ActiveScheduleCount);
    }

    [Fact]
    public void Build_WhenSummaryProvided_AttachesToNode()
    {
        var id = Guid.NewGuid();
        var g = G(id, "Sa sažetkom", 50);
        var summaries = new Dictionary<Guid, GroupSummaryDto>
        {
            [id] = new(ScenarioCount: 5, LastRunAt: DateTime.UtcNow, LastPassRate: 88.0, ActiveScheduleCount: 2),
        };

        var result = GroupTreeBuilder.Build([g], summaries);

        Assert.Equal(5, result[0].Summary.ScenarioCount);
        Assert.Equal(88.0, result[0].Summary.LastPassRate);
    }

    [Fact]
    public void Build_WhenTwoNodeCycle_KeepsBothVisibleWithoutHanging()
    {
        // A→B→A: nijedna nije klasičan root. Ranije su OBJE tiho nestajale iz prikaza.
        // Sada moraju ostati vidljive, i izgradnja ne smije ući u beskonačnu petlju.
        var aId = Guid.NewGuid();
        var bId = Guid.NewGuid();
        var a = G(aId, "A", 50, bId);
        var b = G(bId, "B", 50, aId);

        var result = GroupTreeBuilder.Build([a, b], NoSummaries);

        // Svaka grupa se pojavljuje tačno jednom u cijelom stablu (kao root ili dijete).
        var allNazivi = Flatten(result).Select(n => n.Group.Naziv).OrderBy(x => x).ToList();
        Assert.Equal(["A", "B"], allNazivi);
    }

    [Fact]
    public void Build_WhenSelfReference_AppearsOnceWithoutHanging()
    {
        // A→A: samo-referenca. Mora se pojaviti tačno jednom, bez beskonačne rekurzije.
        var id = Guid.NewGuid();
        var self = G(id, "Self", 50, id);

        var result = GroupTreeBuilder.Build([self], NoSummaries);

        var all = Flatten(result).ToList();
        Assert.Single(all);
        Assert.Equal("Self", all[0].Group.Naziv);
    }

    [Fact]
    public void Build_WhenValidChildAndCycleMixed_KeepsValidTreeAndSurfacesCycle()
    {
        // Validan root+dijete plus zaseban ciklus — validno stablo ostaje ispravno,
        // a grupe iz ciklusa se ipak prikažu (ne nestaju).
        var rootId = Guid.NewGuid();
        var childId = Guid.NewGuid();
        var root = G(rootId, "Root", 50);
        var child = G(childId, "Child", 50, rootId);

        var cxId = Guid.NewGuid();
        var cyId = Guid.NewGuid();
        var cx = G(cxId, "CycleX", 10, cyId);
        var cy = G(cyId, "CycleY", 10, cxId);

        var result = GroupTreeBuilder.Build([root, child, cx, cy], NoSummaries);

        var all = Flatten(result).Select(n => n.Group.Naziv).OrderBy(x => x).ToList();
        Assert.Equal(["Child", "CycleX", "CycleY", "Root"], all);

        // Validno gniježđenje Root→Child je očuvano.
        var rootNode = result.Single(n => n.Group.Naziv == "Root");
        Assert.Equal("Child", Assert.Single(rootNode.Children).Group.Naziv);
    }

    private static IEnumerable<GroupTreeNodeDto> Flatten(IEnumerable<GroupTreeNodeDto> nodes)
    {
        foreach (var n in nodes)
        {
            yield return n;
            foreach (var c in Flatten(n.Children))
                yield return c;
        }
    }
}
