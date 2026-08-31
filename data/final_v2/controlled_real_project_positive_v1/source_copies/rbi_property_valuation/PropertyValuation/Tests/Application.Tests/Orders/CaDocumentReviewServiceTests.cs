// CS0618: AppraisalOrder.ChangeStatus() is marked [Obsolete] in production code.
// In tests, deliberately using this method to bypass the state machine and set up
// arbitrary order states for test scenarios — this is intentional and acceptable.
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

public sealed class CaDocumentReviewServiceTests : IDisposable
{
    private readonly ApplicationDbContext       _db;
    private readonly ICurrentUserService        _user;
    private readonly IAuditService              _audit;
    private readonly INotificationProvider      _notify;
    private readonly CaDocumentReviewService    _sut;

    private int _reasonCodeId;

    public CaDocumentReviewServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;

        _db     = new ApplicationDbContext(options);
        _user   = Substitute.For<ICurrentUserService>();
        _audit  = Substitute.For<IAuditService>();
        _notify = Substitute.For<INotificationProvider>();

        _user.UserId.Returns("user-ca-1");
        _user.IsAuthenticated.Returns(true);

        _sut = new CaDocumentReviewService(
            _db,
            _user,
            _notify,
            _audit,
            Substitute.For<ILogger<CaDocumentReviewService>>());

