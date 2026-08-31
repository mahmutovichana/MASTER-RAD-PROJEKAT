using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using Microsoft.Extensions.Options;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Application.Users.Models;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Domain.Documents;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using ApplicationAppRoles = RBBH.CollateralAppraisal.Application.Security.AppRoles;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

public sealed class OrderApprovalService : IOrderApprovalService
{
    private const string FinalAppraisalDocumentCode = Application.Common.Constants.DocumentTypeCodes.FinalAppraisal;
    private const string DocumentTypesCodebookKey = Application.Common.Constants.CodebookKeys.DocumentTypes;
    private const string FinalAppraisalReadyMessage = "Procjena može dalje u proceduru";
    private const string OrderFinalAppraisalApprovedAction = "ORDER_FINAL_APPRAISAL_APPROVED";

    private readonly ApplicationDbContext _db;
    private readonly ICurrentUserService _currentUser;
    private readonly INotificationService _notificationService;
    private readonly INotificationProvider _notificationProvider;
    private readonly IAuditService _auditService;
    private readonly IUserRoleProvider _userRoleProvider;
    private readonly ILogger<OrderApprovalService> _logger;
    private readonly WorkflowSlaOptions _sla;
    private readonly IClock _clock;

    public OrderApprovalService(
        ApplicationDbContext db,
        ICurrentUserService currentUser,
        INotificationService notificationService,
        INotificationProvider notificationProvider,
        IAuditService auditService,
        IUserRoleProvider userRoleProvider,
        ILogger<OrderApprovalService> logger,
        IOptions<WorkflowSlaOptions> slaOptions,
        IClock clock)
    {
        _db = db;
        _currentUser = currentUser;
        _notificationService = notificationService;
        _notificationProvider = notificationProvider;
        _auditService = auditService;
        _userRoleProvider = userRoleProvider;
        _logger = logger;
        _sla = slaOptions.Value;
        _clock = clock;
    }

    public async Task<ApproveFinalAppraisalResultDto> ApproveFinalAppraisalAsync(
        int orderId,
        int? appraiserRating = null,
        CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();
        var order = await FindOrderAsync(orderId, ct);
        EnsureNotCreator(userId, order);
        var finalAppraisal = await FindFinalAppraisalDocumentAsync(order, ct);

        EnsureCanApprove(order);

        if (!appraiserRating.HasValue)
            throw new ConflictException(
                "Ocjena procjenitelja je obavezna za odobrenje procjene.",
                "APPRAISER_RATING_REQUIRED");

        if (appraiserRating.Value is < 1 or > 5)
            throw new ConflictException(
                "Ocjena procjenitelja mora biti između 1 i 5.",
                "APPRAISER_RATING_OUT_OF_RANGE");

        var oldStatus = order.Status;
        var now = _clock.UtcNow;

        if (appraiserRating.HasValue)
            order.SetAppraiserRating(appraiserRating.Value, now);

        if (order.CoDocumentationReviewStartedAt is null)
            order.StartCoDocumentationReview(now);
        order.RecordCoOpinionSentToAm(now);
        order.ApproveByCO(userId, now);

        var task = await _db.TaskItems
            .Where(x => x.AppraisalOrderId == order.Id
                     && x.TaskType == TaskItemType.ApproveFinalAppraisal
                     && x.Status != TaskItemStatus.Completed
                     && x.Status != TaskItemStatus.Cancelled)
            .OrderByDescending(x => x.CreatedAt)
            .FirstOrDefaultAsync(ct);

        task?.Complete(userId, FinalAppraisalReadyMessage, now);

        _db.TaskItems.Add(TaskItem.Create(
            orderId:      order.Id,
            type:         TaskItemType.ConfirmOriginalReceived,
            title:        $"Preuzimanje originala procjene — {order.OrderNumber}",
            description:  "Vještak treba dostaviti original procjene u poslovnicu. Rok: 2 radna dana.",
            assignedRole: null,
            dueDate:      now.AddDays(_sla.OriginalReceivedDueDays)));

        try
        {
            await _db.SaveChangesAsync(ct);
        }
        catch (DbUpdateConcurrencyException)
        {
            throw new ConflictException(
                "Narudžba je u međuvremenu izmijenjena od drugog korisnika. Osvježite stranicu.",
                "OPTIMISTIC_CONCURRENCY_CONFLICT");
        }

        var notificationSent = await NotifyOrderCreatorAsync(order, ct);
        await NotifyAppraiserApprovedAsync(order, ct);
        await NotifyProdajaSegmentApprovedAsync(order, ct);
        await RecordApprovalAuditAsync(order, finalAppraisal, oldStatus, notificationSent, ct);

        return new ApproveFinalAppraisalResultDto(
            order.Id,
            order.OrderNumber,
            order.Status.ToString(),
            order.CoApprovedAt!.Value,
            order.CoApprovedByUserId!,
            order.ReadyForProcedureAt!.Value,
            finalAppraisal.Id,
            BuildDownloadUrl(finalAppraisal.Id),
            notificationSent,
            FinalAppraisalReadyMessage);
    }

