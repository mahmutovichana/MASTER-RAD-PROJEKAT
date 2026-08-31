using System.Text;
using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Api.Jobs;
using Hangfire;
using Microsoft.EntityFrameworkCore;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Infrastructure;

namespace RBBH.TestAutomation.Api.Services;

public class ScheduleService(TestForgeDbContext db, IRecurringJobManager hangfire) : IScheduleService
{
    public async Task<IReadOnlyList<ScheduleConfigDto>> GetAllAsync(CancellationToken ct = default) =>
        await db.Schedules
            .Include(s => s.Group)
            .OrderBy(s => s.Group!.Naziv)
            .Select(s => ToDto(s))
            .ToListAsync(ct);

    public async Task<IReadOnlyList<ScheduleConfigDto>> GetByGroupAsync(Guid groupId, CancellationToken ct = default) =>
        await db.Schedules
            .Include(s => s.Group)
            .Where(s => s.GroupId == groupId)
            .Select(s => ToDto(s))
            .ToListAsync(ct);

    public async Task<Guid> CreateAsync(CreateScheduleRequest r, CancellationToken ct = default)
    {
        var config = new ScheduleConfig
        {
            Id             = Guid.NewGuid(),
            GroupId        = r.GroupId,
            CronExpression = r.CronExpression,
            IsActive       = r.IsActive,
            Timezone       = r.Timezone,
        };

        db.Schedules.Add(config);
        await db.SaveChangesAsync(ct);

        if (config.IsActive)
            Register(config, await GetGroupNazivAsync(config.GroupId, ct));

        return config.Id;
    }

    public async Task UpdateAsync(Guid id, UpdateScheduleRequest r, CancellationToken ct = default)
    {
        var config = await db.Schedules.FindAsync([id], ct)
            ?? throw new InvalidOperationException($"Raspored {id} nije pronađen.");

        config.CronExpression = r.CronExpression;
        config.Timezone       = r.Timezone;
        config.IsActive       = r.IsActive;

        await db.SaveChangesAsync(ct);

        var naziv = await GetGroupNazivAsync(config.GroupId, ct);
        if (config.IsActive)
            Register(config, naziv);
        else
            hangfire.RemoveIfExists(JobId(naziv, id));
    }

    public async Task DeleteAsync(Guid id, CancellationToken ct = default)
    {
        var config = await db.Schedules.FindAsync([id], ct);
        if (config is null) return;

        var naziv = await GetGroupNazivAsync(config.GroupId, ct);
        hangfire.RemoveIfExists(JobId(naziv, id));
        db.Schedules.Remove(config);
        await db.SaveChangesAsync(ct);
    }

    public async Task TriggerNowAsync(Guid id, CancellationToken ct = default)
    {
        var config = await db.Schedules.FindAsync([id], ct)
            ?? throw new InvalidOperationException($"Raspored {id} nije pronađen.");

        hangfire.Trigger(JobId(await GetGroupNazivAsync(config.GroupId, ct), id));
    }

    private void Register(ScheduleConfig config, string groupNaziv)
    {
        var tz = ParseTimezone(config.Timezone);
        hangfire.AddOrUpdate<GroupTestJob>(
            JobId(groupNaziv, config.Id),
            job => job.ExecuteAsync(config.GroupId, null),
            config.CronExpression,
            new RecurringJobOptions { TimeZone = tz });
    }

    private async Task<string> GetGroupNazivAsync(Guid groupId, CancellationToken ct) =>
        await db.Groups
            .Where(g => g.Id == groupId)
            .Select(g => g.Naziv)
            .FirstOrDefaultAsync(ct) ?? "grupa";

    /// <summary>
    /// Recurring job ID koji se prikazuje u Hangfire Dashboard-u — počinje nazivom grupe
    /// (da imena odgovaraju grupama testova), a sufiks s ID-om garantuje jedinstvenost.
    /// </summary>
    private static string JobId(string groupNaziv, Guid scheduleId) =>
        $"{Sanitize(groupNaziv)} [{scheduleId.ToString()[..8]}]";

    private static string Sanitize(string s)
    {
        var sb = new StringBuilder(s.Length);
        foreach (var c in s)
            sb.Append(char.IsLetterOrDigit(c) || c is ' ' or '-' or '_' ? c : '-');
        var rez = sb.ToString().Trim();
        return rez.Length == 0 ? "grupa" : rez;
    }

    private static TimeZoneInfo ParseTimezone(string tz)
    {
        try   { return TimeZoneInfo.FindSystemTimeZoneById(tz); }
        catch { return TimeZoneInfo.Utc; }
    }

    private static ScheduleConfigDto ToDto(ScheduleConfig s) =>
        new(s.Id, s.GroupId, s.Group?.Naziv ?? "—", s.CronExpression, s.IsActive, s.Timezone);
}
