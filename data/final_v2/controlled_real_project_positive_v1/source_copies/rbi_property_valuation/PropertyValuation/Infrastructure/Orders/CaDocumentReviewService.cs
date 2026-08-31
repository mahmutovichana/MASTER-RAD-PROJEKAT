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
/// CA pregled dokumentacije (US-91/92) — petlja "Dopuna podataka" ↔ "Podaci dopunjeni" / "Završi pregled".
/// </summary>
public sealed class CaDocumentReviewService : ICaDocumentReviewService
{
    private const string ReasonsCodebookKey = Application.Common.Constants.CodebookKeys.DocumentationSupplementReasons;

    private readonly ApplicationDbContext  _db;
    private readonly ICurrentUserService   _currentUser;
    private readonly INotificationProvider _notificationProvider;
    private readonly IAuditService         _audit;
    private readonly ILogger<CaDocumentReviewService> _logger;

    public CaDocumentReviewService(
        ApplicationDbContext db,
        ICurrentUserService currentUser,
        INotificationProvider notificationProvider,
        IAuditService audit,
        ILogger<CaDocumentReviewService> logger)
    {
        _db                   = db;
        _currentUser          = currentUser;
        _notificationProvider = notificationProvider;
        _audit                = audit;
        _logger               = logger;
    }

    public async Task<CaDocumentReviewResultDto> RequestCorrectionAsync(
        int orderId, int reasonCodeId, string? comment, CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();
        var order = await FindOrderAsync(orderId, ct);

        if (order.Status is not (AppraisalOrderStatus.DocumentationReviewInProgress
                               or AppraisalOrderStatus.CorrectionSubmitted
                               or AppraisalOrderStatus.AccessCheckRejected))
            throw new ConflictException(
                "Dopuna podataka je dozvoljena samo tokom pregleda dokumentacije.",
                "REVIEW_INVALID_STATUS");

        var reasonLabel = await _db.CodebookValues
            .AsNoTracking()
            .Where(x => x.CodebookKey == ReasonsCodebookKey && x.Id == reasonCodeId)
            .Select(x => x.Label)
            .FirstOrDefaultAsync(ct)
            ?? throw new NotFoundException(
                "Razlog dopune dokumentacije nije pronađen.",
                "CORRECTION_REASON_NOT_FOUND");

        var reviewTask = await FindActiveTaskAsync(orderId, TaskItemType.ReviewDocumentation, ct)
            ?? throw new ConflictException(
                "Aktivan zadatak pregleda dokumentacije nije pronađen.",
                "REVIEW_TASK_NOT_FOUND");

        var now = DateTime.UtcNow;
        var oldStatus = order.Status;
        var reasonText = string.IsNullOrWhiteSpace(comment) ? reasonLabel : $"{reasonLabel}: {comment}";

        order.ReturnForCorrection(now);
        reviewTask.Complete(userId, reasonText, now);

        // Dodjeljujemo tačnoj AM/SM/UB roli koja je inicirala narudžbu — "Prodaja"
        // nije Keycloak rola pod kojom bi se ikom prijavio (vidi AppRoles.ProdajaSegment).
        var initiatorRole = order.CreatedByRole ?? ApplicationAppRoles.ProdajaSegment;

        _db.TaskItems.Add(TaskItem.Create(
            orderId:      order.Id,
            type:         TaskItemType.CorrectDocumentation,
            title:        $"Dopuna podataka — {order.OrderNumber}",
            description:  reasonText,
            assignedRole: initiatorRole));

        await _db.SaveChangesAsync(ct);

        var notificationSent = await NotifyOrderCreatorAsync(
            order,
            "Potrebna dopuna podataka",
            $"Narudžba {order.OrderNumber} — {order.Title}: potrebna je dopuna podataka. Razlog: {reasonText}",
            ct);

        // AC6.5 — email notifikacija AM/SM/UB o potrebnoj dopuni
        if (!string.IsNullOrWhiteSpace(order.CreatedByEmail))
        {
            try
            {
                await _notificationProvider.SendAsync(new NotificationRequest(
                    RecipientUserId:   order.CreatedByUserId,
                    RecipientRole:     null,
                    Channel:           NotificationChannel.Email,
                    Subject:           $"Potrebna dopuna podataka — {order.OrderNumber}",
                    Message:           $"Narudžba {order.OrderNumber} — {order.Title}: " +
                                       $"vraćena je na dopunu podataka.\nRazlog: {reasonText}",
                    RelatedEntityType: "AppraisalOrder",
                    RelatedEntityId:   order.Id.ToString(),
                    RecipientEmail:    order.CreatedByEmail
                ), ct);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex,
                    "Email o dopuni podataka nije poslan na adresu {Email} za narudžbu {OrderId}",
                    order.CreatedByEmail, order.Id);
            }
        }

