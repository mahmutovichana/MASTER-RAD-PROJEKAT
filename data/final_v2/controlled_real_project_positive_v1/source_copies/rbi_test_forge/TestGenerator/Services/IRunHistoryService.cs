using RBBH.TestAutomation.Api.DTO;

namespace RBBH.TestAutomation.Api.Services;

public interface IRunHistoryService
{
    Task<IReadOnlyList<RunHistoryRow>> GetHistoryAsync(RunHistoryFilter filter, CancellationToken ct = default);
    Task<HistoryDashboard> GetDashboardAsync(CancellationToken ct = default);
    Task<IReadOnlyList<TrendPoint>> GetTrendAsync(int days = 30, CancellationToken ct = default);
    Task<IReadOnlyList<FlakyTestInfo>> GetFlakyTestsAsync(int minRuns = 3, CancellationToken ct = default);
    Task<RunHistoryRow?> GetRunByIdAsync(Guid runId, CancellationToken ct = default);
}
