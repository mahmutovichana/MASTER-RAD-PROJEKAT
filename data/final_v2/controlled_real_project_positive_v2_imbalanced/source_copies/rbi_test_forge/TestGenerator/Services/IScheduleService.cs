using RBBH.TestAutomation.Api.DTO;

namespace RBBH.TestAutomation.Api.Services;

public interface IScheduleService
{
    Task<IReadOnlyList<ScheduleConfigDto>> GetAllAsync(CancellationToken ct = default);
    Task<IReadOnlyList<ScheduleConfigDto>> GetByGroupAsync(Guid groupId, CancellationToken ct = default);
    Task<Guid> CreateAsync(CreateScheduleRequest r, CancellationToken ct = default);
    Task UpdateAsync(Guid id, UpdateScheduleRequest r, CancellationToken ct = default);
    Task DeleteAsync(Guid id, CancellationToken ct = default);
    Task TriggerNowAsync(Guid id, CancellationToken ct = default);
}
