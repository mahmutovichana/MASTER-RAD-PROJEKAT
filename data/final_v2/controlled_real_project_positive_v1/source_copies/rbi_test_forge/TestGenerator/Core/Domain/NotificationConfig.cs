namespace RBBH.TestAutomation.Core.Domain;

/// <summary>
/// Konfiguracija notifikacija po grupi — serijalizuje se kao JSON kolona na <see cref="TestGroup"/>.
/// </summary>
public sealed class NotificationConfig
{
    public bool NotifyOnSuccess { get; set; }
    public bool NotifyOnFailure { get; set; } = true;
    public List<string> EmailRecipients { get; set; } = [];
    public string? SlackWebhookUrl { get; set; }
    public string? TeamsWebhookUrl { get; set; }
}
