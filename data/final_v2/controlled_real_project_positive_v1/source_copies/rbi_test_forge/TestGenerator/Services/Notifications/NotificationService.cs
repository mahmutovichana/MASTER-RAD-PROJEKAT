using System.Text.Json;
using RBBH.TestAutomation.Core.Domain;

namespace RBBH.TestAutomation.Api.Services.Notifications;

public sealed class NotificationService(
    EmailSender email,
    SlackSender slack,
    TeamsSender teams,
    IConfiguration config,
    ILogger<NotificationService> logger) : INotificationService
{
    public async Task SendRunCompletionAsync(RunResult run, TestGroup group, CancellationToken ct = default)
    {
        var nc = Deserialize(group.NotificationConfigJson);
        if (nc is null) return;

        var isPassed = run.State == RBBH.TestAutomation.Core.Domain.Enums.RunState.Passed;
        if (isPassed && !nc.NotifyOnSuccess) return;
        if (!isPassed && !nc.NotifyOnFailure) return;

        var appBaseUrl = config["Notifications:AppBaseUrl"]?.TrimEnd('/') ?? "";
        var reportUrl = string.IsNullOrEmpty(appBaseUrl)
            ? null
            : $"{appBaseUrl}/grupe?runId={run.Id}";

        var msg = new NotificationMessage(
            GroupName: group.Naziv,
            Status: isPassed ? "Passed" : "Failed",
            PassRate: run.PassRate,
            Passed: run.PassedCount,
            Failed: run.FailedCount,
            Total: run.TotalCount,
            Duration: run.Duration,
            TriggerType: run.TriggerType.ToString(),
            ReportUrl: reportUrl);

        var allRecipients = MergeRecipients(nc);
        var tasks = new List<Task>();

        if (allRecipients.Count > 0 && config.GetValue("Notifications:Email:Enabled", false))
            tasks.Add(SafeSendAsync("Email", () => email.SendAsync(allRecipients, msg, ct)));

        if (!string.IsNullOrWhiteSpace(nc.SlackWebhookUrl))
            tasks.Add(SafeSendAsync("Slack", () => slack.SendAsync(nc.SlackWebhookUrl, msg, ct)));

        if (!string.IsNullOrWhiteSpace(nc.TeamsWebhookUrl))
            tasks.Add(SafeSendAsync("Teams", () => teams.SendAsync(nc.TeamsWebhookUrl, msg, ct)));

        await Task.WhenAll(tasks);
    }

    public async Task SendTestNotificationAsync(NotificationConfig nc, CancellationToken ct = default)
    {
        var msg = new NotificationMessage(
            GroupName: "Test notifikacija",
            Status: "Passed",
            PassRate: 100,
            Passed: 5,
            Failed: 0,
            Total: 5,
            Duration: TimeSpan.FromSeconds(12),
            TriggerType: "Manual",
            ReportUrl: null);

        var allRecipients = MergeRecipients(nc);
        var tasks = new List<Task>();

        if (allRecipients.Count > 0)
            tasks.Add(SafeSendAsync("Email", () => email.SendAsync(allRecipients, msg, ct)));

        if (!string.IsNullOrWhiteSpace(nc.SlackWebhookUrl))
            tasks.Add(SafeSendAsync("Slack", () => slack.SendAsync(nc.SlackWebhookUrl, msg, ct)));

        if (!string.IsNullOrWhiteSpace(nc.TeamsWebhookUrl))
            tasks.Add(SafeSendAsync("Teams", () => teams.SendAsync(nc.TeamsWebhookUrl, msg, ct)));

        await Task.WhenAll(tasks);
    }

    private List<string> MergeRecipients(NotificationConfig nc)
    {
        var global = config.GetSection("Notifications:GlobalRecipients").Get<List<string>>() ?? [];
        var merged = new HashSet<string>(global, StringComparer.OrdinalIgnoreCase);
        foreach (var r in nc.EmailRecipients)
            merged.Add(r);
        return merged.ToList();
    }

    private async Task SafeSendAsync(string channel, Func<Task> action)
    {
        try
        {
            await action();
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Greška pri slanju {Channel} notifikacije", channel);
        }
    }

    private static NotificationConfig? Deserialize(string? json)
    {
        if (string.IsNullOrWhiteSpace(json)) return null;
        try { return JsonSerializer.Deserialize<NotificationConfig>(json, JsonOpts); }
        catch { return null; }
    }

    private static readonly JsonSerializerOptions JsonOpts = new(JsonSerializerDefaults.Web);
}
