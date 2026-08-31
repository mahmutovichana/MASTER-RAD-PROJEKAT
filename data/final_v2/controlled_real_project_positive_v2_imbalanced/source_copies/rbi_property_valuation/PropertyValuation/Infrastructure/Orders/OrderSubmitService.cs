using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Common.Validation;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using ApplicationAppRoles = RBBH.CollateralAppraisal.Application.Security.AppRoles;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

/// <summary>
/// Submit i otkazivanje narudžbi — fizički split iz AppraisalOrderService (I-1 refactoring).
/// Odgovoran za: SubmitAsync, CancelAsync.
/// </summary>
public sealed class OrderSubmitService : IOrderSubmitService
{
    private readonly ApplicationDbContext  _db;
    private readonly ICurrentUserService   _currentUser;
    private readonly INotificationProvider _notificationProvider;
    private readonly IAuditService         _audit;
    private readonly ILogger<OrderSubmitService> _logger;
    private readonly OrderNotificationsOptions _notificationOptions;
    private readonly WorkflowSlaOptions    _sla;
    private readonly IClock                _clock;
    private readonly OrderAuthorizationGuard _authGuard;

    public OrderSubmitService(
        ApplicationDbContext db,
        ICurrentUserService  currentUser,
        INotificationProvider notificationProvider,
        IAuditService        audit,
        ILogger<OrderSubmitService> logger,
        IOptions<OrderNotificationsOptions> notificationOptions,
        IOptions<WorkflowSlaOptions> slaOptions,
        IClock clock)
    {
        _db                   = db;
        _currentUser          = currentUser;
        _notificationProvider = notificationProvider;
        _audit                = audit;
        _logger               = logger;
        _notificationOptions  = notificationOptions.Value;
        _sla                  = slaOptions.Value;
        _clock                = clock;
        _authGuard            = new OrderAuthorizationGuard(currentUser, audit);
    }

