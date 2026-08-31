using System.Text;
using System.Text.Json;

namespace RBBH.TestAutomation.Api.Services.Notifications;

public sealed class TeamsSender(IHttpClientFactory httpFactory, ILogger<TeamsSender> logger)
{
    public async Task SendAsync(string webhookUrl, NotificationMessage msg, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(webhookUrl)) return;

        var statusEmoji = msg.Status == "Passed" ? "✅" : "❌";
        var themeColor = msg.Status == "Passed" ? "00c853" : "ff1744";

        var facts = new List<object>
        {
            new { name = "Status", value = $"{statusEmoji} {msg.Status}" },
            new { name = "Pass Rate", value = $"{msg.PassRate:F1}%" },
            new { name = "Rezultat", value = $"{msg.Passed} prošlo / {msg.Failed} palo / {msg.Total} ukupno" },
            new { name = "Trajanje", value = $"{msg.Duration:mm\\:ss}" },
            new { name = "Trigger", value = msg.TriggerType },
        };

        var actions = new List<object>();
        if (msg.ReportUrl is not null)
        {
            actions.Add(new
            {
                @type = "OpenUri",
                name = "Pogledaj report",
                targets = new[] { new { os = "default", uri = msg.ReportUrl } }
            });
        }

        var card = new
        {
            @type = "MessageCard",
            @context = "http://schema.org/extensions",
            themeColor,
            summary = $"Test Run: {msg.GroupName} — {msg.Status}",
            sections = new[]
            {
                new
                {
                    activityTitle = $"{statusEmoji} Test Run: {msg.GroupName}",
                    activitySubtitle = "Test Automation Generator",
                    facts,
                    markdown = true
                }
            },
            potentialAction = actions,
        };

        var json = JsonSerializer.Serialize(card);
        using var client = httpFactory.CreateClient();
        using var content = new StringContent(json, Encoding.UTF8, "application/json");
        var resp = await client.PostAsync(webhookUrl, content, ct);

        if (resp.IsSuccessStatusCode)
            logger.LogInformation("Teams notifikacija poslana za grupu {Group}", msg.GroupName);
        else
            logger.LogWarning("Teams webhook vratio {Status} za grupu {Group}", resp.StatusCode, msg.GroupName);
    }
}
