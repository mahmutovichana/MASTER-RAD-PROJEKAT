using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Documents;
using RBBH.CollateralAppraisal.Application.Documents.Dtos;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Opinions;
using RBBH.CollateralAppraisal.Application.Opinions.Dtos;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Application.Users.Models;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Opinions;

public sealed class OpinionService : IOpinionService
{
    private const string DocumentTypesCodebookKey = Application.Common.Constants.CodebookKeys.DocumentTypes;
    private const string CoOpinionDocumentCode    = Application.Common.Constants.DocumentTypeCodes.CoOpinion;
    private const string LegalOpinionDocumentCode = Application.Common.Constants.DocumentTypeCodes.LegalOpinion;
    private const string OpinionsRequestedAction  = "ORDER_OPINIONS_REQUESTED";
    private const string OpinionSubmittedAction   = "ORDER_OPINION_SUBMITTED";

    private readonly ApplicationDbContext      _db;
    private readonly INotificationService      _notifications;
    private readonly IDocumentService          _documentService;
    private readonly IUserRoleProvider         _userRoleProvider;
    private readonly IAuditService             _auditService;
    private readonly ILogger<OpinionService>   _logger;

    public OpinionService(
        ApplicationDbContext     db,
        INotificationService     notifications,
        IDocumentService         documentService,
        IUserRoleProvider        userRoleProvider,
        IAuditService            auditService,
        ILogger<OpinionService>  logger)
    {
        _db               = db;
        _notifications    = notifications;
        _documentService  = documentService;
        _userRoleProvider = userRoleProvider;
        _auditService     = auditService;
        _logger           = logger;
    }

    // ── RequestOpinions ───────────────────────────────────────────────────────
    public async Task RequestOpinionsAsync(int appraisalOrderId, CancellationToken ct = default)
    {
        var order = await _db.AppraisalOrders
            .FirstOrDefaultAsync(o => o.Id == appraisalOrderId, ct)
            ?? throw new InvalidOperationException($"Narudžba {appraisalOrderId} nije pronađena.");

        // Kreiraj Opinion redove za CO i Pravnu
        _db.Opinions.Add(Opinion.CreateRequested(appraisalOrderId, OpinionType.CO));
        _db.Opinions.Add(Opinion.CreateRequested(appraisalOrderId, OpinionType.Pravna));

        // Kreiraj TaskItem tipa RequestOpinion za CO
        _db.TaskItems.Add(TaskItem.Create(
            orderId:      appraisalOrderId,
            type:         TaskItemType.RequestOpinion,
            title:        "Mišljenje CO",
            description:  $"Zahtjev za mišljenje CO za narudžbu {order.OrderNumber}.",
            assignedRole: AppRoles.KolateralOficir));

        // Kreiraj TaskItem tipa RequestOpinion za Pravnu
        _db.TaskItems.Add(TaskItem.Create(
            orderId:      appraisalOrderId,
            type:         TaskItemType.RequestOpinion,
            title:        "Mišljenje Pravne službe",
            description:  $"Zahtjev za mišljenje Pravne službe za narudžbu {order.OrderNumber}.",
            assignedRole: AppRoles.PravnaSluzba));

        await _db.SaveChangesAsync(ct);

        // Notifikacija KolateralOficir korisnicima
        var coUsers = await GetUserIdsByRoleAsync(AppRoles.KolateralOficir, ct);
        await _notifications.NotifyUsersAsync(
            coUsers,
            subject:           "Zahtjev za mišljenje CO",
            message:           $"Molim mišljenje CO za klijenta {order.ClientName} (nalog {order.OrderNumber}).",
            relatedEntityType: "AppraisalOrder",
            relatedEntityId:   appraisalOrderId.ToString(),
            ct:                ct);

        // Notifikacija PravnaSluzba korisnicima
        var pravnaUsers = await GetUserIdsByRoleAsync(AppRoles.PravnaSluzba, ct);
        await _notifications.NotifyUsersAsync(
            pravnaUsers,
            subject:           "Zahtjev za mišljenje Pravne službe",
            message:           $"Molim mišljenje Pravne službe za klijenta {order.ClientName} (nalog {order.OrderNumber}).",
            relatedEntityType: "AppraisalOrder",
            relatedEntityId:   appraisalOrderId.ToString(),
            ct:                ct);

        await RecordOpinionAuditAsync(
            OpinionsRequestedAction,
            AuditOperationTypes.Create,
            order,
            new
            {
                CoUsersNotified     = coUsers.Count,
                PravnaUsersNotified = pravnaUsers.Count
            },
            ct);
    }

