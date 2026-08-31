using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Documents.Dtos;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Domain.Documents;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Documents;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Documents;

public sealed class DocumentServiceTests : IDisposable
{
    private readonly ApplicationDbContext _db;
    private readonly IFileStorageProvider _storage;
    private readonly ICurrentUserService _currentUser;
    private readonly IAuditService _audit;
    private readonly DocumentService _sut;

    public DocumentServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db          = new ApplicationDbContext(options);
        _storage     = Substitute.For<IFileStorageProvider>();
        _currentUser = Substitute.For<ICurrentUserService>();
        _audit       = Substitute.For<IAuditService>();

        _currentUser.IsAuthenticated.Returns(true);
        _currentUser.UserId.Returns("user-1");
        _currentUser.Roles.Returns(Array.Empty<string>());

        _sut = CreateService();
    }

    public void Dispose() => _db.Dispose();

    private DocumentService CreateService(long maxFileSizeBytes = 10 * 1024 * 1024)
    {
        var configuration = new ConfigurationBuilder()
            .AddInMemoryCollection(new Dictionary<string, string?>
            {
                ["Documents:MaxFileSizeBytes"] = maxFileSizeBytes.ToString()
            })
            .Build();

        return new DocumentService(
            _db, _storage, _currentUser, configuration, _audit, Substitute.For<ILogger<DocumentService>>());
    }

    private AppraisalOrder SeedOrder()
    {
        var order = AppraisalOrder.Create(
            "2026-000001", "Procjena", "Petar Petrović", "FL", "0101985100123",
            "Petar Petrović", "061-123-456", "petar@test.ba",
            "Sarajevo", "POS_SARAJEVO_CENTAR", "Titova 1", "Obala 1",
            null, null,
            "user-am-1", "AM", "Amina AM",
            "Amina Dostavljač", "Amar Primalac");
        _db.AppraisalOrders.Add(order);
        _db.SaveChanges();
        return order;
    }

    private CodebookValue SeedDocumentType(bool active = true)
    {
        var value = CodebookValue.Create("tipovi_dokumenata", "OSTALO", "Ostalo", null, 99, "seed");
        if (!active)
            value.Deactivate(DateTime.UtcNow, "admin", "test");
        _db.CodebookValues.Add(value);
        _db.SaveChanges();
        return value;
    }

    private Document SeedDocument(int orderId, int documentTypeId, string uploadedByUserId = "user-1")
    {
        var document = Document.Create(
            orderId, documentTypeId, "saved.pdf", "original.pdf", "application/pdf", 4,
            $"appraisal-orders/{orderId}/documents/saved.pdf", uploadedByUserId);
        _db.Documents.Add(document);
        _db.SaveChanges();
        return document;
    }

    private static DocumentUploadFile MakeFile(
        string fileName = "izvod.pdf",
        string? contentType = "application/pdf",
        long length = 4) =>
        new(new MemoryStream([1, 2, 3, 4]), fileName, contentType, length);

    // ── UploadAsync ─────────────────────────────────────────────────────────

    [Fact]
    public async Task UploadAsync_NotAuthenticated_ThrowsForbiddenException()
    {
        _currentUser.IsAuthenticated.Returns(false);
        var order   = SeedOrder();
        var docType = SeedDocumentType();

        var ex = await Assert.ThrowsAsync<ForbiddenException>(
            () => _sut.UploadAsync(order.Id, docType.Id, [MakeFile()]));

        Assert.Equal("USER_NOT_AUTHENTICATED", ex.ErrorCode);
    }

    [Fact]
    public async Task UploadAsync_EmptyFileList_ThrowsConflictException()
    {
        var order   = SeedOrder();
        var docType = SeedDocumentType();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.UploadAsync(order.Id, docType.Id, []));

        Assert.Equal("DOCUMENT_FILE_REQUIRED", ex.ErrorCode);
    }

    [Fact]
    public async Task UploadAsync_OrderNotFound_ThrowsNotFoundException()
    {
        var docType = SeedDocumentType();

        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.UploadAsync(999, docType.Id, [MakeFile()]));

        Assert.Equal("APPRAISAL_ORDER_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task UploadAsync_DocumentTypeNotFound_ThrowsNotFoundException()
    {
        var order = SeedOrder();

        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.UploadAsync(order.Id, 9999, [MakeFile()]));

        Assert.Equal("DOCUMENT_TYPE_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task UploadAsync_DocumentTypeInactive_ThrowsNotFoundException()
    {
        var order   = SeedOrder();
        var docType = SeedDocumentType(active: false);

        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.UploadAsync(order.Id, docType.Id, [MakeFile()]));

        Assert.Equal("DOCUMENT_TYPE_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task UploadAsync_EmptyFile_ThrowsConflictException()
    {
        var order   = SeedOrder();
        var docType = SeedDocumentType();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.UploadAsync(order.Id, docType.Id, [MakeFile(length: 0)]));

        Assert.Equal("DOCUMENT_EMPTY_FILE", ex.ErrorCode);
    }

    [Fact]
    public async Task UploadAsync_FileTooLarge_ThrowsConflictException()
    {
        var sut     = CreateService(maxFileSizeBytes: 10);
        var order   = SeedOrder();
        var docType = SeedDocumentType();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => sut.UploadAsync(order.Id, docType.Id, [MakeFile(length: 2048)]));

        Assert.Equal("DOCUMENT_FILE_TOO_LARGE", ex.ErrorCode);
    }

    [Fact]
    public async Task UploadAsync_InvalidExtension_ThrowsConflictException()
    {
        var order   = SeedOrder();
        var docType = SeedDocumentType();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.UploadAsync(order.Id, docType.Id, [MakeFile(fileName: "izvod.docx")]));

        Assert.Equal("DOCUMENT_INVALID_EXTENSION", ex.ErrorCode);
    }

    [Fact]
    public async Task UploadAsync_InvalidContentType_ThrowsConflictException()
    {
        var order   = SeedOrder();
        var docType = SeedDocumentType();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.UploadAsync(order.Id, docType.Id, [MakeFile(contentType: "application/msword")]));

        Assert.Equal("DOCUMENT_INVALID_CONTENT_TYPE", ex.ErrorCode);
    }

    [Fact]
    public async Task UploadAsync_ValidSinglePdf_SavesDocumentAndReturnsDto()
    {
        var order   = SeedOrder();
        var docType = SeedDocumentType();

        _storage.SaveAsync(Arg.Any<Stream>(), Arg.Any<string>(), Arg.Any<string>(), Arg.Any<CancellationToken>())
            .Returns(callInfo => new FileStorageResult(
                $"appraisal-orders/{order.Id}/documents/{Guid.NewGuid()}.pdf",
                callInfo.ArgAt<Stream>(0).Length));

        var result = await _sut.UploadAsync(order.Id, docType.Id, [MakeFile(fileName: "izvod.pdf")]);

        var dto = Assert.Single(result);
        Assert.Equal(order.Id, dto.OrderId);
        Assert.Equal(docType.Id, dto.DocumentTypeId);
        Assert.Equal("izvod.pdf", dto.OriginalFileName);
        Assert.Equal("user-1", dto.UploadedByUserId);
        Assert.Equal(4, dto.FileSize);
        Assert.Equal($"/api/documents/{dto.Id}/download", dto.DownloadUrl);

        var saved = await _db.Documents.SingleAsync();
        Assert.Equal("user-1", saved.UploadedByUserId);

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == "DOCUMENT_UPLOADED" && e.EntityKey == saved.Id.ToString()),
            Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task UploadAsync_MultipleValidFiles_SavesAllAndRecordsAuditForEach()
    {
        var order   = SeedOrder();
        var docType = SeedDocumentType();

        _storage.SaveAsync(Arg.Any<Stream>(), Arg.Any<string>(), Arg.Any<string>(), Arg.Any<CancellationToken>())
            .Returns(callInfo => new FileStorageResult($"path/{Guid.NewGuid()}.pdf", callInfo.ArgAt<Stream>(0).Length));

        var files = new[] { MakeFile(fileName: "a.pdf"), MakeFile(fileName: "b.pdf") };

        var result = await _sut.UploadAsync(order.Id, docType.Id, files);

        Assert.Equal(2, result.Count);
        await _storage.Received(2).SaveAsync(
            Arg.Any<Stream>(), Arg.Any<string>(), Arg.Any<string>(), Arg.Any<CancellationToken>());
        await _audit.Received(2).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == "DOCUMENT_UPLOADED"), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task UploadAsync_OneInvalidFileAmongMany_ThrowsAndSavesNothing()
    {
        var order   = SeedOrder();
        var docType = SeedDocumentType();

        var files = new[] { MakeFile(fileName: "a.pdf"), MakeFile(fileName: "b.docx") };

        await Assert.ThrowsAsync<ConflictException>(() => _sut.UploadAsync(order.Id, docType.Id, files));

        await _storage.DidNotReceive().SaveAsync(
            Arg.Any<Stream>(), Arg.Any<string>(), Arg.Any<string>(), Arg.Any<CancellationToken>());
        Assert.Empty(_db.Documents);
    }

    [Fact]
    public async Task UploadAsync_AuditRecordingThrows_StillReturnsResult()
    {
        var order   = SeedOrder();
        var docType = SeedDocumentType();

        _storage.SaveAsync(Arg.Any<Stream>(), Arg.Any<string>(), Arg.Any<string>(), Arg.Any<CancellationToken>())
            .Returns(new FileStorageResult("path/a.pdf", 4));

        _audit.RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("audit down")));

        var result = await _sut.UploadAsync(order.Id, docType.Id, [MakeFile()]);

        Assert.Single(result);
    }

    // ── GetByOrderAsync ─────────────────────────────────────────────────────

    [Fact]
    public async Task GetByOrderAsync_OrderNotFound_ThrowsNotFoundException()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.GetByOrderAsync(999));

        Assert.Equal("APPRAISAL_ORDER_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task GetByOrderAsync_ReturnsDocumentsForOrder()
    {
        var order   = SeedOrder();
        var docType = SeedDocumentType();
        SeedDocument(order.Id, docType.Id);
        SeedDocument(order.Id, docType.Id);

        var result = await _sut.GetByOrderAsync(order.Id);

        Assert.Equal(2, result.Count);
        Assert.All(result, d => Assert.Equal(order.Id, d.OrderId));
    }

    [Fact]
    public async Task GetByOrderAsync_NoDocuments_ReturnsEmptyList()
    {
        var order = SeedOrder();

        var result = await _sut.GetByOrderAsync(order.Id);

        Assert.Empty(result);
    }

    // ── OpenDownloadAsync ───────────────────────────────────────────────────

    [Fact]
    public async Task OpenDownloadAsync_DocumentNotFound_ThrowsNotFoundException()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.OpenDownloadAsync(999));

        Assert.Equal("DOCUMENT_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task OpenDownloadAsync_ValidDocument_ReturnsStreamFromStorage()
    {
        var order   = SeedOrder();
        var docType = SeedDocumentType();
        var doc     = SeedDocument(order.Id, docType.Id);

        var stream = new MemoryStream([9, 9, 9]);
        _storage.OpenReadAsync(doc.StoragePath, Arg.Any<CancellationToken>()).Returns(stream);

        var dto = await _sut.OpenDownloadAsync(doc.Id);

        Assert.Same(stream, dto.Content);
        Assert.Equal("original.pdf", dto.FileName);
        Assert.Equal("application/pdf", dto.ContentType);
    }

    [Fact]
    public async Task OpenDownloadAsync_NullContentType_DefaultsToPdfContentType()
    {
        var order   = SeedOrder();
        var docType = SeedDocumentType();

        var doc = Document.Create(
            order.Id, docType.Id, "saved.pdf", "original.pdf", null, 4,
            "appraisal-orders/1/documents/saved.pdf", "user-1");
        _db.Documents.Add(doc);
        await _db.SaveChangesAsync();

        _storage.OpenReadAsync(doc.StoragePath, Arg.Any<CancellationToken>()).Returns(Stream.Null);

        var dto = await _sut.OpenDownloadAsync(doc.Id);

        Assert.Equal("application/pdf", dto.ContentType);
    }

    // ── DeleteAsync ─────────────────────────────────────────────────────────

    [Fact]
    public async Task DeleteAsync_NotAuthenticated_ThrowsForbiddenException()
    {
        _currentUser.IsAuthenticated.Returns(false);
        var order   = SeedOrder();
        var docType = SeedDocumentType();
        var doc     = SeedDocument(order.Id, docType.Id);

        var ex = await Assert.ThrowsAsync<ForbiddenException>(() => _sut.DeleteAsync(doc.Id));

        Assert.Equal("USER_NOT_AUTHENTICATED", ex.ErrorCode);
    }

    [Fact]
    public async Task DeleteAsync_DocumentNotFound_ThrowsNotFoundException()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.DeleteAsync(999));

        Assert.Equal("DOCUMENT_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task DeleteAsync_NotUploaderAndNotCA_ThrowsForbiddenException()
    {
        var order   = SeedOrder();
        var docType = SeedDocumentType();
        var doc     = SeedDocument(order.Id, docType.Id, uploadedByUserId: "other-user");

        var ex = await Assert.ThrowsAsync<ForbiddenException>(() => _sut.DeleteAsync(doc.Id));

        Assert.Equal("DOCUMENT_DELETE_FORBIDDEN", ex.ErrorCode);
    }

    [Fact]
    public async Task DeleteAsync_ByUploader_SoftDeletesAndRecordsAudit()
    {
        var order   = SeedOrder();
        var docType = SeedDocumentType();
        var doc     = SeedDocument(order.Id, docType.Id, uploadedByUserId: "user-1");

        await _sut.DeleteAsync(doc.Id);

        var reloaded = await _db.Documents.IgnoreQueryFilters().SingleAsync(x => x.Id == doc.Id);
        Assert.True(reloaded.IsDeleted);
        Assert.Equal("user-1", reloaded.DeletedByUserId);

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == "DOCUMENT_DELETED" && e.EntityKey == doc.Id.ToString()),
            Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task DeleteAsync_ByKolateralAdministrator_SoftDeletes()
    {
        _currentUser.UserId.Returns("ca-user");
        _currentUser.Roles.Returns([AppRoles.KolateralAdministrator]);

        var order   = SeedOrder();
        var docType = SeedDocumentType();
        var doc     = SeedDocument(order.Id, docType.Id, uploadedByUserId: "other-user");

        await _sut.DeleteAsync(doc.Id);

        var reloaded = await _db.Documents.IgnoreQueryFilters().SingleAsync(x => x.Id == doc.Id);
        Assert.True(reloaded.IsDeleted);
    }

    [Fact]
    public async Task DeleteAsync_AuditRecordingThrows_StillSoftDeletes()
    {
        var order   = SeedOrder();
        var docType = SeedDocumentType();
        var doc     = SeedDocument(order.Id, docType.Id, uploadedByUserId: "user-1");

        _audit.RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("audit down")));

        await _sut.DeleteAsync(doc.Id);

        var reloaded = await _db.Documents.IgnoreQueryFilters().SingleAsync(x => x.Id == doc.Id);
        Assert.True(reloaded.IsDeleted);
    }
}
