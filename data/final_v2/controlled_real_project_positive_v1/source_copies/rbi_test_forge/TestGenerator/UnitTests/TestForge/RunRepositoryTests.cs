using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Domain.Enums;
using RBBH.TestAutomation.Core.Infrastructure;
using RBBH.TestAutomation.Core.Repositories;

namespace UnitTests.TestForge;

public class RunRepositoryTests
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
    public async Task AddAsync_PersistsRun()
    {
        var (db, gid) = await SetupAsync();
        await using (db)
        {
            var repo = new RunRepository(db);
            var run = new RunResult { Id = Guid.NewGuid(), GroupId = gid, State = RunState.Passed, PassRate = 1.0 };
            await repo.AddAsync(run);
            Assert.Single(db.RunResults);
        }
    }

    [Fact]
    public async Task GetLatestByGroupAsync_ReturnsNewest()
    {
        var (db, gid) = await SetupAsync();
        await using (db)
        {
            var repo = new RunRepository(db);
            var old = new RunResult { Id = Guid.NewGuid(), GroupId = gid, State = RunState.Failed, StartedAt = DateTime.UtcNow.AddHours(-2) };
            var newer = new RunResult { Id = Guid.NewGuid(), GroupId = gid, State = RunState.Passed, StartedAt = DateTime.UtcNow.AddHours(-1) };
            db.RunResults.AddRange(old, newer);
            await db.SaveChangesAsync();
            var latest = await repo.GetLatestByGroupAsync(gid);
            Assert.Equal(newer.Id, latest!.Id);
        }
    }
}
