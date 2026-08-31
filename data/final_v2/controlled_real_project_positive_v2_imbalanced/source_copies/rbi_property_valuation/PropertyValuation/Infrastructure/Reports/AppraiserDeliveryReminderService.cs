using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Reports;
using RBBH.CollateralAppraisal.Application.Reports.Dtos;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Reports;

/// <summary>
/// Implementacija S3-15: Reminder vještaku za dostavu procjene.
///
/// Filter: narudžba je u "aktivnom" statusu kod vještaka
///         I OrderSentToAppraiserAt > N radnih dana.
/// Notifikacija: "U kojem je statusu izrada procjene za klijenta XY?"
/// Ovlaštenje: isključivo CA (AppPermissions.OrdersRemindAppraiser).
/// </summary>
public sealed class AppraiserDeliveryReminderService : IAppraiserDeliveryReminderService
{
    // Statusi koji znače da je narudžba kod vještaka ("u obradi")
    private static readonly HashSet<AppraisalOrderStatus> AppraiserActiveStatuses =
    [
        AppraisalOrderStatus.OrderSentToAppraiser,
        AppraisalOrderStatus.AppraisalInProgress,
        AppraisalOrderStatus.AdditionalPaymentRequested,
        AppraisalOrderStatus.AdditionalPaymentCompleted
    ];

    private readonly ApplicationDbContext    _db;
    private readonly INotificationProvider   _notifications;
    private readonly IAuditService           _audit;
    private readonly ICurrentUserService     _currentUser;
    private readonly ILogger<AppraiserDeliveryReminderService> _logger;

    public AppraiserDeliveryReminderService(
        ApplicationDbContext                           db,
        INotificationProvider                         notifications,
        IAuditService                                 audit,
        ICurrentUserService                           currentUser,
        ILogger<AppraiserDeliveryReminderService>     logger)
    {
        _db            = db;
        _notifications = notifications;
        _audit         = audit;
        _currentUser   = currentUser;
        _logger        = logger;
    }

    public async Task<AppraiserReminderReportDto> GetOverdueAppraisalsAsync(
        int?  appraiserId,
        int   minBusinessDays,
        int   page,
        int   pageSize,
        CancellationToken ct = default)
    {
        // Cutoff = danas minus N radnih dana (samo radni dani se računaju)
        var cutoff = BusinessDaysHelper.SubtractBusinessDays(DateTime.UtcNow, minBusinessDays);

        var query = _db.AppraisalOrders
            .AsNoTracking()
            .Where(o => AppraiserActiveStatuses.Contains(o.Status)
                     && o.OrderSentToAppraiserAt.HasValue
                     && o.OrderSentToAppraiserAt.Value < cutoff);

        if (appraiserId.HasValue)
            query = query.Where(o => o.AppraiserId == appraiserId.Value);

        var total = await query.CountAsync(ct);

        var orders = await query
            .OrderBy(o => o.OrderSentToAppraiserAt)   // najduže čekanje prvo
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Select(o => new
            {
                o.Id, o.OrderNumber, o.ClientName, o.City, o.Status,
                o.AppraiserId, o.OrderSentToAppraiserAt, o.AppraisalDeliveredToCoAt
            })
            .ToListAsync(ct);

        // Dohvati vještake za prikazivanje imena i emaila
        var appraiserIds = orders
            .Where(o => o.AppraiserId.HasValue)
            .Select(o => o.AppraiserId!.Value)
            .Distinct()
            .ToList();

        var appraisers = await _db.Appraisers
            .AsNoTracking()
            .Where(a => appraiserIds.Contains(a.Id))
            .ToDictionaryAsync(a => a.Id, ct);

        var now   = DateTime.UtcNow;
        var dtos  = orders.Select(o =>
        {
            var appraiser = o.AppraiserId.HasValue && appraisers.TryGetValue(o.AppraiserId.Value, out var a) ? a : null;
            var daysBusiness = o.OrderSentToAppraiserAt.HasValue
                ? BusinessDaysHelper.BusinessDaysBetween(o.OrderSentToAppraiserAt.Value, now)
                : 0;

            return new ReminderOrderDto(
                OrderId:                  o.Id,
                OrderNumber:              o.OrderNumber,
                ClientName:               o.ClientName,
                City:                     o.City ?? string.Empty,
                OrderStatus:              o.Status.ToString(),
                StatusLabel:              ToStatusLabel(o.Status),
                AppraiserId:              o.AppraiserId,
                AppraiserName:            appraiser?.Name,
                AppraiserEmail:           appraiser?.ContactEmail,
                OrderSentToAppraiserAt:   o.OrderSentToAppraiserAt,
                AppraisalDeliveredToCoAt: o.AppraisalDeliveredToCoAt,
                BusinessDaysOverdue:      daysBusiness);
        }).ToList();

        return new AppraiserReminderReportDto(total, dtos, now, minBusinessDays);
    }

