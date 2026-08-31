using RBBH.TestAutomation.Api.DTO;

namespace RBBH.TestAutomation.Api.Services;

public class MockScheduleService : IScheduleService
{
    private readonly List<ScheduleConfigDto> _schedules = [];
    private readonly Dictionary<Guid, string> _groupNames = [];

    public Task<IReadOnlyList<ScheduleConfigDto>> GetAllAsync(CancellationToken ct = default) =>
        Task.FromResult<IReadOnlyList<ScheduleConfigDto>>(_schedules.ToList());

    public Task<IReadOnlyList<ScheduleConfigDto>> GetByGroupAsync(Guid groupId, CancellationToken ct = default) =>
        Task.FromResult<IReadOnlyList<ScheduleConfigDto>>(
            _schedules.Where(s => s.GroupId == groupId).ToList());

    public Task<Guid> CreateAsync(CreateScheduleRequest r, CancellationToken ct = default)
    {
        var id = Guid.NewGuid();
        _groupNames.TryGetValue(r.GroupId, out var naziv);
        _schedules.Add(new ScheduleConfigDto(id, r.GroupId, naziv ?? "—", r.CronExpression, r.IsActive, r.Timezone));
        return Task.FromResult(id);
    }

    public Task UpdateAsync(Guid id, UpdateScheduleRequest r, CancellationToken ct = default)
    {
        var idx = _schedules.FindIndex(s => s.Id == id);
        if (idx < 0) return Task.CompletedTask;
        var old = _schedules[idx];
        _schedules[idx] = old with
        {
            CronExpression = r.CronExpression,
            Timezone = r.Timezone,
            IsActive = r.IsActive
        };
        return Task.CompletedTask;
    }

    public Task DeleteAsync(Guid id, CancellationToken ct = default)
    {
        _schedules.RemoveAll(s => s.Id == id);
        return Task.CompletedTask;
    }

    public Task TriggerNowAsync(Guid id, CancellationToken ct = default) =>
        Task.CompletedTask;

    public void SeedGroupNames(IEnumerable<(Guid Id, string Naziv)> groups)
    {
        foreach (var (gid, naziv) in groups)
            _groupNames[gid] = naziv;
    }
}
