namespace RBBH.TestAutomation.Api.Services.Notifications;

/// <summary>Poruka koja se šalje putem email/Slack/Teams kanala.</summary>
public sealed record NotificationMessage(
    string GroupName,
    string Status,
    double PassRate,
    int Passed,
    int Failed,
    int Total,
    TimeSpan Duration,
    string TriggerType,
    string? ReportUrl);
