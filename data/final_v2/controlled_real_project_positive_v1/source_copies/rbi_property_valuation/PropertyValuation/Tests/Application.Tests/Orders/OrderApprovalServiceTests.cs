// CS0618: AppraisalOrder.ChangeStatus() is marked [Obsolete] in production code.
// In tests, deliberately using this method to bypass the state machine and set up
// arbitrary order states for test scenarios — this is intentional and acceptable.
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Tests.Helpers;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Domain.Documents;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

public sealed class OrderApprovalServiceTests : IDisposable
{
    private readonly ApplicationDbContext  _db;
    private readonly ICurrentUserService   _user;
    private readonly IAuditService         _audit;
    private readonly INotificationService  _notify;
    private readonly OrderApprovalService  _sut;

    public OrderApprovalServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db     = new ApplicationDbContext(options);
        _user   = Substitute.For<ICurrentUserService>();
        _audit  = Substitute.For<IAuditService>();
        _notify = Substitute.For<INotificationService>();

        _user.UserId.Returns("user-co-1");
        _user.Role.Returns("CA");
        _user.Roles.Returns(["CA"]);
        _user.IsAuthenticated.Returns(true);

        _sut = new OrderApprovalService(
            _db,
            _user,
            _notify,
            Substitute.For<INotificationProvider>(),
            _audit,
            Substitute.For<IUserRoleProvider>(),
            Substitute.For<ILogger<OrderApprovalService>>(),
            Options.Create(new WorkflowSlaOptions()),
            new FakeClock());
    }

    private async Task<AppraisalOrder> CreateOrderAsync()
    {
        var order = AppraisalOrder.Create(
            orderNumber:              $"2026/{Guid.NewGuid():N}".Substring(0, 12),
            title:                    "Procjena – Stan, Sarajevo",
            clientName:               "Petar Petrović",
            clientType:               "FL",
            clientIdentifier:         "0101985100123",
            contactName:              "Petar Petrović",
            contactPhone:             "061-123-456",
            contactEmail:             "petar@test.ba",
            city:                     "Sarajevo",
            branch:                   "POS_SARAJEVO_CENTAR",
            branchAddress:            "Titova 1",
            propertyAddress:          "Obala 1",
            collateralTypeId:         null,
            combinedCollateralTypeId: null,
            createdByUserId:          "user-am-1",
            createdByRole:            "AM",
            createdByName:            "Amar Amarović",
            deliveryContactName:      "Amina Dostavljač",
            amRecipientName:          "Amar Primalac");

        // CS0618: bypass state machine to put order into AppraisalInProgress so that
        // SetFinalAppraisalDocument (→ AppraisalReceived) has a valid pre-state in tests.
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();
        return order;
    }

    private async Task<Document> CreateDocumentAsync(int orderId, int? documentTypeId = null)
    {
        var document = Document.Create(
            orderId:          orderId,
            documentTypeId:   documentTypeId,
            fileName:         $"{Guid.NewGuid():N}.pdf",
            originalFileName: "Procjena_final.pdf",
            contentType:      "application/pdf",
            fileSize:         123456,
            storagePath:      $"/storage/{Guid.NewGuid():N}.pdf",
            uploadedByUserId: "user-vjestak-1");

        _db.Documents.Add(document);
        await _db.SaveChangesAsync();
        return document;
    }

    private async Task<int> SeedFinalAppraisalDocumentTypeAsync()
    {
        var codebookValue = CodebookValue.Create(
            "tipovi_dokumenata", "FINALNA_PROCJENA", "Finalna procjena", null, 10, "system-seed");

        _db.CodebookValues.Add(codebookValue);
        await _db.SaveChangesAsync();
        return codebookValue.Id;
    }

    // ── Happy path: ApproveFinalAppraisalAsync ─────────────────────────────────

    [Fact]
    public async Task ApproveFinalAppraisalAsync_LinkedDocument_TransitionsToReadyForProcedure()
    {
        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var result = await _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: 5);

        Assert.Equal("ReadyForProcedure", result.Status);
        Assert.Equal(document.Id, result.FinalAppraisalDocumentId);
        Assert.Equal("user-co-1", result.CoApprovedByUserId);

        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        Assert.Equal(AppraisalOrderStatus.ReadyForProcedure, updated.Status);
        Assert.NotNull(updated.CoApprovedAt);
        Assert.NotNull(updated.ReadyForProcedureAt);
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_NoLinkedDocument_FallsBackToCodebookLookup()
    {
        var order = await CreateOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var documentTypeId = await SeedFinalAppraisalDocumentTypeAsync();
        var document = await CreateDocumentAsync(order.Id, documentTypeId);

        var result = await _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: 5);

        Assert.Equal("ReadyForProcedure", result.Status);
        Assert.Equal(document.Id, result.FinalAppraisalDocumentId);
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_CompletesOpenApprovalTask()
    {
        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);

        var task = TaskItem.Create(order.Id, TaskItemType.ApproveFinalAppraisal, "Odobri finalnu procjenu", null, "CA");
        _db.TaskItems.Add(task);
        await _db.SaveChangesAsync();

        await _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: 5);

        var updatedTask = await _db.TaskItems.FirstAsync(t => t.Id == task.Id);
        Assert.Equal(TaskItemStatus.Completed, updatedTask.Status);
        Assert.Equal("user-co-1", updatedTask.CompletedByUserId);
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_NotifiesOrderCreator()
    {
        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var result = await _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: 5);

        Assert.True(result.NotificationSent);
        await _notify.Received(1).NotifyUserAsync(
            order.CreatedByUserId!,
            Arg.Any<string>(),
            Arg.Any<string>(),
            nameof(AppraisalOrder),
            order.Id.ToString(),
            Arg.Any<bool>(),
            Arg.Any<string?>(),
            Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_RecordsAuditEvent()
    {
        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: 5);

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == "ORDER_FINAL_APPRAISAL_APPROVED" && e.EntityKey == order.Id.ToString()),
            Arg.Any<CancellationToken>());
    }

    // ── Sad path: ApproveFinalAppraisalAsync ───────────────────────────────────

    [Fact]
    public async Task ApproveFinalAppraisalAsync_AlreadyApproved_ThrowsConflict()
    {
        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        order.ApproveByCO("user-co-0", DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ApproveFinalAppraisalAsync(order.Id));
        Assert.Equal("FINAL_APPRAISAL_ALREADY_APPROVED", ex.ErrorCode);
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_InvalidStatus_ThrowsConflict()
    {
        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        order.ChangeStatus(AppraisalOrderStatus.SubmittedBySales, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ApproveFinalAppraisalAsync(order.Id));
        Assert.Equal("FINAL_APPRAISAL_INVALID_STATUS", ex.ErrorCode);
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_OrderNotFound_ThrowsNotFound()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.ApproveFinalAppraisalAsync(9999));
        Assert.Equal("APPRAISAL_ORDER_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_DocumentTypeCodebookMissing_ThrowsNotFound()
    {
        var order = await CreateOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.ApproveFinalAppraisalAsync(order.Id));
        Assert.Equal("FINAL_APPRAISAL_DOCUMENT_TYPE_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_NoDocumentUploaded_ThrowsConflict()
    {
        var order = await CreateOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await SeedFinalAppraisalDocumentTypeAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ApproveFinalAppraisalAsync(order.Id));
        Assert.Equal("FINAL_APPRAISAL_NOT_UPLOADED", ex.ErrorCode);
    }

    // ── GetFinalAppraisalAsync ──────────────────────────────────────────────────

    [Fact]
    public async Task GetFinalAppraisalAsync_ReturnsDocumentMetadata()
    {
        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var dto = await _sut.GetFinalAppraisalAsync(order.Id);

        Assert.Equal(order.Id, dto.OrderId);
        Assert.Equal(document.Id, dto.DocumentId);
        Assert.Equal(document.OriginalFileName, dto.OriginalFileName);
        Assert.Equal($"/api/documents/{document.Id}/download", dto.DownloadUrl);
    }

    [Fact]
    public async Task GetFinalAppraisalAsync_OrderNotFound_ThrowsNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.GetFinalAppraisalAsync(9999));
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_SameUserAsCreator_ThrowsForbidden()
    {
        _user.UserId.Returns("user-am-1");
        _user.Role.Returns("KolateralOficir");
        _user.Roles.Returns(["KolateralOficir"]);

        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ForbiddenException>(() => _sut.ApproveFinalAppraisalAsync(order.Id, 5));
        Assert.Equal("FOUR_EYES_VIOLATION", ex.ErrorCode);
    }

    [Fact]
    public async Task ReturnForReworkAsync_SameUserAsCreator_ThrowsForbidden()
    {
        _user.UserId.Returns("user-am-1");
        _user.Role.Returns("KolateralOficir");
        _user.Roles.Returns(["KolateralOficir"]);

        var order = await CreateOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ForbiddenException>(
            () => _sut.ReturnForReworkAsync(order.Id, "Tehničke greške", "Test komentar"));
        Assert.Equal("FOUR_EYES_VIOLATION", ex.ErrorCode);
    }

    // ── Happy path: ReturnForReworkAsync ─────────────────────────────────────

    [Fact]
    public async Task ReturnForReworkAsync_ValidOrder_TransitionsToReturnedForRework()
    {
        var order = await CreateOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var result = await _sut.ReturnForReworkAsync(order.Id, "Tehničke greške", "Komentar dorade");

        Assert.Equal("AppraisalReturnedForRework", result.Status);
        Assert.Equal(order.Id, result.OrderId);
        Assert.Equal(order.OrderNumber, result.OrderNumber);
        Assert.Contains("vraćena na doradu", result.Message);

        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        Assert.Equal(AppraisalOrderStatus.AppraisalReturnedForRework, updated.Status);
    }

    [Fact]
    public async Task ReturnForReworkAsync_CompletesOpenApprovalTask()
    {
        var order = await CreateOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);

        var task = TaskItem.Create(order.Id, TaskItemType.ApproveFinalAppraisal, "Odobri finalnu procjenu", null, "CA");
        _db.TaskItems.Add(task);
        await _db.SaveChangesAsync();

        await _sut.ReturnForReworkAsync(order.Id, "Tehničke greške", "Komentar dorade");

        var updatedTask = await _db.TaskItems.FirstAsync(t => t.Id == task.Id);
        Assert.Equal(TaskItemStatus.Completed, updatedTask.Status);
        Assert.Equal("user-co-1", updatedTask.CompletedByUserId);
    }

    [Fact]
    public async Task ReturnForReworkAsync_CreatesReworkTask()
    {
        var order = await CreateOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await _sut.ReturnForReworkAsync(order.Id, "Tehničke greške", "Komentar dorade");

        var reworkTask = await _db.TaskItems
            .FirstOrDefaultAsync(t => t.AppraisalOrderId == order.Id && t.TaskType == TaskItemType.ReworkAppraisal);
        Assert.NotNull(reworkTask);
        Assert.Contains("Dorada procjene", reworkTask!.Title);
    }

    [Fact]
    public async Task ReturnForReworkAsync_RecordsAuditEvent()
    {
        var order = await CreateOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await _sut.ReturnForReworkAsync(order.Id, "Tehničke greške", "Komentar dorade");

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.AppraisalReturnedForRework && e.EntityKey == order.Id.ToString()),
            Arg.Any<CancellationToken>());
    }

    // ── Sad path: ReturnForReworkAsync ───────────────────────────────────────

    [Fact]
    public async Task ReturnForReworkAsync_OrderNotFound_ThrowsNotFound()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.ReturnForReworkAsync(9999, "Cat", "Comment"));
        Assert.Equal("APPRAISAL_ORDER_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task ReturnForReworkAsync_WrongStatus_ThrowsConflict()
    {
        var order = await CreateOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.SubmittedBySales, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ReturnForReworkAsync(order.Id, "Cat", "Comment"));
        Assert.Equal("APPRAISAL_NOT_RECEIVED", ex.ErrorCode);
    }

    [Fact]
    public async Task ReturnForReworkAsync_DraftStatus_ThrowsConflict()
    {
        var order = await CreateOrderAsync();
        // order is still in Draft status

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ReturnForReworkAsync(order.Id, "Cat", "Comment"));
        Assert.Equal("APPRAISAL_NOT_RECEIVED", ex.ErrorCode);
    }

    // ── Auth edge cases ─────────────────────────────────────────────────────

    [Fact]
    public async Task ApproveFinalAppraisalAsync_NotAuthenticated_ThrowsForbidden()
    {
        _user.IsAuthenticated.Returns(false);
        _user.UserId.Returns((string?)null);

        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await Assert.ThrowsAsync<ForbiddenException>(() => _sut.ApproveFinalAppraisalAsync(order.Id, 5));
    }

    [Fact]
    public async Task ReturnForReworkAsync_NotAuthenticated_ThrowsForbidden()
    {
        _user.IsAuthenticated.Returns(false);
        _user.UserId.Returns((string?)null);

        var order = await CreateOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await Assert.ThrowsAsync<ForbiddenException>(
            () => _sut.ReturnForReworkAsync(order.Id, "Cat", "Comment"));
    }

    // ── ApproveFinalAppraisalAsync additional edge cases ─────────────────────

    [Fact]
    public async Task ApproveFinalAppraisalAsync_NoAppraiserRating_ThrowsConflict()
    {
        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: null));
        Assert.Equal("APPRAISER_RATING_REQUIRED", ex.ErrorCode);
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_CreatesConfirmOriginalReceivedTask()
    {
        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: 5);

        var confirmTask = await _db.TaskItems
            .FirstOrDefaultAsync(t => t.AppraisalOrderId == order.Id && t.TaskType == TaskItemType.ConfirmOriginalReceived);
        Assert.NotNull(confirmTask);
        Assert.Contains("Preuzimanje originala procjene", confirmTask!.Title);
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_CreatorWithoutUserId_NotificationNotSent()
    {
        var order = AppraisalOrder.Create(
            orderNumber:              $"2026/{Guid.NewGuid():N}".Substring(0, 12),
            title:                    "Procjena – Stan, Sarajevo",
            clientName:               "Petar Petrović",
            clientType:               "FL",
            clientIdentifier:         "0101985100123",
            contactName:              "Petar Petrović",
            contactPhone:             "061-123-456",
            contactEmail:             "petar@test.ba",
            city:                     "Sarajevo",
            branch:                   "POS_SARAJEVO_CENTAR",
            branchAddress:            "Titova 1",
            propertyAddress:          "Obala 1",
            collateralTypeId:         null,
            combinedCollateralTypeId: null,
            createdByUserId:          "  ",
            createdByRole:            "AM",
            createdByName:            "Amar Amarović",
            deliveryContactName:      "Amina Dostavljač",
            amRecipientName:          "Amar Primalac");
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, DateTime.UtcNow);
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var result = await _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: 5);

        Assert.False(result.NotificationSent);
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_NotificationThrows_StillSucceeds()
    {
        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        _notify.NotifyUserAsync(
                Arg.Any<string>(), Arg.Any<string>(), Arg.Any<string>(),
                Arg.Any<string?>(), Arg.Any<string?>(), Arg.Any<bool>(), Arg.Any<string?>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("notify down")));

        var result = await _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: 5);

        Assert.Equal("ReadyForProcedure", result.Status);
        Assert.False(result.NotificationSent);
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_AuditThrows_StillSucceeds()
    {
        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        _audit.RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("audit sink down")));

        var result = await _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: 5);

        Assert.Equal("ReadyForProcedure", result.Status);
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_SetsDownloadUrl()
    {
        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var result = await _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: 5);

        Assert.Equal($"/api/documents/{document.Id}/download", result.DownloadUrl);
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_SetsAppraiserRating()
    {
        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: 4);

        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        Assert.Equal(4, updated.AppraiserRating);
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_OrderWithAppraiser_NotifiesAppraiser()
    {
        var order = await CreateOrderAsync();
        // SelectAppraiser needs a valid pre-state — bypass via ChangeStatus, then call it
        order.ChangeStatus(AppraisalOrderStatus.DocumentationApproved, DateTime.UtcNow);
        order.SelectAppraiser(42, DateTime.UtcNow);  // → AppraiserSelected, sets AppraiserId = 42 ✓
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, DateTime.UtcNow);
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);  // → AppraisalReceived ✓
        await _db.SaveChangesAsync();

        await _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: 5);

        await _notify.Received(1).NotifyUserAsync(
            "42",
            Arg.Any<string>(),
            Arg.Any<string>(),
            Arg.Any<string?>(),
            Arg.Any<string?>(),
            Arg.Any<bool>(),
            Arg.Any<string?>(),
            Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task ApproveFinalAppraisalAsync_OrderWithNoAppraiser_DoesNotNotifyAppraiser()
    {
        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: 5);

        // Only one call for creator notification, not for appraiser
        await _notify.Received(1).NotifyUserAsync(
            Arg.Any<string>(),
            Arg.Any<string>(),
            Arg.Any<string>(),
            Arg.Any<string?>(),
            Arg.Any<string?>(),
            Arg.Any<bool>(),
            Arg.Any<string?>(),
            Arg.Any<CancellationToken>());
    }

    // ── ReturnForRework notification edge cases ─────────────────────────────

    [Fact]
    public async Task ReturnForReworkAsync_OrderWithNoAppraiser_NotificationNotSent()
    {
        var order = await CreateOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var result = await _sut.ReturnForReworkAsync(order.Id, "Cat", "Comment");

        Assert.False(result.NotificationSent);
    }

    [Fact]
    public async Task ReturnForReworkAsync_AuditThrows_StillSucceeds()
    {
        var order = await CreateOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        _audit.RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("audit sink down")));

        var result = await _sut.ReturnForReworkAsync(order.Id, "Cat", "Comment");

        Assert.Equal("AppraisalReturnedForRework", result.Status);
    }

    // ── GetFinalAppraisalAsync edge cases ────────────────────────────────────

    [Fact]
    public async Task GetFinalAppraisalAsync_NoLinkedDocument_FallsBackToCodebookLookup()
    {
        var order = await CreateOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var documentTypeId = await SeedFinalAppraisalDocumentTypeAsync();
        var document = await CreateDocumentAsync(order.Id, documentTypeId);

        var dto = await _sut.GetFinalAppraisalAsync(order.Id);

        Assert.Equal(document.Id, dto.DocumentId);
    }

    [Fact]
    public async Task GetFinalAppraisalAsync_NoDocument_ThrowsConflict()
    {
        var order = await CreateOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
        await _db.SaveChangesAsync();
        await SeedFinalAppraisalDocumentTypeAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.GetFinalAppraisalAsync(order.Id));
        Assert.Equal("FINAL_APPRAISAL_NOT_UPLOADED", ex.ErrorCode);
    }

    [Fact]
    public async Task GetFinalAppraisalAsync_DocumentTypeMissing_ThrowsNotFound()
    {
        var order = await CreateOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
        await _db.SaveChangesAsync();
        // No codebook value seeded

        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.GetFinalAppraisalAsync(order.Id));
        Assert.Equal("FINAL_APPRAISAL_DOCUMENT_TYPE_NOT_FOUND", ex.ErrorCode);
    }

    // ── AppraiserRating boundary tests (FAZA 1) ─────────────────────────────────

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(6)]
    public async Task ApproveFinalAppraisalAsync_InvalidRating_ThrowsConflict(int rating)
    {
        // Arrange
        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        // Act & Assert
        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: rating));
        Assert.Equal("APPRAISER_RATING_OUT_OF_RANGE", ex.ErrorCode);
    }

    [Theory]
    [InlineData(1)]
    [InlineData(3)]
    [InlineData(5)]
    public async Task ApproveFinalAppraisalAsync_ValidRating_Succeeds(int rating)
    {
        // Arrange
        var order = await CreateOrderAsync();
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        // Act
        var result = await _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: rating);

        // Assert
        Assert.Equal("ReadyForProcedure", result.Status);
        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        Assert.Equal(rating, updated.AppraiserRating);
    }

    // ── Four-eyes: CA who accepted cannot approve (FAZA 1) ───────────────────────

    [Fact]
    public async Task ApproveFinalAppraisalAsync_CAWhoAcceptedOrder_ThrowsFourEyesViolation()
    {
        // Arrange: create order and record that CA "user-co-1" accepted it
        var order = await CreateOrderAsync();
        // Simulate CA accepting the order (sets AcceptedByCAUserId)
        // CS0618: ChangeStatus used below to skip state machine for test setup
        order.ChangeStatus(AppraisalOrderStatus.SubmittedBySales, DateTime.UtcNow);
        order.AcceptByCA("user-co-1", "CO Korisnik", DateTime.UtcNow);  // → AcceptedByCA ✓
        // CS0618: bypass to AppraisalInProgress (valid pre-state for SetFinalAppraisalDocument)
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, DateTime.UtcNow);
        var document = await CreateDocumentAsync(order.Id);
        order.SetFinalAppraisalDocument(document.Id, DateTime.UtcNow);  // → AppraisalReceived ✓
        await _db.SaveChangesAsync();

        // user-co-1 is already set as current user (from constructor)
        // Act & Assert
        var ex = await Assert.ThrowsAsync<ForbiddenException>(
            () => _sut.ApproveFinalAppraisalAsync(order.Id, appraiserRating: 5));
        Assert.Equal("FOUR_EYES_VIOLATION", ex.ErrorCode);
    }

    public void Dispose() => _db.Dispose();
}