    public async Task<FinalAppraisalDto> GetFinalAppraisalAsync(
        int orderId,
        CancellationToken ct = default)
    {
        var order = await FindOrderAsync(orderId, ct);
        var document = await FindFinalAppraisalDocumentAsync(order, ct);
        return ToFinalAppraisalDto(order.Id, document);
    }

    public async Task<ReturnForReworkResultDto> ReturnForReworkAsync(
        int orderId, string internalCategory, string comment, CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();
        var order = await FindOrderAsync(orderId, ct);
        EnsureNotCreator(userId, order);

        if (order.Status != AppraisalOrderStatus.AppraisalReceived)
            throw new ConflictException(
                "Procjena se može vratiti na doradu samo kad je u statusu 'Zaprimljena'.",
                "APPRAISAL_NOT_RECEIVED");

        var now = _clock.UtcNow;
        var oldStatus = order.Status;

        order.ReturnForRework(now);

        var approveTask = await _db.TaskItems
            .Where(x => x.AppraisalOrderId == order.Id
                     && x.TaskType == TaskItemType.ApproveFinalAppraisal
                     && x.Status != TaskItemStatus.Completed
                     && x.Status != TaskItemStatus.Cancelled)
            .OrderByDescending(x => x.CreatedAt)
            .FirstOrDefaultAsync(ct);
        approveTask?.Complete(userId, $"Vraćeno na doradu: {internalCategory}", now);

        var appraiserUserId = await ResolveAppraiserUserIdAsync(order, ct);
        _db.TaskItems.Add(TaskItem.Create(
            orderId:        order.Id,
            type:           TaskItemType.ReworkAppraisal,
            title:          $"Dorada procjene — {order.OrderNumber}",
            description:    $"CO je vratio procjenu na doradu. Komentar: {comment}",
            assignedRole:   ApplicationAppRoles.Vjestak,
            assignedUserId: appraiserUserId));

        try
        {
            await _db.SaveChangesAsync(ct);
        }
        catch (DbUpdateConcurrencyException)
        {
            throw new ConflictException(
                "Narudžba je u međuvremenu izmijenjena od drugog korisnika. Osvježite stranicu.",
                "OPTIMISTIC_CONCURRENCY_CONFLICT");
        }

        var notificationSent = await NotifyAppraiserReworkAsync(order, comment, ct);

        try
        {
            await _auditService.RecordAsync(new AuditEvent
            {
                Action = AuditActions.AppraisalReturnedForRework,
                OperationType = AuditOperationTypes.Update,
                Module = AuditModules.AppraisalOrders,
                EntityType = "AppraisalOrder",
                EntityKey = order.Id.ToString(),
                EntityDisplayName = order.OrderNumber,
                OldValues = new { Status = oldStatus.ToString() },
                NewValues = new { Status = order.Status.ToString(), InternalCategory = internalCategory, Comment = comment },
                Status = AuditStatuses.Success,
                Severity = AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Audit za rework narudžbe {OrderId} nije zapisan.", order.Id);
        }

        return new ReturnForReworkResultDto(
            order.Id, order.OrderNumber, order.Status.ToString(),
            notificationSent, "Procjena vraćena na doradu — vještak obaviješten.");
    }

    private async Task<string?> ResolveAppraiserUserIdAsync(AppraisalOrder order, CancellationToken ct)
    {
        if (order.AppraiserId is null) return null;
        var appraiser = await _db.Appraisers.AsNoTracking()
            .FirstOrDefaultAsync(a => a.Id == order.AppraiserId.Value, ct);
        if (appraiser is null || string.IsNullOrWhiteSpace(appraiser.ContactEmail)) return null;
        try
        {
            var res = await _userRoleProvider.GetUsersWithRolesAsync(
                new UserRoleListRequest { Search = appraiser.ContactEmail, Role = ApplicationAppRoles.Vjestak, PageSize = 5 }, ct);
            return res.Items.FirstOrDefault()?.UserId;
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Resolving appraiser userId za narudžbu {OrderId} nije uspjelo.", order.Id);
            return null;
        }
    }

    private async Task<bool> NotifyAppraiserReworkAsync(AppraisalOrder order, string comment, CancellationToken ct)
    {
        if (order.AppraiserId is null) return false;
        var appraiser = await _db.Appraisers.AsNoTracking()
            .FirstOrDefaultAsync(a => a.Id == order.AppraiserId.Value, ct);
        if (appraiser is null) return false;

        var sent = false;

        var appraiserUserId = await ResolveAppraiserUserIdAsync(order, ct);
        if (!string.IsNullOrWhiteSpace(appraiserUserId))
        {
            try
            {
                await _notificationProvider.SendAsync(new NotificationRequest(
                    RecipientUserId: appraiserUserId, RecipientRole: null,
                    Channel: NotificationChannel.InApp,
                    Subject: $"Procjena vraćena na doradu — {order.OrderNumber}",
                    Message: $"Procjena za narudžbu {order.OrderNumber} je vraćena na doradu. {comment}",
                    RelatedEntityType: "AppraisalOrder", RelatedEntityId: order.Id.ToString()), ct);
                sent = true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "In-app notifikacija vještaku pri doradi narudžbe {OrderId}.", order.Id);
            }
        }

        if (!string.IsNullOrWhiteSpace(appraiser.ContactEmail))
        {
            try
            {
                await _notificationProvider.SendAsync(new NotificationRequest(
                    RecipientUserId: null, RecipientRole: null,
                    Channel: NotificationChannel.Email,
                    Subject: $"Procjena vraćena na doradu — {order.OrderNumber}",
                    Message: $"Poštovani {appraiser.Name},\n\n" +
                             $"Procjena za narudžbu {order.OrderNumber} ({order.ClientName}) je vraćena na doradu.\n\n" +
                             $"Razlog: {comment}\n\n" +
                             $"Molimo dostavite korigovanu procjenu.",
                    RelatedEntityType: "AppraisalOrder", RelatedEntityId: order.Id.ToString(),
                    RecipientEmail: appraiser.ContactEmail), ct);
                sent = true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Email notifikacija vještaku pri doradi narudžbe {OrderId}.", order.Id);
            }
        }

        return sent;
    }

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

    private async Task<Document> FindFinalAppraisalDocumentAsync(
        AppraisalOrder order,
        CancellationToken ct)
    {
        if (order.FinalAppraisalDocumentId is int finalDocumentId)
        {
            var linkedDocument = await _db.Documents
                .AsNoTracking()
                .FirstOrDefaultAsync(x => x.Id == finalDocumentId
                                       && x.AppraisalOrderId == order.Id, ct);

            if (linkedDocument is not null)
                return linkedDocument;
        }

        var finalDocumentTypeId = await _db.CodebookValues
            .AsNoTracking()
            .Where(x => x.CodebookKey == DocumentTypesCodebookKey
                     && x.Code == FinalAppraisalDocumentCode)
            .Select(x => (int?)x.Id)
            .FirstOrDefaultAsync(ct);

        if (finalDocumentTypeId is null)
            throw new NotFoundException(
                "Tip dokumenta FINALNA_PROCJENA nije pronađen u šifarniku.",
                "FINAL_APPRAISAL_DOCUMENT_TYPE_NOT_FOUND");

        var document = await _db.Documents
            .AsNoTracking()
            .Where(x => x.AppraisalOrderId == order.Id
                     && x.DocumentTypeId == finalDocumentTypeId.Value)
            .OrderByDescending(x => x.UploadedAt)
            .ThenByDescending(x => x.Id)
            .FirstOrDefaultAsync(ct);

        if (document is null)
            throw new ConflictException(
                "Finalna procjena nije uploadovana za ovu narudžbu.",
                "FINAL_APPRAISAL_NOT_UPLOADED");

        return document;
    }

    private static void EnsureNotCreator(string userId, AppraisalOrder order)
    {
        if (string.Equals(userId, order.CreatedByUserId, StringComparison.OrdinalIgnoreCase))
            throw new ForbiddenException(
                "Kreator narudžbe ne može odobriti ili vratiti vlastitu narudžbu (four-eyes princip).",
                "FOUR_EYES_VIOLATION");

        if (!string.IsNullOrWhiteSpace(order.AcceptedByCAUserId)
            && string.Equals(userId, order.AcceptedByCAUserId, StringComparison.OrdinalIgnoreCase))
            throw new ForbiddenException(
                "CA koji je prihvatio narudžbu ne može odobriti finalnu procjenu (four-eyes princip).",
                "FOUR_EYES_VIOLATION");
    }

    private static void EnsureCanApprove(AppraisalOrder order)
    {
        if (order.Status == AppraisalOrderStatus.ReadyForProcedure)
            throw new ConflictException(
                "Procjena je već označena da može dalje u proceduru.",
                "FINAL_APPRAISAL_ALREADY_APPROVED");

        if (order.Status is not (AppraisalOrderStatus.AppraisalReceived or AppraisalOrderStatus.COApproved))
            throw new ConflictException(
                "Finalna procjena se može odobriti tek nakon što je zaprimljena.",
                "FINAL_APPRAISAL_INVALID_STATUS");
    }

    /// <summary>
    /// US 4, AC 5 — obavještava Prodaja segment (AM/SM/UB) da procjena može dalje u proceduru.
    /// Fan-out po roli ide kroz <see cref="INotificationProvider"/> (in-app + email), koji sam razrješava
    /// aktivne korisnike svake role preko IUserRoleProvider-a.
    /// </summary>
    private async Task NotifyProdajaSegmentApprovedAsync(AppraisalOrder order, CancellationToken ct)
    {
        var subject = $"Procjena može dalje u proceduru — {order.OrderNumber}";
        var message = $"Finalna procjena za narudžbu {order.OrderNumber} ({order.ClientName}) je odobrena od " +
                      $"strane Kolateral oficira i može dalje u proceduru.";

        foreach (var role in new[] { ApplicationAppRoles.AM, ApplicationAppRoles.SM, ApplicationAppRoles.UB })
        {
            try
            {
                await _notificationProvider.SendAsync(new NotificationRequest(
                    RecipientUserId: null,
                    RecipientRole: role,
                    Channel: NotificationChannel.InApp,
                    Subject: subject,
                    Message: message,
                    RelatedEntityType: nameof(AppraisalOrder),
                    RelatedEntityId: order.Id.ToString()), ct);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex,
                    "Notifikacija roli {Role} pri CO odobrenju narudžbe {OrderId} nije poslana.",
                    role, order.Id);
            }
        }
    }

