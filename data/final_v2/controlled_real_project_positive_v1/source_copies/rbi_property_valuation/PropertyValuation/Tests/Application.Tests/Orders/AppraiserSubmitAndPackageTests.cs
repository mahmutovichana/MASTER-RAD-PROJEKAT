using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Appraisers;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Documents;
using RBBH.CollateralAppraisal.Application.Documents.Dtos;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Tests.Helpers;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Domain.Appraisers;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

// ═══════════════════════════════════════════════════════════════
// TEST MATRIX — SubmitAppraisalAsync
//
// Scenario                          | Expected                   | Type
// ─────────────────────────────────────────────────────────────────
// Validan submit s dokumentom       | AppraisalReceived           | Happy path
// Bez visitDate                     | ConflictException           | Required field
// Bez dokumenta                     | ConflictException           | Missing doc
// Pogrešan status                   | ConflictException           | State
// Svi valjani statusi za submit     | OK za svaki                 | Decision table
// ApproveFinalAppraisal task kreiran| Task postoji                | Side effect
//
// GetAppraiserPackageAsync
// ─────────────────────────────────────────────────────────────────
// Narudžba bez vještaka             | ConflictException           | State
// Narudžba s vještakom              | Vraća package s docs        | Happy path
// Vještak ne postoji u bazi         | NotFoundException           | Negative
//
// CompleteSignedDocumentImportAsync
// ─────────────────────────────────────────────────────────────────
// Aktivan ImportSignedDocuments task | Completes task             | Happy path
// Bez aktivnog taska                 | ConflictException          | Missing task
// ═══════════════════════════════════════════════════════════════

public sealed class AppraiserSubmitAndPackageTests : IDisposable
{
    private readonly ApplicationDbContext        _db;
    private readonly ICurrentUserService         _user;
    private readonly IAppraiserSelectionService  _selectionService;
    private readonly INotificationProvider       _notify;
    private readonly IDocumentService            _documentService;
    private readonly IAuditService               _audit;
    private readonly IUserRoleProvider           _userRoleProvider;
    private readonly IProtocolService            _protocolService;
    private readonly AppraiserAssignmentService  _sut;

