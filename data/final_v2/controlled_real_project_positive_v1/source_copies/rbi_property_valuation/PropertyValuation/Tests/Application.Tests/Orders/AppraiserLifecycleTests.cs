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
// TEST MATRIX — AppraiserAssignmentService lifecycle metode
//
// AcceptByAppraiserAsync
// ─────────────────────────────────────────────────────────────
// Validan status OrderSentToAppraiser      → AppraiserInProgress
// Pogrešan status (Draft)                  → ConflictException
//
// RejectByAppraiserAsync
// ─────────────────────────────────────────────────────────────
// Validan status, sa razlogom              → AppraiserRejected
// Bez dodijeljenog vještaka                → ConflictException
// Pogrešan status (Draft)                  → ConflictException
// OrderDeclinedAppraiser se kreira         → Side-effect
//
// RejectOrderAsync (CA/CO admin reject)
// ─────────────────────────────────────────────────────────────
// AppraisalInProgress → AppraiserRejected  → Sada validan (state machine fix)
//
// RequestAdditionalPaymentAsync
// ─────────────────────────────────────────────────────────────
// Validan status AppraisalInProgress       → AdditionalPaymentRequested
// Validan status OrderSentToAppraiser      → AdditionalPaymentRequested
// Pogrešan status                          → ConflictException
// Bez vještaka                             → ConflictException
//
// ConfirmAdditionalPaymentAsync
// ─────────────────────────────────────────────────────────────
// Validan status AdditionalPaymentRequested → AdditionalPaymentCompleted
// Pogrešan status                           → ConflictException
// Vještak ne postoji                        → NotFoundException
// ═══════════════════════════════════════════════════════════════

public sealed class AppraiserLifecycleTests : IDisposable
{
    private readonly ApplicationDbContext         _db;
    private readonly ICurrentUserService          _user;
    private readonly IAppraiserSelectionService   _selectionService;
    private readonly INotificationProvider        _notify;
    private readonly IDocumentService             _documentService;
    private readonly IAuditService                _audit;
    private readonly IUserRoleProvider            _userRoleProvider;
    private readonly IProtocolService             _protocolService;
    private readonly AppraiserAssignmentService   _sut;

    public AppraiserLifecycleTests()
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

    // ── Test Data Builders ────────────────────────────────────────────────────