    public async Task<ReminderSentResultDto> SendAppraisalStatusReminderAsync(
        int orderId, CancellationToken ct = default)
    {
        var order = await _db.AppraisalOrders
            .AsNoTracking()
            .FirstOrDefaultAsync(o => o.Id == orderId, ct)
            ?? throw new KeyNotFoundException($"Narudžba {orderId} nije pronađena.");

        if (!AppraiserActiveStatuses.Contains(order.Status))
            throw new InvalidOperationException(
                $"Reminder nije moguć — narudžba nije u statusu 'u obradi'. Status: {order.Status}");

        var appraiser = order.AppraiserId.HasValue
            ? await _db.Appraisers.AsNoTracking().FirstOrDefaultAsync(a => a.Id == order.AppraiserId.Value, ct)
            : null;

        var notificationSent = false;

        // Slanje email notifikacije vještaku (S3-15 spec: "U kojem je statusu izrada procjene za klijenta XY?")
        if (appraiser?.ContactEmail is not null)
        {
            try
            {
                await _notifications.SendAsync(new NotificationRequest(
                    RecipientUserId:   null,
                    RecipientRole:     null,
                    Channel:           NotificationChannel.Email,
                    Subject:           $"Status izrade procjene — {order.OrderNumber}",
                    Message:           $"Poštovani/a {appraiser.Name},\n\n" +
                                       $"U kojem je statusu izrada procjene za klijenta {order.ClientName}" +
                                       (string.IsNullOrEmpty(order.City) ? "" : $" — {order.City}") +
                                       $"?\n\nBroj narudžbe: {order.OrderNumber}.\n\n" +
                                       $"Molim vas da nas informišete o trenutnom statusu i očekivanom datumu dostave procjene.",
                    RelatedEntityType: "AppraisalOrder",
                    RelatedEntityId:   orderId.ToString(),
                    RecipientEmail:    appraiser.ContactEmail
                ), ct);

                notificationSent = true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex,
                    "Reminder email nije poslan vještaku {AppraiserId} za narudžbu {OrderId}.",
                    appraiser.Id, orderId);
            }
        }
        else
        {
            _logger.LogWarning(
                "Vještak za narudžbu {OrderId} nema email adresu — reminder je samo zabilježen.",
                orderId);
        }

        // Audit
        try
        {
            await _audit.RecordAsync(new AuditEvent
            {
                Action            = "APPRAISER_DELIVERY_STATUS_REMINDER_SENT",
                OperationType     = AuditOperationTypes.Update,
                Module            = AuditModules.AppraisalOrders,
                EntityType        = "AppraisalOrder",
                EntityKey         = orderId.ToString(),
                EntityDisplayName = order.OrderNumber,
                NewValues         = new
                {
                    AppraiserId     = order.AppraiserId,
                    AppraiserEmail  = appraiser?.ContactEmail,
                    NotificationSent = notificationSent,
                    Message         = "U kojem je statusu izrada procjene?"
                },
                Status   = AuditStatuses.Success,
                Severity = AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Audit za reminder nije zapisan za narudžbu {OrderId}.", orderId);
        }

        return new ReminderSentResultDto(
            orderId,
            order.OrderNumber,
            notificationSent,
            notificationSent
                ? $"Reminder poslan vještaku {appraiser?.Name} ({appraiser?.ContactEmail})."
                : "Reminder evidentiran ali email nije poslan (vještak nema email adresu).");
    }

    private static string ToStatusLabel(AppraisalOrderStatus status) => status switch
    {
        AppraisalOrderStatus.OrderSentToAppraiser          => "Poslano vještaku",
        AppraisalOrderStatus.AppraisalInProgress           => "Procjena u toku",
        AppraisalOrderStatus.AdditionalPaymentRequested    => "Zahtjev za doplatu",
        AppraisalOrderStatus.AdditionalPaymentCompleted    => "Doplata izvršena",
        _                                                  => status.ToString()
    };
}