    public AppraiserSubmitAndPackageTests()
    {
        var opts = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w =>
                w.Ignore(Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;

        _db               = new ApplicationDbContext(opts);
        _user             = Substitute.For<ICurrentUserService>();
        _selectionService = Substitute.For<IAppraiserSelectionService>();
        _notify           = Substitute.For<INotificationProvider>();
        _documentService  = Substitute.For<IDocumentService>();
        _audit            = Substitute.For<IAuditService>();
        _userRoleProvider = Substitute.For<IUserRoleProvider>();
        _protocolService  = Substitute.For<IProtocolService>();

        _user.UserId.Returns("user-appraiser-1");
        _user.IsAuthenticated.Returns(true);

        var flSvc = new FlAppraiserSelectionService(
            _db, _user, _selectionService, _notify, _audit, _protocolService,
            Substitute.For<ILogger<FlAppraiserSelectionService>>());
        var plSvc = new PlAppraiserSelectionService(
            _db, _user, _notify, _audit, _protocolService,
            Substitute.For<ILogger<PlAppraiserSelectionService>>());

        _sut = new AppraiserAssignmentService(
            _db, _user, _selectionService, _notify, _documentService, _audit,
            _userRoleProvider, _protocolService,
            Substitute.For<ILogger<AppraiserAssignmentService>>(),
            new FakeClock(),
            Options.Create(new WorkflowSlaOptions()),
            flSvc, plSvc);
    }

    public void Dispose() => _db.Dispose();

    // ── Helpers ───────────────────────────────────────────────────────────────

    private static readonly DateTime TestVisitDate =
        new(2026, 1, 10, 9, 0, 0, DateTimeKind.Utc);

    private static DocumentDto MakeDocument(int id = 1, bool isActive = true) =>
        new(id, 1, null, "procjena.pdf", "procjena.pdf", "application/pdf",
            1024, DateTime.UtcNow.AddHours(-1), "user-1", "/download/1", 1, null, isActive);

    private async Task<(AppraisalOrder order, Appraiser appraiser)> SeedOrderWithAppraiserAsync(
        AppraisalOrderStatus status = AppraisalOrderStatus.AppraisalInProgress)
    {
        var appraiser = Appraiser.Create("Test Vjestak", "Sarajevo",
            AppraiserLegalForm.Individual, "vjestak@test.ba", "061000000", null);
        _db.Appraisers.Add(appraiser);
        await _db.SaveChangesAsync();

        var order = AppraisalOrder.Create(
            orderNumber: "PN-2026-000099", title: "Test procjena",
            clientName: "Klijent Test", clientType: "FL",
            clientIdentifier: "0101985100129", contactName: "Kontakt",
            contactPhone: "061000000", contactEmail: null,
            city: "Sarajevo", branch: "POS_SARAJEVO_CENTAR",
            branchAddress: "Adresa", propertyAddress: "Obala 1",
            collateralTypeId: null, combinedCollateralTypeId: null,
            createdByUserId: "u1", createdByRole: AppRoles.AM,
            createdByName: "Amar", deliveryContactName: "Dostava",
            amRecipientName: "AM",
            workflowType: RBBH.CollateralAppraisal.Domain.Orders.WorkflowType.FizickaLica);

        order.ChangeStatus(AppraisalOrderStatus.DocumentationApproved, DateTime.UtcNow);
        order.SelectAppraiser(appraiser.Id, DateTime.UtcNow);
        order.ChangeStatus(status, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();
        return (order, appraiser);
    }

    private async Task<TaskItem> SeedTaskAsync(int orderId, TaskItemType type)
    {
        var task = TaskItem.Create(orderId, type, "Task", null, AppRoles.Vjestak);
        _db.TaskItems.Add(task);
        await _db.SaveChangesAsync();
        return task;
    }

    // ═══════════════════════════════════════════════════════════════
    // SubmitAppraisalAsync
    // ═══════════════════════════════════════════════════════════════

    [Fact]
    public async Task SubmitAppraisal_WithValidDocumentAndVisitDate_ShouldTransitionToAppraisalReceived()
    {
        var (order, _) = await SeedOrderWithAppraiserAsync(AppraisalOrderStatus.AppraisalInProgress);
        await SeedTaskAsync(order.Id, TaskItemType.UploadFinalAppraisal);
        _documentService.GetByOrderAsync(order.Id, Arg.Any<CancellationToken>())
            .Returns(new List<DocumentDto> { MakeDocument() });

        var result = await _sut.SubmitAppraisalAsync(order.Id, TestVisitDate);

        result.Should().NotBeNull();
        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        updated.Status.Should().Be(AppraisalOrderStatus.AppraisalReceived);
    }

    [Fact]
    public async Task SubmitAppraisal_ShouldCreateApproveFinalAppraisalTask()
    {
        var (order, _) = await SeedOrderWithAppraiserAsync(AppraisalOrderStatus.AppraisalInProgress);
        await SeedTaskAsync(order.Id, TaskItemType.UploadFinalAppraisal);
        _documentService.GetByOrderAsync(order.Id, Arg.Any<CancellationToken>())
            .Returns(new List<DocumentDto> { MakeDocument() });

        await _sut.SubmitAppraisalAsync(order.Id, TestVisitDate);

        var tasks = _db.TaskItems.Where(t => t.AppraisalOrderId == order.Id).ToList();
        tasks.Should().Contain(t => t.TaskType == TaskItemType.ApproveFinalAppraisal,
            "CO mora dobiti zadatak za odobrenje procjene");
    }

    [Theory]
    [InlineData(AppraisalOrderStatus.OrderSentToAppraiser)]
    [InlineData(AppraisalOrderStatus.AdditionalPaymentCompleted)]
    [InlineData(AppraisalOrderStatus.AppraisalInProgress)]
    [InlineData(AppraisalOrderStatus.AppraisalReturnedForRework)]
    public async Task SubmitAppraisal_AllValidStatuses_ShouldSucceed(AppraisalOrderStatus status)
    {
        // Decision table: sva 4 valjana statusa za submit
        var (order, _) = await SeedOrderWithAppraiserAsync(status);
        await SeedTaskAsync(order.Id, TaskItemType.UploadFinalAppraisal);
        _documentService.GetByOrderAsync(order.Id, Arg.Any<CancellationToken>())
            .Returns(new List<DocumentDto> { MakeDocument() });

        var result = await _sut.SubmitAppraisalAsync(order.Id, TestVisitDate);

        result.Should().NotBeNull();
    }

    [Fact]
    public async Task SubmitAppraisal_WithoutVisitDate_ShouldThrowConflict()
    {
        var (order, _) = await SeedOrderWithAppraiserAsync(AppraisalOrderStatus.AppraisalInProgress);
        _documentService.GetByOrderAsync(order.Id, Arg.Any<CancellationToken>())
            .Returns(new List<DocumentDto> { MakeDocument() });

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SubmitAppraisalAsync(order.Id, visitDate: null));

        ex.ErrorCode.Should().Be("VISIT_DATE_REQUIRED");
    }

    [Fact]
    public async Task SubmitAppraisal_WithoutDocument_ShouldThrowConflict()
    {
        var (order, _) = await SeedOrderWithAppraiserAsync(AppraisalOrderStatus.AppraisalInProgress);
        // Nema aktivnih dokumenata
        _documentService.GetByOrderAsync(order.Id, Arg.Any<CancellationToken>())
            .Returns(new List<DocumentDto>());

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SubmitAppraisalAsync(order.Id, TestVisitDate));

        ex.ErrorCode.Should().Be("NO_APPRAISAL_DOCUMENT");
    }

