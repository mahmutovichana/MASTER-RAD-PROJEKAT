using RBBH.TestAutomation.Core.Domain;

namespace RBBH.TestAutomation.Core.Repositories;

public interface IRunRepository
{
    Task<IReadOnlyList<RunResult>> GetByGroupAsync(Guid groupId, CancellationToken ct = default);
    Task<RunResult?> GetLatestByGroupAsync(Guid groupId, CancellationToken ct = default);
    Task<Guid> AddAsync(RunResult run, CancellationToken ct = default);
    Task UpdateAsync(RunResult run, CancellationToken ct = default);
}
