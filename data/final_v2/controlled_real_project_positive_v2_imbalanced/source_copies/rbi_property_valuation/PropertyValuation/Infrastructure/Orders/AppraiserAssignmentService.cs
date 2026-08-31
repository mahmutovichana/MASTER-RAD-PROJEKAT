using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Appraisers;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Documents;
using RBBH.CollateralAppraisal.Application.Notifications;
using Microsoft.Extensions.Options;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Application.Users.Models;
using RBBH.CollateralAppraisal.Domain.Appraisers;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using RBBH.CollateralAppraisal.Application.Common;
using ApplicationAppRoles = RBBH.CollateralAppraisal.Application.Security.AppRoles;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

/// <summary>
/// Post-selekcijski lifecycle vještaka + facade za IAppraiserAssignmentService.
/// FL selekcija delegira na FlAppraiserSelectionService.
/// PL selekcija delegira na PlAppraiserSelectionService.
/// Lifecycle (SendTo, Accept, Reject, Payment, Submit itd.) je implementiran ovdje.
/// I-2 refactoring — fizički split iz originalnog monolitnog servisa.
/// </summary>
public sealed class AppraiserAssignmentService : IAppraiserAssignmentService
{
    private readonly ApplicationDbContext       _db;
    private readonly ICurrentUserService        _currentUser;
    private readonly INotificationProvider      _notificationProvider;
    private readonly IDocumentService           _documentService;
    private readonly IAuditService              _audit;
    private readonly IUserRoleProvider          _userRoleProvider;
    private readonly IProtocolService           _protocolService;
    private readonly ILogger<AppraiserAssignmentService> _logger;
    private readonly IClock                     _clock;
    private readonly int                        _appraiserTimeoutHours;
    private readonly AppraiserAssignmentHelpers _h;
    // TryAutoReassignAsync u lifecycle-u treba algoritam selekcije
    private readonly IAppraiserSelectionService _selectionService;

    // Sub-servisi za selekciju
    private readonly IFlAppraiserSelectionService _flSvc;
    private readonly IPlAppraiserSelectionService _plSvc;

    public AppraiserAssignmentService(
        ApplicationDbContext db,
        ICurrentUserService currentUser,
        IAppraiserSelectionService selectionService,
        INotificationProvider notificationProvider,
        IDocumentService documentService,
        IAuditService audit,
        IUserRoleProvider userRoleProvider,
        IProtocolService protocolService,
        ILogger<AppraiserAssignmentService> logger,
        IClock clock,
        IOptions<WorkflowSlaOptions> slaOptions,
        IFlAppraiserSelectionService flSvc,
        IPlAppraiserSelectionService plSvc)
    {
        _db                    = db;
        _currentUser           = currentUser;
        _selectionService      = selectionService;
        _notificationProvider  = notificationProvider;
        _documentService       = documentService;
        _audit                 = audit;
        _userRoleProvider      = userRoleProvider;
        _protocolService       = protocolService;
        _logger                = logger;
        _clock                 = clock;
        _appraiserTimeoutHours = slaOptions.Value.AppraiserTimeoutWindowHours;
        _flSvc                 = flSvc;
        _plSvc                 = plSvc;
        _h                     = new AppraiserAssignmentHelpers(db, currentUser, notificationProvider, audit, logger);
    }

    // ── Delegiranje na FL/PL sub-servise ──────────────────────────────────────

    public Task<AppraiserAssignmentResultDto> AutoSelectAppraiserAsync(int orderId, CancellationToken ct = default)
        => _flSvc.AutoSelectAppraiserAsync(orderId, ct);

    public Task<IReadOnlyList<AppraiserDto>> GetCandidatesForOrderAsync(int orderId, CancellationToken ct = default)
        => _plSvc.GetCandidatesForOrderAsync(orderId, ct);

    public Task<AppraiserAssignmentResultDto> ManualSelectAppraiserAsync(int orderId, int appraiserId, CancellationToken ct = default)
        => _plSvc.ManualSelectAppraiserAsync(orderId, appraiserId, ct);

