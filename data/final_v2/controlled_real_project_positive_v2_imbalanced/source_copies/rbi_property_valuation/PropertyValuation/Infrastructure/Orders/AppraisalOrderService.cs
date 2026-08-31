using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Application.Orders.Requests;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using ApplicationAppRoles = RBBH.CollateralAppraisal.Application.Security.AppRoles;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

/// <summary>
/// Facade implementacija IAppraisalOrderService — delegira na fokusirane sub-servise.
/// Fizički split izvršen u I-1 refactoringu:
///   - OrderCreateService  → CreateAsync, CreateDraftAsync, UpdateDraftAsync
///   - OrderSubmitService  → SubmitAsync, CancelAsync
///   - GetByIdAsync ostaje ovdje (potreban direktan pristup DB + audit)
///
/// AppraisalOrderService je registriran kao IAppraisalOrderService u DI kontejneru;
/// sub-servisi su dostupni i direktno (IOrderCreateService, IOrderSubmitService).
/// </summary>
public sealed class AppraisalOrderService : IAppraisalOrderService
{
    private readonly ApplicationDbContext _db;
    private readonly ICurrentUserService  _currentUser;
    private readonly IAuditService        _audit;
    private readonly OrderAuthorizationGuard _authGuard;
    private readonly IOrderCreateService  _createSvc;
    private readonly IOrderSubmitService  _submitSvc;

    public AppraisalOrderService(
        ApplicationDbContext db,
        ICurrentUserService  currentUser,
        IAuditService        audit,
        IOrderCreateService  createSvc,
        IOrderSubmitService  submitSvc)
    {
        _db        = db;
        _currentUser = currentUser;
        _audit     = audit;
        _authGuard = new OrderAuthorizationGuard(currentUser, audit);
        _createSvc = createSvc;
        _submitSvc = submitSvc;
    }

    // ── Delegiranje na sub-servise ─────────────────────────────────────────────

    public Task<AppraisalOrderDto> CreateAsync(CreateOrderRequest request, CancellationToken ct = default)
        => _createSvc.CreateAsync(request, ct);

    public Task<AppraisalOrderDto> CreateDraftAsync(string? workflowType = null, CancellationToken ct = default)
        => _createSvc.CreateDraftAsync(workflowType, ct);

    public Task<AppraisalOrderDto> UpdateDraftAsync(int id, UpdateOrderRequest request, bool isAutosave = false, CancellationToken ct = default)
        => _createSvc.UpdateDraftAsync(id, request, isAutosave, ct);

    public Task<AppraisalOrderDto> SubmitAsync(int id, CancellationToken ct = default)
        => _submitSvc.SubmitAsync(id, ct);

    public Task CancelAsync(int id, CancellationToken ct = default)
        => _submitSvc.CancelAsync(id, ct);

    // ── GetByIdAsync — direktna query operacija (ostaje ovdje jer je query, ne command) ──

    public async Task<AppraisalOrderDto> GetByIdAsync(int id, CancellationToken ct = default)
    {
        var order = await _db.AppraisalOrders.FindAsync([id], ct)
            ?? throw new NotFoundException($"Narudžba s ID-om {id} nije pronađena.");

        await _authGuard.EnsureCanViewAsync(order, ct);

        await _audit.RecordAsync(new AuditEvent
        {
            Action            = AuditActions.OrderViewed,
            OperationType     = AuditOperationTypes.Read,
            Module            = AuditModules.AppraisalOrders,
            EntityType        = "AppraisalOrder",
            EntityKey         = order.Id.ToString(),
            EntityDisplayName = order.Title,
            Status            = AuditStatuses.Success,
            Severity          = AuditSeverity.Info
        }, ct);

        var collateralLabel = order.CollateralTypeId.HasValue
            ? await CodebookQueryHelper.GetLabelAsync(_db, order.CollateralTypeId.Value, ct) : null;
        var combinedLabel = order.CombinedCollateralTypeId.HasValue
            ? await CodebookQueryHelper.GetLabelAsync(_db, order.CombinedCollateralTypeId.Value, ct) : null;

        var protocolNumber = await _db.OrderProtocolEntries
            .AsNoTracking()
            .Where(p => p.OrderId == order.Id)
            .Select(p => p.ProtocolNumber)
            .FirstOrDefaultAsync(ct);

        return OrderDtoMapper.ToDto(order, _currentUser, collateralLabel, combinedLabel, protocolNumber);
    }

