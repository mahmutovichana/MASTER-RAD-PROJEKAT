using Microsoft.EntityFrameworkCore;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Infrastructure;

namespace RBBH.TestAutomation.Core.Repositories;

public class ScenarioRepository(TestForgeDbContext db) : IScenarioRepository
{
    public async Task<IReadOnlyList<TestScenario>> GetByGroupAsync(Guid groupId, CancellationToken ct = default) =>
        await db.Scenarios
            .Where(s => s.GroupId == groupId)
            .OrderBy(s => s.Redoslijed)
            .ToListAsync(ct);

    public async Task<TestScenario?> GetByIdAsync(Guid id, CancellationToken ct = default) =>
        await db.Scenarios.FirstOrDefaultAsync(s => s.Id == id, ct);

    public async Task<Guid> AddAsync(TestScenario scenario, CancellationToken ct = default)
    {
        scenario.KreiranAt = DateTime.UtcNow;
        db.Scenarios.Add(scenario);
        await db.SaveChangesAsync(ct);
        return scenario.Id;
    }

    public async Task UpdateAsync(TestScenario scenario, CancellationToken ct = default)
    {
        db.Scenarios.Update(scenario);
        await db.SaveChangesAsync(ct);
    }

    public async Task DeleteAsync(Guid id, CancellationToken ct = default)
    {
        var s = await db.Scenarios.FindAsync([id], ct)
            ?? throw new InvalidOperationException($"Scenarij {id} ne postoji.");
        db.Scenarios.Remove(s);
        await db.SaveChangesAsync(ct);
    }

    public async Task<TestScenario> CloneAsync(Guid sourceId, Guid targetGroupId, CancellationToken ct = default)
    {
        var source = await db.Scenarios.AsNoTracking().FirstOrDefaultAsync(s => s.Id == sourceId, ct)
            ?? throw new InvalidOperationException($"Izvorni scenarij {sourceId} ne postoji.");
        var maxOrder = await db.Scenarios
            .Where(s => s.GroupId == targetGroupId)
            .MaxAsync(s => (int?)s.Redoslijed, ct) ?? -1;
        var copy = new TestScenario
        {
            Id = Guid.NewGuid(),
            GroupId = targetGroupId,
            Naziv = source.Naziv + " (kopija)",
            Tip = source.Tip,
            Target = source.Target,
            Arrange = source.Arrange,
            Act = source.Act,
            Assert = source.Assert,
            Redoslijed = maxOrder + 1,
            KreiranAt = DateTime.UtcNow,
            KreiranOd = source.KreiranOd,
        };
        db.Scenarios.Add(copy);
        await db.SaveChangesAsync(ct);
        return copy;
    }
}