    private async Task NotifyAppraiserApprovedAsync(AppraisalOrder order, CancellationToken ct)
    {
        if (order.AppraiserId is null) return;
        try
        {
            await _notificationService.NotifyUserAsync(
                order.AppraiserId.Value.ToString(),
                "Procjena može dalje u proceduru",
                $"Procjena za narudžbu {order.OrderNumber} — {order.ClientName} je odobrena. " +
                $"Molimo dostavite original u poslovnicu u roku od 2 radna dana.",
                relatedEntityType: nameof(AppraisalOrder),
                relatedEntityId: order.Id.ToString(),
                ct: ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Notifikacija vještaku pri CO odobrenju za narudžbu {OrderId} nije poslana.", order.Id);
        }
    }

    private async Task<bool> NotifyOrderCreatorAsync(AppraisalOrder order, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(order.CreatedByUserId))
        {
            _logger.LogWarning(
                "Narudžba {OrderId} nema CreatedByUserId; notifikacija Prodaji nije poslana.",
                order.Id);
            return false;
        }

        var subject = FinalAppraisalReadyMessage;
        var message = BuildNotificationMessage(order);

        try
        {
            await _notificationService.NotifyUserAsync(
                order.CreatedByUserId,
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
                "Notifikacija nije poslana kreatoru narudžbe {OrderId}.",
                order.Id);
            return false;
        }
    }

