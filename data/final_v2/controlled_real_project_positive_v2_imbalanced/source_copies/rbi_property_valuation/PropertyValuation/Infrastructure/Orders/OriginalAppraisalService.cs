using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using ApplicationAppRoles = RBBH.CollateralAppraisal.Application.Security.AppRoles;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

public sealed class OriginalAppraisalService : IOriginalAppraisalService
{
    private const string OriginalReceivedSubject = "Original procjene preuzet";
    private const string AppraiserReminderSubject = "Podsjetnik: dostavite original procjene u poslovnicu";

    private const string OrderOriginalReceivedAction = "ORDER_ORIGINAL_RECEIVED";
    private const string OrderAppraiserReminderSentAction = "ORDER_APPRAISER_REMINDER_SENT";

    private readonly ApplicationDbContext _db;
    private readonly ICurrentUserService _currentUser;
    private readonly INotificationService _notificationService;
    private readonly IAuditService _auditService;
    private readonly ILogger<OriginalAppraisalService> _logger;

    public OriginalAppraisalService(
        ApplicationDbContext db,
        ICurrentUserService currentUser,
        INotificationService notificationService,
        IAuditService auditService,
        ILogger<OriginalAppraisalService> logger)
    {
        _db = db;
        _currentUser = currentUser;
        _notificationService = notificationService;
        _auditService = auditService;
        _logger = logger;
    }

    // ── 1. Preuzet original procjene ─────────────────────────────────────
// ── AC6: Vještak dostavlja original u poslovnicu ─────────────────────

