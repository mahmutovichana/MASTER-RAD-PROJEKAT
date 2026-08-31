using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Common.Validation;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Application.Orders.Requests;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using RBBH.CollateralAppraisal.Application.Security;
using ApplicationAppRoles = RBBH.CollateralAppraisal.Application.Security.AppRoles;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

/// <summary>
/// Kreiranje i ažuriranje narudžbi — fizički split iz AppraisalOrderService (I-1 refactoring).
/// Odgovoran za: CreateAsync, CreateDraftAsync, UpdateDraftAsync.
/// </summary>
public sealed class OrderCreateService : IOrderCreateService
{
    private readonly ApplicationDbContext _db;
    private readonly ICurrentUserService  _currentUser;
    private readonly IOrderTitleGenerator _titleGenerator;
    private readonly IOrderNumberGenerator _numberGenerator;
    private readonly IAuditService        _audit;
    private readonly IClock               _clock;
    private readonly OrderAuthorizationGuard _authGuard;

    public OrderCreateService(
        ApplicationDbContext    db,
        ICurrentUserService     currentUser,
        IOrderTitleGenerator    titleGenerator,
        IOrderNumberGenerator   numberGenerator,
        IAuditService           audit,
        IClock                  clock)
    {
        _db            = db;
        _currentUser   = currentUser;
        _titleGenerator = titleGenerator;
        _numberGenerator = numberGenerator;
        _audit         = audit;
        _clock         = clock;
        _authGuard     = new OrderAuthorizationGuard(currentUser, audit);
    }

    public async Task<AppraisalOrderDto> CreateAsync(
        CreateOrderRequest request, CancellationToken ct = default)
    {
        OrderRequestValidator.ValidateCreate(request);

        var collateralValue = await GetCodebookValueAsync(request.CollateralTypeId, ct);
        CodebookValue? combinedValue = null;
        if (request.CombinedCollateralTypeId.HasValue)
            combinedValue = await GetCodebookValueAsync(request.CombinedCollateralTypeId.Value, ct);

        EnsureCombinedCollateralIsValid(collateralValue.Code, request.CombinedCollateralTypeId);

        var collateralLabel = collateralValue.Label;
        var combinedLabel   = combinedValue?.Label;

        var orderNumber = await _numberGenerator.GenerateAsync(ct);
        var title       = _titleGenerator.Generate(collateralLabel, combinedLabel, request.ClientName, request.City);

        var order = AppraisalOrder.Create(
            orderNumber, title,
            request.ClientName, request.ClientType, request.ClientIdentifier,
            request.ContactName, request.ContactPhone, request.ContactEmail,
            request.City, request.Branch, request.BranchAddress, request.PropertyAddress,
            request.CollateralTypeId, request.CombinedCollateralTypeId,
            _currentUser.UserId ?? "unknown", _currentUser.Role ?? "unknown", _currentUser.FullName,
            request.DeliveryContactName, request.AmRecipientName,
            workflowType: WorkflowTypes.FromClientType(request.ClientType),
            requestReceivedAt: request.RequestReceivedAt,
            requestSentAt: request.RequestSentAt,
            squareMetersCommercial: request.SquareMetersCommercial,
            squareMetersResidential: request.SquareMetersResidential,
            propertyCity: request.PropertyCity,
            createdByEmail: _currentUser.Email);

        if (!string.IsNullOrWhiteSpace(request.InternalNote))
            order.SetInternalNote(request.InternalNote, _clock.UtcNow);

        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync(ct);

        await _audit.RecordAsync(new AuditEvent
        {
            Action            = AuditActions.OrderCreated,
            OperationType     = AuditOperationTypes.Create,
            Module            = AuditModules.AppraisalOrders,
            EntityType        = "AppraisalOrder",
            EntityKey         = order.Id.ToString(),
            EntityDisplayName = order.Title,
            Status            = AuditStatuses.Success,
            Severity          = AuditSeverity.Info,
            NewValues         = new { order.OrderNumber, order.Title, order.Status }
        }, ct);

        return OrderDtoMapper.ToDto(order, _currentUser, collateralLabel, combinedLabel);
    }

