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

/// <summary>
/// CO provjera pristupa prije narudžbe (US-93) — "Uredan pristup" / "Dopuna".
/// </summary>
public sealed class AccessCheckService : IAccessCheckService
{
    private readonly ApplicationDbContext  _db;
    private readonly ICurrentUserService   _currentUser;
    private readonly INotificationProvider _notificationProvider;
    private readonly IAuditService         _audit;
    private readonly ILogger<AccessCheckService> _logger;

    public AccessCheckService(
        ApplicationDbContext db,
        ICurrentUserService currentUser,
        INotificationProvider notificationProvider,
        IAuditService audit,
        ILogger<AccessCheckService> logger)
    {
        _db                   = db;
        _currentUser          = currentUser;
        _notificationProvider = notificationProvider;
        _audit                = audit;
        _logger               = logger;
    }

    public async Task<CaDocumentReviewResultDto> ApproveAccessAsync(
        int orderId, string? comment, CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();
        var order = await FindOrderAsync(orderId, ct);

        if (order.Status != AppraisalOrderStatus.AccessCheckRequested)
            throw new ConflictException(
                "Provjera pristupa je dozvoljena samo dok je narudžba u statusu zahtjeva za provjeru pristupa.",
                "ACCESS_CHECK_INVALID_STATUS");

        var accessCheckTask = await FindActiveTaskAsync(orderId, TaskItemType.AccessCheckCO, ct)
            ?? throw new ConflictException(
                "Aktivan zadatak provjere pristupa nije pronađen.",
                "ACCESS_CHECK_TASK_NOT_FOUND");

        var now = DateTime.UtcNow;
        var oldStatus = order.Status;

        order.ApproveAccessCheck(now);
        if (order.CoDocumentationReviewStartedAt is null)
            order.StartCoDocumentationReview(now);
        accessCheckTask.Complete(userId, comment ?? "Pristup potvrđen — uredan.", now);

        _db.TaskItems.Add(TaskItem.Create(
            orderId:      order.Id,
            type:         TaskItemType.SelectAppraiser,
            title:        $"Odabir vještaka — {order.OrderNumber}",
            description:  null,
            assignedRole: ApplicationAppRoles.KolateralAdministrator));

        await _db.SaveChangesAsync(ct);

        var notificationSent = await NotifyRoleAsync(
            ApplicationAppRoles.KolateralAdministrator,
            "Pristup potvrđen — spremno za izbor vještaka",
            $"Narudžba {order.OrderNumber} — {order.Title}: CO je potvrdio uredan pristup. Narudžba je spremna za odabir vještaka.",
            order.Id, ct);

        await NotifyOrderCreatorAsync(
            order,
            "Pristup uredan — procjena se može nastaviti",
            $"Narudžba {order.OrderNumber} — {order.Title}: CO je potvrdio uredan pristup. Procjena se može nastaviti.",
            ct);

        await RecordAuditAsync(
            AuditActions.OrderAccessCheckApproved, order, oldStatus, notificationSent,
            new { Comment = comment }, ct);

        return new CaDocumentReviewResultDto(
            order.Id, order.OrderNumber, order.Status.ToString(), (int)order.Status,
            notificationSent, "Pristup potvrđen. Narudžba je spremna za odabir vještaka.");
    }

    public async Task<CaDocumentReviewResultDto> RejectAccessAsync(
        int orderId, string comment, CancellationToken ct = default)
    {
        if (string.IsNullOrWhiteSpace(comment))
            throw new ValidationException("comment", "Komentar je obavezan prilikom traženja dopune.");

        var userId = RequireCurrentUserId();
        var order = await FindOrderAsync(orderId, ct);

        if (order.Status != AppraisalOrderStatus.AccessCheckRequested)
            throw new ConflictException(
                "Provjera pristupa je dozvoljena samo dok je narudžba u statusu zahtjeva za provjeru pristupa.",
                "ACCESS_CHECK_INVALID_STATUS");

        var accessCheckTask = await FindActiveTaskAsync(orderId, TaskItemType.AccessCheckCO, ct)
            ?? throw new ConflictException(
                "Aktivan zadatak provjere pristupa nije pronađen.",
                "ACCESS_CHECK_TASK_NOT_FOUND");

        var now = DateTime.UtcNow;
        var oldStatus = order.Status;

        order.RejectAccessCheck(now);
        accessCheckTask.Complete(userId, comment, now);

        _db.TaskItems.Add(TaskItem.Create(
            orderId:      order.Id,
            type:         TaskItemType.ReviewDocumentation,
            title:        $"Pregled dokumentacije — {order.OrderNumber}",
            description:  comment,
            assignedRole: ApplicationAppRoles.KolateralAdministrator));

        await _db.SaveChangesAsync(ct);

        var notificationSent = await NotifyRoleAsync(
            ApplicationAppRoles.KolateralAdministrator,
            "CO traži dopunu — provjera pristupa",
            $"Narudžba {order.OrderNumber} — {order.Title}: CO traži dopunu prije provjere pristupa. Komentar: {comment}",
            order.Id, ct);

        await NotifyOrderCreatorAsync(
            order,
            "CO traži dopunu — provjera pristupa",
            $"Narudžba {order.OrderNumber} — {order.Title}: CO traži dopunu prije provjere pristupa. Komentar: {comment}",
            ct);

        await RecordAuditAsync(
            AuditActions.OrderAccessCheckRejected, order, oldStatus, notificationSent,
            new { Comment = comment }, ct);

        return new CaDocumentReviewResultDto(
            order.Id, order.OrderNumber, order.Status.ToString(), (int)order.Status,
            notificationSent, "CO traži dopunu prije provjere pristupa. Narudžba je vraćena CA na ponovni pregled.");
    }

