using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging.Abstractions;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Documents.Dtos;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Documents;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Infrastructure.Tests.Documents;

public class DocumentServiceTests
{
    [Fact]
    public async Task UploadAsync_ValidPdf_CreatesDocumentAndRecordsUploader()
    {
        await using var db = CreateDbContext();
        var (order, documentType) = await SeedOrderAndDocumentTypeAsync(db);

        var storage = new FakeFileStorageProvider();
        var service = CreateService(db, storage);

        var files = new List<DocumentUploadFile>
        {
            new(new MemoryStream([1, 2, 3, 4]), "izvod.pdf", "application/pdf", 4)
        };

        var result = await service.UploadAsync(order.Id, documentType.Id, files);

        Assert.Single(result);
        Assert.Equal(order.Id, result[0].OrderId);
        Assert.Equal(documentType.Id, result[0].DocumentTypeId);
        Assert.Equal("co-user", result[0].UploadedByUserId);
        Assert.Equal(1, storage.SaveCallCount);

        var saved = await db.Documents.SingleAsync();
        Assert.Equal("co-user", saved.UploadedByUserId);
    }

    [Fact]
    public async Task UploadAsync_NonPdfContentType_ThrowsConflictAndDoesNotPersist()
    {
        await using var db = CreateDbContext();
        var (order, documentType) = await SeedOrderAndDocumentTypeAsync(db);

        var storage = new FakeFileStorageProvider();
        var service = CreateService(db, storage);

        var files = new List<DocumentUploadFile>
        {
            new(new MemoryStream([1, 2, 3, 4]), "izvod.pdf", "application/msword", 4)
        };

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => service.UploadAsync(order.Id, documentType.Id, files));