    /// <summary>Pronalazi prijavljeni (Keycloak) nalog vještaka po kontakt-emailu.</summary>
    private async Task<string?> ResolveAppraiserUserIdAsync(Appraiser appraiser, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(appraiser.ContactEmail))
            return null;
        try
        {
            var res = await _userRoleProvider.GetUsersWithRolesAsync(
                new UserRoleListRequest { Search = appraiser.ContactEmail, Role = ApplicationAppRoles.Vjestak, PageSize = 5 }, ct);
            return res.Items.FirstOrDefault()?.UserId;
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Ne mogu razriješiti nalog vještaka po emailu {Email}.", appraiser.ContactEmail);
            return null;
        }
    }

    public async Task<SendToAppraiserResultDto> SendToAppraiserAsync(int orderId, CancellationToken ct = default)
    {
        var userId = _h.RequireCurrentUserId();
        var order  = await _h.FindOrderAsync(orderId, ct);

        if (order.Status != AppraisalOrderStatus.AppraiserSelected || order.AppraiserId is null)
            throw new ConflictException(
                "Narudžba mora imati odabranog vještaka prije slanja.",
                "ORDER_NOT_READY_FOR_APPRAISER");

        var hasProtocol = await _db.OrderProtocolEntries
            .AnyAsync(p => p.OrderId == orderId, ct);
        if (!hasProtocol)
            throw new ConflictException(
                "Narudžba mora imati dodijeljen broj protokola prije slanja vještaku.",
                "PROTOCOL_NUMBER_REQUIRED");

        var sendTask = await _h.FindActiveTaskAsync(orderId, TaskItemType.SendOrderToAppraiser, ct)
            ?? throw new ConflictException(
                "Aktivan zadatak slanja narudžbe vještaku nije pronađen.",
                "SEND_TO_APPRAISER_TASK_NOT_FOUND");

        var appraiser = await _db.Appraisers.AsNoTracking().FirstOrDefaultAsync(x => x.Id == order.AppraiserId.Value, ct)
            ?? throw new NotFoundException($"Vještak ID={order.AppraiserId} nije pronađen.", "APPRAISER_NOT_FOUND");

        var now       = _clock.UtcNow;
        var oldStatus = order.Status;

        order.SendToAppraiser(now);
        sendTask.Complete(userId, $"Narudžba poslana vještaku: {appraiser.Name}", now);

        // Kreira zadatak "Prihvati narudžbu procjene" za vještaka s rokom 24h.
        var appraiserUserId = await ResolveAppraiserUserIdAsync(appraiser, ct);
        var emailSubject    = BuildAppraiserEmailSubject(order);

        _db.TaskItems.Add(TaskItem.Create(
            orderId:        order.Id,
            type:           TaskItemType.AcceptAppraiserOrder,
            title:          $"Prihvati narudžbu procjene — {order.OrderNumber}",
            description:    $"Klijent: {order.ClientName}, {order.PropertyCity ?? order.City}. Rok prihvatanja: {_appraiserTimeoutHours}h.",
            assignedRole:   ApplicationAppRoles.Vjestak,
            dueDate:        now.AddHours(_appraiserTimeoutHours),
            assignedUserId: appraiserUserId));

        await _db.SaveChangesAsync(ct);

        // In-app notifikacija vještaku (ako ima nalog) + email.
        var notificationSent = false;
        if (!string.IsNullOrWhiteSpace(appraiserUserId))
        {
            await NotifyAppraiserInAppAsync(appraiserUserId, order, emailSubject, ct);
            notificationSent = true;
        }

        await NotifyAppraiserByEmailAsync(order, appraiser, emailSubject,
            $"Narudžba procjene {order.OrderNumber} — {order.Title} je dodijeljena vama.", ct);

        // US3: AM/SM/UB prima notifikaciju "Procjena je naručena"
        await _h.NotifyRoleAsync(
            ApplicationAppRoles.AM,
            "Procjena je naručena",
            $"Narudžba {order.OrderNumber} — {order.Title}: procjena je naručena, vještak {appraiser.Name} je obaviješten.",
            order.Id, ct);

        foreach (var salesRole in new[] { ApplicationAppRoles.SM, ApplicationAppRoles.UB })
        {
            await _h.NotifyRoleAsync(salesRole,
                "Procjena je naručena",
                $"Narudžba {order.OrderNumber} — {order.Title}: procjena je naručena, vještak {appraiser.Name} je obaviješten.",
                order.Id, ct);
        }

        if (!string.IsNullOrWhiteSpace(order.CreatedByUserId))
        {
            try
            {
                await _notificationProvider.SendAsync(new NotificationRequest(
                    RecipientUserId: order.CreatedByUserId, RecipientRole: null,
                    Channel: NotificationChannel.InApp,
                    Subject: "Procjena je naručena",
                    Message: $"Procjena za narudžbu {order.OrderNumber} — {order.Title} je naručena. Vještak: {appraiser.Name}.",
                    RelatedEntityType: "AppraisalOrder", RelatedEntityId: order.Id.ToString()), ct);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Notifikacija AM/SM/UB za narudžbu {OrderId} nije poslana.", order.Id);
            }
        }

        await _h.RecordAuditAsync(
            AuditActions.OrderSentToAppraiser, order, oldStatus, notificationSent,
            new { AppraiserId = appraiser.Id, AppraiserName = appraiser.Name, AppraiserEmail = appraiser.ContactEmail }, ct);

        return new SendToAppraiserResultDto(
            order.Id, order.OrderNumber, order.Status.ToString(), (int)order.Status,
            appraiser.Id, appraiser.Name, appraiser.ContactEmail,
            notificationSent, $"Narudžba poslana vještaku: {appraiser.Name}.");
    }

    public async Task<SendToAppraiserResultDto> AcceptByAppraiserAsync(int orderId, CancellationToken ct = default)
    {
        var userId = _h.RequireCurrentUserId();
        var order  = await _h.FindOrderAsync(orderId, ct);

        if (order.Status != AppraisalOrderStatus.OrderSentToAppraiser)
            throw new ConflictException(
                "Narudžbu je moguće prihvatiti samo dok je upravo poslana vještaku.",
                "ORDER_NOT_SENT_TO_APPRAISER");

        var now       = _clock.UtcNow;
        var oldStatus = order.Status;

        order.StartAppraisal(now);

        // Završi AcceptAppraiserOrder task i kreiraj UploadFinalAppraisal.
        var acceptTask = await _h.FindActiveTaskAsync(orderId, TaskItemType.AcceptAppraiserOrder, ct);
        acceptTask?.Complete(userId, "Narudžba prihvaćena.", now);

        _db.TaskItems.Add(TaskItem.Create(
            orderId:        order.Id,
            type:           TaskItemType.UploadFinalAppraisal,
            title:          $"Izrada procjene — {order.OrderNumber}",
            description:    $"Klijent: {order.ClientName}, {order.PropertyCity ?? order.City}. Uploadujte finalnu procjenu.",
            assignedRole:   ApplicationAppRoles.Vjestak,
            assignedUserId: userId));

        _db.TaskItems.Add(TaskItem.Create(
            orderId:        order.Id,
            type:           TaskItemType.ImportSignedDocuments,
            title:          $"Import potpisanih dokumenata — {order.OrderNumber}",
            description:    "Preuzmite narudžbenicu i izjavu, potpišite ih i uploadujte potpisane dokumente. Rok: 24 sata.",
            assignedRole:   ApplicationAppRoles.Vjestak,
            assignedUserId: userId,
            dueDate:        now.AddDays(1)));

        await _db.SaveChangesAsync(ct);

        var notificationSent = await _h.NotifyRoleAsync(
            ApplicationAppRoles.KolateralAdministrator,
            "Vještak prihvatio narudžbu",
            $"Narudžba {order.OrderNumber} — {order.Title}: vještak je prihvatio narudžbu i započeo izradu procjene.",
            order.Id, ct);

        await _h.RecordAuditAsync("ORDER_ACCEPTED_BY_APPRAISER", order, oldStatus, notificationSent, new { }, ct);

        return new SendToAppraiserResultDto(
            order.Id, order.OrderNumber, order.Status.ToString(), (int)order.Status,
            order.AppraiserId ?? 0, string.Empty, null,
            notificationSent, "Narudžba prihvaćena — možete pristupiti izradi i dostavi procjene.");
    }

    public async Task<SendToAppraiserResultDto> RejectByAppraiserAsync(
        int orderId,
        AppraiserDeclineReason reason,
        string? freeText,
        CancellationToken ct = default)
    {
        var userId = _h.RequireCurrentUserId();
        var order  = await _h.FindOrderAsync(orderId, ct);

        if (order.Status != AppraisalOrderStatus.OrderSentToAppraiser)
            throw new ConflictException(
                "Narudžbu je moguće odbiti samo dok je upravo poslana vještaku.",
                "ORDER_NOT_SENT_TO_APPRAISER");

        if (order.AppraiserId is null)
            throw new ConflictException("Narudžba nema dodijeljenog vještaka.", "APPRAISER_NOT_ASSIGNED");

        var now               = _clock.UtcNow;
        var oldStatus         = order.Status;
        var rejectedAppraiserId = order.AppraiserId.Value;

        var rejectedAppraiser = await _db.Appraisers.AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == rejectedAppraiserId, ct)
            ?? throw new NotFoundException($"Vještak ID={rejectedAppraiserId} nije pronađen.", "APPRAISER_NOT_FOUND");

        // Evidentiraj odbijanje.
        _db.Set<OrderDeclinedAppraiser>().Add(
            OrderDeclinedAppraiser.Create(orderId, rejectedAppraiserId, reason, freeText, false, now));

        // Završi AcceptAppraiserOrder task s razlogom odbijanja.
        var acceptTask = await _h.FindActiveTaskAsync(orderId, TaskItemType.AcceptAppraiserOrder, ct);
        acceptTask?.Complete(userId, $"Odbijeno: {DeclineReasonLabel(reason)}{(freeText is not null ? $" — {freeText}" : "")}", now);

        // Resetuj narudžbu — AppraiserId = null, status → AppraiserSelected.
        order.RejectByAppraiser(now);

        await _db.SaveChangesAsync(ct);

        // Notifikacija CA: "Odbijeno"
        await _h.NotifyRoleAsync(
            ApplicationAppRoles.KolateralAdministrator,
            $"Vještak odbio narudžbu — {order.OrderNumber}",
            $"Narudžba {order.OrderNumber} — {order.Title}: vještak {rejectedAppraiser.Name} je odbio narudžbu. " +
            $"Razlog: {DeclineReasonLabel(reason)}{(freeText is not null ? $" ({freeText})" : "")}. " +
            "Sistem pokušava dodijeliti sljedećeg vještaka.",
            order.Id, ct);

        // Notifikacija odbijenom vještaku: potvrda odbijanja
        if (!string.IsNullOrWhiteSpace(rejectedAppraiser.ContactEmail))
        {
            await NotifyByEmailAsync(
                rejectedAppraiser.ContactEmail,
                $"Potvrda odbijanja — narudžba procjene za klijenta {order.ClientName}",
                $"Poštovani {rejectedAppraiser.Name},\n\n" +
                $"Potvrđujemo da ste odbili narudžbu procjene {order.OrderNumber} za klijenta {order.ClientName}.\n" +
                $"Razlog: {DeclineReasonLabel(reason)}{(freeText is not null ? $" — {freeText}" : "")}.\n\n" +
                $"Proces narudžbe procjene za klijenta {order.ClientName} se obustavlja za vas. " +
                "Narudžba će biti dodijeljena sljedećem vještaku.",
                order.Id, ct);
        }

        // Pokušaj automatski odabrati sljedećeg vještaka.
        var declinedIds   = await GetDeclinedAppraiserIdsAsync(orderId, ct);
        var nextAppraiser = await _selectionService.SelectForOrderAsync(order, declinedIds, ct);

        if (nextAppraiser is not null)
        {
            await SendOrderToNewAppraiserAsync(order, nextAppraiser, now, ct);
        }
        else
        {
            // Nema sljedećeg vještaka — CA treba ručno odabrati.
            _db.TaskItems.Add(TaskItem.Create(
                orderId:      order.Id,
                type:         TaskItemType.SelectAppraiser,
                title:        $"Odabir vještaka — {order.OrderNumber}",
                description:  "Svi dostupni vještaci su odbili ili prekoračili rok. Potreban ručni odabir.",
                assignedRole: ApplicationAppRoles.KolateralAdministrator));

            await _db.SaveChangesAsync(ct);

            await _h.NotifyRoleAsync(
                ApplicationAppRoles.KolateralAdministrator,
                $"Nema dostupnog vještaka — {order.OrderNumber}",
                $"Narudžba {order.OrderNumber}: nema dostupnog vještaka za automatski odabir. Potrebna ručna intervencija.",
                order.Id, ct);
        }

        await _h.RecordAuditAsync("ORDER_REJECTED_BY_APPRAISER", order, oldStatus, true,
            new { RejectedAppraiserId = rejectedAppraiserId, Reason = reason.ToString(), FreeText = freeText }, ct);

        return new SendToAppraiserResultDto(
            order.Id, order.OrderNumber, order.Status.ToString(), (int)order.Status,
            rejectedAppraiserId, rejectedAppraiser.Name, rejectedAppraiser.ContactEmail,
            true, $"Narudžba odbijena — sistem traži sljedećeg vještaka.");
    }

    public async Task<SendToAppraiserResultDto> RequestAdditionalPaymentAsync(int orderId, CancellationToken ct = default)
    {
        var userId = _h.RequireCurrentUserId();
        var order  = await _h.FindOrderAsync(orderId, ct);

        if (order.Status is not (AppraisalOrderStatus.AppraisalInProgress
                               or AppraisalOrderStatus.OrderSentToAppraiser))
            throw new ConflictException(
                "Doplata se može zatražiti samo dok je narudžba u izradi procjene.",
                "ORDER_NOT_IN_PROGRESS");

        if (order.AppraiserId is null)
            throw new ConflictException("Narudžba nema dodijeljenog vještaka.", "APPRAISER_NOT_ASSIGNED");

        var now       = _clock.UtcNow;
        var oldStatus = order.Status;

        order.RequestAdditionalPayment(now);

        // Zadatak za CA: "Doplata izvršena"
        _db.TaskItems.Add(TaskItem.Create(
            orderId:      order.Id,
            type:         TaskItemType.ConfirmAdditionalPayment,
            title:        $"Doplata izvršena — {order.OrderNumber}",
            description:  $"Vještak {userId} je zatražio doplatu za narudžbu {order.OrderNumber} — {order.Title}. " +
                          "Po uplati, označite doplatu kao izvršenu da vještak može nastaviti s izradom procjene.",
            assignedRole: ApplicationAppRoles.KolateralAdministrator));

        await _db.SaveChangesAsync(ct);

        var notificationSent = await _h.NotifyRoleAsync(
            ApplicationAppRoles.KolateralAdministrator,
            $"Vještak traži doplatu — {order.OrderNumber}",
            $"Narudžba {order.OrderNumber} — {order.Title}: vještak je zatražio doplatu. " +
            "Po uplati, koristite zadatak 'Doplata izvršena' da obavijestite vještaka.",
            order.Id, ct);

        await _h.RecordAuditAsync("ORDER_ADDITIONAL_PAYMENT_REQUESTED", order, oldStatus, notificationSent, new { }, ct);

        return new SendToAppraiserResultDto(
            order.Id, order.OrderNumber, order.Status.ToString(), (int)order.Status,
            order.AppraiserId.Value, string.Empty, null,
            notificationSent, "Doplata zatražena — CA je obaviješten.");
    }

    public async Task<SendToAppraiserResultDto> ConfirmAdditionalPaymentAsync(int orderId, CancellationToken ct = default)
    {
        var userId = _h.RequireCurrentUserId();
        var order  = await _h.FindOrderAsync(orderId, ct);

        if (order.Status != AppraisalOrderStatus.AdditionalPaymentRequested)
            throw new ConflictException(
                "Doplata se može potvrditi samo kada je zatražena od strane vještaka.",
                "ORDER_NOT_AWAITING_PAYMENT");

        if (order.AppraiserId is null)
            throw new ConflictException("Narudžba nema dodijeljenog vještaka.", "APPRAISER_NOT_ASSIGNED");

        var appraiser = await _db.Appraisers.AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == order.AppraiserId.Value, ct)
            ?? throw new NotFoundException($"Vještak ID={order.AppraiserId} nije pronađen.", "APPRAISER_NOT_FOUND");

        var now       = _clock.UtcNow;
        var oldStatus = order.Status;

        order.CompleteAdditionalPayment(now);

        var paymentTask = await _h.FindActiveTaskAsync(orderId, TaskItemType.ConfirmAdditionalPayment, ct);
        paymentTask?.Complete(userId, "Doplata izvršena.", now);

        await _db.SaveChangesAsync(ct);

        // Notifikacija vještaku: može nastaviti
        var appraiserUserId = await ResolveAppraiserUserIdAsync(appraiser, ct);

        if (!string.IsNullOrWhiteSpace(appraiserUserId))
        {
            await _h.NotifyUserAsync(
                appraiserUserId,
                $"Doplata izvršena — {order.OrderNumber}",
                $"CA je potvrdio da je doplata izvršena za narudžbu {order.OrderNumber}. Možete nastaviti s izradom procjene.",
                order.Id, ct);
        }

        if (!string.IsNullOrWhiteSpace(appraiser.ContactEmail))
        {
            await NotifyByEmailAsync(
                appraiser.ContactEmail,
                $"Doplata izvršena — narudžba {order.OrderNumber}",
                $"Poštovani {appraiser.Name},\n\n" +
                $"Obavještavamo vas da je doplata za narudžbu procjene {order.OrderNumber} — {order.Title} izvršena.\n" +
                "Možete nastaviti s izradom procjene.",
                order.Id, ct);
        }

        await _h.RecordAuditAsync("ORDER_ADDITIONAL_PAYMENT_CONFIRMED", order, oldStatus, true, new { }, ct);

        return new SendToAppraiserResultDto(
            order.Id, order.OrderNumber, order.Status.ToString(), (int)order.Status,
            appraiser.Id, appraiser.Name, appraiser.ContactEmail,
            true, "Doplata potvrđena — vještak je obaviješten.");
    }

    public async Task<SendToAppraiserResultDto> SubmitAppraisalAsync(int orderId, DateTime? visitDate = null, CancellationToken ct = default)
    {
        var userId = _h.RequireCurrentUserId();
        var order  = await _h.FindOrderAsync(orderId, ct);

        if (order.Status is not (AppraisalOrderStatus.OrderSentToAppraiser
                               or AppraisalOrderStatus.AdditionalPaymentCompleted
                               or AppraisalOrderStatus.AppraisalInProgress
                               or AppraisalOrderStatus.AppraisalReturnedForRework))
            throw new ConflictException(
                "Procjena se može dostaviti samo kada je narudžba kod vještaka.",
                "ORDER_NOT_WITH_APPRAISER");

        if (!visitDate.HasValue)
            throw new ConflictException(
                "Datum obilaska imovine je obavezan za dostavu procjene.",
                "VISIT_DATE_REQUIRED");

        var documents = await _documentService.GetByOrderAsync(orderId, ct);
        var finalDoc  = documents.Where(d => d.IsActive).OrderByDescending(d => d.UploadedAt).FirstOrDefault()
            ?? throw new ConflictException(
                "Prvo uploadujte dokument procjene u tabu \"Dokumenti\", zatim dostavite procjenu.",
                "NO_APPRAISAL_DOCUMENT");

        var now       = _clock.UtcNow;
        var oldStatus = order.Status;

        if (visitDate.HasValue)
            order.SetAppraiserVisitDate(visitDate.Value, now);

        order.SetFinalAppraisalDocument(finalDoc.Id, now); // status → AppraisalReceived

        var uploadTask = await _h.FindActiveTaskAsync(orderId, TaskItemType.UploadFinalAppraisal, ct);
        uploadTask?.Complete(userId, "Procjena dostavljena na kolateral oficira.", now);

        var reworkTask = await _h.FindActiveTaskAsync(orderId, TaskItemType.ReworkAppraisal, ct);
        reworkTask?.Complete(userId, "Korigovana procjena dostavljena.", now);

        // Zadatak za CO da analizira i odobri procjenu.
        _db.TaskItems.Add(TaskItem.Create(
            orderId:      order.Id,
            type:         TaskItemType.ApproveFinalAppraisal,
            title:        $"Pregled i odobrenje procjene — {order.OrderNumber}",
            description:  $"Vještak je dostavio procjenu za narudžbu {order.OrderNumber}.",
            assignedRole: ApplicationAppRoles.KolateralOficir));

        await _db.SaveChangesAsync(ct);

        var notificationSent = await _h.NotifyRoleAsync(
            ApplicationAppRoles.KolateralOficir,
            "Procjena zaprimljena",
            $"Vještak je dostavio procjenu za narudžbu {order.OrderNumber} — {order.Title}. Potrebna je analiza i odobrenje procjene.",
            order.Id, ct);

        await _h.RecordAuditAsync("ORDER_APPRAISAL_SUBMITTED", order, oldStatus, notificationSent,
            new { FinalDocumentId = finalDoc.Id }, ct);

        return new SendToAppraiserResultDto(
            order.Id, order.OrderNumber, order.Status.ToString(), (int)order.Status,
            order.AppraiserId ?? 0, finalDoc.FileName, null,
            notificationSent, "Procjena je dostavljena kolateral oficiru na pregled.");
    }

    public async Task<SendToAppraiserResultDto> RejectOrderAsync(
        int orderId, string rejectionReason, string? rejectionComment, CancellationToken ct = default)
    {
        var userId = _h.RequireCurrentUserId();
        var order  = await _h.FindOrderAsync(orderId, ct);

        if (order.Status is not (AppraisalOrderStatus.OrderSentToAppraiser
                                or AppraisalOrderStatus.AppraisalInProgress))
            throw new ConflictException(
                "Narudžba se može odbiti samo dok je kod vještaka.",
                "ORDER_NOT_WITH_APPRAISER");

        var rejectedAppraiserId = order.AppraiserId;
        var rejectedAppraiser = rejectedAppraiserId.HasValue
            ? await _db.Appraisers.AsNoTracking().FirstOrDefaultAsync(a => a.Id == rejectedAppraiserId.Value, ct)
            : null;
        var rejectedName = rejectedAppraiser?.Name ?? "—";

        var now       = _clock.UtcNow;
        var oldStatus = order.Status;

        var uploadTask = await _h.FindActiveTaskAsync(orderId, TaskItemType.UploadFinalAppraisal, ct);
        uploadTask?.Cancel(now);

        order.RejectByAppraiser(now);

        var fullReason = string.IsNullOrWhiteSpace(rejectionComment)
            ? rejectionReason
            : $"{rejectionReason}: {rejectionComment}";

        _db.TaskItems.Add(TaskItem.Create(
            orderId:      order.Id,
            type:         TaskItemType.AppraiserRejected,
            title:        $"Odbijeno od vještaka — {order.OrderNumber}",
            description:  $"Vještak {rejectedName} odbio narudžbu. Razlog: {fullReason}",
            assignedRole: ApplicationAppRoles.KolateralAdministrator));

        await _db.SaveChangesAsync(ct);

        await _h.RecordAuditAsync(AuditActions.OrderRejectedByAppraiser, order, oldStatus, false,
            new { RejectedAppraiser = rejectedName, Reason = rejectionReason, Comment = rejectionComment }, ct);

        var notifiedCA = await _h.NotifyRoleAsync(
            ApplicationAppRoles.KolateralAdministrator,
            $"Odbijeno — {order.OrderNumber}",
            $"Vještak {rejectedName} je odbio narudžbu {order.OrderNumber}. Razlog: {fullReason}. Sistem pokreće ponovni odabir vještaka.",
            order.Id, ct);

        if (rejectedAppraiser is not null)
        {
            await NotifyAppraiserByEmailAsync(order, rejectedAppraiser,
                $"Obustava narudžbe procjene — {order.OrderNumber}",
                $"Poštovani {rejectedName},\n\n" +
                $"Obustavlja se narudžba procjene za klijenta {order.ClientName} ({order.OrderNumber}).\n" +
                $"Razlog: {fullReason}\n\nHvala na obavijesti.", ct);
        }

        var autoReassigned = await TryAutoReassignAsync(order, rejectedAppraiserId, ct);

        return new SendToAppraiserResultDto(
            order.Id, order.OrderNumber, order.Status.ToString(), (int)order.Status,
            order.AppraiserId ?? 0, autoReassigned ? "Auto-dodijeljen novi vještak" : "Potreban ručni odabir", null,
            notifiedCA,
            autoReassigned
                ? $"Narudžba odbijena od {rejectedName}. Automatski dodijeljen novi vještak."
                : $"Narudžba odbijena od {rejectedName}. Potreban ručni odabir — nema dostupnih vještaka.");
    }

    private async Task<bool> TryAutoReassignAsync(AppraisalOrder order, int? excludeAppraiserId, CancellationToken ct)
    {
        try
        {
            var excludeIds = excludeAppraiserId.HasValue ? new[] { excludeAppraiserId.Value } : null;
            var candidate = await _selectionService.SelectForOrderAsync(order, excludeIds, ct);
            if (candidate is null)
                return false;

            if (!candidate.CanHandle(order.WorkflowType))
                return false;

            var now = _clock.UtcNow;
            order.SelectAppraiser(candidate.Id, now);

            _db.TaskItems.Add(TaskItem.Create(
                orderId:      order.Id,
                type:         TaskItemType.SendOrderToAppraiser,
                title:        $"Slanje narudžbe vještaku — {order.OrderNumber}",
                description:  $"Automatski re-dodijeljen vještak: {candidate.Name} (prethodni odbio).",
                assignedRole: ApplicationAppRoles.KolateralAdministrator));

            await _db.SaveChangesAsync(ct);

            await _h.NotifyRoleAsync(
                ApplicationAppRoles.KolateralAdministrator,
                $"Novi vještak dodijeljen — {order.OrderNumber}",
                $"Nakon odbijanja, automatski je dodijeljen novi vještak: {candidate.Name}. Narudžba je spremna za slanje.",
                order.Id, ct);

            await _h.RecordAuditAsync(AuditActions.OrderReassignedAppraiser, order,
                AppraisalOrderStatus.AppraiserRejected, true,
                new { NewAppraiserId = candidate.Id, NewAppraiserName = candidate.Name }, ct);

            return true;
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Auto-reassign vještaka za narudžbu {OrderId} nije uspio.", order.Id);
            return false;
        }
    }

    private async Task NotifyAppraiserByEmailAsync(AppraisalOrder order, Domain.Appraisers.Appraiser appraiser,
        string subject, string message, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(appraiser.ContactEmail)) return;
        try
        {
            await _notificationProvider.SendAsync(new NotificationRequest(
                RecipientUserId: null, RecipientRole: null,
                Channel: NotificationChannel.Email,
                Subject: subject, Message: message,
                RelatedEntityType: "AppraisalOrder", RelatedEntityId: order.Id.ToString(),
                RecipientEmail: appraiser.ContactEmail), ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Email notifikacija vještaku pri odbijanju narudžbe {OrderId}.", order.Id);
        }
    }

    public async Task<AppraiserPackageDto> GetAppraiserPackageAsync(int orderId, CancellationToken ct = default)
    {
        var order = await _h.FindOrderAsync(orderId, ct);

        if (order.AppraiserId is null)
            throw new ConflictException("Narudžba nema odabranog vještaka.", "APPRAISER_NOT_SELECTED");

        var appraiser = await _db.Appraisers.AsNoTracking().FirstOrDefaultAsync(x => x.Id == order.AppraiserId.Value, ct)
            ?? throw new NotFoundException($"Vještak ID={order.AppraiserId} nije pronađen.", "APPRAISER_NOT_FOUND");

        var documents = await _documentService.GetByOrderAsync(orderId, ct);

        return new AppraiserPackageDto(
            order.Id, order.OrderNumber, appraiser.Id, appraiser.Name, appraiser.ContactEmail, documents);
    }

    public async Task<SendToAppraiserResultDto> CompleteSignedDocumentImportAsync(int orderId, CancellationToken ct = default)
    {
        var userId = _h.RequireCurrentUserId();
        var order  = await _h.FindOrderAsync(orderId, ct);

        var task = await _db.TaskItems
            .Where(t => t.AppraisalOrderId == orderId
                     && t.TaskType == TaskItemType.ImportSignedDocuments
                     && t.Status != TaskItemStatus.Completed
                     && t.Status != TaskItemStatus.Cancelled)
            .OrderByDescending(t => t.CreatedAt)
            .FirstOrDefaultAsync(ct)
            ?? throw new ConflictException(
                "Nema aktivnog zadatka za import potpisanih dokumenata.",
                "NO_SIGNED_DOCS_TASK");

        var now = _clock.UtcNow;
        task.Complete(userId, "Potpisani dokumenti uploadovani.", now);
        order.SetSignedDocumentsReceivedAt(now, now);
        await _db.SaveChangesAsync(ct);

        var notificationSent = await _h.NotifyRoleAsync(
            ApplicationAppRoles.KolateralAdministrator,
            "Završen import dokumenata",
            $"Vještak je uploadovao potpisane dokumente za narudžbu {order.OrderNumber} — {order.Title}.",
            order.Id, ct);

        await _h.RecordAuditAsync(
            "SIGNED_DOCUMENTS_IMPORTED", order, order.Status, notificationSent,
            new { TaskId = task.Id }, ct);

        return new SendToAppraiserResultDto(
            order.Id, order.OrderNumber, order.Status.ToString(), (int)order.Status,
            order.AppraiserId ?? 0, string.Empty, null,
            notificationSent, "Potpisani dokumenti uspješno uvezeni.");
    }

    // ── Pomoćne metode ────────────────────────────────────────────────────

    private async Task SendOrderToNewAppraiserAsync(
        AppraisalOrder order, Appraiser nextAppraiser, DateTime now, CancellationToken ct)
    {
        order.SelectAppraiser(nextAppraiser.Id, now);
        order.SendToAppraiser(now);

        var nextUserId   = await ResolveAppraiserUserIdAsync(nextAppraiser, ct);
        var emailSubject = BuildAppraiserEmailSubject(order);

        _db.TaskItems.Add(TaskItem.Create(
            orderId:        order.Id,
            type:           TaskItemType.AcceptAppraiserOrder,
            title:          $"Prihvati narudžbu procjene — {order.OrderNumber}",
            description:    $"Klijent: {order.ClientName}, {order.PropertyCity ?? order.City}. Rok prihvatanja: {_appraiserTimeoutHours}h.",
            assignedRole:   ApplicationAppRoles.Vjestak,
            dueDate:        now.AddHours(_appraiserTimeoutHours),
            assignedUserId: nextUserId));

        await _db.SaveChangesAsync(ct);

        if (!string.IsNullOrWhiteSpace(nextUserId))
            await NotifyAppraiserInAppAsync(nextUserId, order, emailSubject, ct);

        await NotifyAppraiserByEmailAsync(order, nextAppraiser, emailSubject,
            $"Narudžba procjene {order.OrderNumber} — {order.Title} je dodijeljena vama.", ct);

        await _h.NotifyRoleAsync(
            ApplicationAppRoles.KolateralAdministrator,
            $"Narudžba prosljeđena novom vještaku — {order.OrderNumber}",
            $"Narudžba {order.OrderNumber} prosljeđena novom vještaku: {nextAppraiser.Name}.",
            order.Id, ct);
    }

    private static string BuildAppraiserEmailSubject(AppraisalOrder order) =>
        $"Narudžba procjene za klijenta {order.ClientName}_{order.PropertyCity ?? order.City ?? order.OrderNumber}";

    private static string DeclineReasonLabel(AppraiserDeclineReason reason) => reason switch
    {
        AppraiserDeclineReason.NisamUGradu        => "Nisam u gradu",
        AppraiserDeclineReason.NeModuSticiObaveze => "Ne mogu stići od dr. obaveza",
        AppraiserDeclineReason.Bolest             => "Bolest",
        AppraiserDeclineReason.SmrtniSlucaj       => "Smrtni slučaj",
        AppraiserDeclineReason.OstaliRazlozi      => "Ostali razlozi",
        AppraiserDeclineReason.Timeout            => "Prekoračen rok prihvatanja (24h)",
        _                                          => reason.ToString()
    };

    private async Task<List<int>> GetDeclinedAppraiserIdsAsync(int orderId, CancellationToken ct) =>
        await _db.Set<OrderDeclinedAppraiser>()
            .Where(d => d.AppraisalOrderId == orderId)
            .Select(d => d.AppraiserId)
            .ToListAsync(ct);

    private async Task<Dictionary<int, int>> GetActiveCountsAsync(CancellationToken ct) =>
        await _db.AppraisalOrders
            .Where(o => o.AppraiserId != null && AppraisalOrderStatusGroups.ActiveAppraisalStatuses.Contains(o.Status))
            .GroupBy(o => o.AppraiserId!.Value)
            .Select(g => new { AppraiserId = g.Key, Count = g.Count() })
            .ToDictionaryAsync(x => x.AppraiserId, x => x.Count, ct);

    // ── Lifecycle-specifični notifikacijski helperi ────────────────────────────

    private async Task NotifyAppraiserInAppAsync(
        string userId, AppraisalOrder order, string subject, CancellationToken ct)
    {
        try
        {
            await _notificationProvider.SendAsync(new NotificationRequest(
                RecipientUserId:   userId,
                RecipientRole:     null,
                Channel:           NotificationChannel.InApp,
                Subject:           subject,
                Message:           $"Narudžba {order.OrderNumber} — {order.Title}",
                RelatedEntityType: "AppraisalOrder",
                RelatedEntityId:   order.Id.ToString()
            ), ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Greška pri in-app notifikaciji vještaku {UserId} za narudžbu {OrderId}", userId, order.Id);
        }
    }

    private async Task NotifyByEmailAsync(
        string email, string subject, string body, int orderId, CancellationToken ct)
    {
        try
        {
            await _notificationProvider.SendAsync(new NotificationRequest(
                RecipientUserId:   null,
                RecipientRole:     null,
                Channel:           NotificationChannel.Email,
                Subject:           subject,
                Message:           body,
                RelatedEntityType: "AppraisalOrder",
                RelatedEntityId:   orderId.ToString(),
                RecipientEmail:    email
            ), ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Greška pri email notifikaciji na {Email} za narudžbu {OrderId}", email, orderId);
        }
    }
}
