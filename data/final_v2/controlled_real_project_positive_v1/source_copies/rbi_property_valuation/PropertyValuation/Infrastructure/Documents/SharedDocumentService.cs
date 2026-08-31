using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Documents;
using RBBH.CollateralAppraisal.Application.Documents.Dtos;
using RBBH.CollateralAppraisal.Domain.Documents;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Documents;

public sealed class SharedDocumentService : ISharedDocumentService
{
    private const string PdfContentType  = "application/pdf";
    private const string XlsxContentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
    private const string XlsContentType  = "application/vnd.ms-excel";

    private readonly ApplicationDbContext _db;
    private readonly IFileStorageProvider _storage;
    private readonly ICurrentUserService  _currentUser;
    private readonly IConfiguration       _configuration;
    private readonly ILogger<SharedDocumentService> _logger;

    public SharedDocumentService(
        ApplicationDbContext db,
        IFileStorageProvider storage,
        ICurrentUserService currentUser,
        IConfiguration configuration,
        ILogger<SharedDocumentService> logger)
    {
        _db            = db;
        _storage       = storage;
        _currentUser   = currentUser;
        _configuration = configuration;
        _logger        = logger;
    }

    public async Task<IReadOnlyList<SharedDocumentDto>> GetAllAsync(CancellationToken ct = default)
    {
        return await _db.SharedDocuments
            .AsNoTracking()
            .Where(x => x.IsActive)
            .OrderBy(x => x.Category)
            .ThenBy(x => x.Title)
            .Select(x => ToDto(x))
            .ToListAsync(ct);
    }

    public async Task<SharedDocumentDto> UploadAsync(
        string title,
        string category,
        DocumentUploadFile file,
        CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();

        ValidatePdf(file);
        ValidateTitle(title);
        ValidateCategory(category);

        await using var content = file.Content;

        var result = await _storage.SaveAsync(
            content,
            file.FileName,
            "shared-documents",
            ct);

        var doc = SharedDocument.Create(
            title,
            category,
            System.IO.Path.GetFileName(result.StoragePath),
            file.FileName,
            file.ContentType,
            result.FileSize,
            result.StoragePath,
            userId);

        _db.SharedDocuments.Add(doc);
        await _db.SaveChangesAsync(ct);

        return ToDto(doc);
    }

    public async Task<DocumentDownloadDto> DownloadAsync(int id, CancellationToken ct = default)
    {
        var doc = await _db.SharedDocuments
            .AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == id, ct)
            ?? throw new NotFoundException("Dokument nije pronađen.", "SHARED_DOCUMENT_NOT_FOUND");

        var stream = await _storage.OpenReadAsync(doc.StoragePath, ct);

        return new DocumentDownloadDto(
            stream,
            doc.OriginalFileName,
            doc.ContentType ?? PdfContentType);
    }

    public async Task DeleteAsync(int id, CancellationToken ct = default)
    {
        var userId = RequireCurrentUserId();

        var doc = await _db.SharedDocuments
            .FirstOrDefaultAsync(x => x.Id == id, ct)
            ?? throw new NotFoundException("Dokument nije pronađen.", "SHARED_DOCUMENT_NOT_FOUND");

        doc.Deactivate(userId, DateTime.UtcNow);
        await _db.SaveChangesAsync(ct);
    }

    private static readonly HashSet<string> AllowedExtensions =
        [".pdf", ".xlsx", ".xls", ".xlsm"];

    private static readonly HashSet<string> AllowedContentTypes =
    [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel",
        "application/vnd.ms-excel.sheet.macroEnabled.12",
        "application/octet-stream"  // browser ponekad šalje ovaj content-type za Excel
    ];

    private void ValidatePdf(DocumentUploadFile file)
    {
        var maxBytes = _configuration.GetValue<long>("Documents:MaxFileSizeBytes", 10 * 1024 * 1024);

        if (file.Length <= 0)
            throw new ConflictException("Fajl je prazan.", "DOCUMENT_EMPTY_FILE");

        if (file.Length > maxBytes)
            throw new ConflictException("Fajl prelazi maksimalnu dozvoljenu veličinu (10 MB).", "DOCUMENT_FILE_TOO_LARGE");

        var ext = System.IO.Path.GetExtension(file.FileName ?? "").ToLowerInvariant();
        if (!AllowedExtensions.Contains(ext))
            throw new ConflictException(
                $"Dozvoljen je PDF ili Excel fajl (.pdf, .xlsx, .xls). Primljeno: {ext}",
                "DOCUMENT_INVALID_EXTENSION");
    }

    private static void ValidateTitle(string title)
    {
        if (string.IsNullOrWhiteSpace(title) || title.Length > 300)
            throw new ConflictException("Naziv dokumenta je obavezan (max 300 znakova).", "INVALID_TITLE");
    }

    private static void ValidateCategory(string category)
    {
        if (!SharedDocumentCategories.All.Contains(category))
            throw new ConflictException($"Nepoznata kategorija: {category}.", "INVALID_CATEGORY");
    }

    private string RequireCurrentUserId()
    {
        if (!_currentUser.IsAuthenticated || string.IsNullOrWhiteSpace(_currentUser.UserId))
            throw new ForbiddenException("Korisnik mora biti prijavljen.");

        return _currentUser.UserId;
    }

    private static SharedDocumentDto ToDto(SharedDocument doc) =>
        new(doc.Id, doc.Title, doc.Category,
            doc.FileName, doc.OriginalFileName, doc.ContentType, doc.FileSize,
            doc.UploadedAt, doc.UploadedByUserId,
            $"/api/shared-documents/{doc.Id}/download",
            doc.IsActive);
}