    public async Task<AppraisalOrderDto> CreateDraftAsync(
        string? workflowType = null, CancellationToken ct = default)
    {
        var orderNumber = await _numberGenerator.GenerateAsync(ct);
        var wfType      = WorkflowTypes.Parse(workflowType);

        var order = AppraisalOrder.Create(
            orderNumber, "Nacrt narudžbe",
            clientName: "", clientType: null, clientIdentifier: null,
            contactName: null, contactPhone: null, contactEmail: null,
            city: null, branch: null, branchAddress: null, propertyAddress: null,
            collateralTypeId: null, combinedCollateralTypeId: null,
            _currentUser.UserId ?? "unknown", _currentUser.Role ?? "unknown",
            createdByName: _currentUser.FullName,
            deliveryContactName: null, amRecipientName: null,
            workflowType: wfType,
            createdByEmail: _currentUser.Email);

        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync(ct);

        await _audit.RecordAsync(new AuditEvent
        {
            Action            = AuditActions.OrderDraftCreated,
            OperationType     = AuditOperationTypes.Create,
            Module            = AuditModules.AppraisalOrders,
            EntityType        = "AppraisalOrder",
            EntityKey         = order.Id.ToString(),
            EntityDisplayName = order.Title,
            Status            = AuditStatuses.Success,
            Severity          = AuditSeverity.Info,
            NewValues         = new { order.OrderNumber, order.Title, order.Status }
        }, ct);

        return OrderDtoMapper.ToDto(order, _currentUser, null, null);
    }

    public async Task<AppraisalOrderDto> UpdateDraftAsync(
        int id, UpdateOrderRequest request, bool isAutosave = false, CancellationToken ct = default)
    {
        var order = await _db.AppraisalOrders.FindAsync([id], ct)
            ?? throw new NotFoundException($"Narudžba s ID-om {id} nije pronađena.");

        await _authGuard.EnsureOwnerAsync(order, ct);

        if (order.Status != AppraisalOrderStatus.Draft)
            throw new ValidationException("status", "Samo narudžbe u statusu Draft se mogu mijenjati.");

        var effectiveClientType = request.ClientType ?? order.ClientType;
        var effectiveCity       = request.City       ?? order.City;
        var effectiveBranch     = request.Branch     ?? order.Branch;
        OrderRequestValidator.ValidateUpdate(request, effectiveClientType, effectiveCity, effectiveBranch);

        var collateralId = request.CollateralTypeId ?? order.CollateralTypeId;
        var combinedId   = request.CombinedCollateralTypeId ?? order.CombinedCollateralTypeId;

        if (request.CombinedCollateralTypeId.HasValue && request.CombinedCollateralTypeId.Value == 0)
            combinedId = null;

        var collateralValue = collateralId.HasValue ? await GetCodebookValueAsync(collateralId.Value, ct) : null;
        var combinedValue   = combinedId.HasValue   ? await GetCodebookValueAsync(combinedId.Value,   ct) : null;

        EnsureCombinedCollateralIsValid(collateralValue?.Code, combinedId);

        var collateralLabel = collateralValue?.Label;
        var combinedLabel   = combinedValue?.Label;
        var clientName      = request.ClientName ?? order.ClientName;
        var city            = request.City       ?? order.City ?? string.Empty;
        var title           = _titleGenerator.Generate(collateralLabel ?? "", combinedLabel, clientName, city);
        var before          = SnapshotForAudit(order);
        var now             = _clock.UtcNow;

        order.UpdateDraft(
            title, clientName,
            request.ClientType       ?? order.ClientType,
            request.ClientIdentifier ?? order.ClientIdentifier,
            request.ContactName      ?? order.ContactName,
            request.ContactPhone     ?? order.ContactPhone,
            request.ContactEmail     ?? order.ContactEmail,
            city,
            request.Branch           ?? order.Branch,
            request.BranchAddress    ?? order.BranchAddress,
            request.PropertyAddress  ?? order.PropertyAddress,
            collateralId, combinedId,
            request.DeliveryContactName ?? order.DeliveryContactName,
            request.AmRecipientName     ?? order.AmRecipientName,
            now,
            request.RequestReceivedAt       ?? order.RequestReceivedAt,
            request.RequestSentAt           ?? order.RequestSentAt,
            request.SquareMetersCommercial  ?? order.SquareMetersCommercial,
            request.SquareMetersResidential ?? order.SquareMetersResidential,
            request.PropertyCity            ?? order.PropertyCity);

        if (request.InternalNote != null)
            order.SetInternalNote(request.InternalNote, now);

        if (!string.IsNullOrWhiteSpace(effectiveClientType))
        {
            var wf = WorkflowTypes.FromClientType(effectiveClientType);
            if (order.WorkflowType != wf) order.SetWorkflowType(wf, now);
        }

        await _db.SaveChangesAsync(ct);

        var (oldValues, newValues) = BuildAuditDiff(before, SnapshotForAudit(order));

        await _audit.RecordAsync(new AuditEvent
        {
            Action            = isAutosave ? AuditActions.OrderDraftAutosaved : AuditActions.OrderDraftUpdated,
            OperationType     = AuditOperationTypes.Update,
            Module            = AuditModules.AppraisalOrders,
            EntityType        = "AppraisalOrder",
            EntityKey         = order.Id.ToString(),
            EntityDisplayName = order.Title,
            Status            = AuditStatuses.Success,
            Severity          = AuditSeverity.Info,
            OldValues         = oldValues.Count > 0 ? oldValues : null,
            NewValues         = newValues.Count > 0 ? newValues : null
        }, ct);

        return OrderDtoMapper.ToDto(order, _currentUser, collateralLabel, combinedLabel);
    }

