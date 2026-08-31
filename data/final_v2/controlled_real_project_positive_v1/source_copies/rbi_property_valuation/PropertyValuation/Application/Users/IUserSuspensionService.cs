namespace RBBH.CollateralAppraisal.Application.Users;

public interface IUserSuspensionService
{
    Task SuspendAsync(string userId, string? reason, CancellationToken ct = default);
    Task ReactivateAsync(string userId, CancellationToken ct = default);
}
