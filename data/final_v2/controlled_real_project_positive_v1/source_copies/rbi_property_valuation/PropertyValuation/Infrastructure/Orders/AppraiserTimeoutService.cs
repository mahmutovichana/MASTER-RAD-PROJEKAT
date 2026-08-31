using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using ApplicationAppRoles = RBBH.CollateralAppraisal.Application.Security.AppRoles;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

[System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage]
public sealed class AppraiserTimeoutService : BackgroundService
{
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly ILogger<AppraiserTimeoutService> _logger;
    private readonly TimeSpan _checkInterval;
    private readonly TimeSpan _timeoutWindow;

    public AppraiserTimeoutService(
        IServiceScopeFactory scopeFactory,
        ILogger<AppraiserTimeoutService> logger,
        IOptions<WorkflowSlaOptions> slaOptions)
    {
        _scopeFactory   = scopeFactory;
        _logger         = logger;
        _checkInterval  = TimeSpan.FromMinutes(slaOptions.Value.AppraiserTimeoutCheckIntervalMinutes);
        _timeoutWindow  = TimeSpan.FromHours(slaOptions.Value.AppraiserTimeoutWindowHours);
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await TryCheckTimeoutsAsync(stoppingToken);
            }
            catch (OperationCanceledException)
            {
                // Normalan shutdown — ne logujemo kao grešku
                break;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Greška pri provjeri timeout-a vještaka.");
            }

            await Task.Delay(_checkInterval, stoppingToken);
        }
    }

    private async Task TryCheckTimeoutsAsync(CancellationToken ct)
    {
        using var scope = _scopeFactory.CreateScope();
        var jobLock     = scope.ServiceProvider.GetRequiredService<IDistributedJobLock>();

        if (!await jobLock.TryAcquireAsync(DistributedLockKeys.AppraiserUploadTimeout, ct))
        {
            _logger.LogDebug("AppraiserTimeoutService: preskačem ciklus — lock drži drugi čvor.");
            return;
        }

        try   { await CheckTimeoutsAsync(scope.ServiceProvider, ct); }
        finally { await jobLock.ReleaseAsync(DistributedLockKeys.AppraiserUploadTimeout, ct); }
    }

    private async Task CheckTimeoutsAsync(IServiceProvider sp, CancellationToken ct)
    {
        var db = sp.GetRequiredService<ApplicationDbContext>();
        var notificationProvider = sp.GetRequiredService<INotificationProvider>();
        var audit = sp.GetRequiredService<IAuditService>();

        var cutoff = DateTime.UtcNow.Subtract(_timeoutWindow);

        var timedOutTasks = await db.TaskItems
            .Include(t => t.AppraisalOrder)
            .Where(t => t.TaskType == TaskItemType.UploadFinalAppraisal
                     && t.Status == TaskItemStatus.Open
                     && t.CreatedAt <= cutoff
                     && t.AppraisalOrder != null
                     && t.AppraisalOrder.Status == AppraisalOrderStatus.OrderSentToAppraiser)
            .ToListAsync(ct);

        if (timedOutTasks.Count == 0) return;

        _logger.LogInformation("Pronađeno {Count} narudžbi s isteklim rokom prihvatanja vještaka.", timedOutTasks.Count);

        foreach (var task in timedOutTasks)
        {
            try
            {
                var order = task.AppraisalOrder!;
                var now = DateTime.UtcNow;
                var rejectedAppraiserId = order.AppraiserId;

                string? appraiserName = null;
                string? appraiserEmail = null;
                if (rejectedAppraiserId.HasValue)
                {
                    var appraiser = await db.Appraisers
                        .AsNoTracking()
                        .FirstOrDefaultAsync(a => a.Id == rejectedAppraiserId.Value, ct);
                    appraiserName = appraiser?.Name;
                    appraiserEmail = appraiser?.ContactEmail;
                }

                task.Cancel(now);
                order.RejectByAppraiser(now);

                db.TaskItems.Add(TaskItem.Create(
                    orderId: order.Id,
                    type: TaskItemType.SelectAppraiser,
                    title: $"Ponovni odabir vještaka — {order.OrderNumber}",
                    description: $"Vještak {appraiserName ?? "—"} nije reagovao u roku od 24h. Potreban novi odabir.",
                    assignedRole: ApplicationAppRoles.KolateralAdministrator));

                await db.SaveChangesAsync(ct);

                try
                {
                    await notificationProvider.SendAsync(new NotificationRequest(
                        RecipientUserId: null,
                        RecipientRole: ApplicationAppRoles.KolateralAdministrator,
                        Channel: NotificationChannel.InApp,
                        Subject: $"Timeout vještaka — {order.OrderNumber}",
                        Message: $"Vještak {appraiserName ?? "—"} nije prihvatio narudžbu {order.OrderNumber} u roku od 24h. Potreban je ponovni odabir vještaka.",
                        RelatedEntityType: "AppraisalOrder",
                        RelatedEntityId: order.Id.ToString()), ct);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Notifikacija CA za timeout narudžbe {OrderId}.", order.Id);
                }

                if (!string.IsNullOrWhiteSpace(appraiserEmail))
                {
                    try
                    {
                        await notificationProvider.SendAsync(new NotificationRequest(
                            RecipientUserId: null, RecipientRole: null,
                            Channel: NotificationChannel.Email,
                            Subject: $"Obustava narudžbe procjene — {order.OrderNumber}",
                            Message: $"Poštovani {appraiserName ?? ""},\n\n" +
                                     $"Proces narudžbe procjene za klijenta {order.ClientName} ({order.OrderNumber}) se obustavlja jer narudžba nije prihvaćena u roku od 24 sata.",
                            RelatedEntityType: "AppraisalOrder",
                            RelatedEntityId: order.Id.ToString(),
                            RecipientEmail: appraiserEmail), ct);
                    }
                    catch (Exception ex)
                    {
                        _logger.LogError(ex, "Email notifikacija vještaku za timeout narudžbe {OrderId}.", order.Id);
                    }
                }

                try
                {
                    await audit.RecordAsync(new AuditEvent
                    {
                        Action = "ORDER_APPRAISER_TIMEOUT",
                        OperationType = AuditOperationTypes.Update,
                        Module = AuditModules.AppraisalOrders,
                        EntityType = "AppraisalOrder",
                        EntityKey = order.Id.ToString(),
                        EntityDisplayName = order.OrderNumber,
                        NewValues = new { TimedOutAppraiser = appraiserName, After = "24h" },
                        Status = AuditStatuses.Success,
                        Severity = AuditSeverity.Warning
                    }, ct);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Audit za timeout narudžbe {OrderId}.", order.Id);
                }

                _logger.LogInformation("Timeout vještaka {Appraiser} za narudžbu {OrderNumber}.", appraiserName, order.OrderNumber);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Greška pri obradi timeout-a za task {TaskId}.", task.Id);
            }
        }
    }
}
