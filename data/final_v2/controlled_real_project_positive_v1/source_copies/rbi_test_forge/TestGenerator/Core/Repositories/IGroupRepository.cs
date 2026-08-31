using RBBH.TestAutomation.Core.Domain;

namespace RBBH.TestAutomation.Core.Repositories;

public interface IGroupRepository
{
    Task<IReadOnlyList<TestGroup>> GetAllAsync(CancellationToken ct = default);
    Task<TestGroup?> GetByIdAsync(Guid id, CancellationToken ct = default);
    Task<IReadOnlyList<TestGroup>> GetRootGroupsAsync(CancellationToken ct = default);
    /// <exception cref="InvalidOperationException">Ako bi se prekršilo pravilo ≤2 nivoa.</exception>
    Task<Guid> AddAsync(TestGroup group, string actorId, string actorName, CancellationToken ct = default);
    Task UpdateAsync(TestGroup group, string actorId, string actorName, CancellationToken ct = default);
    /// <exception cref="InvalidOperationException">Ako grupa ima podgrupe.</exception>
    Task DeleteAsync(Guid id, string actorId, string actorName, CancellationToken ct = default);
    Task ReorderScenariosAsync(Guid groupId, IReadOnlyList<Guid> orderedIds, CancellationToken ct = default);
    Task<GroupSummary> GetSummaryAsync(Guid groupId, CancellationToken ct = default);
    Task SetScheduleActiveAsync(Guid groupId, bool isActive, CancellationToken ct = default);
}
