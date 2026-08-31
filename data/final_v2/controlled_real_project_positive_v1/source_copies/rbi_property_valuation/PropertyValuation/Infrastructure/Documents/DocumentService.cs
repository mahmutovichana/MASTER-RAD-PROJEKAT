using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Documents;
using RBBH.CollateralAppraisal.Application.Documents.Dtos;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Domain.Documents;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Documents;

public sealed class DocumentService : IDocumentService
{
    private const string PdfContentType = "application/pdf";

    private readonly ApplicationDbContext _db;
    private readonly IFileStorageProvider _storage;
    private readonly ICurrentUserService _currentUser;
    private readonly IConfiguration _configuration;
    private readonly IAuditService _auditService;
    private readonly ILogger<DocumentService> _logger;

    public DocumentService(
        ApplicationDbContext db,
        IFileStorageProvider storage,
        ICurrentUserService currentUser,
        IConfiguration configuration,
        IAuditService auditService,
        ILogger<DocumentService> logger)
    {
        _db = db;
        _storage = storage;
        _currentUser = currentUser;
        _configuration = configuration;
        _auditService = auditService;
        _logger = logger;
    }

    public async Task<IReadOnlyList<DocumentDto>> UploadAsync(
        int orderId,
        int documentTypeId,
        IReadOnlyList<DocumentUploadFile> files,
        CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();

        if (files.Count == 0)
            throw new ConflictException("Potrebno je poslati barem jedan PDF dokument.", "DOCUMENT_FILE_REQUIRED");

        var orderExists = await _db.AppraisalOrders
            .AsNoTracking()
            .AnyAsync(x => x.Id == orderId, ct);

        if (!orderExists)
            throw new NotFoundException("Narudžba procjene nije pronađena.", "APPRAISAL_ORDER_NOT_FOUND");

        var documentTypeExists = await _db.CodebookValues
            .AsNoTracking()
            .AnyAsync(x => x.Id == documentTypeId && x.IsActive, ct);

        if (!documentTypeExists)
            throw new NotFoundException("Tip dokumenta nije pronađen ili nije aktivan.", "DOCUMENT_TYPE_NOT_FOUND");

        // Validiraj sve fajlove prije nego što bilo šta snimimo na disk —
        // izbjegava osirotjele fajlove ako kasniji fajl u listi ne prođe validaciju.
        foreach (var file in files)
            ValidatePdf(file);

        var savedDocuments = new List<Document>();

        foreach (var file in files)
        {
            await using var content = file.Content;

            var result = await _storage.SaveAsync(
                content,
                file.FileName,
                $"appraisal-orders/{orderId}/documents",
                ct);

            var document = Document.Create(
                orderId,
                documentTypeId,
                Path.GetFileName(result.StoragePath),
                file.FileName,
                file.ContentType,
                result.FileSize,
                result.StoragePath,
                userId);

            _db.Documents.Add(document);
            savedDocuments.Add(document);
        }

        await _db.SaveChangesAsync(ct);

        foreach (var document in savedDocuments)
            await RecordDocumentAuditAsync(AuditActions.DocumentUploaded, AuditOperationTypes.Create, document, ct);

        return savedDocuments.Select(ToDto).ToList();
    }

    public async Task<IReadOnlyList<DocumentDto>> GetByOrderAsync(
        int orderId,
        CancellationToken ct = default)
    {
        var orderExists = await _db.AppraisalOrders
            .AsNoTracking()
            .AnyAsync(x => x.Id == orderId, ct);

        if (!orderExists)
            throw new NotFoundException("Narudžba procjene nije pronađena.", "APPRAISAL_ORDER_NOT_FOUND");

        return await _db.Documents
            .AsNoTracking()
            .Where(x => x.AppraisalOrderId == orderId)
            .OrderByDescending(x => x.UploadedAt)
            .ThenByDescending(x => x.Id)
            .Select(x => ToDto(x))
            .ToListAsync(ct);
    }