    // ── SubmitOpinion ─────────────────────────────────────────────────────────
    public async Task SubmitOpinionAsync(
        int           appraisalOrderId,
        OpinionType   opinionType,
        Stream        fileStream,
        string        fileName,
        string?       contentType,
        string?       comment,
        string        userId,
        CancellationToken ct = default)
    {
        var order = await _db.AppraisalOrders
            .FirstOrDefaultAsync(o => o.Id == appraisalOrderId, ct)
            ?? throw new InvalidOperationException($"Narudžba {appraisalOrderId} nije pronađena.");

        var opinion = await _db.Opinions
            .FirstOrDefaultAsync(o => o.AppraisalOrderId == appraisalOrderId
                                   && o.OpinionType == opinionType, ct)
            ?? throw new InvalidOperationException(
                $"Opinion tipa {opinionType} za narudžbu {appraisalOrderId} nije pronađen.");

        // Upload PDF-a preko IDocumentService (T2) — reuse storage + validacija,
        // klasifikovan kao MISLJENJE_CO / MISLJENJE_PRAVNA u šifarniku dokumenata.
        var documentTypeCode = opinionType == OpinionType.CO
            ? CoOpinionDocumentCode
            : LegalOpinionDocumentCode;

        var documentTypeId = await GetDocumentTypeIdAsync(documentTypeCode, ct);

        var uploadFile = new DocumentUploadFile(fileStream, fileName, contentType, fileStream.Length);
        var uploaded = await _documentService.UploadAsync(
            appraisalOrderId,
            documentTypeId,
            [uploadFile],
            ct);

        var document = uploaded[0];

        // Importuj mišljenje na entitetu
        var now = DateTime.UtcNow;
        opinion.Import(document.Id, userId, comment, now);

        // Kompletiraj odgovarajući TaskItem
        var assignedRole = opinionType == OpinionType.CO
            ? AppRoles.KolateralOficir
            : AppRoles.PravnaSluzba;

        var task = await _db.TaskItems
            .FirstOrDefaultAsync(t => t.AppraisalOrderId == appraisalOrderId
                                   && t.TaskType         == TaskItemType.RequestOpinion
                                   && t.AssignedRole     == assignedRole, ct);

        task?.Complete(userId, comment, now);

        await _db.SaveChangesAsync(ct);

        await RecordOpinionAuditAsync(
            OpinionSubmittedAction,
            AuditOperationTypes.Import,
            order,
            new
            {
                OpinionType      = opinionType.ToString(),
                DocumentId       = document.Id,
                ImportedByUserId = userId,
                Comment          = comment
            },
            ct);

        // Provjeri jesu li OBA mišljenja importovana
        var svaOpinions = await _db.Opinions
            .Where(o => o.AppraisalOrderId == appraisalOrderId)
            .ToListAsync(ct);

        if (svaOpinions.All(o => o.Status == OpinionStatus.Imported))
        {
            order.MarkOpinionsCompleted(now);
            await _db.SaveChangesAsync(ct);

            // Notifikacija inicijatoru narudžbe (AM/SM/UB) — narudžba pamti tačno
            // koji je korisnik inicirao (CreatedByUserId), pa notifikaciju šaljemo
            // direktno njemu umjesto generičkog broadcast-a na cijeli segment Prodaja
            // (AM/SM/UB su odvojene role, "Prodaja" nije Keycloak rola za koju bi
            // postojao spisak korisnika).
            var recipients = !string.IsNullOrWhiteSpace(order.CreatedByUserId)
                ? [order.CreatedByUserId]
                : await GetUserIdsByRolesAsync(AppRoles.SalesRoles, ct);

            await _notifications.NotifyUsersAsync(
                recipients,
                subject:           "Završen import mišljenja",
                message:           $"Završen import mišljenja za klijenta {order.ClientName} (nalog {order.OrderNumber}).",
                relatedEntityType: "AppraisalOrder",
                relatedEntityId:   appraisalOrderId.ToString(),
                ct:                ct);

            var coUserIds = await GetUserIdsByRoleAsync(AppRoles.KolateralOficir, ct);
            if (coUserIds.Count > 0)
                await _notifications.NotifyUsersAsync(
                    coUserIds,
                    subject:           "Završen import mišljenja",
                    message:           $"Završen import mišljenja za klijenta {order.ClientName} (nalog {order.OrderNumber}).",
                    relatedEntityType: "AppraisalOrder",
                    relatedEntityId:   appraisalOrderId.ToString(),
                    ct:                ct);

            var pravnaUserIds = await GetUserIdsByRoleAsync(AppRoles.PravnaSluzba, ct);
            if (pravnaUserIds.Count > 0)
                await _notifications.NotifyUsersAsync(
                    pravnaUserIds,
                    subject:           "Završen import mišljenja",
                    message:           $"Završen import mišljenja za klijenta {order.ClientName} (nalog {order.OrderNumber}).",
                    relatedEntityType: "AppraisalOrder",
                    relatedEntityId:   appraisalOrderId.ToString(),
                    ct:                ct);
        }
    }

