using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Domain.Enums;
using RBBH.TestAutomation.Core.Infrastructure;
using RBBH.TestAutomation.Core.Repositories;

namespace UnitTests.TestForge;

public class GroupRepositoryTests
{
    private static TestGroup MakeGroup(string naziv, Guid? parentId = null) =>
        new() { Id = Guid.NewGuid(), Naziv = naziv, Tag = TestTag.Smoke, ParentGroupId = parentId };

    [Fact]
    public async Task AddAsync_RootGroup_Succeeds()
    {
        await using var db = TestForgeFixture.CreateInMemory();
        var repo = new GroupRepository(db);
        var g = MakeGroup("Root");
        var id = await repo.AddAsync(g, "user1", "User One");
        Assert.NotEqual(Guid.Empty, id);
        Assert.Single(db.Groups);
    }

    [Fact]
    public async Task AddAsync_ChildGroup_Succeeds()
    {
        await using var db = TestForgeFixture.CreateInMemory();
        var repo = new GroupRepository(db);
        var root = MakeGroup("Root");
        await repo.AddAsync(root, "u", "U");
        var child = MakeGroup("Child", root.Id);
        var id = await repo.AddAsync(child, "u", "U");
        Assert.NotEqual(Guid.Empty, id);
    }

    [Fact]
    public async Task AddAsync_ThirdLevel_Throws()
    {
        await using var db = TestForgeFixture.CreateInMemory();
        var repo = new GroupRepository(db);
        var root = MakeGroup("Root");
        await repo.AddAsync(root, "u", "U");
        var child = MakeGroup("Child", root.Id);
        await repo.AddAsync(child, "u", "U");
        var grandchild = MakeGroup("Grandchild", child.Id);
        await Assert.ThrowsAsync<InvalidOperationException>(() => repo.AddAsync(grandchild, "u", "U"));
    }

    [Fact]
    public async Task DeleteAsync_GroupWithChildren_Throws()
    {
        await using var db = TestForgeFixture.CreateInMemory();
        var repo = new GroupRepository(db);
        var root = MakeGroup("Root");
        await repo.AddAsync(root, "u", "U");
        var child = MakeGroup("Child", root.Id);
        await repo.AddAsync(child, "u", "U");
        await Assert.ThrowsAsync<InvalidOperationException>(() => repo.DeleteAsync(root.Id, "u", "U"));
    }

    [Fact]
    public async Task ReorderScenariosAsync_ChangesOrder()
    {
        await using var db = TestForgeFixture.CreateInMemory();
        var repo = new GroupRepository(db);
        var g = MakeGroup("G");
        await repo.AddAsync(g, "u", "U");
        var s1 = new TestScenario { Id = Guid.NewGuid(), GroupId = g.Id, Naziv = "S1", Redoslijed = 0 };
        var s2 = new TestScenario { Id = Guid.NewGuid(), GroupId = g.Id, Naziv = "S2", Redoslijed = 1 };
        db.Scenarios.AddRange(s1, s2);
        await db.SaveChangesAsync();
        await repo.ReorderScenariosAsync(g.Id, [s2.Id, s1.Id]);
        Assert.Equal(0, db.Scenarios.First(s => s.Id == s2.Id).Redoslijed);
        Assert.Equal(1, db.Scenarios.First(s => s.Id == s1.Id).Redoslijed);
    }

    [Fact]
    public async Task GetSummaryAsync_ReturnsCorrectCounts()
    {
        await using var db = TestForgeFixture.CreateInMemory();
        var repo = new GroupRepository(db);
        var g = MakeGroup("G");
        await repo.AddAsync(g, "u", "U");
        db.Scenarios.Add(new TestScenario { Id = Guid.NewGuid(), GroupId = g.Id, Naziv = "S" });
        db.Schedules.Add(new ScheduleConfig { Id = Guid.NewGuid(), GroupId = g.Id, IsActive = true });
        await db.SaveChangesAsync();
        var summary = await repo.GetSummaryAsync(g.Id);
        Assert.Equal(1, summary.ScenarioCount);
        Assert.Equal(1, summary.ActiveScheduleCount);
        Assert.Null(summary.LastRunAt);
    }
}