    public async Task<DeliverOriginalResultDto> DeliverOriginalToOfficeAsync(
        int orderId,
        CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();
        var order  = await FindOrderAsync(orderId, ct);

        if (order.Status is not (AppraisalOrderStatus.ReadyForProcedure
                                or AppraisalOrderStatus.COApproved))
            throw new ConflictException(
                "Original se može dostaviti samo nakon CO odobrenja procjene.",
                "ORIGINAL_DELIVERY_INVALID_STATUS");

        var alreadyDelivered = await _db.TaskItems.AnyAsync(
            t => t.AppraisalOrderId == orderId
              && t.TaskType == TaskItemType.DeliverOriginalToOffice
              && t.Status == TaskItemStatus.Completed, ct);

        if (alreadyDelivered)
            throw new ConflictException(
                "Original procjene je već označen kao dostavljen u poslovnicu.",
                "ORIGINAL_ALREADY_DELIVERED");

        var now = DateTime.UtcNow;

        // Kreira i odmah zatvara task — vještak jednim klikom potvrđuje dostavu
        var task = TaskItem.Create(
            orderId:        order.Id,
            type:           TaskItemType.DeliverOriginalToOffice,
            title:          "Original procjene dostavljen u poslovnicu",
            description:    $"Vještak potvrdio dostavu originalnog dokumenta procjene za narudžbu {order.OrderNumber}.",
            assignedRole:   ApplicationAppRoles.Vjestak,
            assignedUserId: userId);

        task.Accept(userId, now);
        task.Complete(userId, "Vještak potvrdio dostavu originala.", now);

        _db.TaskItems.Add(task);
        await _db.SaveChangesAsync(ct);

        try
        {
            await _auditService.RecordAsync(new AuditEvent
            {
                Action            = "ORDER_ORIGINAL_DELIVERED_BY_APPRAISER",
                OperationType     = AuditOperationTypes.Update,
                Module            = AuditModules.AppraisalOrders,
                EntityType        = nameof(AppraisalOrder),
                EntityKey         = order.Id.ToString(),
                EntityDisplayName = order.OrderNumber,
                NewValues         = new { DeliveredByUserId = userId, DeliveredAt = now },
                Status            = AuditStatuses.Success,
                Severity          = AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Audit za dostavu originala narudžbe {OrderId} nije zapisan.", order.Id);
        }

        return new DeliverOriginalResultDto(
            order.Id,
            order.OrderNumber,
            now,
            userId,
            "Original procjene označen kao dostavljen u poslovnicu.");
    }




    public async Task<OriginalReceivedResultDto> ConfirmOriginalReceivedAsync(
        int orderId,
        CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();
        var order = await FindOrderAsync(orderId, ct);

        EnsureCanConfirmOriginalReceived(order);

        var oldStatus = order.Status;
        var now = DateTime.UtcNow;
        order.ConfirmOriginalReceived(userId, now);

        await _db.SaveChangesAsync(ct);

        var notificationsSent = await NotifyOriginalReceivedAsync(order, ct);
        await RecordOriginalReceivedAuditAsync(order, oldStatus, notificationsSent, ct);

        return new OriginalReceivedResultDto(
            order.Id,
            order.OrderNumber,
            order.Status.ToString(),
            order.OriginalReceivedAt!.Value,
            order.OriginalReceivedByUserId!,
            notificationsSent,
            BuildOriginalReceivedMessage(order));
    }

    // ── 2. Reminder vještaku ─────────────────────────────────────────────

    public async Task<AppraiserReminderResultDto> SendAppraiserReminderAsync(
        int orderId,
        CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();
        var order = await FindOrderAsync(orderId, ct);

        EnsureCanSendAppraiserReminder(order);

        var now = DateTime.UtcNow;
        order.RecordAppraiserReminder(now);
        await _db.SaveChangesAsync(ct);

        var notificationSent = await NotifyAppraiserAsync(order, ct);
        await RecordReminderAuditAsync(order, userId, notificationSent, ct);

        return new AppraiserReminderResultDto(
            order.Id,
            order.OrderNumber,
            order.AppraiserReminderCount,
            order.AppraiserReminderLastSentAt!.Value,
            notificationSent,
            $"Reminder #{order.AppraiserReminderCount} evidentiran za narudžbu {order.OrderNumber}.");
    }

    // ── Validacije ───────────────────────────────────────────────────────

    private static void EnsureCanConfirmOriginalReceived(AppraisalOrder order)
    {
        // Potvrda preuzimanja finalizira narudžbu (status → Completed), pa dvostruku
        // potvrdu prepoznajemo po OriginalReceivedAt (status više ne ostaje OriginalReceived).
        if (order.OriginalReceivedAt is not null
            || order.Status == AppraisalOrderStatus.Completed)
            throw new ConflictException(
                "Original procjene je već preuzet za ovu narudžbu.",
                "ORIGINAL_ALREADY_RECEIVED");

        if (order.Status != AppraisalOrderStatus.ReadyForProcedure)
            throw new ConflictException(
                "Preuzimanje originala je dozvoljeno tek kada CO odobri procjenu (status ReadyForProcedure).",
                "ORIGINAL_INVALID_STATUS");
    }

    private static void EnsureCanSendAppraiserReminder(AppraisalOrder order)
    {
        if (order.OriginalReceivedAt is not null)
            throw new ConflictException(
                "Reminder vještaku nije dozvoljen jer je original procjene već preuzet.",
                "APPRAISER_REMINDER_NOT_ALLOWED");
    }

    // ── Pomoćne metode ────────────────────────────────────────────────────

    private async Task<AppraisalOrder> FindOrderAsync(int orderId, CancellationToken ct)
    {
        var order = await _db.AppraisalOrders
            .FirstOrDefaultAsync(x => x.Id == orderId, ct);

        if (order is null)
            throw new NotFoundException(
                $"Narudžba procjene ID={orderId} nije pronađena.",
                "APPRAISAL_ORDER_NOT_FOUND");

        return order;
    }

    private string RequireCurrentUserId()
    {
        if (!_currentUser.IsAuthenticated || string.IsNullOrWhiteSpace(_currentUser.UserId))
            throw new ForbiddenException("Korisnik mora biti prijavljen za ovu akciju.");

        return _currentUser.UserId;
    }

    // ── Notifikacije ──────────────────────────────────────────────────────

    private async Task<bool> NotifyOriginalReceivedAsync(AppraisalOrder order, CancellationToken ct)
    {
        var subject = OriginalReceivedSubject;
        var message = BuildOriginalReceivedMessage(order);

        var recipients = new List<string>();
        if (!string.IsNullOrWhiteSpace(order.AcceptedByCAUserId))
            recipients.Add(order.AcceptedByCAUserId);
        if (!string.IsNullOrWhiteSpace(order.CoApprovedByUserId))
            recipients.Add(order.CoApprovedByUserId);

        if (recipients.Count == 0)
        {
            _logger.LogWarning(
                "Narudžba {OrderId} nema poznate CA/CO korisnike; notifikacije o preuzimanju originala nisu poslane.",
                order.Id);
            return false;
        }

        var anySent = false;
        foreach (var recipientUserId in recipients.Distinct())
        {
            try
            {
                await _notificationService.NotifyUserAsync(
                    recipientUserId,
                    subject,
                    message,
                    relatedEntityType: nameof(AppraisalOrder),
                    relatedEntityId: order.Id.ToString(),
                    ct: ct);
                anySent = true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex,
                    "Notifikacija o preuzimanju originala nije poslana korisniku {UserId} za narudžbu {OrderId}.",
                    recipientUserId, order.Id);
            }
        }

        return anySent;
    }

    private async Task<bool> NotifyAppraiserAsync(AppraisalOrder order, CancellationToken ct)
    {
        // Vještak je u domeni vezan preko AppraiserId (int). Trenutno sistem nema
        // direktnu mapu Appraiser→UserAccount, pa reminder primarno evidentiramo
        // u bazi i audit logu. Kada se uvede mapiranje (ili eksterni email),
        // ovdje ide stvarna isporuka notifikacije.
        if (order.AppraiserId is null)
        {
            _logger.LogWarning(
                "Narudžba {OrderId} nema dodijeljenog vještaka; reminder je samo evidentiran u bazi (count={Count}).",
                order.Id, order.AppraiserReminderCount);
            return false;
        }

        var subject = AppraiserReminderSubject;
        var message =
            $"{AppraiserReminderSubject} za narudžbu {order.OrderNumber} " +
            $"(klijent: {order.ClientName}). Ovo je podsjetnik broj {order.AppraiserReminderCount}.";

        try
        {
            // AppraiserId se šalje kao logički recipient identifier; implementacija servisa
            // interno razrješava email/Keycloak korisnika.
            await _notificationService.NotifyUserAsync(
                order.AppraiserId.Value.ToString(),
                subject,
                message,
                relatedEntityType: nameof(AppraisalOrder),
                relatedEntityId: order.Id.ToString(),
                ct: ct);
            return true;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Reminder vještaku (AppraiserId={AppraiserId}) nije poslan za narudžbu {OrderId}; reminder je evidentiran u bazi.",
                order.AppraiserId, order.Id);
            return false;
        }
    }

