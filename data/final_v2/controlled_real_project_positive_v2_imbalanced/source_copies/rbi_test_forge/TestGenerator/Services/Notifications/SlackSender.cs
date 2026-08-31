using System.Text;
using System.Text.Json;

namespace RBBH.TestAutomation.Api.Services.Notifications;

public sealed class SlackSender(IHttpClientFactory httpFactory, ILogger<SlackSender> logger)
{
    public async Task SendAsync(string webhookUrl, NotificationMessage msg, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(webhookUrl)) return;

        var statusEmoji = msg.Status == "Passed" ? ":white_check_mark:" : ":x:";
        var color = msg.Status == "Passed" ? "#36a64f" : "#e01e5a";

        var payload = new
        {
            blocks = new object[]
            {
                new
                {
                    type = "header",
                    text = new { type = "plain_text", text = $"{(msg.Status == "Passed" ? "✅" : "❌")} Test Run: {msg.GroupName}" }
                },
                new
                {
                    type = "section",
                    fields = new object[]
                    {
                        new { type = "mrkdwn", text = $"*Status:*\n{statusEmoji} {msg.Status}" },
                        new { type = "mrkdwn", text = $"*Pass Rate:*\n{msg.PassRate:F1}%" },
                        new { type = "mrkdwn", text = $"*Rezultat:*\n{msg.Passed} prošlo / {msg.Failed} palo" },
                        new { type = "mrkdwn", text = $"*Trajanje:*\n{msg.Duration:mm\\:ss}" },
                    }
                },
                new
                {
                    type = "context",
                    elements = new object[]
                    {
                        new { type = "mrkdwn", text = $"Trigger: *{msg.TriggerType}* | Ukupno: *{msg.Total}* scenarija" }
                    }
                }
            }
        };

        if (msg.ReportUrl is not null)
        {
            var blocks = payload.blocks.ToList();
            blocks.Add(new
            {
                type = "actions",
                elements = new object[]
                {
                    new { type = "button", text = new { type = "plain_text", text = "Pogledaj report" }, url = msg.ReportUrl }
                }
            });
        }

        var json = JsonSerializer.Serialize(payload);
        using var client = httpFactory.CreateClient();
        using var content = new StringContent(json, Encoding.UTF8, "application/json");
        var resp = await client.PostAsync(webhookUrl, content, ct);

        if (resp.IsSuccessStatusCode)
            logger.LogInformation("Slack notifikacija poslana za grupu {Group}", msg.GroupName);
        else
            logger.LogWarning("Slack webhook vratio {Status} za grupu {Group}", resp.StatusCode, msg.GroupName);
    }
}