        Assert.Equal("DOCUMENT_INVALID_CONTENT_TYPE", ex.ErrorCode);
        Assert.Equal(0, storage.SaveCallCount);
        Assert.Empty(db.Documents);
    }

    [Fact]
    public async Task UploadAsync_FileTooLarge_ThrowsConflictAndDoesNotPersist()
    {
        await using var db = CreateDbContext();
        var (order, documentType) = await SeedOrderAndDocumentTypeAsync(db);

        var storage = new FakeFileStorageProvider();
        var service = CreateService(db, storage, maxFileSizeBytes: 1024);

        var files = new List<DocumentUploadFile>
        {
            new(new MemoryStream(new byte[2048]), "izvod.pdf", "application/pdf", 2048)
        };

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => service.UploadAsync(order.Id, documentType.Id, files));

        Assert.Equal("DOCUMENT_FILE_TOO_LARGE", ex.ErrorCode);
        Assert.Equal(0, storage.SaveCallCount);
        Assert.Empty(db.Documents);
    }

    [Fact]
    public async Task UploadAsync_OneInvalidFileAmongMany_RejectsAllAndSavesNothingToStorage()
    {
        await using var db = CreateDbContext();
        var (order, documentType) = await SeedOrderAndDocumentTypeAsync(db);

        var storage = new FakeFileStorageProvider();
        var service = CreateService(db, storage);

        var files = new List<DocumentUploadFile>
        {
            new(new MemoryStream([1, 2, 3, 4]), "izvod1.pdf", "application/pdf", 4),
            new(new MemoryStream([1, 2, 3, 4]), "izvod2.docx", "application/msword", 4)
        };

        await Assert.ThrowsAsync<ConflictException>(
            () => service.UploadAsync(order.Id, documentType.Id, files));

        // Ni prvi (validan) fajl ne smije biti snimljen niti persistovan kao "osiroteo" Document
        Assert.Equal(0, storage.SaveCallCount);
        Assert.Empty(db.Documents);
    }

    // ── Download audit (sigurnosni/audit mehanizam) ────────────────────────────

    [Fact]
    public async Task OpenDownloadAsync_ExistingDocument_RecordsSuccessAuditWithVersionAndOrder()
    {
        await using var db = CreateDbContext();
        var (order, documentType) = await SeedOrderAndDocumentTypeAsync(db);
        var document = await SeedDocumentAsync(db, order.Id, documentType.Id, "co-user");

        var audit = new FakeAuditService();
        var currentUser = new FakeCurrentUserService { UserId = "am-user", Roles = [AppRoles.AM] };
        var service = CreateService(db, new FakeFileStorageProvider(), currentUser: currentUser, auditService: audit);

        var result = await service.OpenDownloadAsync(document.Id);

        Assert.NotNull(result);

        var evt = Assert.Single(audit.Recorded);
        Assert.Equal(AuditActions.DocumentDownloaded, evt.Action);
        Assert.Equal(AuditModules.Documents, evt.Module);
        Assert.Equal(AuditOperationTypes.Read, evt.OperationType);
        Assert.Equal(AuditStatuses.Success, evt.Status);
        Assert.Equal(document.Id.ToString(), evt.EntityKey);
        Assert.Contains(order.OrderNumber, evt.EntityDisplayName);

        Assert.Equal(document.Id, GetProp<int?>(evt.NewValues, "DocumentId"));
        Assert.Equal(document.OriginalFileName, GetProp<string?>(evt.NewValues, "DocumentName"));
        Assert.Equal(document.Version, GetProp<int?>(evt.NewValues, "DocumentVersion"));
        Assert.Equal(order.Id, GetProp<int?>(evt.NewValues, "OrderId"));
        Assert.Equal(order.OrderNumber, GetProp<string?>(evt.NewValues, "OrderNumber"));
        Assert.Equal(order.ClientName, GetProp<string?>(evt.NewValues, "ClientName"));
    }

    [Fact]
    public async Task OpenDownloadAsync_NonExistentDocument_RecordsFailedAuditAndThrowsNotFound()
    {
        await using var db = CreateDbContext();
        var audit = new FakeAuditService();
        var service = CreateService(db, new FakeFileStorageProvider(), auditService: audit);

        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => service.OpenDownloadAsync(9999));

        Assert.Equal("DOCUMENT_NOT_FOUND", ex.ErrorCode);

        var evt = Assert.Single(audit.Recorded);
        Assert.Equal(AuditActions.DocumentDownloadFailed, evt.Action);
        Assert.Equal(AuditStatuses.Failed, evt.Status);
        Assert.Equal("9999", evt.EntityKey);
        Assert.NotNull(evt.Reason);
    }

    [Fact]
    public async Task UploadAsync_RecordsAuditWithDocumentVersion()
    {
        await using var db = CreateDbContext();
        var (order, documentType) = await SeedOrderAndDocumentTypeAsync(db);

        var audit = new FakeAuditService();
        var service = CreateService(db, new FakeFileStorageProvider(), auditService: audit);

        var files = new List<DocumentUploadFile>
        {
            new(new MemoryStream([1, 2, 3, 4]), "izvod.pdf", "application/pdf", 4)
        };

        await service.UploadAsync(order.Id, documentType.Id, files);

        var evt = Assert.Single(audit.Recorded);
        Assert.Equal(AuditActions.DocumentUploaded, evt.Action);
        Assert.Equal(1, GetProp<int?>(evt.NewValues, "Version"));
    }

    private static T? GetProp<T>(object? source, string propertyName)
    {
        var value = source?.GetType().GetProperty(propertyName)?.GetValue(source);
        return value is null ? default : (T)value;
    }

    // ── Verzionisanje / deaktivacija ────────────────────────────────────────────

    [Fact]
    public async Task ReplaceAsync_CreatesNewVersionAndDeactivatesPrevious()
    {
        await using var db = CreateDbContext();
        var (order, documentType) = await SeedOrderAndDocumentTypeAsync(db);
        var original = await SeedDocumentAsync(db, order.Id, documentType.Id, "co-user");

        var audit = new FakeAuditService();
        var currentUser = new FakeCurrentUserService { UserId = "co-user", Roles = ["KolateralOficir"] };
        var service = CreateService(db, new FakeFileStorageProvider(), currentUser: currentUser, auditService: audit);

        var newFile = new DocumentUploadFile(new MemoryStream([9, 9, 9, 9]), "izvod-v2.pdf", "application/pdf", 4);

        var result = await service.ReplaceAsync(original.Id, newFile);

        Assert.Equal(2, result.Version);
        Assert.True(result.IsActive);
        Assert.Equal(original.Id, result.PreviousVersionId);

        var oldInDb = await db.Documents.IgnoreQueryFilters().SingleAsync(x => x.Id == original.Id);
        Assert.False(oldInDb.IsActive);
        Assert.Equal("Zamijenjen novom verzijom", oldInDb.DeactivationReason);

        Assert.Equal(2, audit.Recorded.Count);
        Assert.Equal(AuditActions.DocumentDeactivated, audit.Recorded[0].Action);
        Assert.Equal(AuditActions.DocumentVersionCreated, audit.Recorded[1].Action);
        Assert.Equal(2, GetProp<int?>(audit.Recorded[1].NewValues, "Version"));
    }

    [Fact]
    public async Task DeactivateAsync_SetsInactiveAndRecordsAudit()
    {
        await using var db = CreateDbContext();
        var (order, documentType) = await SeedOrderAndDocumentTypeAsync(db);
        var document = await SeedDocumentAsync(db, order.Id, documentType.Id, "co-user");

        var audit = new FakeAuditService();
        var service = CreateService(db, new FakeFileStorageProvider(), auditService: audit);

        var result = await service.DeactivateAsync(document.Id, "Pogrešan fajl");

        Assert.False(result.IsActive);

        var evt = Assert.Single(audit.Recorded);
        Assert.Equal(AuditActions.DocumentDeactivated, evt.Action);
        Assert.Equal("Pogrešan fajl", GetProp<string?>(evt.NewValues, "DeactivationReason"));
    }

    [Fact]
    public async Task DeactivateAsync_AlreadyInactive_ThrowsConflict()
    {
        await using var db = CreateDbContext();
        var (order, documentType) = await SeedOrderAndDocumentTypeAsync(db);
        var document = await SeedDocumentAsync(db, order.Id, documentType.Id, "co-user");

        var service = CreateService(db, new FakeFileStorageProvider());
        await service.DeactivateAsync(document.Id, null);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => service.DeactivateAsync(document.Id, null));

        Assert.Equal("DOCUMENT_ALREADY_INACTIVE", ex.ErrorCode);
    }

    [Fact]
    public async Task ReactivateAsync_SetsActiveAndRecordsAudit()
    {
        await using var db = CreateDbContext();
        var (order, documentType) = await SeedOrderAndDocumentTypeAsync(db);
        var document = await SeedDocumentAsync(db, order.Id, documentType.Id, "co-user");

        var service = CreateService(db, new FakeFileStorageProvider());
        await service.DeactivateAsync(document.Id, null);

        var audit = new FakeAuditService();
        var service2 = CreateService(db, new FakeFileStorageProvider(), auditService: audit);

        var result = await service2.ReactivateAsync(document.Id);

        Assert.True(result.IsActive);

        var evt = Assert.Single(audit.Recorded);
        Assert.Equal(AuditActions.DocumentReactivated, evt.Action);
        Assert.True(GetProp<bool?>(evt.NewValues, "IsActive"));
    }

    [Fact]
    public async Task DeleteAsync_ByUploader_SoftDeletes()
    {
        await using var db = CreateDbContext();
        var (order, documentType) = await SeedOrderAndDocumentTypeAsync(db);
        var document = await SeedDocumentAsync(db, order.Id, documentType.Id, "co-user");

        var service = CreateService(db, new FakeFileStorageProvider());

        await service.DeleteAsync(document.Id);

        var deleted = await db.Documents.IgnoreQueryFilters().SingleAsync(x => x.Id == document.Id);
        Assert.True(deleted.IsDeleted);
    }

    [Fact]
    public async Task DeleteAsync_ByOtherUserWithoutCaRole_ThrowsForbidden()
    {
        await using var db = CreateDbContext();
        var (order, documentType) = await SeedOrderAndDocumentTypeAsync(db);
        var document = await SeedDocumentAsync(db, order.Id, documentType.Id, "drugi-korisnik");

        var service = CreateService(db, new FakeFileStorageProvider());

        var ex = await Assert.ThrowsAsync<ForbiddenException>(
            () => service.DeleteAsync(document.Id));

        Assert.Equal("DOCUMENT_DELETE_FORBIDDEN", ex.ErrorCode);
    }

    [Fact]
    public async Task DeleteAsync_ByKolateralAdministrator_SoftDeletes()
    {
        await using var db = CreateDbContext();
        var (order, documentType) = await SeedOrderAndDocumentTypeAsync(db);
        var document = await SeedDocumentAsync(db, order.Id, documentType.Id, "drugi-korisnik");

        var currentUser = new FakeCurrentUserService
        {
            UserId = "ca-user",
            Roles = [AppRoles.KolateralAdministrator]
        };
        var service = CreateService(db, new FakeFileStorageProvider(), currentUser: currentUser);

        await service.DeleteAsync(document.Id);

        var deleted = await db.Documents.IgnoreQueryFilters().SingleAsync(x => x.Id == document.Id);
        Assert.True(deleted.IsDeleted);
    }

    private static DocumentService CreateService(
        ApplicationDbContext db,
        IFileStorageProvider storage,
        long maxFileSizeBytes = 10 * 1024 * 1024,
        FakeCurrentUserService? currentUser = null,
        FakeAuditService? auditService = null)
    {
        var configuration = new ConfigurationBuilder()
            .AddInMemoryCollection(new Dictionary<string, string?>
            {
                ["Documents:MaxFileSizeBytes"] = maxFileSizeBytes.ToString()
            })
            .Build();

        return new DocumentService(
            db,
            storage,
            currentUser ?? new FakeCurrentUserService(),
            configuration,
            auditService ?? new FakeAuditService(),
            NullLogger<DocumentService>.Instance);
    }

    private static ApplicationDbContext CreateDbContext()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;

        return new ApplicationDbContext(options);
    }

    private static async Task<(AppraisalOrder Order, CodebookValue DocumentType)> SeedOrderAndDocumentTypeAsync(
        ApplicationDbContext db)
    {
        var documentType = CodebookValue.Create(
            "tipovi_dokumenata",
            "OSTALO",
            "Ostalo",
            null,
            99,
            "seed");
        db.CodebookValues.Add(documentType);

        var order = AppraisalOrder.Create(
            orderNumber:              "NP-DOC-1",
            title:                    "Test narudžba",
            clientName:               "Klijent Test",
            clientType:               "FL",
            clientIdentifier:         null,
            contactName:              null,
            contactPhone:             null,
            contactEmail:             null,
            city:                     "Sarajevo",
            branch:                   null,
            branchAddress:            null,
            propertyAddress:          null,
            collateralTypeId:         null,
            combinedCollateralTypeId: null,
            createdByUserId:          "sales-user",
            createdByRole:            "Prodaja",
            createdByName:            null,
            deliveryContactName:      null,
            amRecipientName:          null);
        db.AppraisalOrders.Add(order);

        await db.SaveChangesAsync();

        return (order, documentType);
    }

    private static async Task<RBBH.CollateralAppraisal.Domain.Documents.Document> SeedDocumentAsync(
        ApplicationDbContext db,
        int orderId,
        int documentTypeId,
        string uploadedByUserId)
    {
        var document = RBBH.CollateralAppraisal.Domain.Documents.Document.Create(
            orderId,
            documentTypeId,
            "izvod.pdf",
            "Izvod.pdf",
            "application/pdf",
            4,
            "appraisal-orders/1/documents/izvod.pdf",
            uploadedByUserId);

        db.Documents.Add(document);
        await db.SaveChangesAsync();

        return document;
    }

    private sealed class FakeFileStorageProvider : IFileStorageProvider
    {
        public int SaveCallCount { get; private set; }

        public Task<FileStorageResult> SaveAsync(
            Stream content, string originalFileName, string subPath, CancellationToken ct = default)
        {
            SaveCallCount++;
            return Task.FromResult(new FileStorageResult($"{subPath}/{originalFileName}", content.Length));
        }

        public Task<Stream> OpenReadAsync(string storagePath, CancellationToken ct = default) =>
            Task.FromResult<Stream>(Stream.Null);

        public Task DeleteAsync(string storagePath, CancellationToken ct = default) =>
            Task.CompletedTask;

        public Task<bool> ExistsAsync(string storagePath, CancellationToken ct = default) =>
            Task.FromResult(true);
    }

    private sealed class FakeCurrentUserService : ICurrentUserService
    {
        public string? UserId { get; set; } = "co-user";
        public string? Username => "co.test";
        public string? FullName => "Co Test";
        public string? Email => "co.test@rbbh.ba";
        public string? Role => "KolateralOficir";
        public IReadOnlyList<string> Roles { get; set; } = ["KolateralOficir"];
        public IReadOnlyList<string> Permissions => ["documents.delete"];
        public bool IsAuthenticated => true;
    }

    private sealed class FakeAuditService : IAuditService
    {
        public List<AuditEvent> Recorded { get; } = [];

        public Task RecordAsync(AuditEvent auditEvent, CancellationToken cancellationToken = default)
        {
            Recorded.Add(auditEvent);
            return Task.CompletedTask;
        }
    }
}
