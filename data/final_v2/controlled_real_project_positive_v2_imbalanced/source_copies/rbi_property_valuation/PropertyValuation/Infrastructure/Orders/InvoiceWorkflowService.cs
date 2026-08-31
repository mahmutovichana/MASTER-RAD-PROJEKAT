using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Application.Users.Models;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using ApplicationAppRoles = RBBH.CollateralAppraisal.Application.Security.AppRoles;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

public sealed class InvoiceWorkflowService : IInvoiceWorkflowService
{
    private readonly ApplicationDbContext  _db;
    private readonly ICurrentUserService   _currentUser;
    private readonly INotificationProvider _notificationProvider;
    private readonly IAuditService         _audit;
    private readonly IUserRoleProvider     _userRoleProvider;
    private readonly ILogger<InvoiceWorkflowService> _logger;

    public InvoiceWorkflowService(
        ApplicationDbContext db,
        ICurrentUserService currentUser,
        INotificationProvider notificationProvider,
        IAuditService audit,
        IUserRoleProvider userRoleProvider,
        ILogger<InvoiceWorkflowService> logger)
    {
        _db                   = db;
        _currentUser          = currentUser;
        _notificationProvider = notificationProvider;
        _audit                = audit;
        _userRoleProvider     = userRoleProvider;
        _logger               = logger;
    }

    public async Task<InvoiceWorkflowResultDto> UploadInvoiceAsync(
        int orderId, int documentId, CancellationToken ct = default)
    {
        var userId   = RequireCurrentUserId();
        var userName = await ResolveDisplayNameAsync(userId, ct) ?? userId;
        var order    = await FindOrderAsync(orderId, ct);

        if (order.InvoiceStatus != InvoiceWorkflowStatus.None)
            throw new ConflictException(
                "Faktura je već uploadovana za ovu narudžbu.",
                "INVOICE_ALREADY_UPLOADED");

        var document = await _db.Documents
            .AsNoTracking()
            .FirstOrDefaultAsync(d => d.Id == documentId, ct)
            ?? throw new NotFoundException(
                $"Dokument ID={documentId} nije pronađen.", "DOCUMENT_NOT_FOUND");

        var now = DateTime.UtcNow;
        order.UploadInvoice(documentId, userId, userName, now);

        var appraiserName = await ResolveAppraiserNameAsync(order, ct);

        _db.TaskItems.Add(TaskItem.Create(
            orderId:      order.Id,
            type:         TaskItemType.SendInvoiceForPayment,
            title:        $"Pošalji fakturu na plaćanje — {order.OrderNumber}",
            description:  $"Protokol je uploadovao fakturu vještaka {appraiserName ?? "—"}, klijent {order.ClientName}. Preuzmite i proslijedite na plaćanje.",
            assignedRole: ApplicationAppRoles.KolateralAdministrator));

        await _db.SaveChangesAsync(ct);

        var notified = await NotifyRoleAsync(
            ApplicationAppRoles.KolateralAdministrator,
            $"Izvršen upload fakture — {order.OrderNumber}",
            $"Izvršen upload fakture vještaka {appraiserName ?? "—"}, klijenta {order.ClientName}.",
            order.Id, ct);

        await RecordAuditAsync(AuditActions.InvoiceUploaded, order,
            new { DocumentId = documentId, UploadedBy = userName, AppraiserName = appraiserName }, ct);

        return new InvoiceWorkflowResultDto(
            order.Id, order.OrderNumber, order.InvoiceStatus.ToString(),
            notified, "Faktura uploadovana — CA obaviješten.");
    }