    public async Task<DocumentDownloadDto> OpenDownloadAsync(
        int documentId,
        CancellationToken ct = default)
    {
        // AsNoTracking + ručni lookup narudžbe (Document nema navigation property na
        // AppraisalOrder) — potrebno za audit (OrderNumber/ClientName se moraju vidjeti
        // u audit zapisu, ne samo DocumentId).
        var document = await _db.Documents
            .AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == documentId, ct);

        if (document is null)
        {
            // Svaki pokušaj preuzimanja nepostojećeg/obrisanog dokumenta MORA biti
            // evidentiran — bez ovoga, probing/enumeraciju document ID-ova niko ne vidi.
            await RecordDocumentDownloadAuditAsync(
                documentId, document: null, orderNumber: null, clientName: null,
                success: false, reason: "Dokument nije pronađen.", ct);

            throw new NotFoundException("Dokument nije pronađen.", "DOCUMENT_NOT_FOUND");
        }

        var order = await _db.AppraisalOrders
            .AsNoTracking()
            .Where(x => x.Id == document.AppraisalOrderId)
            .Select(x => new { x.OrderNumber, x.ClientName })
            .FirstOrDefaultAsync(ct);

        try
        {
            var stream = await _storage.OpenReadAsync(document.StoragePath, ct);

            await RecordDocumentDownloadAuditAsync(
                document.Id, document, order?.OrderNumber, order?.ClientName,
                success: true, reason: null, ct);

            return new DocumentDownloadDto(
                stream,
                document.OriginalFileName ?? document.FileName,
                document.ContentType ?? PdfContentType);
        }
        catch (Exception ex)
        {
            // Npr. fajl fizički nedostaje na storage-u — i ovo je sigurnosno/operativno
            // relevantan podatak (mora ostati u audit tragu, ne samo u app logu).
            await RecordDocumentDownloadAuditAsync(
                document.Id, document, order?.OrderNumber, order?.ClientName,
                success: false, reason: ex.Message, ct);

            throw;
        }
    }

    public async Task DeleteAsync(
        int documentId,
        CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();

        var document = await _db.Documents
            .FirstOrDefaultAsync(x => x.Id == documentId, ct);

        if (document is null)
            throw new NotFoundException("Dokument nije pronađen.", "DOCUMENT_NOT_FOUND");

        if (!CanManage(document, userId))
            throw new ForbiddenException("Dokument može obrisati samo uploader ili CA.", "DOCUMENT_DELETE_FORBIDDEN");

        document.SoftDelete(userId, DateTime.UtcNow);

        await _db.SaveChangesAsync(ct);

        await RecordDocumentAuditAsync(AuditActions.DocumentDeleted, AuditOperationTypes.Delete, document, ct);
    }

    public async Task<DocumentDto> ReplaceAsync(
        int documentId,
        DocumentUploadFile file,
        CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();

        var previous = await _db.Documents
            .FirstOrDefaultAsync(x => x.Id == documentId, ct);

        if (previous is null)
            throw new NotFoundException("Dokument nije pronađen.", "DOCUMENT_NOT_FOUND");

        if (!CanManage(previous, userId))
            throw new ForbiddenException("Dokument može zamijeniti samo uploader ili CA.", "DOCUMENT_REPLACE_FORBIDDEN");

        ValidatePdf(file);

        await using var content = file.Content;
        var stored = await _storage.SaveAsync(
            content,
            file.FileName,
            $"appraisal-orders/{previous.AppraisalOrderId}/documents",
            ct);

        var newVersion = Document.CreateNewVersion(
            previous,
            Path.GetFileName(stored.StoragePath),
            file.FileName,
            file.ContentType,
            stored.FileSize,
            stored.StoragePath,
            userId);

        var now = DateTime.UtcNow;
        previous.Deactivate(userId, now, "Zamijenjen novom verzijom");

        _db.Documents.Add(newVersion);
        await _db.SaveChangesAsync(ct);

        await RecordDocumentAuditAsync(AuditActions.DocumentDeactivated, AuditOperationTypes.Update, previous, ct);
        await RecordDocumentAuditAsync(AuditActions.DocumentVersionCreated, AuditOperationTypes.Create, newVersion, ct);

        return ToDto(newVersion);
    }

    public async Task<DocumentDto> DeactivateAsync(
        int documentId,
        string? reason,
        CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();

        var document = await _db.Documents
            .FirstOrDefaultAsync(x => x.Id == documentId, ct);

        if (document is null)
            throw new NotFoundException("Dokument nije pronađen.", "DOCUMENT_NOT_FOUND");

        if (!CanManage(document, userId))
            throw new ForbiddenException("Dokument može deaktivirati samo uploader ili CA.", "DOCUMENT_DEACTIVATE_FORBIDDEN");

        if (!document.IsActive)
            throw new ConflictException("Dokument je već deaktiviran.", "DOCUMENT_ALREADY_INACTIVE");

        document.Deactivate(userId, DateTime.UtcNow, reason);
        await _db.SaveChangesAsync(ct);

        await RecordDocumentAuditAsync(AuditActions.DocumentDeactivated, AuditOperationTypes.Update, document, ct);

        return ToDto(document);
    }

    public async Task<DocumentDto> ReactivateAsync(
        int documentId,
        CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();

        var document = await _db.Documents
            .FirstOrDefaultAsync(x => x.Id == documentId, ct);

        if (document is null)
            throw new NotFoundException("Dokument nije pronađen.", "DOCUMENT_NOT_FOUND");

        if (!CanManage(document, userId))
            throw new ForbiddenException("Dokument može ponovo aktivirati samo uploader ili CA.", "DOCUMENT_REACTIVATE_FORBIDDEN");

        if (document.IsActive)
            throw new ConflictException("Dokument je već aktivan.", "DOCUMENT_ALREADY_ACTIVE");

        document.Reactivate(DateTime.UtcNow);
        await _db.SaveChangesAsync(ct);

        await RecordDocumentAuditAsync(AuditActions.DocumentReactivated, AuditOperationTypes.Update, document, ct);

        return ToDto(document);
    }

    private void ValidatePdf(DocumentUploadFile file)
    {
        var maxFileSizeBytes = _configuration.GetValue<long>(
            "Documents:MaxFileSizeBytes",
            10 * 1024 * 1024);

        if (file.Length <= 0)
            throw new ConflictException("Fajl je prazan.", "DOCUMENT_EMPTY_FILE");

        if (file.Length > maxFileSizeBytes)
            throw new ConflictException("Fajl prelazi maksimalnu dozvoljenu veličinu.", "DOCUMENT_FILE_TOO_LARGE");

        var extension = Path.GetExtension(file.FileName);

        if (!string.Equals(extension, ".pdf", StringComparison.OrdinalIgnoreCase))
            throw new ConflictException("Dozvoljen je samo PDF fajl (.pdf).", "DOCUMENT_INVALID_EXTENSION");

        if (!string.Equals(file.ContentType, PdfContentType, StringComparison.OrdinalIgnoreCase))
            throw new ConflictException("Dozvoljen je samo PDF content-type.", "DOCUMENT_INVALID_CONTENT_TYPE");

        // V2: PDF magic bytes provjera (%PDF- header)
        if (file.Content.CanSeek && file.Content.Length >= 5)
        {
            var originalPosition = file.Content.Position;
            var header = new byte[5];
            var bytesRead = file.Content.Read(header, 0, 5);
            file.Content.Position = originalPosition;

            if (bytesRead >= 5 &&
                !(header[0] == 0x25 && header[1] == 0x50 && header[2] == 0x44 &&
                  header[3] == 0x46 && header[4] == 0x2D))
            {
                throw new ConflictException(
                    "Fajl nema validan PDF header (%PDF-).", "DOCUMENT_INVALID_PDF_HEADER");
            }
        }
    }

    private string RequireCurrentUserId()
    {
        if (!_currentUser.IsAuthenticated || string.IsNullOrWhiteSpace(_currentUser.UserId))
            throw new ForbiddenException("Korisnik mora biti prijavljen.", "USER_NOT_AUTHENTICATED");

        return _currentUser.UserId;
    }

    /// <summary>Zajednička provjera vlasništva/ovlaštenja za Delete/Replace/Deactivate/Reactivate.</summary>
    private bool CanManage(Document document, string userId)
    {
        if (document.UploadedByUserId == userId)
            return true;

        return _currentUser.Roles.Any(role =>
            role.Equals(AppRoles.KolateralAdministrator, StringComparison.OrdinalIgnoreCase));
    }

    private async Task RecordDocumentAuditAsync(
        string action,
        string operationType,
        Document document,
        CancellationToken ct)
    {
        try
        {
            await _auditService.RecordAsync(new AuditEvent
            {
                Action = action,
                OperationType = operationType,
                Module = AuditModules.Documents,
                EntityType = nameof(Document),
                EntityKey = document.Id.ToString(),
                EntityDisplayName = document.OriginalFileName ?? document.FileName,
                NewValues = new
                {
                    document.AppraisalOrderId,
                    document.DocumentTypeId,
                    document.FileName,
                    document.FileSize,
                    document.UploadedByUserId,
                    document.Version,
                    document.PreviousVersionId,
                    document.IsActive,
                    document.DeactivationReason
                },
                Status = AuditStatuses.Success,
                Severity = AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Audit log nije zapisan za dokument {DocumentId}.",
                document.Id);
        }
    }

    /// <summary>
    /// Audituje SVAKI pokušaj preuzimanja dokumenta — uspješan i neuspješan. Bilježi tačnu
    /// verziju dokumenta (document.Version), narudžbu i klijenta iz koje dokument potiče,
    /// ne samo naziv fajla. Ne baca grešku ako audit ne uspije — download ne smije pucati
    /// zbog audit infrastrukture (vidi <see cref="IAuditService"/> — best-effort, isti
    /// pattern kao i ostatak modula).
    /// </summary>
    private async Task RecordDocumentDownloadAuditAsync(
        int documentId,
        Document? document,
        string? orderNumber,
        string? clientName,
        bool success,
        string? reason,
        CancellationToken ct)
    {
        try
        {
            await _auditService.RecordAsync(new AuditEvent
            {
                Action = success ? AuditActions.DocumentDownloaded : AuditActions.DocumentDownloadFailed,
                OperationType = AuditOperationTypes.Read,
                Module = AuditModules.Documents,
                EntityType = nameof(Document),
                EntityKey = documentId.ToString(),
                EntityDisplayName = document is not null
                    ? $"{document.OriginalFileName ?? document.FileName}" +
                      (orderNumber is not null ? $" — {orderNumber}" : "")
                    : null,
                NewValues = new
                {
                    DocumentId = documentId,
                    DocumentName = document?.OriginalFileName ?? document?.FileName,
                    DocumentVersion = document?.Version,
                    OrderId = document?.AppraisalOrderId,
                    OrderNumber = orderNumber,
                    ClientName = clientName
                },
                Status = success ? AuditStatuses.Success : AuditStatuses.Failed,
                Severity = success ? AuditSeverity.Info : AuditSeverity.Warning,
                Reason = reason
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Audit log nije zapisan za download dokumenta {DocumentId}.",
                documentId);
        }
    }

    private static DocumentDto ToDto(Document document) =>
        new(
            document.Id,
            document.AppraisalOrderId,
            document.DocumentTypeId,
            document.FileName,
            document.OriginalFileName,
            document.ContentType,
            document.FileSize,
            document.UploadedAt,
            document.UploadedByUserId,
            $"/api/documents/{document.Id}/download",
            document.Version,
            document.PreviousVersionId,
            document.IsActive);
}