    // ── Pomoćne metode ────────────────────────────────────────────────────

    private async Task<AppraisalOrder> FindOrderAsync(int orderId, CancellationToken ct)
    {
        var order = await _db.AppraisalOrders.FirstOrDefaultAsync(x => x.Id == orderId, ct);

        if (order is null)
            throw new NotFoundException(
                $"Narudžba procjene ID={orderId} nije pronađena.",
                "APPRAISAL_ORDER_NOT_FOUND");

        return order;
    }

    private async Task<TaskItem?> FindActiveTaskAsync(int orderId, TaskItemType type, CancellationToken ct) =>
        await _db.TaskItems
            .Where(x => x.AppraisalOrderId == orderId
                     && x.TaskType == type
                     && x.Status != TaskItemStatus.Completed
                     && x.Status != TaskItemStatus.Cancelled)
            .OrderByDescending(x => x.CreatedAt)
            .FirstOrDefaultAsync(ct);

    private string RequireCurrentUserId()
    {
        if (!_currentUser.IsAuthenticated || string.IsNullOrWhiteSpace(_currentUser.UserId))
            throw new ForbiddenException("Korisnik mora biti prijavljen za ovu akciju.");

        return _currentUser.UserId;
    }

    private async Task<bool> NotifyRoleAsync(
        string role, string subject, string message, int orderId, CancellationToken ct)
    {
        try
        {
            await _notificationProvider.SendAsync(new NotificationRequest(
                RecipientUserId:   null,
                RecipientRole:     role,
                Channel:           NotificationChannel.InApp,
                Subject:           subject,
                Message:           message,
                RelatedEntityType: "AppraisalOrder",
                RelatedEntityId:   orderId.ToString()
            ), ct);

            return true;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Greška pri slanju notifikacije roli {Role} za narudžbu {OrderId}", role, orderId);
            return false;
        }
    }

    private async Task NotifyOrderCreatorAsync(
        AppraisalOrder order, string subject, string message, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(order.CreatedByUserId))
        {
            await NotifyRoleAsync(
                order.CreatedByRole ?? ApplicationAppRoles.ProdajaSegment, subject, message, order.Id, ct);
            return;
        }

        try
        {
            await _notificationProvider.SendAsync(new NotificationRequest(
                RecipientUserId:   order.CreatedByUserId,
                RecipientRole:     null,
                Channel:           NotificationChannel.InApp,
                Subject:           subject,
                Message:           message,
                RelatedEntityType: "AppraisalOrder",
                RelatedEntityId:   order.Id.ToString()
            ), ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Greška pri slanju notifikacije korisniku {UserId} za narudžbu {OrderId}",
                order.CreatedByUserId, order.Id);
        }
    }

    private async Task RecordAuditAsync(
        string action, AppraisalOrder order, AppraisalOrderStatus oldStatus,
        bool notificationSent, object extra, CancellationToken ct)
    {
        try
        {
            await _audit.RecordAsync(new AuditEvent
            {
                Action            = action,
                OperationType     = AuditOperationTypes.Update,
                Module            = AuditModules.AppraisalOrders,
                EntityType        = "AppraisalOrder",
                EntityKey         = order.Id.ToString(),
                EntityDisplayName = order.OrderNumber,
                OldValues         = new { Status = oldStatus.ToString() },
                NewValues         = new { Status = order.Status.ToString(), NotificationSent = notificationSent, Extra = extra },
                Status            = AuditStatuses.Success,
                Severity          = AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Audit log nije zapisan za akciju {Action} narudžbe {OrderId}.", action, order.Id);
        }
    }
}