        SeedReasonCodebook();
    }

    private void SeedReasonCodebook()
    {
        var reason = CodebookValue.Create(
            "razlozi_dopune_dokumentacije",
            "NEDOSTAJE_DOK",
            "Nedostaje dokumentacija",
            null, 1, "system-seed");
        _db.CodebookValues.Add(reason);
        _db.SaveChanges();
        _reasonCodeId = reason.Id;
    }

    // ── Helper: create order in a given status ────────────────────────────────

    private async Task<AppraisalOrder> CreateOrderAsync(
        AppraisalOrderStatus status = AppraisalOrderStatus.DocumentationReviewInProgress,
        string createdBy = "user-am-1")
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
            createdByUserId:          createdBy,
            createdByRole:            AppRoles.AM,
            createdByName:            "Amar Amarović",
            deliveryContactName:      "Amina Dostavljač",
            amRecipientName:          "Amar Primalac");

        // CS0618: deliberate state machine bypass for test setup
        order.ChangeStatus(status, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();
        return order;
    }

    private async Task<TaskItem> AddActiveTaskAsync(int orderId, TaskItemType type)
    {
        var task = TaskItem.Create(orderId, type, $"Task {type}", null, AppRoles.KolateralAdministrator);
        _db.TaskItems.Add(task);
        await _db.SaveChangesAsync();
        return task;
    }

    // ── RequestCorrectionAsync — happy path ───────────────────────────────────

    [Fact]
    public async Task RequestCorrectionAsync_ValidStatus_TransitionsToReturnedForCorrection()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.DocumentationReviewInProgress);
        await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        var result = await _sut.RequestCorrectionAsync(order.Id, _reasonCodeId, "komentar");

        Assert.Equal("ReturnedForCorrection", result.Status);
        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        Assert.Equal(AppraisalOrderStatus.ReturnedForCorrection, updated.Status);
    }

    [Fact]
    public async Task RequestCorrectionAsync_FromCorrectionSubmitted_TransitionsToReturnedForCorrection()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.CorrectionSubmitted);
        await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        var result = await _sut.RequestCorrectionAsync(order.Id, _reasonCodeId, null);

        Assert.Equal("ReturnedForCorrection", result.Status);
    }

    [Fact]
    public async Task RequestCorrectionAsync_FromAccessCheckRejected_TransitionsToReturnedForCorrection()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.AccessCheckRejected);
        await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        var result = await _sut.RequestCorrectionAsync(order.Id, _reasonCodeId, "razlog");

        Assert.Equal("ReturnedForCorrection", result.Status);
    }

    [Fact]
    public async Task RequestCorrectionAsync_CompletesReviewTask()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.DocumentationReviewInProgress);
        var task  = await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        await _sut.RequestCorrectionAsync(order.Id, _reasonCodeId, "komentar");

        var updatedTask = await _db.TaskItems.FirstAsync(t => t.Id == task.Id);
        Assert.Equal(TaskItemStatus.Completed, updatedTask.Status);
        Assert.Equal("user-ca-1", updatedTask.CompletedByUserId);
    }

    [Fact]
    public async Task RequestCorrectionAsync_CreatesCorrectDocumentationTask()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.DocumentationReviewInProgress);
        await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        await _sut.RequestCorrectionAsync(order.Id, _reasonCodeId, "komentar");

        var correctTask = await _db.TaskItems
            .FirstOrDefaultAsync(t => t.AppraisalOrderId == order.Id
                                   && t.TaskType == TaskItemType.CorrectDocumentation);
        Assert.NotNull(correctTask);
        Assert.Contains("Dopuna podataka", correctTask!.Title);
    }

    [Fact]
    public async Task RequestCorrectionAsync_RecordsAuditEvent()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.DocumentationReviewInProgress);
        await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        await _sut.RequestCorrectionAsync(order.Id, _reasonCodeId, null);

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.OrderReturnedForCorrection
                                 && e.EntityKey == order.Id.ToString()),
            Arg.Any<CancellationToken>());
    }

    // ── RequestCorrectionAsync — sad path ─────────────────────────────────────

    [Fact]
    public async Task RequestCorrectionAsync_NotAuthenticated_ThrowsForbidden()
    {
        _user.IsAuthenticated.Returns(false);
        _user.UserId.Returns((string?)null);

        var order = await CreateOrderAsync(AppraisalOrderStatus.DocumentationReviewInProgress);
        await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        await Assert.ThrowsAsync<ForbiddenException>(
            () => _sut.RequestCorrectionAsync(order.Id, _reasonCodeId, null));
    }

    [Theory]
    [InlineData(AppraisalOrderStatus.Draft)]
    [InlineData(AppraisalOrderStatus.SubmittedBySales)]
    [InlineData(AppraisalOrderStatus.AcceptedByCA)]
    [InlineData(AppraisalOrderStatus.ReturnedForCorrection)]
    [InlineData(AppraisalOrderStatus.Completed)]
    public async Task RequestCorrectionAsync_InvalidStatus_ThrowsConflict(AppraisalOrderStatus status)
    {
        var order = await CreateOrderAsync(status);
        await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.RequestCorrectionAsync(order.Id, _reasonCodeId, null));
        Assert.Equal("REVIEW_INVALID_STATUS", ex.ErrorCode);
    }

    [Fact]
    public async Task RequestCorrectionAsync_NoActiveReviewTask_ThrowsConflict()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.DocumentationReviewInProgress);
        // No ReviewDocumentation task seeded

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.RequestCorrectionAsync(order.Id, _reasonCodeId, null));
        Assert.Equal("REVIEW_TASK_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task RequestCorrectionAsync_InvalidReasonCodeId_ThrowsNotFound()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.DocumentationReviewInProgress);
        await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.RequestCorrectionAsync(order.Id, 99999, null));
        Assert.Equal("CORRECTION_REASON_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task RequestCorrectionAsync_OrderNotFound_ThrowsNotFound()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.RequestCorrectionAsync(9999, _reasonCodeId, null));
        Assert.Equal("APPRAISAL_ORDER_NOT_FOUND", ex.ErrorCode);
    }

    // ── SubmitCorrectionAsync — happy path ────────────────────────────────────

    [Fact]
    public async Task SubmitCorrectionAsync_ValidStatus_TransitionsToCorrectionSubmitted()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.ReturnedForCorrection);
        await AddActiveTaskAsync(order.Id, TaskItemType.CorrectDocumentation);

        var result = await _sut.SubmitCorrectionAsync(order.Id, "Dopunom je dodat dokument");

        Assert.Equal("CorrectionSubmitted", result.Status);
        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        Assert.Equal(AppraisalOrderStatus.CorrectionSubmitted, updated.Status);
    }

    [Fact]
    public async Task SubmitCorrectionAsync_CompletesCorrectDocumentationTask()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.ReturnedForCorrection);
        var task  = await AddActiveTaskAsync(order.Id, TaskItemType.CorrectDocumentation);

        await _sut.SubmitCorrectionAsync(order.Id, "komentar");

        var updatedTask = await _db.TaskItems.FirstAsync(t => t.Id == task.Id);
        Assert.Equal(TaskItemStatus.Completed, updatedTask.Status);
        Assert.Equal("user-ca-1", updatedTask.CompletedByUserId);
    }

    [Fact]
    public async Task SubmitCorrectionAsync_CreatesNewReviewDocumentationTask()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.ReturnedForCorrection);
        await AddActiveTaskAsync(order.Id, TaskItemType.CorrectDocumentation);

        await _sut.SubmitCorrectionAsync(order.Id, null);

        var reviewTask = await _db.TaskItems
            .FirstOrDefaultAsync(t => t.AppraisalOrderId == order.Id
                                   && t.TaskType == TaskItemType.ReviewDocumentation);
        Assert.NotNull(reviewTask);
        Assert.Contains("Pregled dokumentacije", reviewTask!.Title);
    }

    [Fact]
    public async Task SubmitCorrectionAsync_RecordsAuditEvent()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.ReturnedForCorrection);
        await AddActiveTaskAsync(order.Id, TaskItemType.CorrectDocumentation);

        await _sut.SubmitCorrectionAsync(order.Id, "komentar");

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.OrderCorrectionSubmitted
                                 && e.EntityKey == order.Id.ToString()),
            Arg.Any<CancellationToken>());
    }

    // ── SubmitCorrectionAsync — sad path ──────────────────────────────────────

    [Fact]
    public async Task SubmitCorrectionAsync_NotAuthenticated_ThrowsForbidden()
    {
        _user.IsAuthenticated.Returns(false);
        _user.UserId.Returns((string?)null);

        var order = await CreateOrderAsync(AppraisalOrderStatus.ReturnedForCorrection);
        await AddActiveTaskAsync(order.Id, TaskItemType.CorrectDocumentation);

        await Assert.ThrowsAsync<ForbiddenException>(
            () => _sut.SubmitCorrectionAsync(order.Id, null));
    }

    [Theory]
    [InlineData(AppraisalOrderStatus.Draft)]
    [InlineData(AppraisalOrderStatus.DocumentationReviewInProgress)]
    [InlineData(AppraisalOrderStatus.CorrectionSubmitted)]
    [InlineData(AppraisalOrderStatus.Completed)]
    public async Task SubmitCorrectionAsync_InvalidStatus_ThrowsConflict(AppraisalOrderStatus status)
    {
        var order = await CreateOrderAsync(status);
        await AddActiveTaskAsync(order.Id, TaskItemType.CorrectDocumentation);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SubmitCorrectionAsync(order.Id, null));
        Assert.Equal("CORRECTION_INVALID_STATUS", ex.ErrorCode);
    }

    [Fact]
    public async Task SubmitCorrectionAsync_NoActiveCorrectDocumentationTask_ThrowsConflict()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.ReturnedForCorrection);
        // No CorrectDocumentation task seeded

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SubmitCorrectionAsync(order.Id, null));
        Assert.Equal("CORRECTION_TASK_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task SubmitCorrectionAsync_OrderNotFound_ThrowsNotFound()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.SubmitCorrectionAsync(9999, null));
        Assert.Equal("APPRAISAL_ORDER_NOT_FOUND", ex.ErrorCode);
    }

    // ── CompleteReviewAsync — happy path (apartment-only collateral) ───────────

    [Fact]
    public async Task CompleteReviewAsync_ApartmentCollateral_TransitionsToDocumentationApproved()
    {
        // Seed apartment codebook value
        var apartmentType = CodebookValue.Create(
            "tipovi_kolaterala", "APP_STAN", "Stan", null, 5, "seed");
        _db.CodebookValues.Add(apartmentType);
        await _db.SaveChangesAsync();

        // Create order with apartment-only collateral (no combined type)
        var order = AppraisalOrder.Create(
            orderNumber:              $"2026/{Guid.NewGuid():N}".Substring(0, 12),
            title:                    "Stan – Sarajevo",
            clientName:               "Test Klijent",
            clientType:               "FL",
            clientIdentifier:         "0101985100123",
            contactName:              null,
            contactPhone:             null,
            contactEmail:             null,
            city:                     "Sarajevo",
            branch:                   "POS",
            branchAddress:            null,
            propertyAddress:          "Obala 1",
            collateralTypeId:         apartmentType.Id,
            combinedCollateralTypeId: null,
            createdByUserId:          "user-am-1",
            createdByRole:            AppRoles.AM,
            createdByName:            null,
            deliveryContactName:      null,
            amRecipientName:          null);

        // CS0618: deliberate state machine bypass for test setup
        order.ChangeStatus(AppraisalOrderStatus.DocumentationReviewInProgress, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        var result = await _sut.CompleteReviewAsync(order.Id);

        Assert.Equal("DocumentationApproved", result.Status);
        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        Assert.Equal(AppraisalOrderStatus.DocumentationApproved, updated.Status);
    }

    [Fact]
    public async Task CompleteReviewAsync_NonApartmentCollateral_TransitionsToAccessCheckRequested()
    {
        // No collateral type seeded — CollateralTypeId is null → not apartment-only
        var order = await CreateOrderAsync(AppraisalOrderStatus.DocumentationReviewInProgress);
        await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        var result = await _sut.CompleteReviewAsync(order.Id);

        // Without a collateral type set, IsApartmentOnlyAsync returns false → AccessCheckRequested
        Assert.Equal("AccessCheckRequested", result.Status);
        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        Assert.Equal(AppraisalOrderStatus.AccessCheckRequested, updated.Status);
    }

    [Fact]
    public async Task CompleteReviewAsync_CompletesReviewTask()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.DocumentationReviewInProgress);
        var task  = await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        await _sut.CompleteReviewAsync(order.Id);

        var updatedTask = await _db.TaskItems.FirstAsync(t => t.Id == task.Id);
        Assert.Equal(TaskItemStatus.Completed, updatedTask.Status);
        Assert.Equal("user-ca-1", updatedTask.CompletedByUserId);
    }

    [Fact]
    public async Task CompleteReviewAsync_RecordsAuditEvent()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.DocumentationReviewInProgress);
        await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        await _sut.CompleteReviewAsync(order.Id);

        await _audit.Received().RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.OrderReviewCompleted
                                 && e.EntityKey == order.Id.ToString()),
            Arg.Any<CancellationToken>());
    }

    // ── CompleteReviewAsync — sad path ────────────────────────────────────────

    [Fact]
    public async Task CompleteReviewAsync_NotAuthenticated_ThrowsForbidden()
    {
        _user.IsAuthenticated.Returns(false);
        _user.UserId.Returns((string?)null);

        var order = await CreateOrderAsync(AppraisalOrderStatus.DocumentationReviewInProgress);
        await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        await Assert.ThrowsAsync<ForbiddenException>(
            () => _sut.CompleteReviewAsync(order.Id));
    }

    [Theory]
    [InlineData(AppraisalOrderStatus.Draft)]
    [InlineData(AppraisalOrderStatus.ReturnedForCorrection)]
    [InlineData(AppraisalOrderStatus.DocumentationApproved)]
    [InlineData(AppraisalOrderStatus.Completed)]
    public async Task CompleteReviewAsync_InvalidStatus_ThrowsConflict(AppraisalOrderStatus status)
    {
        var order = await CreateOrderAsync(status);
        await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.CompleteReviewAsync(order.Id));
        Assert.Equal("REVIEW_INVALID_STATUS", ex.ErrorCode);
    }

    [Fact]
    public async Task CompleteReviewAsync_NoActiveReviewTask_ThrowsConflict()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.DocumentationReviewInProgress);
        // No ReviewDocumentation task seeded

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.CompleteReviewAsync(order.Id));
        Assert.Equal("REVIEW_TASK_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task CompleteReviewAsync_OrderNotFound_ThrowsNotFound()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.CompleteReviewAsync(9999));
        Assert.Equal("APPRAISAL_ORDER_NOT_FOUND", ex.ErrorCode);
    }

    // ── Audit resilience ──────────────────────────────────────────────────────

    [Fact]
    public async Task RequestCorrectionAsync_AuditThrows_StillSucceeds()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.DocumentationReviewInProgress);
        await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        _audit.RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("audit down")));

        var result = await _sut.RequestCorrectionAsync(order.Id, _reasonCodeId, null);

        Assert.Equal("ReturnedForCorrection", result.Status);
    }

    [Fact]
    public async Task SubmitCorrectionAsync_AuditThrows_StillSucceeds()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.ReturnedForCorrection);
        await AddActiveTaskAsync(order.Id, TaskItemType.CorrectDocumentation);

        _audit.RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("audit down")));

        var result = await _sut.SubmitCorrectionAsync(order.Id, null);

        Assert.Equal("CorrectionSubmitted", result.Status);
    }

    // ── Dodatni testovi za coverage gapove ────────────────────────────────────

    [Fact]
    public async Task RequestCorrection_WhenWrongStatus_ShouldThrowConflict()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.Draft);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.RequestCorrectionAsync(order.Id, 1, null));

        Assert.Equal("REVIEW_INVALID_STATUS", ex.ErrorCode);
    }

    [Fact]
    public async Task RequestCorrection_WhenReasonCodeNotFound_ShouldThrowNotFound()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.DocumentationReviewInProgress);
        await AddActiveTaskAsync(order.Id, TaskItemType.ReviewDocumentation);

        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.RequestCorrectionAsync(order.Id, 9999, null));

        Assert.Equal("CORRECTION_REASON_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task RequestCorrection_WhenNoReviewTask_ShouldThrowConflict()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.DocumentationReviewInProgress);
        var cv = CodebookValue.Create(
            "razlozi_dopune_dokumentacije", "GRESKA", "Greška u dokumentima", null, 1, "system");
        _db.CodebookValues.Add(cv);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.RequestCorrectionAsync(order.Id, cv.Id, null));

        Assert.Equal("REVIEW_TASK_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task CompleteReview_WhenWrongStatus_ShouldThrowConflict()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.Draft);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.CompleteReviewAsync(order.Id));

        Assert.Equal("REVIEW_INVALID_STATUS", ex.ErrorCode);
    }

    [Fact]
    public async Task CompleteReview_WhenNoTask_ShouldThrowConflict()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.DocumentationReviewInProgress);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.CompleteReviewAsync(order.Id));

        Assert.Equal("REVIEW_TASK_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task SubmitCorrection_WhenWrongStatus_ShouldThrowConflict()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.Draft);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SubmitCorrectionAsync(order.Id, null));

        Assert.Equal("CORRECTION_INVALID_STATUS", ex.ErrorCode);
    }

    [Fact]
    public async Task SubmitCorrection_WhenNoTask_ShouldThrowConflict()
    {
        var order = await CreateOrderAsync(AppraisalOrderStatus.ReturnedForCorrection);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SubmitCorrectionAsync(order.Id, null));

        Assert.Equal("CORRECTION_TASK_NOT_FOUND", ex.ErrorCode);
    }

    public void Dispose() => _db.Dispose();
}
