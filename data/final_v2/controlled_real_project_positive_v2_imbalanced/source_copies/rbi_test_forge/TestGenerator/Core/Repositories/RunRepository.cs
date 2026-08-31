using Microsoft.EntityFrameworkCore;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Infrastructure;

namespace RBBH.TestAutomation.Core.Repositories;

public class RunRepository(TestForgeDbContext db) : IRunRepository
{
    public async Task<IReadOnlyList<RunResult>> GetByGroupAsync(Guid groupId, CancellationToken ct = default) =>
        await db.RunResults
            .Where(r => r.GroupId == groupId)
            .OrderByDescending(r => r.StartedAt)
            .ToListAsync(ct);

    public async Task<RunResult?> GetLatestByGroupAsync(Guid groupId, CancellationToken ct = default) =>
        await db.RunResults
            .Where(r => r.GroupId == groupId)
            .OrderByDescending(r => r.StartedAt)
            .FirstOrDefaultAsync(ct);

    public async Task<Guid> AddAsync(RunResult run, CancellationToken ct = default)
    {
        run.StartedAt = DateTime.UtcNow;
        db.RunResults.Add(run);
        await db.SaveChangesAsync(ct);
        return run.Id;
    }

    public async Task UpdateAsync(RunResult run, CancellationToken ct = default)
    {
        db.RunResults.Update(run);
        await db.SaveChangesAsync(ct);
    }
}