    public async Task<PagedResult<AppraisalOrderListItemDto>> GetListAsync(
        OrderListRequest request, CancellationToken ct = default)
    {
        var query = _db.AppraisalOrders.AsQueryable();

        // Prodajna rola vidi samo vlastite narudžbe; Administrator/CA i ostale
        // workflow role (CO, Vještak, Pravna, Protokol) vide zajednički red narudžbi.
        var seesAllOrders =
            _currentUser.Roles.Contains(ApplicationAppRoles.Administrator) ||
            _currentUser.Roles.Contains(ApplicationAppRoles.KolateralAdministrator) ||
            _currentUser.Roles.Contains(ApplicationAppRoles.KolateralOficir) ||
            _currentUser.Roles.Contains(ApplicationAppRoles.Vjestak) ||
            _currentUser.Roles.Contains(ApplicationAppRoles.PravnaSluzba) ||
            _currentUser.Roles.Contains(ApplicationAppRoles.Protokol);
        if (!seesAllOrders)
        {
            query = query.Where(x => x.CreatedByUserId == _currentUser.UserId);
        }

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
            {
                query = query.Where(x =>
                    x.Status != AppraisalOrderStatus.Draft &&
                    x.Status != AppraisalOrderStatus.SubmittedBySales &&
                    x.Status != AppraisalOrderStatus.Completed &&
                    x.Status != AppraisalOrderStatus.Cancelled);
            }
            else if (Enum.TryParse<AppraisalOrderStatus>(request.Status, out var statusEnum))
            {
                query = query.Where(x => x.Status == statusEnum);
            }
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
                // Čisti stan — bez kombinovanog kolaterala
                var stanId = await _db.CodebookValues
                    .Where(v => v.CodebookKey == "tipovi_kolaterala" && v.Code == "APP_STAN")
                    .Select(v => (int?)v.Id)
                    .FirstOrDefaultAsync(ct);
                if (stanId.HasValue)
                    query = query.Where(x => x.CollateralTypeId == stanId && x.CombinedCollateralTypeId == null);
            }
            else
            {
                // Kombinovani tipovi — filter po konkretnom kombinovanom kolateralu
                var combinedCode = request.AppraisalType switch
                {
                    "STAN_I_GARAZA"        => "APP_STAN_I_GARAZA",
                    "STAN_I_OSTAVA"        => "APP_STAN_I_OSTAVA",
                    "STAN_GARAZA_I_OSTAVA" => "APP_STAN_GARAZA_I_OSTAVA",
                    _                      => null
                };

                if (combinedCode is not null)
                {
                    var combinedId = await _db.CodebookValues
                        .Where(v => v.CodebookKey == "kombinovani_tipovi_kolaterala" && v.Code == combinedCode)
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

        // Batch load labela šifarnika
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
            o.Id,
            o.OrderNumber,
            o.Title,
            o.Status.ToString(),
            (int)o.Status,
            o.WorkflowType?.ToString(),
            o.ClientName,
            o.CollateralTypeId.HasValue ? labels.GetValueOrDefault(o.CollateralTypeId.Value) : null,
            o.CombinedCollateralTypeId.HasValue ? labels.GetValueOrDefault(o.CombinedCollateralTypeId.Value) : null,
            o.City,
            o.CreatedByRole,
            o.CreatedAt,
            o.SubmittedAt,
            o.Branch,
            o.UpdatedAt
        )).ToList();

        return new PagedResult<AppraisalOrderListItemDto>
        {
            Items      = items,
            TotalCount = total,
            Page       = request.Page,
            PageSize   = request.PageSize
        };
    }

    public async Task<OrderSummaryDto> GetSummaryAsync(CancellationToken ct = default)
    {
        var query = _db.AppraisalOrders.AsQueryable();

        // Prodajna rola vidi samo vlastite narudžbe; Administrator/CA i ostale
        // workflow role (CO, Vještak, Pravna, Protokol) vide zajednički red narudžbi.
        var seesAllOrders =
            _currentUser.Roles.Contains(ApplicationAppRoles.Administrator) ||
            _currentUser.Roles.Contains(ApplicationAppRoles.KolateralAdministrator) ||
            _currentUser.Roles.Contains(ApplicationAppRoles.KolateralOficir) ||
            _currentUser.Roles.Contains(ApplicationAppRoles.Vjestak) ||
            _currentUser.Roles.Contains(ApplicationAppRoles.PravnaSluzba) ||
            _currentUser.Roles.Contains(ApplicationAppRoles.Protokol);
        if (!seesAllOrders)
        {
            query = query.Where(x => x.CreatedByUserId == _currentUser.UserId);
        }

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
