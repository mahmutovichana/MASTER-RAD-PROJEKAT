using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using AppRoles = RBBH.CollateralAppraisal.Application.Security.AppRoles;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

public sealed class WorkflowTaskService : IWorkflowTaskService
{
    private readonly ApplicationDbContext         _db;
    private readonly ICurrentUserService          _currentUser;
    private readonly IAuditService                _audit;
    private readonly INotificationProvider        _notifications;
    private readonly ILogger<WorkflowTaskService> _logger;

    public WorkflowTaskService(
        ApplicationDbContext db,
        ICurrentUserService currentUser,
        IAuditService audit,
        INotificationProvider notifications,
        ILogger<WorkflowTaskService> logger)
    {
        _db            = db;
        _currentUser   = currentUser;
        _audit         = audit;
        _notifications = notifications;
        _logger        = logger;
    }

    public async Task<PagedResult<WorkflowTaskDto>> GetMyTasksAsync(
        int page = 1, int pageSize = 20, CancellationToken ct = default)
    {
        var userId = _currentUser.UserId;
        var roles  = _currentUser.Roles;

        var query = _db.TaskItems
            .Include(t => t.AppraisalOrder)
            .Where(t => t.Status != TaskItemStatus.Cancelled &&
                        t.Status != TaskItemStatus.Completed &&
                        (t.AssignedUserId == userId ||
                         (t.AssignedUserId == null && roles.Contains(t.AssignedRole!))));

        var total = await query.CountAsync(ct);
        var tasks = await query
            .OrderBy(t => t.DueDate)
            .ThenByDescending(t => t.CreatedAt)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync(ct);

        return new PagedResult<WorkflowTaskDto>
        {
            Items      = tasks.Select(MapToDto).ToList(),
            TotalCount = total,
            Page       = page,
            PageSize   = pageSize
        };
    }

    public async Task<WorkflowTaskDto> AcceptTaskAsync(int taskId, CancellationToken ct = default)
    {
        var task = await _db.TaskItems
            .Include(t => t.AppraisalOrder)
            .FirstOrDefaultAsync(t => t.Id == taskId, ct)
            ?? throw new NotFoundException($"Task s ID-om {taskId} nije pronađen.");

        if (task.IsLocked)
            throw new ValidationException("task", "Task je već prihvatio drugi korisnik.");

        if (task.Status != TaskItemStatus.Open)
            throw new ValidationException("status", "Samo otvoreni taskovi se mogu prihvatiti.");

        var userId = _currentUser.UserId ?? "unknown";
        var now    = DateTime.UtcNow;
        task.Accept(userId, now);

        var isCaAcceptance = task.TaskType == TaskItemType.AcceptCAOrder
                          && task.AppraisalOrder is not null;

        if (isCaAcceptance)
        {
            if (task.AppraisalOrder!.Status == AppraisalOrderStatus.SubmittedBySales)
            {
                task.AppraisalOrder.AcceptByCA(userId, null, now);
                task.AppraisalOrder.StartDocumentationReview(now);
            }
            task.Complete(userId, "Narudžba prihvaćena — pokrenut pregled dokumentacije.", now);

            var reviewExists = await _db.TaskItems.AnyAsync(
                t => t.AppraisalOrderId == task.AppraisalOrder!.Id &&
                     t.TaskType == TaskItemType.ReviewDocumentation &&
                     t.Status   == TaskItemStatus.Open, ct);

            if (!reviewExists)
            {
                _db.TaskItems.Add(TaskItem.Create(
                    orderId:      task.AppraisalOrder!.Id,
                    type:         TaskItemType.ReviewDocumentation,
                    title:        $"Pregled dokumentacije — {task.AppraisalOrder!.OrderNumber}",
                    description:  null,
                    assignedRole: AppRoles.KolateralAdministrator));
            }
        }

        await _db.SaveChangesAsync(ct);

        if (isCaAcceptance)
        {
            await _audit.RecordAsync(new AuditEvent
            {
                Action            = AuditActions.OrderAcceptedByCA,
                OperationType     = AuditOperationTypes.Approve,
                Module            = AuditModules.AppraisalOrders,
                EntityType        = "AppraisalOrder",
                EntityKey         = task.AppraisalOrder!.Id.ToString(),
                EntityDisplayName = task.AppraisalOrder.Title,
                Status            = AuditStatuses.Success,
                Severity          = AuditSeverity.Info,
                NewValues         = new { task.AppraisalOrder.Status }
            }, ct);
        }
        else
        {
            try
            {
                await _audit.RecordAsync(new AuditEvent
                {
                    Action            = AuditActions.TaskAccepted,
                    OperationType     = AuditOperationTypes.Update,
                    Module            = AuditModules.AppraisalOrders,
                    EntityType        = "TaskItem",
                    EntityKey         = task.Id.ToString(),
                    EntityDisplayName = task.Title,
                    Status            = AuditStatuses.Success,
                    Severity          = AuditSeverity.Info,
                    NewValues         = new { task.Status, task.AcceptedByUserId, task.TaskType }
                }, ct);
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Audit za task acceptance {TaskId} nije snimljen.", task.Id);
            }
        }

        await _db.Entry(task).Reference(t => t.AppraisalOrder).LoadAsync(ct);
        return MapToDto(task);
    }