    private async Task<(AppraisalOrder order, Appraiser appraiser)> SeedOrderSentToAppraiserAsync()
    {
        // FL narudžba u stanju "Poslana vještaku" s dodijeljenim vještakom
        var order = AppraisalOrder.Create(
            orderNumber: $"PN-2026-{Guid.NewGuid():N}".Substring(0, 16),
            title: "Stan FL test", clientName: "Petar Petrovic",
            clientType: "FL", clientIdentifier: "0101985100129",
            contactName: "Kontakt", contactPhone: "061123456", contactEmail: null,
            city: "Sarajevo", branch: "POS_SARAJEVO_CENTAR", branchAddress: "Adresa",
            propertyAddress: "Obala 1", collateralTypeId: null, combinedCollateralTypeId: null,
            createdByUserId: "u1", createdByRole: AppRoles.AM, createdByName: "Amar",
            deliveryContactName: "Dostava", amRecipientName: "AM",
            workflowType: RBBH.CollateralAppraisal.Domain.Orders.WorkflowType.FizickaLica);

        var appraiser = Appraiser.Create("Test Vjestak", "Sarajevo",
            AppraiserLegalForm.Individual, "vjestak@test.ba", "061000000", null);

        _db.Appraisers.Add(appraiser);
        await _db.SaveChangesAsync();

        // CS0618: deliberate state machine bypass for test state setup
        // DocumentationApproved → SelectAppraiser → OrderSentToAppraiser
        order.ChangeStatus(AppraisalOrderStatus.DocumentationApproved, DateTime.UtcNow);
        order.SelectAppraiser(appraiser.Id, DateTime.UtcNow); // valid: DocumentationApproved → AppraiserSelected
        order.ChangeStatus(AppraisalOrderStatus.OrderSentToAppraiser, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();
        return (order, appraiser);
    }

    private async Task AddAcceptTaskAsync(int orderId)
    {
        _db.TaskItems.Add(TaskItem.Create(
            orderId, TaskItemType.AcceptAppraiserOrder, "Prihvati", null, AppRoles.Vjestak));
        await _db.SaveChangesAsync();
    }

    // ═══════════════════════════════════════════════════════════════
    // AcceptByAppraiserAsync
    // ═══════════════════════════════════════════════════════════════

    [Fact]
    public async Task AcceptByAppraiser_WhenOrderSentToAppraiser_ShouldTransitionToAppraisalInProgress()
    {
        var (order, _) = await SeedOrderSentToAppraiserAsync();
        await AddAcceptTaskAsync(order.Id);

        var result = await _sut.AcceptByAppraiserAsync(order.Id);

        result.Should().NotBeNull();
        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        updated.Status.Should().Be(AppraisalOrderStatus.AppraisalInProgress);
    }

    [Fact]
    public async Task AcceptByAppraiser_ShouldCreateUploadFinalAppraisalTask()
    {
        var (order, _) = await SeedOrderSentToAppraiserAsync();
        await AddAcceptTaskAsync(order.Id);

        await _sut.AcceptByAppraiserAsync(order.Id);

        var tasks = _db.TaskItems.Where(t => t.AppraisalOrderId == order.Id).ToList();
        tasks.Should().Contain(t => t.TaskType == TaskItemType.UploadFinalAppraisal);
    }

    [Fact]
    public async Task AcceptByAppraiser_ShouldCreateImportSignedDocumentsTask()
    {
        var (order, _) = await SeedOrderSentToAppraiserAsync();
        await AddAcceptTaskAsync(order.Id);

        await _sut.AcceptByAppraiserAsync(order.Id);

        var tasks = _db.TaskItems.Where(t => t.AppraisalOrderId == order.Id).ToList();
        tasks.Should().Contain(t => t.TaskType == TaskItemType.ImportSignedDocuments);
    }

    [Fact]
    public async Task AcceptByAppraiser_WhenWrongStatus_ShouldThrowConflict()
    {
        var (order, _) = await SeedOrderSentToAppraiserAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.AcceptByAppraiserAsync(order.Id));

        ex.ErrorCode.Should().Be("ORDER_NOT_SENT_TO_APPRAISER");
    }

