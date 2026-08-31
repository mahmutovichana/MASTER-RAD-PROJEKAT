using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Common;
using RBBH.CollateralAppraisal.Application.Common.Constants;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Requests;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;
using ApplicationAppRoles = RBBH.CollateralAppraisal.Application.Security.AppRoles;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

public sealed class OrderQueryService : IOrderQueryService
{
    private readonly ApplicationDbContext _db;
    private readonly ICurrentUserService _currentUser;
    private readonly IUserRoleProvider _userRoleProvider;

    public OrderQueryService(
        ApplicationDbContext db,
        ICurrentUserService currentUser,
        IUserRoleProvider userRoleProvider)
    {
        _db = db;
        _currentUser = currentUser;
        _userRoleProvider = userRoleProvider;
    }

    public async Task<AppraisalOrderDetailDto> GetByIdAsync(int orderId, CancellationToken ct = default)
    {
        var order = await _db.AppraisalOrders
            .AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == orderId, ct);

        if (order is null)
            throw new NotFoundException(
                $"Narudžba procjene ID={orderId} nije pronađena.",
                "APPRAISAL_ORDER_NOT_FOUND");

        var codebookIds = new[] { order.CollateralTypeId, order.CombinedCollateralTypeId }
            .Where(id => id is not null)
            .Select(id => id!.Value)
            .Distinct()
            .ToList();

        var labels = codebookIds.Count == 0
            ? new Dictionary<int, string>()
            : await _db.CodebookValues
                .AsNoTracking()
                .Where(x => codebookIds.Contains(x.Id))
                .ToDictionaryAsync(x => x.Id, x => x.Label, ct);

        var coApprovedByName = await ResolveDisplayNameAsync(order.CoApprovedByUserId, ct);
        var originalReceivedByName = await ResolveDisplayNameAsync(order.OriginalReceivedByUserId, ct);

        var correctionTask = await _db.TaskItems
            .AsNoTracking()
            .Where(x => x.AppraisalOrderId == order.Id && x.TaskType == TaskItemType.CorrectDocumentation)
            .OrderByDescending(x => x.CreatedAt)
            .FirstOrDefaultAsync(ct);

        var accessCheckTask = await _db.TaskItems
            .AsNoTracking()
            .Where(x => x.AppraisalOrderId == order.Id && x.TaskType == TaskItemType.AccessCheckCO)
            .OrderByDescending(x => x.CreatedAt)
            .FirstOrDefaultAsync(ct);

        var appraiser = order.AppraiserId is int appraiserId
            ? await _db.Appraisers
                .AsNoTracking()
                .Where(x => x.Id == appraiserId)
                .Select(x => new { x.Name, x.City })
                .FirstOrDefaultAsync(ct)
            : null;

        var protocolNumber = await _db.OrderProtocolEntries
            .AsNoTracking()
            .Where(x => x.OrderId == order.Id)
            .Select(x => x.ProtocolNumber)
            .FirstOrDefaultAsync(ct);

