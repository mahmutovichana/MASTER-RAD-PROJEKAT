using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Domain.Appraisers;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

[ExcludeFromCodeCoverage]
public sealed class QuoteRequestService : IQuoteRequestService
{
    private readonly ApplicationDbContext        _db;
    private readonly ICurrentUserService         _currentUser;
    private readonly INotificationProvider       _notifications;
    private readonly IAuditService               _audit;
    private readonly IProtocolService            _protocolService;
    private readonly ILogger<QuoteRequestService> _logger;

    public QuoteRequestService(
        ApplicationDbContext db,
        ICurrentUserService currentUser,
        INotificationProvider notifications,
        IAuditService audit,
        IProtocolService protocolService,
        ILogger<QuoteRequestService> logger)
    {
        _db              = db;
        _currentUser     = currentUser;
        _notifications   = notifications;
        _audit           = audit;
        _protocolService = protocolService;
        _logger          = logger;
    }

    public async Task<SendQuoteRequestsResult> SendQuoteRequestsAsync(
        int orderId, SendQuoteRequestsInput command, CancellationToken ct = default)
    {
        var userId = RequireUserId();
        var order  = await FindOrderAsync(orderId, ct);

        if (!order.IsPL())
            throw new ConflictException(
                "Zahtjev za ponudu je dostupan samo za narudžbe pravnih lica (PL).",
                "QUOTE_REQUEST_NOT_PL");

        if (order.Status is not (AppraisalOrderStatus.DocumentationApproved
                                or AppraisalOrderStatus.AccessCheckApproved
                                or AppraisalOrderStatus.ProtocolCreated))
            throw new ConflictException(
                "Zahtjev za ponudu se može poslati nakon odobrenja dokumentacije i pristupa.",
                "QUOTE_REQUEST_INVALID_STATUS");

        if (command.AppraiserIds.Count == 0)
            throw new ValidationException("appraiserIds", "Odaberite barem jednog vještaka.");

        var existing = await _db.QuoteRequests
            .Where(q => q.AppraisalOrderId == orderId)
            .AnyAsync(ct);
        if (existing)
            throw new ConflictException(
                "Zahtjevi za ponudu su već poslani za ovu narudžbu.",
                "QUOTE_REQUESTS_ALREADY_SENT");

        var appraisers = await _db.Appraisers
            .AsNoTracking()
            .Where(a => command.AppraiserIds.Contains(a.Id) && a.IsActive && !a.IsBlacklisted)
            .ToListAsync(ct);

        if (appraisers.Count == 0)
            throw new ConflictException(
                "Nijedan od odabranih vještaka nije dostupan.",
                "NO_AVAILABLE_APPRAISERS");

        var sentCount = 0;
        foreach (var appraiser in appraisers)
        {
            var qr = QuoteRequest.Create(orderId, appraiser.Id, command.Deadline, userId);
            _db.QuoteRequests.Add(qr);
            await SendQuoteNotificationAsync(order, appraiser, command.Deadline, ct);
            sentCount++;
        }

        _db.TaskItems.Add(TaskItem.Create(
            orderId:      order.Id,
            type:         TaskItemType.SendThankYou,
            title:        $"Zahvalnica — {order.OrderNumber}",
            description:  $"Nakon izbora vještaka, pošaljite zahvalnicu ostalim kandidatima.",
            assignedRole: Application.Security.AppRoles.KolateralAdministrator));

        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(AuditActions.QuoteRequestsSent, order,
            new { SentCount = sentCount, AppraiserIds = command.AppraiserIds, Deadline = command.Deadline }, ct);

        return new SendQuoteRequestsResult(
            order.Id, order.OrderNumber, sentCount, true,
            $"Zahtjev za ponudu poslan na {sentCount} vještak(a). Rok: {command.Deadline:dd.MM.yyyy HH:mm}.");
    }