    [Fact]
    public async Task AcceptByAppraiser_WhenOrderNotFound_ShouldThrowNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.AcceptByAppraiserAsync(99999));
    }

    // ═══════════════════════════════════════════════════════════════
    // RejectByAppraiserAsync
    // ═══════════════════════════════════════════════════════════════

    [Fact]
    public async Task RejectByAppraiser_WithValidStatus_ShouldTransitionToAppraiserRejected()
    {
        var (order, _) = await SeedOrderSentToAppraiserAsync();
        await AddAcceptTaskAsync(order.Id);
        _selectionService.SelectForOrderAsync(Arg.Any<AppraisalOrder>(),
            Arg.Any<IReadOnlyList<int>?>(), Arg.Any<CancellationToken>()).Returns((Appraiser?)null);

        var result = await _sut.RejectByAppraiserAsync(
            order.Id, AppraiserDeclineReason.NisamUGradu, null);

        result.Should().NotBeNull();
        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        updated.Status.Should().Be(AppraisalOrderStatus.AppraiserRejected);
    }

    [Fact]
    public async Task RejectByAppraiser_ShouldCreateOrderDeclinedAppraiserRecord()
    {
        var (order, appraiser) = await SeedOrderSentToAppraiserAsync();
        await AddAcceptTaskAsync(order.Id);
        _selectionService.SelectForOrderAsync(Arg.Any<AppraisalOrder>(),
            Arg.Any<IReadOnlyList<int>?>(), Arg.Any<CancellationToken>()).Returns((Appraiser?)null);

        await _sut.RejectByAppraiserAsync(order.Id, AppraiserDeclineReason.Bolest, "Opis");

        var declined = _db.Set<OrderDeclinedAppraiser>()
            .FirstOrDefault(d => d.AppraisalOrderId == order.Id && d.AppraiserId == appraiser.Id);
        declined.Should().NotBeNull("odbijeni vještak mora biti evidentiran");
    }

    [Fact]
    public async Task RejectByAppraiser_WhenWrongStatus_ShouldThrowConflict()
    {
        var (order, _) = await SeedOrderSentToAppraiserAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.RejectByAppraiserAsync(order.Id, AppraiserDeclineReason.NisamUGradu, null));

        ex.ErrorCode.Should().Be("ORDER_NOT_SENT_TO_APPRAISER");
    }

    [Theory]
    [InlineData(AppraiserDeclineReason.NisamUGradu)]
    [InlineData(AppraiserDeclineReason.Bolest)]
    [InlineData(AppraiserDeclineReason.SmrtniSlucaj)]
    [InlineData(AppraiserDeclineReason.OstaliRazlozi)]
    public async Task RejectByAppraiser_AllDeclineReasons_ShouldSucceed(AppraiserDeclineReason reason)
    {
        // Equivalence Partitioning: svaki razlog odbijanja mora biti prihvaćen
        var (order, _) = await SeedOrderSentToAppraiserAsync();
        await AddAcceptTaskAsync(order.Id);
        _selectionService.SelectForOrderAsync(Arg.Any<AppraisalOrder>(),
            Arg.Any<IReadOnlyList<int>?>(), Arg.Any<CancellationToken>()).Returns((Appraiser?)null);

        var result = await _sut.RejectByAppraiserAsync(order.Id, reason, null);

        result.Should().NotBeNull();
    }

    // ═══════════════════════════════════════════════════════════════
    // RejectOrderAsync — ADR-048 state machine fix verifikacija
    // ═══════════════════════════════════════════════════════════════

    [Fact]
    public async Task RejectOrder_WhenAppraisalInProgress_ShouldNowSucceed_StateMachineFix()
    {
        // Regresijski test za state machine fix:
        // AppraisalInProgress → AppraiserRejected je sada validan prijelaz
        var (order, appraiser) = await SeedOrderSentToAppraiserAsync();
        await AddAcceptTaskAsync(order.Id);
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        _selectionService.SelectForOrderAsync(Arg.Any<AppraisalOrder>(),
            Arg.Any<IReadOnlyList<int>?>(), Arg.Any<CancellationToken>()).Returns((Appraiser?)null);

        var result = await _sut.RejectOrderAsync(order.Id, "Greška u podacima", null);

        result.Should().NotBeNull();
        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        updated.Status.Should().Be(AppraisalOrderStatus.AppraiserRejected,
            "AppraisalInProgress → AppraiserRejected je validan nakon state machine fixa");
    }

    // ═══════════════════════════════════════════════════════════════
    // RequestAdditionalPaymentAsync
    // ═══════════════════════════════════════════════════════════════

    [Fact]
    public async Task RequestAdditionalPayment_WhenAppraisalInProgress_ShouldTransitionToAdditionalPaymentRequested()
    {
        var (order, _) = await SeedOrderSentToAppraiserAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var result = await _sut.RequestAdditionalPaymentAsync(order.Id);

        result.Should().NotBeNull();
        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        updated.Status.Should().Be(AppraisalOrderStatus.AdditionalPaymentRequested);
    }

    [Fact]
    public async Task RequestAdditionalPayment_WhenOrderSentToAppraiser_ShouldSucceed()
    {
        // Decision table: oba statusa su validna ulazna stanja
        var (order, _) = await SeedOrderSentToAppraiserAsync();

        var result = await _sut.RequestAdditionalPaymentAsync(order.Id);

        result.Should().NotBeNull();
    }

    [Fact]
    public async Task RequestAdditionalPayment_ShouldCreateConfirmTask()
    {
        var (order, _) = await SeedOrderSentToAppraiserAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await _sut.RequestAdditionalPaymentAsync(order.Id);

        var tasks = _db.TaskItems.Where(t => t.AppraisalOrderId == order.Id).ToList();
        tasks.Should().Contain(t => t.TaskType == TaskItemType.ConfirmAdditionalPayment,
            "CA mora dobiti zadatak potvrde doplate");
    }

    [Fact]
    public async Task RequestAdditionalPayment_WhenWrongStatus_ShouldThrowConflict()
    {
        // State: AppraiserRejected nije validan za doplatu
        var (order, _) = await SeedOrderSentToAppraiserAsync();
        order.ChangeStatus(AppraisalOrderStatus.AppraiserRejected, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.RequestAdditionalPaymentAsync(order.Id));

        ex.ErrorCode.Should().Be("ORDER_NOT_IN_PROGRESS");
    }

    // ═══════════════════════════════════════════════════════════════
    // ConfirmAdditionalPaymentAsync
    // ═══════════════════════════════════════════════════════════════

    [Fact]
    public async Task ConfirmAdditionalPayment_WhenPaymentRequested_ShouldTransitionToCompleted()
    {
        var (order, _) = await SeedOrderSentToAppraiserAsync();
        order.ChangeStatus(AppraisalOrderStatus.AdditionalPaymentRequested, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var result = await _sut.ConfirmAdditionalPaymentAsync(order.Id);

        result.Should().NotBeNull();
        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        updated.Status.Should().Be(AppraisalOrderStatus.AdditionalPaymentCompleted);
    }

    [Fact]
    public async Task ConfirmAdditionalPayment_WhenWrongStatus_ShouldThrowConflict()
    {
        var (order, _) = await SeedOrderSentToAppraiserAsync();
        // Nije u AdditionalPaymentRequested

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ConfirmAdditionalPaymentAsync(order.Id));

        ex.ErrorCode.Should().Be("ORDER_NOT_AWAITING_PAYMENT");
    }

    [Fact]
    public async Task ConfirmAdditionalPayment_WhenOrderHasNoAppraiser_ShouldThrowConflict()
    {
        // Napomena: simulacija "vještak ne postoji" u InMemory bazi je problematična
        // jer EF nullira FK pri brisanju referenced entiteta.
        // Testiramo ekvivalentan slučaj: narudžba bez AppraiserId (AppraiserId == null).
        var (order, _) = await SeedOrderSentToAppraiserAsync();

        // Stavi AppraiserId na null direktno putem EF entry (bypass private setter)
        _db.Entry(order).Property("AppraiserId").CurrentValue = null;
        order.ChangeStatus(AppraisalOrderStatus.AdditionalPaymentRequested, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ConfirmAdditionalPaymentAsync(order.Id));

        ex.ErrorCode.Should().Be("APPRAISER_NOT_ASSIGNED");
    }

    [Fact]
    public async Task ConfirmAdditionalPayment_ShouldCompleteAndRemovePaymentTask()
    {
        var (order, _) = await SeedOrderSentToAppraiserAsync();
        order.ChangeStatus(AppraisalOrderStatus.AdditionalPaymentRequested, DateTime.UtcNow);
        _db.TaskItems.Add(TaskItem.Create(
            order.Id, TaskItemType.ConfirmAdditionalPayment,
            "Doplata", null, AppRoles.KolateralAdministrator));
        await _db.SaveChangesAsync();

        await _sut.ConfirmAdditionalPaymentAsync(order.Id);

        var paymentTask = _db.TaskItems
            .FirstOrDefault(t => t.AppraisalOrderId == order.Id
                              && t.TaskType == TaskItemType.ConfirmAdditionalPayment);
        paymentTask!.Status.Should().Be(TaskItemStatus.Completed,
            "task potvrde doplate mora biti označen kao završen");
    }

    // ── Ordering domain invariants ────────────────────────────────────────────

    [Fact]
    public async Task OrderStateMachine_AppraisalInProgress_CanTransitionToAppraiserRejected()
    {
        // Direktna verifikacija state machine fixa (bez servisa)
        var canTransition = OrderStateMachine.CanTransition(
            AppraisalOrderStatus.AppraisalInProgress,
            AppraisalOrderStatus.AppraiserRejected);

        canTransition.Should().BeTrue(
            "state machine mora dozvoljavati CA/CO admin odbijanje iz AppraisalInProgress");
    }

    [Fact]
    public async Task OrderStateMachine_OrderSentToAppraiser_CanStillTransitionToAppraiserRejected()
    {
        // Regresijski: originalni prijelaz mora ostati validan
        var canTransition = OrderStateMachine.CanTransition(
            AppraisalOrderStatus.OrderSentToAppraiser,
            AppraisalOrderStatus.AppraiserRejected);

        canTransition.Should().BeTrue("originalni vještakov odbijanje mora ostati validan");
    }
}