    public async Task<WorkflowTaskDto> CompleteTaskAsync(
        int taskId, string? comment, CancellationToken ct = default)
    {
        var task = await _db.TaskItems
            .Include(t => t.AppraisalOrder)
            .FirstOrDefaultAsync(t => t.Id == taskId, ct)
            ?? throw new NotFoundException($"Task s ID-om {taskId} nije pronađen.");

        if (task.AssignedUserId != _currentUser.UserId)
            throw new ForbiddenException("Samo korisnik koji je prihvatio task može ga završiti.");

        if (task.Status == TaskItemStatus.Completed)
            throw new ValidationException("status", "Task je već završen.");

        // ── AC 2: Datum obilaska mandatoran za UploadFinalAppraisal ──────────
        if (task.TaskType == TaskItemType.UploadFinalAppraisal)
        {
            var order = task.AppraisalOrder
                ?? await _db.AppraisalOrders.FirstOrDefaultAsync(
                    o => o.Id == task.AppraisalOrderId, ct);

            if (order?.AppraiserVisitDate is null)
                throw new ValidationException(
                    "appraiserVisitDate",
                    "Datum obilaska imovine je obavezan prije završetka importa procjene.");
        }

        var now = DateTime.UtcNow;
        task.Complete(_currentUser.UserId!, comment, now);
        await _db.SaveChangesAsync(ct);

        // ── AC 1: Notifikacija CO-u "Završena procjena" ───────────────────────
        if (task.TaskType == TaskItemType.UploadFinalAppraisal)
        {
            var order = task.AppraisalOrder
                ?? await _db.AppraisalOrders.FirstOrDefaultAsync(
                    o => o.Id == task.AppraisalOrderId, ct);

            if (order is not null)
            {
                try
                {
                    await _notifications.SendAsync(new NotificationRequest(
                        RecipientUserId:   null,
                        RecipientRole:     AppRoles.KolateralOficir,
                        Channel:           NotificationChannel.InApp,
                        Subject:           "Završena procjena",
                        Message:           $"Završen import procjene za narudžbu {order.OrderNumber} — {order.Title}.",
                        RelatedEntityType: "AppraisalOrder",
                        RelatedEntityId:   order.Id.ToString()), ct);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex,
                        "Notifikacija CO-u za završetak procjene narudžbe {OrderId} nije poslana.",
                        order.Id);
                }
            }
        }

        try
        {
            await _audit.RecordAsync(new AuditEvent
            {
                Action            = AuditActions.TaskCompleted,
                OperationType     = AuditOperationTypes.Update,
                Module            = AuditModules.AppraisalOrders,
                EntityType        = "TaskItem",
                EntityKey         = task.Id.ToString(),
                EntityDisplayName = task.Title,
                Status            = AuditStatuses.Success,
                Severity          = AuditSeverity.Info,
                NewValues         = new { task.Status, task.CompletedByUserId, task.TaskType, task.Comment }
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Audit za task completion {TaskId} nije snimljen.", task.Id);
        }

        return MapToDto(task);
    }

    private static WorkflowTaskDto MapToDto(TaskItem t) =>
        new(
            t.Id,
            t.AppraisalOrderId,
            t.AppraisalOrder?.OrderNumber ?? string.Empty,
            t.AppraisalOrder?.Title,
            t.TaskType.ToString(),
            (int)t.TaskType,
            t.Title,
            t.Description,
            t.AssignedRole,
            t.AssignedUserId,
            t.Status.ToString(),
            (int)t.Status,
            t.IsLocked,
            t.DueDate,
            t.AcceptedAt,
            t.AcceptedByUserId,
            t.CompletedAt,
            t.CompletedByUserId,
            t.Comment,
            t.CreatedAt
        );
}