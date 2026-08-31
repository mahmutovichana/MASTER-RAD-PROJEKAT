using RBBH.TestAutomation.Core.Domain;

namespace RBBH.TestAutomation.Api.Services.Notifications;

public interface INotificationService
{
    Task SendRunCompletionAsync(RunResult run, TestGroup group, CancellationToken ct = default);
    Task SendTestNotificationAsync(NotificationConfig config, CancellationToken ct = default);
}
