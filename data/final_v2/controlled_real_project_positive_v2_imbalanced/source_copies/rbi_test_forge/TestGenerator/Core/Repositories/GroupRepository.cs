using Microsoft.EntityFrameworkCore;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Infrastructure;

namespace RBBH.TestAutomation.Core.Repositories;

public class GroupRepository(TestForgeDbContext db, ITestForgeAuditWriter? audit = null) : IGroupRepository
{
    // Lagani snapshot za audit (izbjegava cikluse iz EF navigacija pri JSON serijalizaciji).
    private static object Snapshot(TestGroup g) => new
    {
        g.Id, g.Naziv, g.Opis, g.Boja, Tag = g.Tag.ToString(),
        g.Prioritet, g.ParentGroupId,
    };

    public async Task<IReadOnlyList<TestGroup>> GetAllAsync(CancellationToken ct = default) =>
        await db.Groups
            .Include(g => g.ChildGroups)
            .Include(g => g.Scenarios)
            .OrderByDescending(g => g.Prioritet).ThenBy(g => g.Naziv)
            .ToListAsync(ct);

    public async Task<TestGroup?> GetByIdAsync(Guid id, CancellationToken ct = default) =>
        await db.Groups
            .Include(g => g.ChildGroups)
            .Include(g => g.Scenarios)
            .Include(g => g.Schedules)
            .FirstOrDefaultAsync(g => g.Id == id, ct);

    public async Task<IReadOnlyList<TestGroup>> GetRootGroupsAsync(CancellationToken ct = default) =>
        await db.Groups
            .Where(g => g.ParentGroupId == null)
            .OrderByDescending(g => g.Prioritet).ThenBy(g => g.Naziv)
            .ToListAsync(ct);

    public async Task<Guid> AddAsync(TestGroup group, string actorId, string actorName, CancellationToken ct = default)
    {
        if (group.ParentGroupId.HasValue)
        {
            var parent = await db.Groups.AsNoTracking()
                .FirstOrDefaultAsync(g => g.Id == group.ParentGroupId.Value, ct)
                ?? throw new InvalidOperationException("Nadređena grupa ne postoji.");
            if (parent.ParentGroupId.HasValue)
                throw new InvalidOperationException("Nije dozvoljeno kreirati podgrupu na 3. nivou (max ≤2 nivoa).");
        }
        group.KreiranOd = actorId;
        group.KreiranAt = DateTime.UtcNow;
        db.Groups.Add(group);
        await db.SaveChangesAsync(ct);

        if (audit is not null)
            await audit.WriteAsync(TestForgeAuditEntities.Group, group.Id, TestForgeAuditActions.Create,
                actorId, actorName, oldValues: null, newValues: Snapshot(group), ct);
        return group.Id;
    }

    public async Task UpdateAsync(TestGroup group, string actorId, string actorName, CancellationToken ct = default)
    {
        // Staro stanje iz baze (AsNoTracking → vrijednosti prije SaveChanges) za old_values.
        var old = audit is null
            ? null
            : await db.Groups.AsNoTracking().FirstOrDefaultAsync(g => g.Id == group.Id, ct);

        group.IzmjenjenOd = actorId;
        group.IzmjenjenAt = DateTime.UtcNow;
        db.Groups.Update(group);
        await db.SaveChangesAsync(ct);

        if (audit is not null)
            await audit.WriteAsync(TestForgeAuditEntities.Group, group.Id, TestForgeAuditActions.Update,
                actorId, actorName, oldValues: old is null ? null : Snapshot(old), newValues: Snapshot(group), ct);
    }

    public async Task DeleteAsync(Guid id, string actorId, string actorName, CancellationToken ct = default)
    {
        var group = await db.Groups.Include(g => g.ChildGroups)
            .FirstOrDefaultAsync(g => g.Id == id, ct)
            ?? throw new InvalidOperationException($"Grupa {id} ne postoji.");
        if (group.ChildGroups.Count > 0)
            throw new InvalidOperationException("Nije moguće obrisati grupu koja ima podgrupe. Prvo obrišite podgrupe.");
        var snapshot = Snapshot(group);
        db.Groups.Remove(group);
        await db.SaveChangesAsync(ct);

        if (audit is not null)
            await audit.WriteAsync(TestForgeAuditEntities.Group, id, TestForgeAuditActions.Delete,
                actorId, actorName, oldValues: snapshot, newValues: null, ct);
    }

    public async Task ReorderScenariosAsync(Guid groupId, IReadOnlyList<Guid> orderedIds, CancellationToken ct = default)
    {
        var scenarios = await db.Scenarios.Where(s => s.GroupId == groupId).ToListAsync(ct);
        for (var i = 0; i < orderedIds.Count; i++)
        {
            var s = scenarios.FirstOrDefault(x => x.Id == orderedIds[i]);
            if (s != null) s.Redoslijed = i;
        }
        await db.SaveChangesAsync(ct);
    }

    public async Task<GroupSummary> GetSummaryAsync(Guid groupId, CancellationToken ct = default)
    {
        var scenarioCount = await db.Scenarios.CountAsync(s => s.GroupId == groupId, ct);
        var activeSchedules = await db.Schedules.CountAsync(s => s.GroupId == groupId && s.IsActive, ct);
        var lastRun = await db.RunResults
            .Where(r => r.GroupId == groupId)
            .OrderByDescending(r => r.StartedAt)
            .FirstOrDefaultAsync(ct);
        return new GroupSummary(
            scenarioCount,
            lastRun?.StartedAt,
            lastRun?.PassRate,
            activeSchedules
        );
    }

    public async Task SetScheduleActiveAsync(Guid groupId, bool isActive, CancellationToken ct = default)
    {
        var schedules = await db.Schedules.Where(s => s.GroupId == groupId).ToListAsync(ct);
        foreach (var s in schedules) s.IsActive = isActive;
        await db.SaveChangesAsync(ct);
    }
}