    public async Task<IReadOnlyList<QuoteRequestDto>> GetByOrderAsync(
        int orderId, CancellationToken ct = default)
    {
        var requests = await _db.QuoteRequests
            .AsNoTracking()
            .Where(q => q.AppraisalOrderId == orderId)
            .OrderBy(q => q.SentAt)
            .ToListAsync(ct);

        if (requests.Count == 0) return [];

        var appraiserIds = requests.Select(q => q.AppraiserId).Distinct().ToList();
        var appraisers = await _db.Appraisers
            .AsNoTracking()
            .Where(a => appraiserIds.Contains(a.Id))
            .ToDictionaryAsync(a => a.Id, ct);

        return requests.Select(q =>
        {
            var a = appraisers.GetValueOrDefault(q.AppraiserId);
            return new QuoteRequestDto(
                q.Id, q.AppraisalOrderId, q.AppraiserId,
                a?.Name ?? "—", a?.City, a?.ContactEmail,
                q.Status.ToString(), q.SentAt, q.Deadline,
                q.OfferedPrice, q.OfferedDays, q.RespondedAt, q.ThankYouSentAt);
        }).ToList();
    }

    // ── AC 5: Vještak odgovara na zahtjev za ponudu ───────────────────────
    public async Task<RespondToQuoteResult> RespondToQuoteAsync(
        int orderId, int quoteRequestId, RespondToQuoteCommand command, CancellationToken ct = default)
    {
        RequireUserId();
        var order = await FindOrderAsync(orderId, ct);

        if (order.WorkflowType != WorkflowType.PravnaLica && order.ClientType != "PL")
            throw new ConflictException(
                "Odgovor na ponudu je dostupan samo za narudžbe pravnih lica (PL).",
                "QUOTE_RESPOND_NOT_PL");

        var quote = await _db.QuoteRequests
            .FirstOrDefaultAsync(q => q.Id == quoteRequestId && q.AppraisalOrderId == orderId, ct)
            ?? throw new NotFoundException(
                $"Ponuda ID={quoteRequestId} za narudžbu ID={orderId} nije pronađena.",
                "QUOTE_REQUEST_NOT_FOUND");

        if (quote.Status != QuoteRequestStatus.Sent)
            throw new ConflictException(
                "Odgovor je moguć samo na ponude u statusu 'Sent'.",
                "QUOTE_ALREADY_RESPONDED");

        if (command.OfferedPrice <= 0)
            throw new ValidationException("offeredPrice", "Cijena mora biti veća od 0.");

        if (command.OfferedDays <= 0)
            throw new ValidationException("offeredDays", "Rok izrade mora biti veći od 0.");

        var now = DateTime.UtcNow;
        quote.RecordResponse(command.OfferedPrice, command.OfferedDays, now);
        await _db.SaveChangesAsync(ct);

        // Notifikacija CA da je ponuda stigla
        try
        {
            await _notifications.SendAsync(new NotificationRequest(
                RecipientUserId:   null,
                RecipientRole:     Application.Security.AppRoles.KolateralAdministrator,
                Channel:           NotificationChannel.InApp,
                Subject:           $"Ponuda vještaka — {order.OrderNumber}",
                Message:           $"Vještak je dostavio ponudu za narudžbu {order.OrderNumber}: " +
                                   $"cijena {command.OfferedPrice:N2} KM, rok {command.OfferedDays} dana.",
                RelatedEntityType: "AppraisalOrder",
                RelatedEntityId:   orderId.ToString()), ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Notifikacija CA o ponudi vještaka za narudžbu {OrderId} nije poslana.", orderId);
        }

        await RecordAuditAsync("QUOTE_RESPONDED", order,
            new { QuoteRequestId = quoteRequestId, OfferedPrice = command.OfferedPrice, OfferedDays = command.OfferedDays }, ct);

        return new RespondToQuoteResult(
            orderId, order.OrderNumber, quoteRequestId,
            command.OfferedPrice, command.OfferedDays,
            $"Ponuda dostavljena: {command.OfferedPrice:N2} KM, rok {command.OfferedDays} dana.");
    }

    public async Task<AcceptQuoteResult> AcceptQuoteAsync(
        int orderId, int quoteRequestId, CancellationToken ct = default)
    {
        RequireUserId();
        var order = await FindOrderAsync(orderId, ct);

        var quote = await _db.QuoteRequests
            .FirstOrDefaultAsync(q => q.Id == quoteRequestId && q.AppraisalOrderId == orderId, ct)
            ?? throw new NotFoundException(
                $"Ponuda ID={quoteRequestId} za narudžbu ID={orderId} nije pronaÄ‘ena.",
                "QUOTE_REQUEST_NOT_FOUND");

        if (quote.Status != QuoteRequestStatus.Responded)
            throw new ConflictException(
                "Može se prihvatiti samo ponuda koja je dostavljena (status: Responded).",
                "QUOTE_NOT_RESPONDED");

        var appraiser = await _db.Appraisers
            .AsNoTracking()
            .FirstOrDefaultAsync(a => a.Id == quote.AppraiserId, ct)
            ?? throw new NotFoundException("Vještak nije pronaÄ‘en.", "APPRAISER_NOT_FOUND");

        var now    = DateTime.UtcNow;
        var userId = _currentUser.UserId ?? "system";

        quote.MarkSelected(now);
        order.SelectAppraiser(quote.AppraiserId, now);

        if (quote.OfferedPrice.HasValue)
            order.SetAppraisalFee(quote.OfferedPrice.Value, now);

        // Zatvori SelectAppraiser task ako postoji aktivan (isti kao u ManualSelectAppraiserAsync)
        var selectTask = await _db.TaskItems
            .Where(t => t.AppraisalOrderId == orderId
                     && t.TaskType == TaskItemType.SelectAppraiser
                     && t.Status != TaskItemStatus.Completed
                     && t.Status != TaskItemStatus.Cancelled)
            .OrderByDescending(t => t.CreatedAt)
            .FirstOrDefaultAsync(ct);
        selectTask?.Complete(userId, $"Vještak odabran putem ponude: {appraiser.Name}", now);

        // Kreira SendOrderToAppraiser task za CA — bez ovoga workflow se zaglavljuje
        _db.TaskItems.Add(TaskItem.Create(
            orderId:      order.Id,
            type:         TaskItemType.SendOrderToAppraiser,
            title:        $"Slanje narudžbe vještaku — {order.OrderNumber}",
            description:  $"Odabran vještak: {appraiser.Name} " +
                          $"(ponuda: {quote.OfferedPrice} KM, rok: {quote.OfferedDays} dana)",
            assignedRole: Application.Security.AppRoles.KolateralAdministrator));

        await _db.SaveChangesAsync(ct);

        await _protocolService.CreateProtocolForOrderAsync(order.Id, ct);

        await RecordAuditAsync(AuditActions.QuoteAccepted, order,
            new { QuoteRequestId = quoteRequestId, AppraiserId = quote.AppraiserId, Price = quote.OfferedPrice, Days = quote.OfferedDays }, ct);

        return new AcceptQuoteResult(
            order.Id, order.OrderNumber, appraiser.Id, appraiser.Name,
            $"Ponuda vještaka {appraiser.Name} prihvaćena (cijena: {quote.OfferedPrice}, rok: {quote.OfferedDays} dana).");
    }

    public async Task<SendThankYouResult> SendThankYouAsync(
        int orderId, CancellationToken ct = default)
    {
        var userId = RequireUserId();
        var order  = await FindOrderAsync(orderId, ct);

        if (order.AppraiserId is null)
            throw new ConflictException(
                "Vještak mora biti odabran prije slanja zahvalnice.",
                "APPRAISER_NOT_SELECTED");

        var nonSelected = await _db.QuoteRequests
            .Where(q => q.AppraisalOrderId == orderId
                     && q.AppraiserId != order.AppraiserId.Value
                     && q.Status != QuoteRequestStatus.ThankYouSent)
            .ToListAsync(ct);

        if (nonSelected.Count == 0)
            return new SendThankYouResult(order.Id, order.OrderNumber, 0,
                "Nema vještaka kojima treba poslati zahvalnicu.");

        var appraiserIds = nonSelected.Select(q => q.AppraiserId).ToList();
        var appraisers = await _db.Appraisers
            .AsNoTracking()
            .Where(a => appraiserIds.Contains(a.Id))
            .ToDictionaryAsync(a => a.Id, ct);

        var now = DateTime.UtcNow;
        var sentCount = 0;

        foreach (var qr in nonSelected)
        {
            qr.MarkThankYouSent(now);
            if (appraisers.TryGetValue(qr.AppraiserId, out var appraiser))
            {
                await SendThankYouNotificationAsync(order, appraiser, ct);
                sentCount++;
            }
        }

        var thankYouTask = await _db.TaskItems
            .Where(t => t.AppraisalOrderId == orderId
                     && t.TaskType == TaskItemType.SendThankYou
                     && t.Status != TaskItemStatus.Completed
                     && t.Status != TaskItemStatus.Cancelled)
            .OrderByDescending(t => t.CreatedAt)
            .FirstOrDefaultAsync(ct);
        thankYouTask?.Complete(userId, $"Zahvalnica poslana na {sentCount} vještaka.", now);

        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(AuditActions.QuoteThankYouSent, order,
            new { SentCount = sentCount, AppraiserIds = appraiserIds }, ct);

        return new SendThankYouResult(
            order.Id, order.OrderNumber, sentCount,
            $"Zahvalnica poslana na {sentCount} vještaka.");
    }

    // ── Notifikacije ──────────────────────────────────────────────────────

    private async Task SendQuoteNotificationAsync(
        AppraisalOrder order, Appraiser appraiser, DateTime deadline, CancellationToken ct)
    {
        var collateralLabel = await ResolveCollateralLabelAsync(order, ct);
        var city = order.PropertyCity ?? order.City ?? "—";

        var message =
            $"Poštovani, zamoliti ću dostavljanje ponude za izradu procjene " +
            $"{collateralLabel}, grad {city}. " +
            $"Ponude dostaviti danas do {deadline:HH:mm} sati. " +
            $"Ponuda treba da sadrži bruto cijenu i rok izrade.";

        if (!string.IsNullOrWhiteSpace(appraiser.ContactEmail))
        {
            try
            {
                await _notifications.SendAsync(new NotificationRequest(
                    RecipientUserId:   null,
                    RecipientRole:     null,
                    Channel:           NotificationChannel.Email,
                    Subject:           $"Zahtjev za ponudu — {order.OrderNumber}",
                    Message:           message,
                    RelatedEntityType: "AppraisalOrder",
                    RelatedEntityId:   order.Id.ToString(),
                    RecipientEmail:    appraiser.ContactEmail), ct);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Email zahtjeva za ponudu vještaku {Id} nije poslan.", appraiser.Id);
            }
        }
    }

    private async Task SendThankYouNotificationAsync(
        AppraisalOrder order, Appraiser appraiser, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(appraiser.ContactEmail)) return;
        try
        {
            await _notifications.SendAsync(new NotificationRequest(
                RecipientUserId:   null,
                RecipientRole:     null,
                Channel:           NotificationChannel.Email,
                Subject:           $"Zahvala — {order.OrderNumber}",
                Message:           $"Poštovani {appraiser.Name},\n\n" +
                                   $"Zahvaljujemo na dostavljenoj ponudi za narudžbu {order.OrderNumber}.\n" +
                                   $"Ovim putem Vas obavještavamo da je za ovu procjenu odabran drugi vještak.\n\n" +
                                   $"Srdačan pozdrav.",
                RelatedEntityType: "AppraisalOrder",
                RelatedEntityId:   order.Id.ToString(),
                RecipientEmail:    appraiser.ContactEmail), ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Email zahvalnice vještaku {Id} nije poslan.", appraiser.Id);
        }
    }

    // ── Pomoćne metode ────────────────────────────────────────────────────

    private async Task<AppraisalOrder> FindOrderAsync(int orderId, CancellationToken ct) =>
        await _db.AppraisalOrders.FirstOrDefaultAsync(x => x.Id == orderId, ct)
        ?? throw new NotFoundException($"Narudžba ID={orderId} nije pronaÄ‘ena.", "ORDER_NOT_FOUND");

    private string RequireUserId() =>
        _currentUser.IsAuthenticated && !string.IsNullOrWhiteSpace(_currentUser.UserId)
            ? _currentUser.UserId
            : throw new ForbiddenException("Korisnik mora biti prijavljen.");

    private async Task<string> ResolveCollateralLabelAsync(AppraisalOrder order, CancellationToken ct)
    {
        var id = order.CombinedCollateralTypeId ?? order.CollateralTypeId;
        if (id is null) return "nekretnine";
        return await _db.CodebookValues.AsNoTracking()
            .Where(v => v.Id == id.Value)
            .Select(v => v.Label)
            .FirstOrDefaultAsync(ct) ?? "nekretnine";
    }

    private async Task RecordAuditAsync(string action, AppraisalOrder order, object extra, CancellationToken ct)
    {
        try
        {
            await _audit.RecordAsync(new AuditEvent
            {
                Action            = action,
                OperationType     = AuditOperationTypes.Create,
                Module            = AuditModules.AppraisalOrders,
                EntityType        = "AppraisalOrder",
                EntityKey         = order.Id.ToString(),
                EntityDisplayName = order.OrderNumber,
                NewValues         = extra,
                Status            = AuditStatuses.Success,
                Severity          = AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Audit za {Action} nije zapisan.", action);
        }
    }
}