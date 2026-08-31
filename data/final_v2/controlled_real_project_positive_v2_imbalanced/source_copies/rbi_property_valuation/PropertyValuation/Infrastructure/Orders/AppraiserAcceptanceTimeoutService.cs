using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Appraisers;
using RBBH.CollateralAppraisal.Application.Common;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Application.Users.Models;
using RBBH.CollateralAppraisal.Domain.Appraisers;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using ApplicationAppRoles = RBBH.CollateralAppraisal.Application.Security.AppRoles;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

/// <summary>
/// Pozadinski servis koji svakih 30 minuta provjerava narudžbe u statusu
/// <see cref="AppraisalOrderStatus.OrderSentToAppraiser"/> i blokira vještake
/// koji nisu odgovorili u roku od 24 sata.
/// Blokirani vještak prima email potvrdu; sistem pokušava automatski dodijeliti
/// sljedećeg vještaka.
/// </summary>
[System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage]
public sealed class AppraiserAcceptanceTimeoutService : BackgroundService
{
    private static readonly TimeSpan CheckInterval = TimeSpan.FromMinutes(30);
    private const int AcceptanceHours = 24;

    private readonly IServiceScopeFactory _scopeFactory;
    private readonly ILogger<AppraiserAcceptanceTimeoutService> _logger;

    public AppraiserAcceptanceTimeoutService(
        IServiceScopeFactory scopeFactory,
        ILogger<AppraiserAcceptanceTimeoutService> logger)
    {
        _scopeFactory = scopeFactory;
        _logger       = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation(
            "AppraiserAcceptanceTimeoutService pokrenut — provjera svakih {Interval} min.",
            CheckInterval.TotalMinutes);

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await TryCheckAndHandleTimeoutsAsync(stoppingToken);
            }
            catch (Exception ex) when (ex is not OperationCanceledException)
            {
                _logger.LogError(ex, "Greška pri provjeri isteklih rokova prihvatanja vještaka.");
            }

