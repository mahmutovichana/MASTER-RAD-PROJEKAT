using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using ApplicationAppRoles = RBBH.CollateralAppraisal.Application.Security.AppRoles;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

/// <summary>
/// PL workflow: lista kandidata i ručni odabir vještaka.
/// Fizički split iz AppraiserAssignmentService (I-2 refactoring).
/// </summary>
public sealed class PlAppraiserSelectionService : IPlAppraiserSelectionService
{
    private readonly ApplicationDbContext _db;
    private readonly IProtocolService     _protocolService;
    private readonly AppraiserAssignmentHelpers _h;

    public PlAppraiserSelectionService(
        ApplicationDbContext  db,
        ICurrentUserService   currentUser,
        INotificationProvider notificationProvider,
        IAuditService         audit,
        IProtocolService      protocolService,
        ILogger<PlAppraiserSelectionService> logger)
    {
        _db              = db;
        _protocolService = protocolService;
        _h               = new AppraiserAssignmentHelpers(db, currentUser, notificationProvider, audit, logger);
    }

    public async Task<IReadOnlyList<AppraiserDto>> GetCandidatesForOrderAsync(int orderId, CancellationToken ct = default)
    {
        var order = await _h.FindOrderAsync(orderId, ct);

        var candidates = await _db.Appraisers
            .AsNoTracking()
            .Where(a => a.IsActive && !a.IsBlacklisted && !a.IsOnLeave)
            .ToListAsync(ct);

        candidates = candidates.Where(a => a.CanHandle(order.WorkflowType)).ToList();

        if (!string.IsNullOrWhiteSpace(order.City))
        {
            var inCity = candidates
                .Where(a => string.Equals(a.City, order.City, StringComparison.OrdinalIgnoreCase))
                .ToList();
            if (inCity.Count > 0) candidates = inCity;
        }

        var activeCounts  = await GetActiveCountsAsync(ct);
        var maxCandidates = order.IsPL() ? 3 : int.MaxValue;

        return candidates
            .Select(a => new { Appraiser = a, ActiveCount = activeCounts.TryGetValue(a.Id, out var c) ? c : 0 })
            .OrderBy(x => x.ActiveCount)
            .ThenBy(x => x.Appraiser.Id)
            .Take(maxCandidates)
            .Select(x => new AppraiserDto(
                x.Appraiser.Id, x.Appraiser.Name, x.Appraiser.City, x.Appraiser.LegalForm.ToString(),
                x.Appraiser.IsOnLeave, x.Appraiser.IsBlacklisted, x.Appraiser.IsActive,
                x.ActiveCount, x.Appraiser.ContactEmail, x.Appraiser.ContactPhone, x.Appraiser.Notes,
                x.Appraiser.SupportedPropertyTypes, x.Appraiser.CreatedAt, x.Appraiser.UpdatedAt))
            .ToList();
    }

    public async Task<AppraiserAssignmentResultDto> ManualSelectAppraiserAsync(int orderId, int appraiserId, CancellationToken ct = default)
    {
        var userId = _h.RequireCurrentUserId();
        var order  = await _h.FindOrderAsync(orderId, ct);

        if (order.AppraiserId is not null)
            throw new ConflictException("Vještak je već odabran za ovu narudžbu.", "APPRAISER_ALREADY_SELECTED");

        var selectTask = await _h.FindActiveTaskAsync(orderId, TaskItemType.SelectAppraiser, ct)
            ?? throw new ConflictException("Aktivan zadatak odabira vještaka nije pronađen.", "SELECT_APPRAISER_TASK_NOT_FOUND");

        var appraiser = await _db.Appraisers.FirstOrDefaultAsync(x => x.Id == appraiserId, ct)
            ?? throw new NotFoundException($"Vještak ID={appraiserId} nije pronađen.", "APPRAISER_NOT_FOUND");

        if (!appraiser.IsActive || appraiser.IsBlacklisted || appraiser.IsOnLeave)
            throw new ConflictException("Odabrani vještak nije dostupan (neaktivan, na crnoj listi ili na godišnjem odmoru).", "APPRAISER_NOT_AVAILABLE");

        if (!appraiser.CanHandle(order.WorkflowType))
            throw new ConflictException("Odabrani vještak ne procjenjuje ovu vrstu klijenta (fizička/pravna lica).", "APPRAISER_SCOPE_MISMATCH");

        var now       = DateTime.UtcNow;
        var oldStatus = order.Status;

        order.SelectAppraiser(appraiser.Id, now);
        selectTask.Complete(userId, $"Ručno odabran vještak: {appraiser.Name}", now);

        _db.TaskItems.Add(TaskItem.Create(
            orderId:      order.Id,
            type:         TaskItemType.SendOrderToAppraiser,
            title:        $"Slanje narudžbe vještaku — {order.OrderNumber}",
            description:  $"Odabran vještak: {appraiser.Name}",
            assignedRole: ApplicationAppRoles.KolateralAdministrator));

        await using var tx = await _db.Database.BeginTransactionAsync(ct);
        try
        {
            await _db.SaveChangesAsync(ct);
            await _protocolService.CreateProtocolForOrderAsync(order.Id, ct);
            await tx.CommitAsync(ct);
        }
        catch
        {
            await tx.RollbackAsync(ct);
            throw;
        }

        var notificationSent = await _h.NotifyRoleAsync(
            ApplicationAppRoles.KolateralAdministrator, "Vještak odabran",
            $"Narudžba {order.OrderNumber} — {order.Title}: ručno je odabran vještak {appraiser.Name}. Narudžba je spremna za slanje vještaku.",
            order.Id, ct);

        await _h.RecordAuditAsync(AuditActions.AppraiserSelected, order, oldStatus, notificationSent,
            new { AppraiserId = appraiser.Id, AppraiserName = appraiser.Name, Mode = "Manual" }, ct);

        return new AppraiserAssignmentResultDto(
            order.Id, order.OrderNumber, order.Status.ToString(), (int)order.Status,
            appraiser.Id, appraiser.Name, appraiser.City,
            notificationSent, $"Ručno odabran vještak: {appraiser.Name}.");
    }

    private async Task<Dictionary<int, int>> GetActiveCountsAsync(CancellationToken ct) =>
        await _db.AppraisalOrders
            .Where(o => o.AppraiserId != null && AppraisalOrderStatusGroups.ActiveAppraisalStatuses.Contains(o.Status))
            .GroupBy(o => o.AppraiserId!.Value)
            .Select(g => new { AppraiserId = g.Key, Count = g.Count() })
            .ToDictionaryAsync(x => x.AppraiserId, x => x.Count, ct);
}
