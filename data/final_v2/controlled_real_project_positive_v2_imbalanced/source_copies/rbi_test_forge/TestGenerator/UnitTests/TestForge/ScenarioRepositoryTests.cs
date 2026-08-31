using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Domain.Enums;
using RBBH.TestAutomation.Core.Infrastructure;
using RBBH.TestAutomation.Core.Repositories;

namespace UnitTests.TestForge;

public class ScenarioRepositoryTests
{
    private static async Task<(TestForgeDbContext db, Guid groupId)> SetupAsync()
    {
        var db = TestForgeFixture.CreateInMemory();
        var group = new TestGroup { Id = Guid.NewGuid(), Naziv = "G", Tag = TestTag.Smoke };
        db.Groups.Add(group);
        await db.SaveChangesAsync();
        return (db, group.Id);
    }

    [Fact]
    public async Task CloneAsync_CreatesNewScenario()
    {
        var (db, gid) = await SetupAsync();
        await using (db)
        {
            var repo = new ScenarioRepository(db);
            var s = new TestScenario { Id = Guid.NewGuid(), GroupId = gid, Naziv = "Original", Redoslijed = 0 };
            await repo.AddAsync(s);
            var copy = await repo.CloneAsync(s.Id, gid);
            Assert.NotEqual(s.Id, copy.Id);
            Assert.Contains("(kopija)", copy.Naziv);
            Assert.Equal(2, db.Scenarios.Count());
        }
    }

    [Fact]
    public async Task GetByGroupAsync_ReturnsSortedByOrder()
    {
        var (db, gid) = await SetupAsync();
        await using (db)
        {
            var repo = new ScenarioRepository(db);
            await repo.AddAsync(new TestScenario { Id = Guid.NewGuid(), GroupId = gid, Naziv = "B", Redoslijed = 1 });
            await repo.AddAsync(new TestScenario { Id = Guid.NewGuid(), GroupId = gid, Naziv = "A", Redoslijed = 0 });
            var list = await repo.GetByGroupAsync(gid);
            Assert.Equal("A", list[0].Naziv);
        }
    }

    [Fact]
    public async Task DeleteAsync_NonExistent_Throws()
    {
        var (db, _) = await SetupAsync();
        await using (db)
        {
            var repo = new ScenarioRepository(db);
            await Assert.ThrowsAsync<InvalidOperationException>(() => repo.DeleteAsync(Guid.NewGuid()));
        }
    }
}