            await Task.Delay(CheckInterval, stoppingToken);
        }
    }

    private async Task TryCheckAndHandleTimeoutsAsync(CancellationToken ct)
    {
        using var scope = _scopeFactory.CreateScope();
        var jobLock     = scope.ServiceProvider.GetRequiredService<IDistributedJobLock>();

        if (!await jobLock.TryAcquireAsync(DistributedLockKeys.AppraiserAcceptanceTimeout, ct))
        {
            _logger.LogDebug("AppraiserAcceptanceTimeoutService: preskačem ciklus — lock drži drugi čvor.");
            return;
        }

        try   { await CheckAndHandleTimeoutsAsync(scope.ServiceProvider, ct); }
        finally { await jobLock.ReleaseAsync(DistributedLockKeys.AppraiserAcceptanceTimeout, ct); }
    }

    private async Task CheckAndHandleTimeoutsAsync(IServiceProvider sp, CancellationToken ct)
    {
        var db                   = sp.GetRequiredService<ApplicationDbContext>();
        var notificationProvider = sp.GetRequiredService<INotificationProvider>();
        var selectionService     = sp.GetRequiredService<IAppraiserSelectionService>();
        var userRoleProvider     = sp.GetRequiredService<IUserRoleProvider>();

        var cutoff = DateTime.UtcNow.AddHours(-AcceptanceHours);

        // ID-evi narudžbi koje imaju otvoren AcceptAppraiserOrder task.
        var orderIdsWithOpenTask = await db.TaskItems
            .Where(t => t.TaskType == TaskItemType.AcceptAppraiserOrder
                     && t.Status == TaskItemStatus.Open)
            .Select(t => t.AppraisalOrderId)
            .Distinct()
            .ToListAsync(ct);

        if (orderIdsWithOpenTask.Count == 0)
            return;

        // Narudžbe poslane vještaku > 24h koje imaju otvoren AcceptAppraiserOrder task.
        var timedOutOrders = await db.AppraisalOrders
            .Where(o => o.Status == AppraisalOrderStatus.OrderSentToAppraiser
                     && o.OrderSentToAppraiserAt != null
                     && o.OrderSentToAppraiserAt < cutoff
                     && o.AppraiserId != null
                     && orderIdsWithOpenTask.Contains(o.Id))
            .ToListAsync(ct);

        if (timedOutOrders.Count == 0)
            return;

        _logger.LogInformation("Pronađeno {Count} narudžbi s isteklim rokom prihvatanja.", timedOutOrders.Count);

        foreach (var order in timedOutOrders)
        {
            await HandleTimeoutAsync(order, db, notificationProvider, selectionService, userRoleProvider, ct);
        }
    }

    private async Task HandleTimeoutAsync(
        AppraisalOrder order,
        ApplicationDbContext db,
        INotificationProvider notificationProvider,
        IAppraiserSelectionService selectionService,
        IUserRoleProvider userRoleProvider,
        CancellationToken ct)
    {
        var now                 = DateTime.UtcNow;
        var timedOutAppraiserId = order.AppraiserId!.Value;

        var appraiser = await db.Appraisers.AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == timedOutAppraiserId, ct);

        if (appraiser is null)
        {
            _logger.LogWarning(
                "Vještak ID={Id} nije pronađen za narudžbu {OrderId}.", timedOutAppraiserId, order.Id);
            return;
        }

        _logger.LogInformation(
            "Timeout: narudžba {OrderNumber} — vještak {Appraiser} nije odgovorio u roku {Hours}h.",
            order.OrderNumber, appraiser.Name, AcceptanceHours);

        // Evidentiraj timeout.
        db.Set<OrderDeclinedAppraiser>().Add(
            OrderDeclinedAppraiser.Create(
                order.Id, timedOutAppraiserId,
                AppraiserDeclineReason.Timeout,
                null, true, now));

        // Otkaži otvoren AcceptAppraiserOrder task.
        var acceptTask = await db.TaskItems
            .Where(t => t.AppraisalOrderId == order.Id
                     && t.TaskType == TaskItemType.AcceptAppraiserOrder
                     && t.Status == TaskItemStatus.Open)
            .OrderByDescending(t => t.CreatedAt)
            .FirstOrDefaultAsync(ct);

        acceptTask?.Cancel(now);

        // Resetuj narudžbu — status → AppraiserSelected, AppraiserId = null.
        order.RejectByAppraiser(now);

        await db.SaveChangesAsync(ct);

        // Notifikacija blokiranom vještaku.
        if (!string.IsNullOrWhiteSpace(appraiser.ContactEmail))
        {
            await SendEmailAsync(
                notificationProvider,
                appraiser.ContactEmail,
                $"Narudžba procjene za klijenta {order.ClientName} — istekao rok",
                $"Poštovani {appraiser.Name},\n\n" +
                $"Proces narudžbe procjene za klijenta {order.ClientName} se obustavlja za vas.\n" +
                $"Razlog: niste prihvatili narudžbu {order.OrderNumber} u roku od {AcceptanceHours} sata.\n\n" +
                "Narudžba će biti dodijeljena sljedećem vještaku.",
                order.Id, ct);
        }

        // Notifikacija CA.
        await SendRoleNotificationAsync(
            notificationProvider,
            ApplicationAppRoles.KolateralAdministrator,
            $"Vještak nije odgovorio u roku — {order.OrderNumber}",
            $"Narudžba {order.OrderNumber}: vještak {appraiser.Name} nije prihvatio narudžbu u roku od {AcceptanceHours}h. " +
            "Sistem pokušava dodijeliti sljedećeg vještaka.",
            order.Id, ct);

        // Pokušaj automatski dodijeliti sljedećeg vještaka.
        var declinedIds = await db.Set<OrderDeclinedAppraiser>()
            .Where(d => d.AppraisalOrderId == order.Id)
            .Select(d => d.AppraiserId)
            .ToListAsync(ct);

        var nextAppraiser = await selectionService.SelectForOrderAsync(order, declinedIds, ct);

        if (nextAppraiser is not null)
        {
            await ResendToNextAppraiserAsync(db, notificationProvider, userRoleProvider, order, nextAppraiser, now, ct);
        }
        else
        {
            db.TaskItems.Add(TaskItem.Create(
                orderId:      order.Id,
                type:         TaskItemType.SelectAppraiser,
                title:        $"Odabir vještaka — {order.OrderNumber}",
                description:  "Svi dostupni vještaci su odbili ili prekoračili rok. Potreban ručni odabir.",
                assignedRole: ApplicationAppRoles.KolateralAdministrator));

            await db.SaveChangesAsync(ct);

            await SendRoleNotificationAsync(
                notificationProvider,
                ApplicationAppRoles.KolateralAdministrator,
                $"Nema dostupnog vještaka — {order.OrderNumber}",
                $"Narudžba {order.OrderNumber}: nema dostupnog vještaka za automatski odabir. Potrebna ručna intervencija.",
                order.Id, ct);
        }
    }

    private async Task ResendToNextAppraiserAsync(
        ApplicationDbContext db,
        INotificationProvider notificationProvider,
        IUserRoleProvider userRoleProvider,
        AppraisalOrder order,
        Appraiser nextAppraiser,
        DateTime now,
        CancellationToken ct)
    {
        order.SelectAppraiser(nextAppraiser.Id, now);
        order.SendToAppraiser(now);

        // Razriješi Keycloak nalog vještaka po emailu.
        string? nextUserId = null;
        if (!string.IsNullOrWhiteSpace(nextAppraiser.ContactEmail))
        {
            try
            {
                var res = await userRoleProvider.GetUsersWithRolesAsync(
                    new UserRoleListRequest { Search = nextAppraiser.ContactEmail, Role = ApplicationAppRoles.Vjestak, PageSize = 5 }, ct);
                nextUserId = res.Items.FirstOrDefault()?.UserId;
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Ne mogu razriješiti nalog vještaka po emailu {Email}.", nextAppraiser.ContactEmail);
            }
        }

        var emailSubject = $"Narudžba procjene za klijenta {order.ClientName}_{order.PropertyCity ?? order.City ?? order.OrderNumber}";

        db.TaskItems.Add(TaskItem.Create(
            orderId:        order.Id,
            type:           TaskItemType.AcceptAppraiserOrder,
            title:          $"Prihvati narudžbu procjene — {order.OrderNumber}",
            description:    $"Klijent: {order.ClientName}, {order.PropertyCity ?? order.City}. Rok prihvatanja: {AcceptanceHours}h.",
            assignedRole:   ApplicationAppRoles.Vjestak,
            dueDate:        now.AddHours(AcceptanceHours),
            assignedUserId: nextUserId));

        await db.SaveChangesAsync(ct);

        if (!string.IsNullOrWhiteSpace(nextUserId))
        {
            await SendRoleNotificationAsync(notificationProvider, ApplicationAppRoles.Vjestak,
                emailSubject,
                $"Dodijeljena vam je narudžba procjene {order.OrderNumber}. Klijent: {order.ClientName}. Rok prihvatanja: {AcceptanceHours}h.",
                order.Id, ct);
        }

        if (!string.IsNullOrWhiteSpace(nextAppraiser.ContactEmail))
        {
            await SendEmailAsync(
                notificationProvider, nextAppraiser.ContactEmail, emailSubject,
                $"Poštovani {nextAppraiser.Name},\n\n" +
                $"Dodijeljena vam je narudžba procjene {order.OrderNumber} — {order.Title}.\n" +
                $"Klijent: {order.ClientName}\n" +
                $"Grad: {order.PropertyCity ?? order.City}\n" +
                $"Adresa: {order.PropertyAddress}\n\n" +
                $"Imate {AcceptanceHours} sata da prihvatite ili odbijete narudžbu putem aplikacije.",
                order.Id, ct);
        }

        await SendRoleNotificationAsync(
            notificationProvider, ApplicationAppRoles.KolateralAdministrator,
            $"Narudžba prosljeđena novom vještaku — {order.OrderNumber}",
            $"Narudžba {order.OrderNumber} prosljeđena novom vještaku: {nextAppraiser.Name}.",
            order.Id, ct);
    }

    private async Task SendRoleNotificationAsync(
        INotificationProvider provider, string role, string subject, string message, int orderId, CancellationToken ct)
    {
        try
        {
            await provider.SendAsync(new NotificationRequest(
                RecipientUserId:   null,
                RecipientRole:     role,
                Channel:           NotificationChannel.InApp,
                Subject:           subject,
                Message:           message,
                RelatedEntityType: "AppraisalOrder",
                RelatedEntityId:   orderId.ToString()
            ), ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Greška pri notifikaciji roli {Role} za narudžbu {OrderId}", role, orderId);
        }
    }

    private async Task SendEmailAsync(
        INotificationProvider provider, string email, string subject, string message, int orderId, CancellationToken ct)
    {
        try
        {
            await provider.SendAsync(new NotificationRequest(
                RecipientUserId:   null,
                RecipientRole:     null,
                Channel:           NotificationChannel.Email,
                Subject:           subject,
                Message:           message,
                RelatedEntityType: "AppraisalOrder",
                RelatedEntityId:   orderId.ToString(),
                RecipientEmail:    email
            ), ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Greška pri email notifikaciji na {Email} za narudžbu {OrderId}", email, orderId);
        }
    }
}