    // ── GetOpinions ───────────────────────────────────────────────────────────
    public async Task<List<OpinionDto>> GetOpinionsAsync(int appraisalOrderId, CancellationToken ct = default)
    {
        var opinions = await _db.Opinions
            .Where(o => o.AppraisalOrderId == appraisalOrderId)
            .ToListAsync(ct);

        return opinions.Select(o => new OpinionDto(
            OpinionType:      o.OpinionType,
            Status:           o.Status,
            ImportedByUserId: o.ImportedByUserId,
            ImportedAt:       o.ImportedAt,
            Comment:          o.Comment,
            DocumentId:       o.DocumentId
        )).ToList();
    }

    // ── Helper ────────────────────────────────────────────────────────────────
    private async Task<int> GetDocumentTypeIdAsync(string code, CancellationToken ct)
    {
        var documentTypeId = await _db.CodebookValues
            .AsNoTracking()
            .Where(x => x.CodebookKey == DocumentTypesCodebookKey && x.Code == code)
            .Select(x => (int?)x.Id)
            .FirstOrDefaultAsync(ct);

        if (documentTypeId is null)
            throw new InvalidOperationException($"Tip dokumenta {code} nije pronađen u šifarniku.");

        return documentTypeId.Value;
    }

    private async Task<List<string>> GetUserIdsByRoleAsync(string role, CancellationToken ct)
    {
        var request = new UserRoleListRequest { Role = role, PageSize = 100 };
        var result  = await _userRoleProvider.GetUsersWithRolesAsync(request, ct);
        return result.Items.Select(u => u.UserId).ToList();
    }

    /// <summary>
    /// Unija korisnika za više rola (npr. segment Prodaja = AM ∪ SM ∪ UB).
    /// Fallback put kada narudžba nema poznat CreatedByUserId (npr. stari podaci).
    /// </summary>
    private async Task<List<string>> GetUserIdsByRolesAsync(IEnumerable<string> roles, CancellationToken ct)
    {
        var userIds = new List<string>();
        foreach (var role in roles)
            userIds.AddRange(await GetUserIdsByRoleAsync(role, ct));

        return userIds.Distinct().ToList();
    }

    private async Task RecordOpinionAuditAsync(
        string action,
        string operationType,
        AppraisalOrder order,
        object newValues,
        CancellationToken ct)
    {
        try
        {
            await _auditService.RecordAsync(new AuditEvent
            {
                Action            = action,
                OperationType     = operationType,
                Module            = AuditModules.AppraisalOrders,
                EntityType        = nameof(AppraisalOrder),
                EntityKey         = order.Id.ToString(),
                EntityDisplayName = order.OrderNumber,
                NewValues         = newValues,
                Status            = AuditStatuses.Success,
                Severity          = AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Audit log nije zapisan za mišljenja narudžbe {OrderId}.",
                order.Id);
        }
    }
}
