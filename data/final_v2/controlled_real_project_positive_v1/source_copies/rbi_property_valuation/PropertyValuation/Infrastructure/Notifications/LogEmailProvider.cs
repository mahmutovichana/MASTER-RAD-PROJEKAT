using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Notifications;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Notifications;

/// <summary>
/// Dev/test email provider — loguje poruku umjesto stvarnog slanja.
/// Koristiti dok se ne konfiguriše SMTP provider za produkciju.
/// </summary>
[ExcludeFromCodeCoverage]
public sealed class LogEmailProvider : IEmailProvider
{
    private readonly ILogger<LogEmailProvider> _logger;

    public LogEmailProvider(ILogger<LogEmailProvider> logger) => _logger = logger;

    public Task SendAsync(EmailMessage message, CancellationToken ct = default)
    {
        _logger.LogInformation(
            "[EMAIL-DEV] To={To} Subject={Subject} | {Body}",
            message.ToAddress, message.Subject, message.Body);

        return Task.CompletedTask;
    }
}
