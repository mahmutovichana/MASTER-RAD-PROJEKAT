using System.Net;
using System.Net.Mail;

namespace RBBH.TestAutomation.Api.Services.Notifications;

public sealed class EmailSender(IConfiguration config, ILogger<EmailSender> logger)
{
    public async Task SendAsync(IReadOnlyList<string> recipients, NotificationMessage msg, CancellationToken ct)
    {
        if (recipients.Count == 0) return;

        var smtpHost = config["Notifications:Email:SmtpHost"];
        if (string.IsNullOrWhiteSpace(smtpHost))
        {
            logger.LogWarning("SMTP nije konfigurisan — email notifikacija preskočena");
            return;
        }

        var port = config.GetValue("Notifications:Email:SmtpPort", 587);
        var useSsl = config.GetValue("Notifications:Email:UseSsl", true);
        var username = config["Notifications:Email:Username"] ?? "";
        var password = config["Notifications:Email:Password"] ?? "";
        var fromAddr = config["Notifications:Email:FromAddress"] ?? "noreply@testforge.local";
        var fromName = config["Notifications:Email:FromName"] ?? "Test Automation Generator";

        var statusEmoji = msg.Status == "Passed" ? "✅" : "❌";
        var subject = $"{statusEmoji} [{msg.GroupName}] — {msg.Status} ({msg.PassRate:F0}% pass rate)";

        var body = $"""
            <h2>{statusEmoji} Test Run: {msg.GroupName}</h2>
            <table style="border-collapse:collapse;">
              <tr><td style="padding:4px 12px;"><b>Status</b></td><td style="padding:4px 12px;">{msg.Status}</td></tr>
              <tr><td style="padding:4px 12px;"><b>Pass Rate</b></td><td style="padding:4px 12px;">{msg.PassRate:F1}%</td></tr>
              <tr><td style="padding:4px 12px;"><b>Rezultat</b></td><td style="padding:4px 12px;">{msg.Passed} prošlo / {msg.Failed} palo / {msg.Total} ukupno</td></tr>
              <tr><td style="padding:4px 12px;"><b>Trajanje</b></td><td style="padding:4px 12px;">{msg.Duration:mm\:ss}</td></tr>
              <tr><td style="padding:4px 12px;"><b>Pokrenuo</b></td><td style="padding:4px 12px;">{msg.TriggerType}</td></tr>
            </table>
            {(msg.ReportUrl is not null ? $"<p><a href=\"{msg.ReportUrl}\">Pogledaj detaljan report →</a></p>" : "")}
            <hr/><p style="color:#888;font-size:12px;">Test Automation Generator — automatska notifikacija</p>
            """;

        using var smtp = new SmtpClient(smtpHost, port)
        {
            EnableSsl = useSsl,
            Credentials = string.IsNullOrEmpty(username) ? null : new NetworkCredential(username, password),
        };

        var mail = new MailMessage
        {
            From = new MailAddress(fromAddr, fromName),
            Subject = subject,
            Body = body,
            IsBodyHtml = true,
        };
        foreach (var r in recipients)
            mail.To.Add(r);

        await smtp.SendMailAsync(mail, ct);
        logger.LogInformation("Email notifikacija poslana na {Count} primatelja za grupu {Group}", recipients.Count, msg.GroupName);
    }
}