    public async Task<AppraisalOrderDto> SubmitAsync(int id, CancellationToken ct = default)
    {
        var order = await _db.AppraisalOrders.FindAsync([id], ct)
            ?? throw new NotFoundException($"Narudžba s ID-om {id} nije pronađena.");

        await _authGuard.EnsureOwnerAsync(order, ct);

        if (order.Status != AppraisalOrderStatus.Draft)
            throw new ValidationException("status", "Samo narudžbe u statusu Draft se mogu podnijeti.");

        await ValidateSubmitRequirementsAsync(order, ct);

        var now = _clock.UtcNow;
        string? failedStage = null;
        TaskItem task = default!;

        await using var transaction = await _db.Database.BeginTransactionAsync(ct);
        try
        {
            order.Submit(now);
            await _db.SaveChangesAsync(ct);

            failedStage = AuditActions.CaTaskCreationFailed;
            task = TaskItem.Create(
                order.Id, TaskItemType.AcceptCAOrder,
                $"Prihvatanje narudžbe — {order.OrderNumber}",
                $"Nova narudžba '{order.Title}' čeka vaše prihvatanje.",
                assignedRole: ApplicationAppRoles.KolateralAdministrator,
                dueDate: now.AddDays(_sla.CaAcceptDueDays));

            _db.TaskItems.Add(task);
            await _db.SaveChangesAsync(ct);

            failedStage = null;
            await transaction.CommitAsync(ct);
        }
        catch (Exception ex)
        {
            await transaction.RollbackAsync(ct);
            _db.ChangeTracker.Clear();

            if (failedStage is not null)
                await _audit.RecordAsync(new AuditEvent
                {
                    Action            = failedStage,
                    OperationType     = AuditOperationTypes.Create,
                    Module            = AuditModules.AppraisalOrders,
                    EntityType        = "AppraisalOrder",
                    EntityKey         = order.Id.ToString(),
                    EntityDisplayName = order.Title,
                    Status            = AuditStatuses.Failed,
                    Severity          = AuditSeverity.Critical,
                    Reason            = ex.Message
                }, ct);
            throw;
        }

        // Post-commit: notifikacije i audit — greške se loguju ali ne blokiraju HTTP odgovor
        await NotifyCAAsync(order, ct);

        try
        {
            await _audit.RecordAsync(new AuditEvent
            {
                Action            = AuditActions.OrderSubmitted,
                OperationType     = AuditOperationTypes.Process,
                Module            = AuditModules.AppraisalOrders,
                EntityType        = "AppraisalOrder",
                EntityKey         = order.Id.ToString(),
                EntityDisplayName = order.Title,
                Status            = AuditStatuses.Success,
                Severity          = AuditSeverity.Info,
                NewValues         = new { order.Status, TaskId = task.Id }
            }, ct);

            await _audit.RecordAsync(new AuditEvent
            {
                Action            = AuditActions.TaskCreated,
                OperationType     = AuditOperationTypes.Create,
                Module            = AuditModules.AppraisalOrders,
                EntityType        = "TaskItem",
                EntityKey         = task.Id.ToString(),
                EntityDisplayName = task.Title,
                Status            = AuditStatuses.Success,
                Severity          = AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Post-commit audit za submit narudžbe {OrderId} nije uspio.", order.Id);
        }

        var collateralLabel = order.CollateralTypeId.HasValue
            ? await CodebookQueryHelper.GetLabelAsync(_db, order.CollateralTypeId.Value, ct) : null;
        var combinedLabel = order.CombinedCollateralTypeId.HasValue
            ? await CodebookQueryHelper.GetLabelAsync(_db, order.CombinedCollateralTypeId.Value, ct) : null;

        return OrderDtoMapper.ToDto(order, _currentUser, collateralLabel, combinedLabel);
    }

    public async Task CancelAsync(int id, CancellationToken ct = default)
    {
        var order = await _db.AppraisalOrders.FindAsync([id], ct)
            ?? throw new NotFoundException($"Narudžba s ID-om {id} nije pronađena.");

        await _authGuard.EnsureOwnerAsync(order, ct);

        if (order.Status != AppraisalOrderStatus.Draft)
            throw new ValidationException("status", "Samo narudžbe u statusu Draft se mogu otkazati.");

        order.SoftDelete(_currentUser.UserId ?? "unknown", _clock.UtcNow);
        await _db.SaveChangesAsync(ct);

        await _audit.RecordAsync(new AuditEvent
        {
            Action            = AuditActions.OrderCancelled,
            OperationType     = AuditOperationTypes.Cancel,
            Module            = AuditModules.AppraisalOrders,
            EntityType        = "AppraisalOrder",
            EntityKey         = order.Id.ToString(),
            EntityDisplayName = order.Title,
            Status            = AuditStatuses.Success,
            Severity          = AuditSeverity.Warning
        }, ct);
    }

    // ── Privatni helperi ──────────────────────────────────────────────────────

    private async Task ValidateSubmitRequirementsAsync(AppraisalOrder order, CancellationToken ct)
    {
        var errors = new List<ValidationFieldError>();

        if (string.IsNullOrWhiteSpace(order.ClientName))
            errors.Add(new ValidationFieldError("clientName", ValidationErrorCodes.RequiredField, "Klijent je obavezan."));
        if (string.IsNullOrWhiteSpace(order.ClientIdentifier))
            errors.Add(new ValidationFieldError("clientIdentifier", ValidationErrorCodes.RequiredJmbg, "JMBG je obavezan."));
        if (!order.CollateralTypeId.HasValue && !order.CombinedCollateralTypeId.HasValue)
            errors.Add(new ValidationFieldError("collateralTypeId", ValidationErrorCodes.RequiredField, "Tip kolaterala je obavezan."));
        if (string.IsNullOrWhiteSpace(order.City))
            errors.Add(new ValidationFieldError("city", ValidationErrorCodes.RequiredField, "Grad je obavezan."));
        if (string.IsNullOrWhiteSpace(order.ContactName))
            errors.Add(new ValidationFieldError("contactName", ValidationErrorCodes.RequiredField, "Kontakt ime je obavezno."));
        if (string.IsNullOrWhiteSpace(order.ContactPhone))
            errors.Add(new ValidationFieldError("contactPhone", ValidationErrorCodes.RequiredField, "Kontakt telefon je obavezan."));
        if (string.IsNullOrWhiteSpace(order.Branch))
            errors.Add(new ValidationFieldError("branch", ValidationErrorCodes.RequiredField, "Poslovnica je obavezna."));
        if (string.IsNullOrWhiteSpace(order.BranchAddress))
            errors.Add(new ValidationFieldError("branchAddress", ValidationErrorCodes.RequiredField, "Adresa poslovnice je obavezna."));
        if (string.IsNullOrWhiteSpace(order.PropertyAddress))
            errors.Add(new ValidationFieldError("propertyAddress", ValidationErrorCodes.RequiredField, "Adresa nekretnine je obavezna."));
        if (string.IsNullOrWhiteSpace(order.DeliveryContactName))
            errors.Add(new ValidationFieldError("deliveryContactName", ValidationErrorCodes.RequiredField, "Osoba u poslovnici za dostavu originala procjene je obavezna."));
        if (string.IsNullOrWhiteSpace(order.AmRecipientName))
            errors.Add(new ValidationFieldError("amRecipientName", ValidationErrorCodes.RequiredField, "Ime AM-a na kojeg se šalje procjena mailom je obavezno."));
        if (!order.RequestReceivedAt.HasValue)
            errors.Add(new ValidationFieldError("requestReceivedAt", ValidationErrorCodes.RequiredField, "Datum i vrijeme prijema zahtjeva od klijenta je obavezan."));

        if (!string.IsNullOrWhiteSpace(order.ContactEmail))
            errors.AddRange(EmailValidator.Validate(order.ContactEmail, "contactEmail"));

        // K4: Provjera obaveznih dokumenata
        var documentTypeCodes = await _db.CodebookValues
            .AsNoTracking()
            .Where(v => v.CodebookKey == RBBH.CollateralAppraisal.Application.Common.Constants.CodebookKeys.DocumentTypes && v.IsActive)
            .Select(v => new { v.Id, v.Code })
            .ToListAsync(ct);

        if (documentTypeCodes.Count > 0)
        {
            var uploadedTypeIds = await _db.Documents
                .AsNoTracking()
                .Where(d => d.AppraisalOrderId == order.Id && !d.IsDeleted && d.IsActive)
                .Select(d => d.DocumentTypeId)
                .Distinct()
                .ToListAsync(ct);

            var zkType = documentTypeCodes.FirstOrDefault(t => t.Code == RBBH.CollateralAppraisal.Application.Common.Constants.DocumentTypeCodes.ZkExtract);
            if (zkType is not null && !uploadedTypeIds.Contains(zkType.Id))
                errors.Add(new ValidationFieldError("documents.zk", ValidationErrorCodes.RequiredField, "ZK izvadak je obavezan dokument."));

            if (order.IsFL())
            {
                var uplatnicaType = documentTypeCodes.FirstOrDefault(t => t.Code == RBBH.CollateralAppraisal.Application.Common.Constants.DocumentTypeCodes.PaymentReceipt);
                if (uplatnicaType is not null && !uploadedTypeIds.Contains(uplatnicaType.Id))
                    errors.Add(new ValidationFieldError("documents.uplatnica", ValidationErrorCodes.RequiredField, "Uplatnica je obavezan dokument za fizička lica."));
            }
            else if (order.IsPL())
            {
                var saglasnostType = documentTypeCodes.FirstOrDefault(t => t.Code == RBBH.CollateralAppraisal.Application.Common.Constants.DocumentTypeCodes.Consent);
                if (saglasnostType is not null && !uploadedTypeIds.Contains(saglasnostType.Id))
                    errors.Add(new ValidationFieldError("documents.saglasnost", ValidationErrorCodes.RequiredField, "Saglasnost je obavezan dokument za pravna lica."));
            }
        }

        if (errors.Count > 0) throw new ValidationException(errors);
    }

    private async Task NotifyCAAsync(AppraisalOrder order, CancellationToken ct)
    {
        try
        {
            await _notificationProvider.SendAsync(new NotificationRequest(
                RecipientUserId:   null,
                RecipientRole:     ApplicationAppRoles.KolateralAdministrator,
                Channel:           NotificationChannel.InApp,
                Subject:           "Nova narudžba za prihvatanje",
                Message:           BuildCaTaskMessage(order),
                RelatedEntityType: "AppraisalOrder",
                RelatedEntityId:   order.Id.ToString()
            ), ct);

            await _audit.RecordAsync(new AuditEvent
            {
                Action        = AuditActions.NotificationCreated,
                OperationType = AuditOperationTypes.Create,
                Module        = AuditModules.AppraisalOrders,
                EntityType    = "Notification",
                EntityKey     = order.Id.ToString(),
                Status        = AuditStatuses.Success,
                Severity      = AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Greška pri slanju notifikacije CA za narudžbu {OrderId}", order.Id);
            await _audit.RecordAsync(new AuditEvent
            {
                Action        = AuditActions.EmailFailed,
                OperationType = AuditOperationTypes.Process,
                Module        = AuditModules.AppraisalOrders,
                EntityType    = "Notification",
                EntityKey     = order.Id.ToString(),
                Status        = AuditStatuses.Failed,
                Severity      = AuditSeverity.Warning,
                Reason        = ex.Message
            }, ct);
        }

        await NotifyCAByEmailAsync(order, ct);
    }

    private static string BuildCaTaskMessage(AppraisalOrder order)
    {
        const string titlePrefix = "Narudžba procjene ";
        var initiatorRole = order.CreatedByRole ?? ApplicationAppRoles.ProdajaSegment;
        var titleSuffix = order.Title.StartsWith(titlePrefix, StringComparison.OrdinalIgnoreCase)
            ? order.Title[titlePrefix.Length..] : order.Title;
        return $"Dobili ste zadatak iniciranje narudžbe procjene od strane {initiatorRole} {titleSuffix}.";
    }

    private async Task NotifyCAByEmailAsync(AppraisalOrder order, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(_notificationOptions.CaInboxEmail)) return;
        try
        {
            await _notificationProvider.SendAsync(new NotificationRequest(
                RecipientUserId:   null,
                RecipientRole:     ApplicationAppRoles.KolateralAdministrator,
                Channel:           NotificationChannel.Email,
                Subject:           $"Nova narudžba procjene — {order.OrderNumber}",
                Message:           $"Poštovani,\n\nInicirana je narudžba procjene.\n\n" +
                                   $"Klijent: {order.ClientName}\nGrad: {order.City}\nTip nekretnine: {order.Title}\n\n" +
                                   $"Molimo dalje postupanje u aplikaciji.\n\nLp,",
                RelatedEntityType: "AppraisalOrder",
                RelatedEntityId:   order.Id.ToString(),
                RecipientEmail:    _notificationOptions.CaInboxEmail
            ), ct);

            await _audit.RecordAsync(new AuditEvent
            {
                Action            = AuditActions.CaEmailNotificationSent,
                OperationType     = AuditOperationTypes.Process,
                Module            = AuditModules.AppraisalOrders,
                EntityType        = "AppraisalOrder",
                EntityKey         = order.Id.ToString(),
                EntityDisplayName = order.Title,
                Status            = AuditStatuses.Success,
                Severity          = AuditSeverity.Info,
                NewValues         = new { RecipientEmail = _notificationOptions.CaInboxEmail }
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Greška pri slanju email notifikacije CA za narudžbu {OrderId}", order.Id);
            await _audit.RecordAsync(new AuditEvent
            {
                Action            = AuditActions.CaEmailNotificationFailed,
                OperationType     = AuditOperationTypes.Process,
                Module            = AuditModules.AppraisalOrders,
                EntityType        = "AppraisalOrder",
                EntityKey         = order.Id.ToString(),
                EntityDisplayName = order.Title,
                Status            = AuditStatuses.Failed,
                Severity          = AuditSeverity.Warning,
                Reason            = ex.Message
            }, ct);
        }
    }

}
