﻿using Microsoft.EntityFrameworkCore;
using MailKit.Net.Smtp;
using MailKit.Security;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using MimeKit;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Application.Users.Models;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using DomainNotification = RBBH.CollateralAppraisal.Domain.Notifications.Notification;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Notifications;

/// <summary>
/// Notifikacioni provider:
/// - <b>InApp</b> kanal â†’ sprema notifikaciju u <c>notifications</c> tabelu (vidljivo u
///   bell inboxu). Ako je zadana <c>RecipientRole</c> umjesto korisnika, notifikacija se
///   "fan-out"-uje na sve aktivne korisnike te role (preko <see cref="IUserRoleProvider"/>).
/// - <b>Email</b> kanal â†’ SMTP (MailKit); ako SMTP host nije konfigurisan, samo loguje.
/// </summary>
[ExcludeFromCodeCoverage]
public sealed class EmailNotificationProvider : INotificationProvider
{
    private readonly ILogger<EmailNotificationProvider> _logger;
    private readonly SmtpOptions _smtp;
    private readonly ApplicationDbContext _db;
    private readonly IUserRoleProvider _userRoleProvider;

    public EmailNotificationProvider(
        ILogger<EmailNotificationProvider> logger,
        IOptions<SmtpOptions> smtpOptions,
        ApplicationDbContext db,
        IUserRoleProvider userRoleProvider)
    {
        _logger           = logger;
        _smtp             = smtpOptions.Value;
        _db               = db;
        _userRoleProvider = userRoleProvider;
    }

    public async Task SendAsync(NotificationRequest request, CancellationToken ct = default)
    {
        // â”€â”€ In-app: perzistuj u DB (bell inbox) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        if (request.Channel == NotificationChannel.InApp)
        {
            await PersistInAppAsync(request, ct);
            return;
        }

        // â”€â”€ Email: SMTP ili log fallback â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        if (request.Channel == NotificationChannel.Email && !string.IsNullOrWhiteSpace(request.RecipientEmail))
        {
            if (string.IsNullOrWhiteSpace(_smtp.Host))
            {
                _logger.LogInformation(
                    "[EMAIL-SKIPPED] SMTP nije konfigurisan — email za {Email} nije poslan. Subject={Subject} | {Message}",
                    request.RecipientEmail, request.Subject, request.Message);
                return;
            }

            await SendEmailAsync(request, request.RecipientEmail, ct);
            return;
        }

        _logger.LogInformation(
            "[NOTIFICATION] Channel={Channel} To={User}/{Role} Subject={Subject} | {Message}",
            request.Channel,
            request.RecipientUserId ?? "N/A",
            request.RecipientRole ?? "N/A",
            request.Subject,
            request.Message);
    }

    /// <summary>
    /// Sprema in-app notifikaciju za konkretnog korisnika ili — ako je zadana rola —
    /// za sve aktivne korisnike te role. Greška u razrješavanju rola ne smije srušiti tok.
    /// </summary>
    private async Task PersistInAppAsync(NotificationRequest request, CancellationToken ct)
    {
        var recipientIds = new List<string>();

        if (!string.IsNullOrWhiteSpace(request.RecipientUserId))
        {
            recipientIds.Add(request.RecipientUserId);
        }
        else if (!string.IsNullOrWhiteSpace(request.RecipientRole))
        {
            try
            {
                var users = await _userRoleProvider.GetUsersWithRolesAsync(
                    new UserRoleListRequest { Role = request.RecipientRole, PageSize = 100, IsActive = true }, ct);
                recipientIds.AddRange(users.Items.Select(u => u.UserId));
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex,
                    "Ne mogu razriješiti korisnike role {Role} za in-app notifikaciju.", request.RecipientRole);
            }
        }

        recipientIds = recipientIds
            .Where(id => !string.IsNullOrWhiteSpace(id))
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .ToList();

