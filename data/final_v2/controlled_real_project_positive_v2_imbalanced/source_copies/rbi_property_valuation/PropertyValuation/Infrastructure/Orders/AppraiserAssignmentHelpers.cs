using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

/// <summary>
/// Zajednički helperi za sve AppraiserAssignment sub-servise (I-2 refactoring).
/// Enkapsulira: FindOrderAsync, FindActiveTaskAsync, RequireCurrentUserId,
/// NotifyRoleAsync, NotifyUserAsync, RecordAuditAsync.
/// </summary>
internal sealed class AppraiserAssignmentHelpers
{
    private readonly ApplicationDbContext  _db;
    private readonly ICurrentUserService   _currentUser;
    private readonly INotificationProvider _notificationProvider;
    private readonly IAuditService         _audit;
    private readonly ILogger               _logger;

    public AppraiserAssignmentHelpers(
        ApplicationDbContext  db,
        ICurrentUserService   currentUser,
        INotificationProvider notificationProvider,
        IAuditService         audit,
        ILogger               logger)
    {
        _db                   = db;
        _currentUser          = currentUser;
        _notificationProvider = notificationProvider;
        _audit                = audit;
        _logger               = logger;
    }

    public async Task<AppraisalOrder> FindOrderAsync(int orderId, CancellationToken ct)
    {
        var order = await _db.AppraisalOrders.FirstOrDefaultAsync(x => x.Id == orderId, ct);
        return order ?? throw new NotFoundException(
            $"Narudžba procjene ID={orderId} nije pronađena.", "APPRAISAL_ORDER_NOT_FOUND");
    }

    public async Task<TaskItem?> FindActiveTaskAsync(int orderId, TaskItemType type, CancellationToken ct) =>
        await _db.TaskItems
            .Where(x => x.AppraisalOrderId == orderId
                     && x.TaskType == type
                     && x.Status != TaskItemStatus.Completed
                     && x.Status != TaskItemStatus.Cancelled)
            .OrderByDescending(x => x.CreatedAt)
            .FirstOrDefaultAsync(ct);

    public string RequireCurrentUserId()
    {
        if (!_currentUser.IsAuthenticated || string.IsNullOrWhiteSpace(_currentUser.UserId))
            throw new ForbiddenException("Korisnik mora biti prijavljen za ovu akciju.");
        return _currentUser.UserId;
    }

    public async Task<bool> NotifyRoleAsync(
        string role, string subject, string message, int orderId, CancellationToken ct)
    {
        try
        {
            await _notificationProvider.SendAsync(new NotificationRequest(
                RecipientUserId: null, RecipientRole: role,
                Channel: NotificationChannel.InApp, Subject: subject, Message: message,
                RelatedEntityType: "AppraisalOrder", RelatedEntityId: orderId.ToString()
            ), ct);
            return true;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Greška pri slanju notifikacije roli {Role} za narudžbu {OrderId}", role, orderId);
            return false;
        }
    }

    public async Task<bool> NotifyUserAsync(
        string userId, string subject, string message, int orderId, CancellationToken ct)
    {
        try
        {
            await _notificationProvider.SendAsync(new NotificationRequest(
                RecipientUserId: userId, RecipientRole: null,
                Channel: NotificationChannel.InApp, Subject: subject, Message: message,
                RelatedEntityType: "AppraisalOrder", RelatedEntityId: orderId.ToString()
            ), ct);
            return true;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Greška pri in-app notifikaciji korisniku {UserId} za narudžbu {OrderId}", userId, orderId);
            return false;
        }
    }

    public async Task RecordAuditAsync(
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
            _logger.LogError(ex, "Audit log nije zapisan za akciju {Action} narudžbe {OrderId}.", action, order.Id);
        }
    }
}