    private async Task RecordApprovalAuditAsync(
        AppraisalOrder order,
        Document document,
        AppraisalOrderStatus oldStatus,
        bool notificationSent,
        CancellationToken ct)
    {
        try
        {
            await _auditService.RecordAsync(new AuditEvent
            {
                Action = OrderFinalAppraisalApprovedAction,
                OperationType = AuditOperationTypes.Approve,
                Module = AuditModules.AppraisalOrders,
                EntityType = nameof(AppraisalOrder),
                EntityKey = order.Id.ToString(),
                EntityDisplayName = order.OrderNumber,
                OldValues = new { Status = oldStatus.ToString() },
                NewValues = new
                {
                    Status = order.Status.ToString(),
                    order.CoApprovedAt,
                    order.CoApprovedByUserId,
                    order.ReadyForProcedureAt,
                    FinalAppraisalDocumentId = document.Id,
                    NotificationSent = notificationSent
                },
                Status = AuditStatuses.Success,
                Severity = AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Audit log nije zapisan za odobrenje finalne procjene narudžbe {OrderId}.",
                order.Id);
        }
    }

    private string RequireCurrentUserId()
    {
        if (!_currentUser.IsAuthenticated || string.IsNullOrWhiteSpace(_currentUser.UserId))
            throw new ForbiddenException("Korisnik mora biti prijavljen za odobrenje finalne procjene.");

        return _currentUser.UserId;
    }

    private static FinalAppraisalDto ToFinalAppraisalDto(int orderId, Document document) => new(
        orderId,
        document.Id,
        document.OriginalFileName,
        document.ContentType,
        document.FileSize,
        document.UploadedAt,
        document.UploadedByUserId,
        BuildDownloadUrl(document.Id));

    private static string BuildDownloadUrl(int documentId) =>
        $"/api/documents/{documentId}/download";

    /// <summary>
    /// Vraća datum koji je <paramref name="workingDays"/> radnih dana nakon <paramref name="from"/>,
    /// preskačući subotu i nedjelju. Koristi se za rok dostave originala procjene (2 radna dana, US 4).
    /// </summary>
    private static DateTime AddWorkingDays(DateTime from, int workingDays)
    {
        var result = from;
        var added = 0;

        while (added < workingDays)
        {
            result = result.AddDays(1);
            if (result.DayOfWeek is not (DayOfWeek.Saturday or DayOfWeek.Sunday))
                added++;
        }

        return result;
    }

    private static string BuildNotificationMessage(AppraisalOrder order)
    {
        var client = order.ClientName;
        var type = order.ClientType ?? "N/A";
        var city = order.City ?? "N/A";

        return $"{FinalAppraisalReadyMessage} za klijenta {client} (tip: {type}, grad: {city}).";
    }
}