        if (recipientIds.Count == 0)
        {
            _logger.LogInformation(
                "[NOTIFICATION-INAPP] Nema primalaca (role={Role}) — Subject={Subject}",
                request.RecipientRole ?? "N/A", request.Subject);
            return;
        }

        var now = DateTime.UtcNow;
        var deduplicationWindow = now.AddMinutes(-5);

        foreach (var userId in recipientIds)
        {
            var dedupKey = $"InApp:{userId}:{request.RelatedEntityType}:{request.RelatedEntityId}:{request.Subject}";

            var isDuplicate = await _db.Notifications
                .Where(n => n.DeduplicationKey == dedupKey && n.CreatedAt >= deduplicationWindow)
                .AnyAsync(ct);

            if (isDuplicate)
            {
                _logger.LogInformation(
                    "[NOTIFICATION-DEDUP] Preskoćena dupla notifikacija za {User} — {Subject}", userId, request.Subject);
                continue;
            }

            var notification = DomainNotification.CreateInApp(
                userId, request.Subject, request.Message, request.RelatedEntityType, request.RelatedEntityId);
            notification.MarkSent(now);
            _db.Notifications.Add(notification);
        }

        await _db.SaveChangesAsync(ct);
    }

    private async Task SendEmailAsync(NotificationRequest request, string recipientEmail, CancellationToken ct)
    {
        var message = new MimeMessage();
        message.From.Add(new MailboxAddress(_smtp.FromName, _smtp.FromAddress));
        message.To.Add(MailboxAddress.Parse(recipientEmail));
        message.Subject = request.Subject;
        var body = request.Message;
        if (request.RelatedEntityType == "AppraisalOrder" && !string.IsNullOrWhiteSpace(request.RelatedEntityId))
        {
            var appUrl = !string.IsNullOrWhiteSpace(_smtp.AppBaseUrl) ? _smtp.AppBaseUrl.TrimEnd('/') : "";
            if (!string.IsNullOrWhiteSpace(appUrl))
                body += $"\n\nPristup aplikaciji: {appUrl}/narudzbe/{request.RelatedEntityId}";
        }
        message.Body = new TextPart("plain") { Text = body };

        if (request.RelatedEntityType == "AppraisalOrder" && !string.IsNullOrWhiteSpace(request.RelatedEntityId))
        {
            var domain = !string.IsNullOrWhiteSpace(_smtp.FromAddress) && _smtp.FromAddress.Contains('@')
                ? _smtp.FromAddress.Split('@')[1]
                : "procjene.app";
            var threadId = $"<order-{request.RelatedEntityId}@{domain}>";
            message.Headers.Add("References", threadId);
            message.Headers.Add("In-Reply-To", threadId);
            message.MessageId = $"order-{request.RelatedEntityId}-{DateTime.UtcNow.Ticks}@{domain}";
        }

        using var client = new SmtpClient();

        var socketOptions = _smtp.UseSsl ? SecureSocketOptions.SslOnConnect : SecureSocketOptions.StartTlsWhenAvailable;
        await client.ConnectAsync(_smtp.Host, _smtp.Port, socketOptions, ct);

        if (!string.IsNullOrWhiteSpace(_smtp.Username))
            await client.AuthenticateAsync(_smtp.Username, _smtp.Password, ct);

        await client.SendAsync(message, ct);
        await client.DisconnectAsync(true, ct);

        _logger.LogInformation("[EMAIL-SENT] To={Email} Subject={Subject}", recipientEmail, request.Subject);
    }

    public Task<IReadOnlyList<NotificationItem>> GetForUserAsync(
        string userId, int page = 1, int pageSize = 20, CancellationToken ct = default)
    {
        IReadOnlyList<NotificationItem> empty = [];
        return Task.FromResult(empty);
    }

    public Task MarkReadAsync(int notificationId, string userId, CancellationToken ct = default)
        => Task.CompletedTask;
}