    public async Task<InvoiceWorkflowResultDto> SendForPaymentAsync(
        int orderId, CancellationToken ct = default)
    {
        var userId   = RequireCurrentUserId();
        var userName = await ResolveDisplayNameAsync(userId, ct) ?? userId;
        var order    = await FindOrderAsync(orderId, ct);

        if (order.InvoiceStatus != InvoiceWorkflowStatus.Uploaded)
            throw new ConflictException(
                "Faktura mora biti uploadovana prije slanja na plaćanje.",
                "INVOICE_NOT_UPLOADED");

        var now = DateTime.UtcNow;
        order.SendInvoiceForPayment(userId, userName, now);

        var paymentTask = await FindActiveTaskAsync(orderId, TaskItemType.SendInvoiceForPayment, ct);
        paymentTask?.Complete(userId, "Faktura poslana na plaćanje.", now);

        _db.TaskItems.Add(TaskItem.Create(
            orderId:      order.Id,
            type:         TaskItemType.ConfirmInvoicePaid,
            title:        $"Potvrdi plaćanje fakture — {order.OrderNumber}",
            description:  $"Faktura za narudžbu {order.OrderNumber} je poslana na plaćanje. Potvrdite kad je plaćena.",
            assignedRole: ApplicationAppRoles.Likvidatura));

        await _db.SaveChangesAsync(ct);

        var appraiserName = await ResolveAppraiserNameAsync(order, ct);
        var isPL = order.IsPL();
        var notified = false;

        if (isPL)
        {
            var subject = $"Faktura za plaćanje — {order.OrderNumber}";
            var message = $"Faktura vještaka {appraiserName ?? "—"} za narudžbu {order.OrderNumber}, klijent {order.ClientName}. Priložena faktura, saglasnost i narudžbenica.";

            notified |= await NotifyRoleAsync(ApplicationAppRoles.Likvidatura, subject, message, order.Id, ct);
            notified |= await NotifyRoleAsync(ApplicationAppRoles.SpecijalniRacuni, subject, message, order.Id, ct);
            notified |= await NotifyRoleAsync(ApplicationAppRoles.Racunovodstvo, subject, message, order.Id, ct);

            foreach (var salesRole in ApplicationAppRoles.SalesRoles)
            {
                notified |= await NotifyRoleAsync(salesRole,
                    $"Faktura za plaćanje — {order.OrderNumber}",
                    $"CA je poslao fakturu na plaćanje za narudžbu {order.OrderNumber}, klijent {order.ClientName}. Priložena faktura, saglasnost i narudžbenica.",
                    order.Id, ct);
            }
        }
        else
        {
            notified |= await NotifyRoleAsync(ApplicationAppRoles.Likvidatura,
                $"Faktura za plaćanje — {order.OrderNumber}",
                $"Faktura vještaka {appraiserName ?? "—"} za narudžbu {order.OrderNumber}, klijent {order.ClientName}. Priložena faktura.",
                order.Id, ct);
        }

        await RecordAuditAsync(AuditActions.InvoiceSentForPayment, order,
            new { SentBy = userName, IsPL = isPL }, ct);

        return new InvoiceWorkflowResultDto(
            order.Id, order.OrderNumber, order.InvoiceStatus.ToString(),
            notified, "Faktura poslana na plaćanje — nadležne role obaviještene.");
    }

    public async Task<InvoiceWorkflowResultDto> ConfirmPaidAsync(
        int orderId, CancellationToken ct = default)
    {
        var userId   = RequireCurrentUserId();
        var userName = await ResolveDisplayNameAsync(userId, ct) ?? userId;
        var order    = await FindOrderAsync(orderId, ct);

        if (order.InvoiceStatus != InvoiceWorkflowStatus.SentForPayment)
            throw new ConflictException(
                "Faktura mora biti u statusu 'u obradi' prije potvrde plaćanja.",
                "INVOICE_NOT_IN_PAYMENT");

        var now = DateTime.UtcNow;
        order.ConfirmInvoicePaid(userId, userName, now);

        var confirmTask = await FindActiveTaskAsync(orderId, TaskItemType.ConfirmInvoicePaid, ct);
        confirmTask?.Complete(userId, "Plaćanje potvrđeno.", now);

        await _db.SaveChangesAsync(ct);

        var subject = $"Faktura plaćena — {order.OrderNumber}";
        var message = $"Faktura za narudžbu {order.OrderNumber}, klijent {order.ClientName} je plaćena. Potvrdio: {userName}.";

        var notified = false;

        notified |= await NotifyRoleAsync(
            ApplicationAppRoles.KolateralAdministrator,
            subject,
            message,
            order.Id, ct);

        notified |= await NotifyRoleAsync(
            ApplicationAppRoles.Likvidatura,
            subject,
            message,
            order.Id, ct);

        notified |= await NotifyRoleAsync(
            ApplicationAppRoles.Racunovodstvo,
            subject,
            message,
            order.Id, ct);

        await RecordAuditAsync(AuditActions.InvoicePaymentConfirmed, order,
            new { ConfirmedBy = userName }, ct);

        return new InvoiceWorkflowResultDto(
            order.Id, order.OrderNumber, order.InvoiceStatus.ToString(),
            notified, "Plaćanje fakture potvrđeno.");
    }

