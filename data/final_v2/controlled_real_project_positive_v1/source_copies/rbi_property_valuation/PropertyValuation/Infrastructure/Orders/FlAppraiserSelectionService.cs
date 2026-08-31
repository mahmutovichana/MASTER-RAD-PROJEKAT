using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Appraisers;
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
/// FL workflow: automatski algoritamski odabir vještaka.
/// Fizički split iz AppraiserAssignmentService (I-2 refactoring).
/// </summary>
public sealed class FlAppraiserSelectionService : IFlAppraiserSelectionService
{
    private readonly ApplicationDbContext       _db;
    private readonly IAppraiserSelectionService _selectionService;
    private readonly IProtocolService           _protocolService;
    private readonly AppraiserAssignmentHelpers _h;

    public FlAppraiserSelectionService(
        ApplicationDbContext       db,
        ICurrentUserService        currentUser,
        IAppraiserSelectionService selectionService,
        INotificationProvider      notificationProvider,
        IAuditService              audit,
        IProtocolService           protocolService,
        ILogger<FlAppraiserSelectionService> logger)
    {
        _db               = db;
        _selectionService = selectionService;
        _protocolService  = protocolService;
        _h                = new AppraiserAssignmentHelpers(db, currentUser, notificationProvider, audit, logger);
    }

    public async Task<AppraiserAssignmentResultDto> AutoSelectAppraiserAsync(int orderId, CancellationToken ct = default)
    {
        var userId = _h.RequireCurrentUserId();
        var order  = await _h.FindOrderAsync(orderId, ct);

        if (!order.IsFL())
            throw new ConflictException(
                "Automatski odabir vještaka je dostupan samo za narudžbe fizičkih lica (FL).",
                "APPRAISER_AUTO_SELECT_NOT_FL");

        if (order.AppraiserId is not null)
            throw new ConflictException("Vještak je već odabran za ovu narudžbu.", "APPRAISER_ALREADY_SELECTED");

        var selectTask = await _h.FindActiveTaskAsync(orderId, TaskItemType.SelectAppraiser, ct)
            ?? throw new ConflictException(
                "Aktivan zadatak odabira vještaka nije pronađen.",
                "SELECT_APPRAISER_TASK_NOT_FOUND");

        var declinedIds = await GetDeclinedAppraiserIdsAsync(orderId, ct);
        var appraiser   = await _selectionService.SelectForOrderAsync(order, declinedIds, ct)
            ?? throw new ConflictException(
                "Nema dostupnog vještaka koji ispunjava uslove — potrebna ručna intervencija.",
                "NO_APPRAISER_AVAILABLE");

        if (!appraiser.CanHandle(order.WorkflowType))
            throw new ConflictException(
                "Automatski odabrani vještak ne procjenjuje ovu vrstu klijenta — potrebna ručna intervencija.",
                "NO_APPRAISER_AVAILABLE");

        var now       = DateTime.UtcNow;
        var oldStatus = order.Status;

        order.SelectAppraiser(appraiser.Id, now);
        selectTask.Complete(userId, $"Automatski odabran vještak: {appraiser.Name}", now);

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
            $"Narudžba {order.OrderNumber} — {order.Title}: automatski je odabran vještak {appraiser.Name}. Narudžba je spremna za slanje vještaku.",
            order.Id, ct);

        await _h.RecordAuditAsync(AuditActions.AppraiserSelected, order, oldStatus, notificationSent,
            new { AppraiserId = appraiser.Id, AppraiserName = appraiser.Name, Mode = "Auto" }, ct);

        return new AppraiserAssignmentResultDto(
            order.Id, order.OrderNumber, order.Status.ToString(), (int)order.Status,
            appraiser.Id, appraiser.Name, appraiser.City,
            notificationSent, $"Automatski odabran vještak: {appraiser.Name}.");
    }

    private async Task<List<int>> GetDeclinedAppraiserIdsAsync(int orderId, CancellationToken ct) =>
        await _db.Set<OrderDeclinedAppraiser>()
            .Where(d => d.AppraisalOrderId == orderId)
            .Select(d => d.AppraiserId)
            .ToListAsync(ct);
}