        return new AppraisalOrderDetailDto(
            order.Id,
            order.OrderNumber,
            BuildTitle(order),
            order.Status.ToString(),
            (int)order.Status,
            order.WorkflowType?.ToString(),
            OrderWorkflowRouting.CurrentOwnerRole(order.EffectiveWorkflowType, order.Status),
            OrderWorkflowRouting.NextResponsibleRole(order.EffectiveWorkflowType, order.Status),
            order.ClientName,
            order.ClientType,
            order.ClientIdentifier,
            order.CollateralTypeId,
            order.CollateralTypeId is int collateralTypeId ? labels.GetValueOrDefault(collateralTypeId) : null,
            order.CombinedCollateralTypeId,
            order.CombinedCollateralTypeId is int combinedTypeId ? labels.GetValueOrDefault(combinedTypeId) : null,
            order.City,
            order.PropertyAddress,
            order.PropertyCity,
            order.Branch,
            order.BranchAddress,
            order.ContactName,
            order.ContactPhone,
            order.ContactEmail,
            order.CreatedByUserId,
            order.CreatedByRole,
            order.CreatedAt,
            order.UpdatedAt,
            order.SubmittedAt,
            order.InternalNote,
            coApprovedByName,
            order.CoApprovedAt,
            originalReceivedByName,
            order.OriginalReceivedAt,
            order.AppraiserReminderCount,
            order.AppraiserReminderLastSentAt,
            correctionTask?.Description,
            correctionTask?.Comment,
            accessCheckTask?.Comment,
            order.AppraiserId,
            appraiser?.Name,
            appraiser?.City,
            order.InvoiceSentDate,
            order.InvoiceReceivedDate,
            order.AppraiserVisitDate,
            order.AppraiserRating,
            order.EsgCertificate,
            order.InvoiceStatus.ToString(),
            order.InvoiceUploadedByName,
            order.InvoiceUploadedAt,
            order.InvoiceSentForPaymentByName,
            order.InvoiceSentForPaymentAt,
            order.InvoicePaidByName,
            order.InvoicePaidAt,
            order.InvoiceDocumentId,
            order.AppraisalFee,
            order.CollateralStatus,
            protocolNumber,
            order.OrderSentToAppraiserAt,
            order.SignedDocumentsReceivedAt,
            order.AppraisalDeliveredToCoAt,
            order.CorrectionRequestedAt,
            order.CorrectedAppraisalReceivedAt,
            order.ReadyForProcedureAt,
            order.AcceptedByCAName,
            order.DocumentationReviewStatus is { } drs
                ? DocumentationReviewStatusConverter.ToDbValue(drs)
                : null,
            order.CreatedByName,
            order.SalesConsentSigned,
            order.SalesConsentSignedAt,
            order.SalesConsentSignedByName,
            BuildCapabilities(order, _currentUser.Permissions));
    }

    private async Task<string?> ResolveDisplayNameAsync(string? userId, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(userId))
            return null;

        try
        {
            var user = await _userRoleProvider.GetUserWithRolesAsync(userId, ct);
            return user?.DisplayName ?? user?.Username ?? userId;
        }
        catch
        {
            // Prikaz imena je sekundaran — ako provider (Keycloak) nije dostupan, prikaži samo ID.
            return userId;
        }
    }

    private static string BuildTitle(AppraisalOrder order)
    {
        var location = string.IsNullOrWhiteSpace(order.City) ? null : order.City;
        return location is null
            ? $"Procjena nekretnine — {order.ClientName}"
            : $"Procjena nekretnine — {order.ClientName}, {location}";
    }

    private static OrderDetailCapabilitiesDto BuildCapabilities(AppraisalOrder order, IReadOnlyList<string> permissions)
    {
        bool Has(string permission) => permissions.Contains(permission, StringComparer.OrdinalIgnoreCase);

        var canApproveFinal = Has(AppPermissions.OrdersApproveFinal)
            && order.Status is AppraisalOrderStatus.AppraisalReceived or AppraisalOrderStatus.COApproved;

        var canDownloadFinal = Has(AppPermissions.OrdersDownloadAppraisal)
            && order.FinalAppraisalDocumentId is not null;

        var canConfirmOriginal = Has(AppPermissions.OrdersConfirmOriginal)
            && order.Status == AppraisalOrderStatus.ReadyForProcedure;

        var canRemindAppraiser = Has(AppPermissions.OrdersRemindAppraiser)
            && order.OriginalReceivedAt is null
            && order.Status is AppraisalOrderStatus.ReadyForProcedure
                             or AppraisalOrderStatus.COApproved;

        var canCompleteReview = Has(AppPermissions.OrdersCompleteReview)
            && order.Status is AppraisalOrderStatus.DocumentationReviewInProgress
                             or AppraisalOrderStatus.CorrectionSubmitted
                             or AppraisalOrderStatus.AccessCheckRejected;

        var canRequestCorrection = canCompleteReview;

        var canSubmitCorrection = Has(AppPermissions.OrdersSubmitCorrection)
            && order.Status == AppraisalOrderStatus.ReturnedForCorrection;

        var canAccessCheck = Has(AppPermissions.OrdersAccessCheck)
            && order.Status == AppraisalOrderStatus.AccessCheckRequested;

        var canSelectAppraiser = Has(AppPermissions.OrdersSelectAppraiser)
            && order.AppraiserId is null
            && order.Status is AppraisalOrderStatus.DocumentationApproved or AppraisalOrderStatus.AccessCheckApproved;

        var canSendToAppraiser = Has(AppPermissions.OrdersSendToAppraiser)
            && order.Status == AppraisalOrderStatus.AppraiserSelected;

        var canRequestAdditionalPayment = Has(AppPermissions.OrdersAdditionalPayment)
            && order.Status is AppraisalOrderStatus.OrderSentToAppraiser
                             or AppraisalOrderStatus.AppraisalInProgress;

        var canCompleteAdditionalPayment = Has(AppPermissions.OrdersAdditionalPayment)
            && order.Status == AppraisalOrderStatus.AdditionalPaymentRequested;

        var canGenerateDocuments = Has(AppPermissions.DocumentsUpload)
            && order.Status is AppraisalOrderStatus.DocumentationApproved
                             or AppraisalOrderStatus.AccessCheckApproved
                             or AppraisalOrderStatus.ProtocolCreated
                             or AppraisalOrderStatus.AppraiserSelected;

        var isPL = order.IsPL();

        var canSendQuoteRequests = Has(AppPermissions.OrdersSelectAppraiser) && isPL
            && order.AppraiserId is null
            && order.Status is AppraisalOrderStatus.DocumentationApproved
                             or AppraisalOrderStatus.AccessCheckApproved
                             or AppraisalOrderStatus.ProtocolCreated;

        var canSendThankYou = Has(AppPermissions.OrdersSelectAppraiser) && isPL
            && order.AppraiserId is not null
            && order.Status >= AppraisalOrderStatus.AppraiserSelected;

        var canRejectOrder = Has(AppPermissions.OrdersAdditionalPayment)
            && order.Status is AppraisalOrderStatus.OrderSentToAppraiser
                             or AppraisalOrderStatus.AppraisalInProgress;

        var canAdminRejectOrder = Has(AppPermissions.OrdersSendToAppraiser)
            && order.Status is AppraisalOrderStatus.OrderSentToAppraiser
                             or AppraisalOrderStatus.AppraisalInProgress;

        var canSignConsent = Has(AppPermissions.OrdersSignConsent)
            && order.IsPL()
            && !order.SalesConsentSigned;

        var canReturnForRework = Has(AppPermissions.OrdersApproveFinal)
            && order.Status == AppraisalOrderStatus.AppraisalReceived;

        var canUploadInvoice = Has(AppPermissions.InvoiceUpload)
            && order.InvoiceStatus == InvoiceWorkflowStatus.None
            && order.Status >= AppraisalOrderStatus.AppraisalReceived;

        var canSendInvoiceForPayment = Has(AppPermissions.InvoiceSendForPayment)
            && order.InvoiceStatus == InvoiceWorkflowStatus.Uploaded;

        var canConfirmInvoicePaid = Has(AppPermissions.InvoiceConfirmPayment)
            && order.InvoiceStatus == InvoiceWorkflowStatus.SentForPayment;

        return new OrderDetailCapabilitiesDto(
            CanEdit: false,
            CanSubmit: false,
            CanCancel: false,
            CanApproveFinal: canApproveFinal,
            CanDownloadFinal: canDownloadFinal,
            CanConfirmOriginal: canConfirmOriginal,
            CanRemindAppraiser: canRemindAppraiser,
            CanRequestCorrection: canRequestCorrection,
            CanCompleteReview: canCompleteReview,
            CanSubmitCorrection: canSubmitCorrection,
            CanAccessCheck: canAccessCheck,
            CanSelectAppraiser: canSelectAppraiser,
            CanSendToAppraiser: canSendToAppraiser,
            CanRequestAdditionalPayment: canRequestAdditionalPayment,
            CanCompleteAdditionalPayment: canCompleteAdditionalPayment,
            CanGenerateDocuments: canGenerateDocuments,
            CanSendQuoteRequests: canSendQuoteRequests,
            CanSendThankYou: canSendThankYou,
            CanUploadInvoice: canUploadInvoice,
            CanSendInvoiceForPayment: canSendInvoiceForPayment,
            CanConfirmInvoicePaid: canConfirmInvoicePaid,
            CanRejectOrder: canRejectOrder,
            CanReturnForRework: canReturnForRework,
            CanAdminRejectOrder: canAdminRejectOrder,
            CanSignConsent: canSignConsent);
    }

    // ── GetListAsync + GetSummaryAsync premješteni iz AppraisalOrderService ──────

    public async Task<PagedResult<AppraisalOrderListItemDto>> GetListAsync(
        OrderListRequest request, CancellationToken ct = default)
    {
        var query = _db.AppraisalOrders.AsQueryable();

        if (!_currentUser.Roles.Any(ApplicationAppRoles.OrderViewerRoles.Contains))
            query = query.Where(x => x.CreatedByUserId == _currentUser.UserId);

        if (!string.IsNullOrWhiteSpace(request.Search))
        {
            var s = request.Search.ToLower();
            query = query.Where(x =>
                x.Title.ToLower().Contains(s) ||
                x.ClientName.ToLower().Contains(s) ||
                x.OrderNumber.ToLower().Contains(s));
        }

        if (!string.IsNullOrWhiteSpace(request.Status))
        {
            if (request.Status == "InProgress")
                query = query.Where(x =>
                    x.Status != AppraisalOrderStatus.Draft &&
                    x.Status != AppraisalOrderStatus.SubmittedBySales &&
                    x.Status != AppraisalOrderStatus.Completed &&
                    x.Status != AppraisalOrderStatus.Cancelled);
            else if (Enum.TryParse<AppraisalOrderStatus>(request.Status, out var statusEnum))
                query = query.Where(x => x.Status == statusEnum);
        }

        if (!string.IsNullOrWhiteSpace(request.City))
            query = query.Where(x => x.City == request.City);

        if (request.CollateralTypeId.HasValue)
            query = query.Where(x => x.CollateralTypeId == request.CollateralTypeId);

        if (request.CreatedFrom.HasValue)
        {
            var from = DateTime.SpecifyKind(request.CreatedFrom.Value, DateTimeKind.Utc);
            query = query.Where(x => x.CreatedAt >= from);
        }

        if (request.CreatedTo.HasValue)
        {
            var to = DateTime.SpecifyKind(request.CreatedTo.Value, DateTimeKind.Utc).AddDays(1);
            query = query.Where(x => x.CreatedAt < to);
        }

        if (!string.IsNullOrWhiteSpace(request.AppraisalType))
        {
            if (request.AppraisalType == "STAN")
            {
                var stanIds = await _db.CodebookValues
                    .Where(v => v.CodebookKey == CodebookKeys.CollateralTypes &&
                               (v.Code == CollateralTypeCodes.Apartment || v.Code == CollateralTypeCodes.ApartmentLegacy))
                    .Select(v => v.Id)
                    .ToListAsync(ct);
                if (stanIds.Count > 0)
                    query = query.Where(x => stanIds.Contains(x.CollateralTypeId!.Value) && x.CombinedCollateralTypeId == null);
            }
            else
            {
                var combinedCode = AppraisalTypeFilterCodes.ToCombinedDbCode(request.AppraisalType!);
                if (combinedCode is not null)
                {
                    var combinedId = await _db.CodebookValues
                        .Where(v => v.CodebookKey == CodebookKeys.CombinedCollateralTypes && v.Code == combinedCode)
                        .Select(v => (int?)v.Id)
                        .FirstOrDefaultAsync(ct);
                    if (combinedId.HasValue)
                        query = query.Where(x => x.CombinedCollateralTypeId == combinedId);
                }
            }
        }

        query = (request.SortBy, request.SortDescending) switch
        {
            ("OrderNumber", true)  => query.OrderByDescending(x => x.OrderNumber),
            ("OrderNumber", false) => query.OrderBy(x => x.OrderNumber),
            ("Title", true)        => query.OrderByDescending(x => x.Title),
            ("Title", false)       => query.OrderBy(x => x.Title),
            ("Status", true)       => query.OrderByDescending(x => x.Status),
            ("Status", false)      => query.OrderBy(x => x.Status),
            ("City", true)         => query.OrderByDescending(x => x.City),
            ("City", false)        => query.OrderBy(x => x.City),
            ("UpdatedAt", true)    => query.OrderByDescending(x => x.UpdatedAt),
            ("UpdatedAt", false)   => query.OrderBy(x => x.UpdatedAt),
            (_, false)             => query.OrderBy(x => x.CreatedAt),
            _                      => query.OrderByDescending(x => x.CreatedAt)
        };

        var total  = await query.CountAsync(ct);
        var orders = await query
            .Skip((request.Page - 1) * request.PageSize)
            .Take(request.PageSize)
            .ToListAsync(ct);

        var allTypeIds = orders
            .SelectMany(o => new[] { o.CollateralTypeId, o.CombinedCollateralTypeId })
            .Where(id => id.HasValue)
            .Select(id => id!.Value)
            .Distinct()
            .ToList();

        var labels = await _db.CodebookValues
            .Where(v => allTypeIds.Contains(v.Id))
            .ToDictionaryAsync(v => v.Id, v => v.Label, ct);

        var items = orders.Select(o => new AppraisalOrderListItemDto(
            o.Id, o.OrderNumber, o.Title, o.Status.ToString(), (int)o.Status,
            o.WorkflowType?.ToString(), o.ClientName,
            o.CollateralTypeId.HasValue ? labels.GetValueOrDefault(o.CollateralTypeId.Value) : null,
            o.CombinedCollateralTypeId.HasValue ? labels.GetValueOrDefault(o.CombinedCollateralTypeId.Value) : null,
            o.City, o.CreatedByRole, o.CreatedAt, o.SubmittedAt, o.Branch, o.UpdatedAt
        )).ToList();

        return new PagedResult<AppraisalOrderListItemDto>
        {
            Items = items, TotalCount = total, Page = request.Page, PageSize = request.PageSize
        };
    }

    public async Task<OrderSummaryDto> GetSummaryAsync(CancellationToken ct = default)
    {
        var query = _db.AppraisalOrders.AsQueryable();

        if (!_currentUser.Roles.Any(ApplicationAppRoles.OrderViewerRoles.Contains))
            query = query.Where(x => x.CreatedByUserId == _currentUser.UserId);

        var statusCounts = await query
            .GroupBy(x => x.Status)
            .Select(g => new { Status = g.Key, Count = g.Count() })
            .ToListAsync(ct);

        int CountFor(AppraisalOrderStatus status) =>
            statusCounts.Where(x => x.Status == status).Sum(x => x.Count);

        var draft            = CountFor(AppraisalOrderStatus.Draft);
        var submittedBySales = CountFor(AppraisalOrderStatus.SubmittedBySales);
        var completed        = CountFor(AppraisalOrderStatus.Completed);
        var cancelled        = CountFor(AppraisalOrderStatus.Cancelled);
        var total            = statusCounts.Sum(x => x.Count);
        var inProgress       = total - draft - submittedBySales - completed - cancelled;

        return new OrderSummaryDto(total, draft, submittedBySales, inProgress, completed, cancelled);
    }
}
