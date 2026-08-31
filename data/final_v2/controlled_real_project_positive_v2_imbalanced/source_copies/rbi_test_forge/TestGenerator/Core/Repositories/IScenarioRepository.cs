using RBBH.TestAutomation.Core.Domain;

namespace RBBH.TestAutomation.Core.Repositories;

public interface IScenarioRepository
{
    Task<IReadOnlyList<TestScenario>> GetByGroupAsync(Guid groupId, CancellationToken ct = default);
    Task<TestScenario?> GetByIdAsync(Guid id, CancellationToken ct = default);
    Task<Guid> AddAsync(TestScenario scenario, CancellationToken ct = default);
    Task UpdateAsync(TestScenario scenario, CancellationToken ct = default);
    Task DeleteAsync(Guid id, CancellationToken ct = default);
    /// <summary>Kreira kopiju scenarija u ciljnoj grupi (ide na kraj liste, naziv dobija sufiks " (kopija)").</summary>
    Task<TestScenario> CloneAsync(Guid sourceId, Guid targetGroupId, CancellationToken ct = default);
}