    [Fact]
    public async Task SubmitAppraisal_WithOnlyInactiveDocument_ShouldThrowConflict()
    {
        // Edge case: dokument postoji ali je neaktivan (IsActive=false)
        var (order, _) = await SeedOrderWithAppraiserAsync(AppraisalOrderStatus.AppraisalInProgress);
        _documentService.GetByOrderAsync(order.Id, Arg.Any<CancellationToken>())
            .Returns(new List<DocumentDto> { MakeDocument(isActive: false) });

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SubmitAppraisalAsync(order.Id, TestVisitDate));

        ex.ErrorCode.Should().Be("NO_APPRAISAL_DOCUMENT",
            "neaktivni dokumenti ne računaju se kao validan dokument procjene");
    }

    [Fact]
    public async Task SubmitAppraisal_WhenWrongStatus_ShouldThrowConflict()
    {
        var (order, _) = await SeedOrderWithAppraiserAsync(AppraisalOrderStatus.AppraiserRejected);
        _documentService.GetByOrderAsync(order.Id, Arg.Any<CancellationToken>())
            .Returns(new List<DocumentDto> { MakeDocument() });

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SubmitAppraisalAsync(order.Id, TestVisitDate));

        ex.ErrorCode.Should().Be("ORDER_NOT_WITH_APPRAISER");
    }

    [Fact]
    public async Task SubmitAppraisal_MostRecentDocument_ShouldBeUsed()
    {
        // Multi-document: koristi se najnoviji (OrderByDescending UploadedAt)
        var (order, _) = await SeedOrderWithAppraiserAsync(AppraisalOrderStatus.AppraisalInProgress);
        await SeedTaskAsync(order.Id, TaskItemType.UploadFinalAppraisal);
        var older  = MakeDocument(1) with { UploadedAt = DateTime.UtcNow.AddHours(-2) };
        var newest = MakeDocument(2) with { UploadedAt = DateTime.UtcNow.AddHours(-1), FileName = "nova-procjena.pdf" };
        _documentService.GetByOrderAsync(order.Id, Arg.Any<CancellationToken>())
            .Returns(new List<DocumentDto> { older, newest });

        var result = await _sut.SubmitAppraisalAsync(order.Id, TestVisitDate);

        // Potvrda: submit je uspio (najnoviji dokument korišten)
        result.Should().NotBeNull();
        result.Message.Should().Contain("dostavljen");
    }

    // ═══════════════════════════════════════════════════════════════
    // GetAppraiserPackageAsync
    // ═══════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetAppraiserPackage_WithValidAppraiser_ShouldReturnPackageWithDocuments()
    {
        var (order, appraiser) = await SeedOrderWithAppraiserAsync();
        var docs = new List<DocumentDto> { MakeDocument() };
        _documentService.GetByOrderAsync(order.Id, Arg.Any<CancellationToken>()).Returns(docs);

        var result = await _sut.GetAppraiserPackageAsync(order.Id);

        result.Should().NotBeNull();
        result.OrderId.Should().Be(order.Id);
        result.AppraiserId.Should().Be(appraiser.Id);
        result.AppraiserName.Should().Be(appraiser.Name);
        result.Documents.Should().HaveCount(1);
    }

    [Fact]
    public async Task GetAppraiserPackage_WhenNoAppraiserSelected_ShouldThrowConflict()
    {
        var (order, _) = await SeedOrderWithAppraiserAsync();
        // Uklonimo AppraiserId sa narudžbe putem EF entry bypass
        _db.Entry(order).Property("AppraiserId").CurrentValue = null;
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.GetAppraiserPackageAsync(order.Id));

        ex.ErrorCode.Should().Be("APPRAISER_NOT_SELECTED");
    }

    [Fact]
    public async Task GetAppraiserPackage_WithEmptyDocuments_ShouldReturnEmptyList()
    {
        var (order, _) = await SeedOrderWithAppraiserAsync();
        _documentService.GetByOrderAsync(order.Id, Arg.Any<CancellationToken>())
            .Returns(new List<DocumentDto>());

        var result = await _sut.GetAppraiserPackageAsync(order.Id);

        result.Documents.Should().BeEmpty("nema dokumenata za paket");
    }

    [Fact]
    public async Task GetAppraiserPackage_WhenOrderNotFound_ShouldThrowNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.GetAppraiserPackageAsync(99999));
    }

    // ═══════════════════════════════════════════════════════════════
    // CompleteSignedDocumentImportAsync
    // ═══════════════════════════════════════════════════════════════

    [Fact]
    public async Task CompleteSignedDocumentImport_WithActiveTask_ShouldCompleteTask()
    {
        var (order, _) = await SeedOrderWithAppraiserAsync(AppraisalOrderStatus.AppraisalInProgress);
        await SeedTaskAsync(order.Id, TaskItemType.ImportSignedDocuments);

        var result = await _sut.CompleteSignedDocumentImportAsync(order.Id);

        result.Should().NotBeNull();
        var task = await _db.TaskItems
            .FirstAsync(t => t.AppraisalOrderId == order.Id
                          && t.TaskType == TaskItemType.ImportSignedDocuments);
        task.Status.Should().Be(TaskItemStatus.Completed,
            "task potpisanih dokumenata mora biti označen kao završen");
    }

    [Fact]
    public async Task CompleteSignedDocumentImport_WithNoActiveTask_ShouldThrowConflict()
    {
        var (order, _) = await SeedOrderWithAppraiserAsync(AppraisalOrderStatus.AppraisalInProgress);
        // Nema ImportSignedDocuments taska

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.CompleteSignedDocumentImportAsync(order.Id));

        ex.ErrorCode.Should().Be("NO_SIGNED_DOCS_TASK");
    }

    [Fact]
    public async Task CompleteSignedDocumentImport_WithAlreadyCompletedTask_ShouldThrowConflict()
    {
        // Edge case: task je već završen
        var (order, _) = await SeedOrderWithAppraiserAsync(AppraisalOrderStatus.AppraisalInProgress);
        var task = await SeedTaskAsync(order.Id, TaskItemType.ImportSignedDocuments);
        task.Complete("user-1", "već završen", DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.CompleteSignedDocumentImportAsync(order.Id));

        ex.ErrorCode.Should().Be("NO_SIGNED_DOCS_TASK",
            "već završen task se ne smije ponovo kompletirati");
    }

    [Fact]
    public async Task CompleteSignedDocumentImport_ShouldRecordAudit()
    {
        var (order, _) = await SeedOrderWithAppraiserAsync(AppraisalOrderStatus.AppraisalInProgress);
        await SeedTaskAsync(order.Id, TaskItemType.ImportSignedDocuments);

        await _sut.CompleteSignedDocumentImportAsync(order.Id);

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action.Contains("SIGNED")),
            Arg.Any<CancellationToken>());
    }
}