    // ── Privatni helperi ──────────────────────────────────────────────────────

    private async Task<CodebookValue> GetCodebookValueAsync(int id, CancellationToken ct)
    {
        var value = await _db.CodebookValues.FindAsync([id], ct);
        if (value is null)
            throw new ValidationException("collateralTypeId", $"Vrijednost šifarnika s ID-om {id} ne postoji.");
        return value;
    }

    private static void EnsureCombinedCollateralIsValid(string? collateralCode, int? combinedCollateralTypeId)
    {
        if (combinedCollateralTypeId.HasValue &&
            collateralCode is not CombinedBase and not CombinedBaseLegacy)
            throw new ValidationException([
                new ValidationFieldError("combinedCollateralTypeId",
                    ValidationErrorCodes.InvalidCombinedCollateralBase,
                    "Kombinovani tip kolaterala je moguć samo uz osnovni tip 'Stan'.")
            ]);
    }

    private const string CombinedBase       = RBBH.CollateralAppraisal.Application.Common.Constants.CollateralTypeCodes.Apartment;
    private const string CombinedBaseLegacy = RBBH.CollateralAppraisal.Application.Common.Constants.CollateralTypeCodes.ApartmentLegacy;

    private static Dictionary<string, object?> SnapshotForAudit(AppraisalOrder o) => new()
    {
        [nameof(AppraisalOrder.ClientName)]               = o.ClientName,
        [nameof(AppraisalOrder.ClientType)]               = o.ClientType,
        [nameof(AppraisalOrder.ClientIdentifier)]         = o.ClientIdentifier,
        [nameof(AppraisalOrder.City)]                     = o.City,
        [nameof(AppraisalOrder.Branch)]                   = o.Branch,
        [nameof(AppraisalOrder.ContactPhone)]             = o.ContactPhone,
        [nameof(AppraisalOrder.ContactEmail)]             = o.ContactEmail,
        [nameof(AppraisalOrder.CollateralTypeId)]         = o.CollateralTypeId,
        [nameof(AppraisalOrder.CombinedCollateralTypeId)] = o.CombinedCollateralTypeId,
    };

    private static (Dictionary<string, object?> Old, Dictionary<string, object?> New) BuildAuditDiff(
        Dictionary<string, object?> before, Dictionary<string, object?> after)
    {
        var old = new Dictionary<string, object?>();
        var @new = new Dictionary<string, object?>();
        foreach (var (key, oldValue) in before)
        {
            var newValue = after[key];
            if (!Equals(oldValue, newValue)) { old[key] = oldValue; @new[key] = newValue; }
        }
        return (old, @new);
    }
}