    // ── Audit ─────────────────────────────────────────────────────────────

    private async Task RecordOriginalReceivedAuditAsync(
        AppraisalOrder order,
        AppraisalOrderStatus oldStatus,
        bool notificationsSent,
        CancellationToken ct)
    {
        try
        {
            await _auditService.RecordAsync(new AuditEvent
            {
                Action = OrderOriginalReceivedAction,
                OperationType = AuditOperationTypes.Update,
                Module = AuditModules.AppraisalOrders,
                EntityType = nameof(AppraisalOrder),
                EntityKey = order.Id.ToString(),
                EntityDisplayName = order.OrderNumber,
                OldValues = new { Status = oldStatus.ToString() },
                NewValues = new
                {
                    Status = order.Status.ToString(),
                    order.OriginalReceivedAt,
                    order.OriginalReceivedByUserId,
                    NotificationsSent = notificationsSent
                },
                Status = AuditStatuses.Success,
                Severity = AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Audit log nije zapisan za preuzimanje originala narudžbe {OrderId}.",
                order.Id);
        }
    }

    private async Task RecordReminderAuditAsync(
        AppraisalOrder order,
        string actorUserId,
        bool notificationSent,
        CancellationToken ct)
    {
        try
        {
            await _auditService.RecordAsync(new AuditEvent
            {
                Action = OrderAppraiserReminderSentAction,
                OperationType = AuditOperationTypes.Update,
                Module = AuditModules.AppraisalOrders,
                EntityType = nameof(AppraisalOrder),
                EntityKey = order.Id.ToString(),
                EntityDisplayName = order.OrderNumber,
                NewValues = new
                {
                    order.AppraiserId,
                    order.AppraiserReminderCount,
                    order.AppraiserReminderLastSentAt,
                    ActorUserId = actorUserId,
                    NotificationSent = notificationSent
                },
                Status = AuditStatuses.Success,
                Severity = AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Audit log nije zapisan za slanje remindera vještaku za narudžbu {OrderId}.",
                order.Id);
        }
    }

    // ── 3. Saglasnost klijenta (PL) ──────────────────────────────────────

    public async Task<SignConsentResultDto> SignSalesConsentAsync(
        int orderId, CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();
        var order  = await FindOrderAsync(orderId, ct);

        if (!order.IsPL())
            throw new ConflictException(
                "Saglasnost klijenta je dostupna samo za PL narudžbe.",
                "CONSENT_NOT_PL");

        if (order.SalesConsentSigned)
            throw new ConflictException(
                "Saglasnost je već evidentirana za ovu narudžbu.",
                "CONSENT_ALREADY_SIGNED");

        var now      = DateTime.UtcNow;
        var userName = _currentUser.FullName ?? _currentUser.Username ?? userId;

        order.SignSalesConsent(userName, now);
        await _db.SaveChangesAsync(ct);

        try
        {
            await _auditService.RecordAsync(new AuditEvent
            {
                Action            = "ORDER_SALES_CONSENT_SIGNED",
                OperationType     = AuditOperationTypes.Update,
                Module            = AuditModules.AppraisalOrders,
                EntityType        = nameof(AppraisalOrder),
                EntityKey         = order.Id.ToString(),
                EntityDisplayName = order.OrderNumber,
                NewValues         = new { SignedByName = userName, SignedAt = now },
                Status            = AuditStatuses.Success,
                Severity          = AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Audit log nije zapisan za potpisivanje saglasnosti narudžbe {OrderId}.", order.Id);
        }

        return new SignConsentResultDto(
            order.Id,
            order.OrderNumber,
            now,
            userName,
            "Saglasnost klijenta evidentirana.");
    }

    // ── Builders ──────────────────────────────────────────────────────────

    private static string BuildOriginalReceivedMessage(AppraisalOrder order)
    {
        var client = order.ClientName;
        var type = order.ClientType ?? "N/A";
        var city = order.City ?? "N/A";

        return $"{OriginalReceivedSubject} za klijenta {client} (tip: {type}, grad: {city}).";
    }
}