    public async Task<InvoiceStatusDto> GetStatusAsync(
        int orderId, CancellationToken ct = default)
    {
        var order = await _db.AppraisalOrders
            .AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == orderId, ct)
            ?? throw new NotFoundException(
                $"Narudžba ID={orderId} nije pronađena.", "APPRAISAL_ORDER_NOT_FOUND");

        return new InvoiceStatusDto(
            order.Id,
            order.OrderNumber,
            order.InvoiceStatus.ToString(),
            order.InvoiceUploadedByName,
            order.InvoiceUploadedAt,
            order.InvoiceSentForPaymentByName,
            order.InvoiceSentForPaymentAt,
            order.InvoicePaidByName,
            order.InvoicePaidAt,
            order.InvoiceDocumentId);
    }

    private async Task<AppraisalOrder> FindOrderAsync(int orderId, CancellationToken ct) =>
        await _db.AppraisalOrders.FirstOrDefaultAsync(x => x.Id == orderId, ct)
        ?? throw new NotFoundException($"Narudžba ID={orderId} nije pronađena.", "APPRAISAL_ORDER_NOT_FOUND");

    private async Task<TaskItem?> FindActiveTaskAsync(int orderId, TaskItemType type, CancellationToken ct) =>
        await _db.TaskItems
            .Where(x => x.AppraisalOrderId == orderId
                     && x.TaskType == type
                     && x.Status != TaskItemStatus.Completed
                     && x.Status != TaskItemStatus.Cancelled)
            .OrderByDescending(x => x.CreatedAt)
            .FirstOrDefaultAsync(ct);

    private string RequireCurrentUserId() =>
        _currentUser.IsAuthenticated && !string.IsNullOrWhiteSpace(_currentUser.UserId)
            ? _currentUser.UserId
            : throw new ForbiddenException("Korisnik mora biti prijavljen.");

    private async Task<string?> ResolveDisplayNameAsync(string? userId, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(userId)) return null;
        try
        {
            var user = await _userRoleProvider.GetUserWithRolesAsync(userId, ct);
            return user?.DisplayName ?? user?.Username ?? userId;
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Resolving display name za userId={UserId} nije uspjelo — fallback na ID.", userId);
            return userId;
        }
    }

    private async Task<string?> ResolveAppraiserNameAsync(AppraisalOrder order, CancellationToken ct)
    {
        if (order.AppraiserId is null) return null;
        var appraiser = await _db.Appraisers
            .AsNoTracking()
            .Where(a => a.Id == order.AppraiserId.Value)
            .Select(a => a.Name)
            .FirstOrDefaultAsync(ct);
        return appraiser;
    }

    private async Task<bool> NotifyRoleAsync(string role, string subject, string message, int orderId, CancellationToken ct)
    {
        try
        {
            await _notificationProvider.SendAsync(new NotificationRequest(
                RecipientUserId: null, RecipientRole: role,
                Channel: NotificationChannel.InApp,
                Subject: subject, Message: message,
                RelatedEntityType: "AppraisalOrder", RelatedEntityId: orderId.ToString()), ct);
            return true;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Greška pri notifikaciji roli {Role} za narudžbu {OrderId}", role, orderId);
            return false;
        }
    }

    private async Task RecordAuditAsync(string action, AppraisalOrder order, object details, CancellationToken ct)
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
                NewValues         = new { InvoiceStatus = order.InvoiceStatus.ToString(), Details = details },
                Status            = AuditStatuses.Success,
                Severity          = AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Audit za {Action} narudžbe {OrderId} nije zapisan.", action, order.Id);
        }
    }
}