        await RecordAuditAsync(
            AuditActions.OrderReturnedForCorrection, order, oldStatus, notificationSent,
            new { ReasonCodeId = reasonCodeId, Reason = reasonText }, ct);

        return new CaDocumentReviewResultDto(
            order.Id, order.OrderNumber, order.Status.ToString(), (int)order.Status,
            notificationSent, "Narudžba je vraćena na dopunu podataka.");
    }

    public async Task<CaDocumentReviewResultDto> CompleteReviewAsync(
        int orderId, CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();
        var order = await FindOrderAsync(orderId, ct);

        if (order.Status is not (AppraisalOrderStatus.DocumentationReviewInProgress
                               or AppraisalOrderStatus.CorrectionSubmitted
                               or AppraisalOrderStatus.AccessCheckRejected))
            throw new ConflictException(
                "Pregled dokumentacije se može završiti samo tokom pregleda.",
                "REVIEW_INVALID_STATUS");

        var reviewTask = await FindActiveTaskAsync(orderId, TaskItemType.ReviewDocumentation, ct)
            ?? throw new ConflictException(
                "Aktivan zadatak pregleda dokumentacije nije pronađen.",
                "REVIEW_TASK_NOT_FOUND");

        var now = DateTime.UtcNow;
        var oldStatus = order.Status;

        order.ApproveDocumentation(now);
        reviewTask.Complete(userId, "Pregled dokumentacije završen — dokumentacija odobrena.", now);

        // US-93: ako kolateral nije isključivo stan, narudžba ide CO-u na provjeru
        // pristupa prije nego što CA odabere vještaka. Stan → odmah na odabir vještaka.
        var isApartmentOnly = await CollateralTypeRules.IsApartmentOnlyAsync(_db, order, ct);

        string notifyRole;
        string notifySubject;
        string notifyMessage;
        string resultMessage;
        var accessCheckRequested = false;

        if (isApartmentOnly)
        {
            _db.TaskItems.Add(TaskItem.Create(
                orderId:      order.Id,
                type:         TaskItemType.SelectAppraiser,
                title:        $"Odabir vještaka — {order.OrderNumber}",
                description:  null,
                assignedRole: ApplicationAppRoles.KolateralAdministrator));

            notifyRole     = ApplicationAppRoles.KolateralAdministrator;
            notifySubject  = "Spremno za izbor vještaka";
            notifyMessage  = $"Narudžba {order.OrderNumber} — {order.Title}: dokumentacija je odobrena i spremna je za odabir vještaka.";
            resultMessage  = "Pregled dokumentacije završen — dokumentacija odobrena. Narudžba je spremna za odabir vještaka.";
        }
        else
        {
            order.RequestAccessCheck(now);

            _db.TaskItems.Add(TaskItem.Create(
                orderId:      order.Id,
                type:         TaskItemType.AccessCheckCO,
                title:        $"Provjera pristupa prije narudžbe — {order.OrderNumber}",
                description:  null,
                assignedRole: ApplicationAppRoles.KolateralOficir));

            notifyRole     = ApplicationAppRoles.KolateralOficir;
            notifySubject  = "Provjera pristupa prije narudžbe";
            notifyMessage  = $"Narudžba {order.OrderNumber} — {order.Title}: dokumentacija je odobrena, potrebna je provjera pristupa prije narudžbe.";
            resultMessage  = "Pregled dokumentacije završen — dokumentacija odobrena. Poslano CO-u na provjeru pristupa.";
            accessCheckRequested = true;
        }

        await _db.SaveChangesAsync(ct);

        var notificationSent = await NotifyRoleAsync(notifyRole, notifySubject, notifyMessage, order.Id, ct);

        await NotifyOrderCreatorAsync(
            order,
            "Dokumentacija uredna",
            $"Narudžba {order.OrderNumber} — {order.Title}: CA je završio pregled dokumentacije. Dokumentacija je odobrena.",
            ct);

        await RecordAuditAsync(
            AuditActions.OrderReviewCompleted, order, oldStatus, notificationSent,
            new { }, ct);

        if (accessCheckRequested)
        {
            await RecordAuditAsync(
                AuditActions.OrderAccessCheckRequested, order, AppraisalOrderStatus.DocumentationApproved, notificationSent,
                new { }, ct);
        }

        return new CaDocumentReviewResultDto(
            order.Id, order.OrderNumber, order.Status.ToString(), (int)order.Status,
            notificationSent, resultMessage);
    }

    public async Task<CaDocumentReviewResultDto> SubmitCorrectionAsync(
        int orderId, string? comment, CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();
        var order = await FindOrderAsync(orderId, ct);

        if (order.Status != AppraisalOrderStatus.ReturnedForCorrection)
            throw new ConflictException(
                "Dostava dopune je dozvoljena samo dok je narudžba vraćena na dopunu.",
                "CORRECTION_INVALID_STATUS");

        var correctionTask = await FindActiveTaskAsync(orderId, TaskItemType.CorrectDocumentation, ct)
            ?? throw new ConflictException(
                "Aktivan zadatak dopune podataka nije pronađen.",
                "CORRECTION_TASK_NOT_FOUND");

        var now = DateTime.UtcNow;
        var oldStatus = order.Status;

        order.SubmitCorrection(now);
        correctionTask.Complete(userId, comment, now);

        _db.TaskItems.Add(TaskItem.Create(
            orderId:      order.Id,
            type:         TaskItemType.ReviewDocumentation,
            title:        $"Pregled dokumentacije — {order.OrderNumber}",
            description:  null,
            assignedRole: ApplicationAppRoles.KolateralAdministrator));

        await _db.SaveChangesAsync(ct);

        var notificationSent = await NotifyRoleAsync(
            ApplicationAppRoles.KolateralAdministrator,
            "Dopuna podataka dostavljena",
            $"Narudžba {order.OrderNumber} — {order.Title}: dopuna podataka je dostavljena i čeka ponovni pregled.",
            order.Id, ct);

        await RecordAuditAsync(
            AuditActions.OrderCorrectionSubmitted, order, oldStatus, notificationSent,
            new { Comment = comment }, ct);

        return new CaDocumentReviewResultDto(
            order.Id, order.OrderNumber, order.Status.ToString(), (int)order.Status,
            notificationSent, "Dopuna podataka je dostavljena CA na ponovni pregled.");
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

    /// <summary>
    /// Notifikacija ide direktno korisniku koji je inicirao narudžbu (AM/SM/UB) —
    /// preciznije od broadcast-a na rolu, jer narudžba već pamti CreatedByUserId.
    /// Fallback na broadcast po roli inicijatora samo ako CreatedByUserId nedostaje
    /// (npr. stari/legacy podaci).
    /// </summary>
    private async Task<bool> NotifyOrderCreatorAsync(
        AppraisalOrder order, string subject, string message, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(order.CreatedByUserId))
            return await NotifyRoleAsync(
                order.CreatedByRole ?? ApplicationAppRoles.ProdajaSegment, subject, message, order.Id, ct);

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

            return true;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Greška pri slanju notifikacije korisniku {UserId} za narudžbu {OrderId}",
                order.CreatedByUserId, order.Id);
            return false;
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
