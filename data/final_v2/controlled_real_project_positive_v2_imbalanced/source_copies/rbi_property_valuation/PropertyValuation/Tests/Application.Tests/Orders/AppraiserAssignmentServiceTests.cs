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
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Domain.Appraisers;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using RBBH.CollateralAppraisal.Application.Tests.Helpers;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

public sealed class AppraiserAssignmentServiceTests : IDisposable
{
    private readonly ApplicationDbContext          _db;
    private readonly ICurrentUserService           _user;
    private readonly IAppraiserSelectionService    _selectionService;
    private readonly INotificationProvider         _notify;
    private readonly IDocumentService              _documentService;
    private readonly IAuditService                 _audit;
    private readonly IUserRoleProvider             _userRoleProvider;
    private readonly IProtocolService              _protocolService;
    private readonly AppraiserAssignmentService    _sut;

    public AppraiserAssignmentServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;

        _db               = new ApplicationDbContext(options);
        _user             = Substitute.For<ICurrentUserService>();
        _selectionService = Substitute.For<IAppraiserSelectionService>();
        _notify           = Substitute.For<INotificationProvider>();
        _documentService  = Substitute.For<IDocumentService>();
        _audit            = Substitute.For<IAuditService>();
        _userRoleProvider = Substitute.For<IUserRoleProvider>();
        _protocolService  = Substitute.For<IProtocolService>();

        _user.UserId.Returns("user-ca-1");
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

    // ── Helpers ───────────────────────────────────────────────────────────────

    private async Task<AppraisalOrder> CreateOrderAsync(
        string clientType = "FL",
        AppraisalOrderStatus status = AppraisalOrderStatus.DocumentationApproved)
    {
        var order = AppraisalOrder.Create(
            orderNumber:              $"2026/{Guid.NewGuid():N}".Substring(0, 12),
            title:                    "Procjena – Stan, Sarajevo",
            clientName:               "Petar Petrović",
            clientType:               clientType,
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

    private async Task<Appraiser> AddAppraiserAsync(
        string name = "Vjestak Vjestaković",
        bool isActive = true,
        bool isBlacklisted = false,
        AppraiserClientScope scope = AppraiserClientScope.Sve)
    {
        var appraiser = Appraiser.Create(
            name:                  name,
            city:                  "Sarajevo",
            legalForm:             AppraiserLegalForm.Individual,
            contactEmail:          "vjestak@test.ba",
            contactPhone:          "061-999-999",
            notes:                 null,
            clientScope:           scope);

        if (!isActive) appraiser.Deactivate(DateTime.UtcNow);
        if (isBlacklisted) appraiser.SetBlacklisted(true, DateTime.UtcNow);

        _db.Appraisers.Add(appraiser);
        await _db.SaveChangesAsync();
        return appraiser;
    }

    private async Task AddProtocolEntryAsync(int orderId)
    {
        var entry = OrderProtocolEntry.Create(orderId, 2026, 1, "user-ca-1", DateTime.UtcNow);
        _db.OrderProtocolEntries.Add(entry);
        await _db.SaveChangesAsync();
    }

    // ── AutoSelectAppraiserAsync ─────────────────────────────────────────────

    [Fact]
    public async Task AutoSelectAppraiserAsync_FL_SelectsAndAssigns()
    {
        var order    = await CreateOrderAsync("FL");
        var task     = await AddActiveTaskAsync(order.Id, TaskItemType.SelectAppraiser);
        var appraiser = await AddAppraiserAsync();

        _selectionService.SelectForOrderAsync(
            Arg.Any<AppraisalOrder>(),
            Arg.Any<IReadOnlyList<int>?>(),
            Arg.Any<CancellationToken>())
            .Returns(appraiser);

        _protocolService.CreateProtocolForOrderAsync(order.Id, Arg.Any<CancellationToken>())
            .Returns(Task.FromResult(OrderProtocolEntry.Create(order.Id, 2026, 1, "user-ca-1", DateTime.UtcNow)));

        var result = await _sut.AutoSelectAppraiserAsync(order.Id);

        Assert.Equal(appraiser.Id, result.AppraiserId);
        Assert.Equal("AppraiserSelected", result.Status);

        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        Assert.Equal(appraiser.Id, updated.AppraiserId);
    }

    [Fact]
    public async Task AutoSelectAppraiserAsync_PL_ThrowsConflict()
    {
        var order = await CreateOrderAsync("PL");
        await AddActiveTaskAsync(order.Id, TaskItemType.SelectAppraiser);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.AutoSelectAppraiserAsync(order.Id));
        Assert.Equal("APPRAISER_AUTO_SELECT_NOT_FL", ex.ErrorCode);
    }

    [Fact]
    public async Task AutoSelectAppraiserAsync_AppraiserAlreadySelected_ThrowsConflict()
    {
        var order    = await CreateOrderAsync("FL");
        var appraiser = await AddAppraiserAsync();
        order.SelectAppraiser(appraiser.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();
        await AddActiveTaskAsync(order.Id, TaskItemType.SelectAppraiser);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.AutoSelectAppraiserAsync(order.Id));
        Assert.Equal("APPRAISER_ALREADY_SELECTED", ex.ErrorCode);
    }

    [Fact]
    public async Task AutoSelectAppraiserAsync_NoActiveTask_ThrowsConflict()
    {
        var order = await CreateOrderAsync("FL");
        // No SelectAppraiser task

        _selectionService.SelectForOrderAsync(
            Arg.Any<AppraisalOrder>(),
            Arg.Any<IReadOnlyList<int>?>(),
            Arg.Any<CancellationToken>())
            .Returns((Appraiser?)null);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.AutoSelectAppraiserAsync(order.Id));
        Assert.Equal("SELECT_APPRAISER_TASK_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task AutoSelectAppraiserAsync_NoAppraiserAvailable_ThrowsConflict()
    {
        var order = await CreateOrderAsync("FL");
        await AddActiveTaskAsync(order.Id, TaskItemType.SelectAppraiser);

        _selectionService.SelectForOrderAsync(
            Arg.Any<AppraisalOrder>(),
            Arg.Any<IReadOnlyList<int>?>(),
            Arg.Any<CancellationToken>())
            .Returns((Appraiser?)null);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.AutoSelectAppraiserAsync(order.Id));
        Assert.Equal("NO_APPRAISER_AVAILABLE", ex.ErrorCode);
    }

    [Fact]
    public async Task AutoSelectAppraiserAsync_NotAuthenticated_ThrowsForbidden()
    {
        _user.IsAuthenticated.Returns(false);
        _user.UserId.Returns((string?)null);

        var order = await CreateOrderAsync("FL");
        await AddActiveTaskAsync(order.Id, TaskItemType.SelectAppraiser);

        await Assert.ThrowsAsync<ForbiddenException>(
            () => _sut.AutoSelectAppraiserAsync(order.Id));
    }

    [Fact]
    public async Task AutoSelectAppraiserAsync_OrderNotFound_ThrowsNotFound()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.AutoSelectAppraiserAsync(9999));
        Assert.Equal("APPRAISAL_ORDER_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task AutoSelectAppraiserAsync_RecordsAuditEvent()
    {
        var order    = await CreateOrderAsync("FL");
        await AddActiveTaskAsync(order.Id, TaskItemType.SelectAppraiser);
        var appraiser = await AddAppraiserAsync();

        _selectionService.SelectForOrderAsync(
            Arg.Any<AppraisalOrder>(),
            Arg.Any<IReadOnlyList<int>?>(),
            Arg.Any<CancellationToken>())
            .Returns(appraiser);

        _protocolService.CreateProtocolForOrderAsync(order.Id, Arg.Any<CancellationToken>())
            .Returns(Task.FromResult(OrderProtocolEntry.Create(order.Id, 2026, 1, "user-ca-1", DateTime.UtcNow)));

        await _sut.AutoSelectAppraiserAsync(order.Id);

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.AppraiserSelected),
            Arg.Any<CancellationToken>());
    }

    // ── ManualSelectAppraiserAsync ───────────────────────────────────────────

    [Fact]
    public async Task ManualSelectAppraiserAsync_ValidAppraiser_SelectsAndAssigns()
    {
        var order    = await CreateOrderAsync("PL");
        // Set the WorkflowType so CanHandle can evaluate PL scope correctly
        order.SetWorkflowType(WorkflowType.PravnaLica, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var task     = await AddActiveTaskAsync(order.Id, TaskItemType.SelectAppraiser);
        var appraiser = await AddAppraiserAsync(scope: AppraiserClientScope.PravnaLica);

        _protocolService.CreateProtocolForOrderAsync(order.Id, Arg.Any<CancellationToken>())
            .Returns(Task.FromResult(OrderProtocolEntry.Create(order.Id, 2026, 1, "user-ca-1", DateTime.UtcNow)));

        var result = await _sut.ManualSelectAppraiserAsync(order.Id, appraiser.Id);

        Assert.Equal(appraiser.Id, result.AppraiserId);
        Assert.Equal("AppraiserSelected", result.Status);
    }

    [Fact]
    public async Task ManualSelectAppraiserAsync_AppraiserNotFound_ThrowsNotFound()
    {
        var order = await CreateOrderAsync("PL");
        await AddActiveTaskAsync(order.Id, TaskItemType.SelectAppraiser);

        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.ManualSelectAppraiserAsync(order.Id, 9999));
        Assert.Equal("APPRAISER_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task ManualSelectAppraiserAsync_InactiveAppraiser_ThrowsConflict()
    {
        var order    = await CreateOrderAsync("PL");
        await AddActiveTaskAsync(order.Id, TaskItemType.SelectAppraiser);
        var appraiser = await AddAppraiserAsync(isActive: false);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ManualSelectAppraiserAsync(order.Id, appraiser.Id));
        Assert.Equal("APPRAISER_NOT_AVAILABLE", ex.ErrorCode);
    }

    [Fact]
    public async Task ManualSelectAppraiserAsync_BlacklistedAppraiser_ThrowsConflict()
    {
        var order    = await CreateOrderAsync("FL");
        await AddActiveTaskAsync(order.Id, TaskItemType.SelectAppraiser);
        var appraiser = await AddAppraiserAsync(isBlacklisted: true);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ManualSelectAppraiserAsync(order.Id, appraiser.Id));
        Assert.Equal("APPRAISER_NOT_AVAILABLE", ex.ErrorCode);
    }

    [Fact]
    public async Task ManualSelectAppraiserAsync_WrongScope_ThrowsConflict()
    {
        // FL order, but appraiser only handles PL
        var order    = await CreateOrderAsync("FL");
        await AddActiveTaskAsync(order.Id, TaskItemType.SelectAppraiser);
        var appraiser = await AddAppraiserAsync(scope: AppraiserClientScope.PravnaLica);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ManualSelectAppraiserAsync(order.Id, appraiser.Id));
        Assert.Equal("APPRAISER_SCOPE_MISMATCH", ex.ErrorCode);
    }

    [Fact]
    public async Task ManualSelectAppraiserAsync_NoSelectTask_ThrowsConflict()
    {
        var order    = await CreateOrderAsync("PL");
        var appraiser = await AddAppraiserAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ManualSelectAppraiserAsync(order.Id, appraiser.Id));
        Assert.Equal("SELECT_APPRAISER_TASK_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task ManualSelectAppraiserAsync_RecordsAuditEvent()
    {
        var order    = await CreateOrderAsync("PL");
        order.SetWorkflowType(WorkflowType.PravnaLica, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await AddActiveTaskAsync(order.Id, TaskItemType.SelectAppraiser);
        var appraiser = await AddAppraiserAsync(scope: AppraiserClientScope.PravnaLica);

        _protocolService.CreateProtocolForOrderAsync(order.Id, Arg.Any<CancellationToken>())
            .Returns(Task.FromResult(OrderProtocolEntry.Create(order.Id, 2026, 1, "user-ca-1", DateTime.UtcNow)));

        await _sut.ManualSelectAppraiserAsync(order.Id, appraiser.Id);

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.AppraiserSelected),
            Arg.Any<CancellationToken>());
    }

    // ── SendToAppraiserAsync ─────────────────────────────────────────────────

    [Fact]
    public async Task SendToAppraiserAsync_ValidState_TransitionsToOrderSentToAppraiser()
    {
        var appraiser = await AddAppraiserAsync();

        // Create order already in AppraiserSelected status with appraiser set
        var order = await CreateOrderAsync("FL");
        order.SelectAppraiser(appraiser.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await AddProtocolEntryAsync(order.Id);
        await AddActiveTaskAsync(order.Id, TaskItemType.SendOrderToAppraiser);

        var result = await _sut.SendToAppraiserAsync(order.Id);

        Assert.Equal("OrderSentToAppraiser", result.Status);
        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        Assert.Equal(AppraisalOrderStatus.OrderSentToAppraiser, updated.Status);
    }

    [Fact]
    public async Task SendToAppraiserAsync_WrongStatus_ThrowsConflict()
    {
        // Order not in AppraiserSelected status
        var order = await CreateOrderAsync("FL", AppraisalOrderStatus.DocumentationApproved);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SendToAppraiserAsync(order.Id));
        Assert.Equal("ORDER_NOT_READY_FOR_APPRAISER", ex.ErrorCode);
    }

    [Fact]
    public async Task SendToAppraiserAsync_NoProtocolEntry_ThrowsConflict()
    {
        var appraiser = await AddAppraiserAsync();
        var order     = await CreateOrderAsync("FL");
        order.SelectAppraiser(appraiser.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();
        // No protocol entry seeded
        await AddActiveTaskAsync(order.Id, TaskItemType.SendOrderToAppraiser);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SendToAppraiserAsync(order.Id));
        Assert.Equal("PROTOCOL_NUMBER_REQUIRED", ex.ErrorCode);
    }

    [Fact]
    public async Task SendToAppraiserAsync_NoSendTask_ThrowsConflict()
    {
        var appraiser = await AddAppraiserAsync();
        var order     = await CreateOrderAsync("FL");
        order.SelectAppraiser(appraiser.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();
        await AddProtocolEntryAsync(order.Id);
        // No SendOrderToAppraiser task

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SendToAppraiserAsync(order.Id));
        Assert.Equal("SEND_TO_APPRAISER_TASK_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task SendToAppraiserAsync_RecordsAuditEvent()
    {
        var appraiser = await AddAppraiserAsync();
        var order     = await CreateOrderAsync("FL");
        order.SelectAppraiser(appraiser.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();
        await AddProtocolEntryAsync(order.Id);
        await AddActiveTaskAsync(order.Id, TaskItemType.SendOrderToAppraiser);

        await _sut.SendToAppraiserAsync(order.Id);

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.OrderSentToAppraiser),
            Arg.Any<CancellationToken>());
    }

    // ── RequestAdditionalPaymentAsync ─────────────────────────────────────────

    [Fact]
    public async Task RequestAdditionalPaymentAsync_AppraisalInProgress_TransitionsToAdditionalPaymentRequested()
    {
        var appraiser = await AddAppraiserAsync();
        var order     = await CreateOrderAsync("FL");
        // SelectAppraiser sets AppraiserId and status=AppraiserSelected; then override status via ChangeStatus
        order.SelectAppraiser(appraiser.Id, DateTime.UtcNow);
        // CS0618: deliberate state machine bypass for test setup
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var result = await _sut.RequestAdditionalPaymentAsync(order.Id);

        Assert.Equal("AdditionalPaymentRequested", result.Status);
    }

    [Fact]
    public async Task RequestAdditionalPaymentAsync_OrderSentToAppraiser_TransitionsToAdditionalPaymentRequested()
    {
        var appraiser = await AddAppraiserAsync();
        var order     = await CreateOrderAsync("FL");
        order.SelectAppraiser(appraiser.Id, DateTime.UtcNow);
        // CS0618: deliberate state machine bypass for test setup
        order.ChangeStatus(AppraisalOrderStatus.OrderSentToAppraiser, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var result = await _sut.RequestAdditionalPaymentAsync(order.Id);

        Assert.Equal("AdditionalPaymentRequested", result.Status);
    }

    [Fact]
    public async Task RequestAdditionalPaymentAsync_InvalidStatus_ThrowsConflict()
    {
        var order = await CreateOrderAsync("FL", AppraisalOrderStatus.Draft);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.RequestAdditionalPaymentAsync(order.Id));
        Assert.Equal("ORDER_NOT_IN_PROGRESS", ex.ErrorCode);
    }

    [Fact]
    public async Task RequestAdditionalPaymentAsync_NoAppraiser_ThrowsConflict()
    {
        var order = await CreateOrderAsync("FL", AppraisalOrderStatus.AppraisalInProgress);
        // No appraiser selected

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.RequestAdditionalPaymentAsync(order.Id));
        Assert.Equal("APPRAISER_NOT_ASSIGNED", ex.ErrorCode);
    }

    // ── ConfirmAdditionalPaymentAsync ─────────────────────────────────────────

    [Fact]
    public async Task ConfirmAdditionalPaymentAsync_AdditionalPaymentRequested_TransitionsToCompleted()
    {
        var appraiser = await AddAppraiserAsync();
        var order     = await CreateOrderAsync("FL");
        // SelectAppraiser sets AppraiserId, then override status to AdditionalPaymentRequested
        order.SelectAppraiser(appraiser.Id, DateTime.UtcNow);
        // CS0618: deliberate state machine bypass for test setup
        order.ChangeStatus(AppraisalOrderStatus.AdditionalPaymentRequested, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var result = await _sut.ConfirmAdditionalPaymentAsync(order.Id);

        Assert.NotNull(result);
        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        Assert.Equal(AppraisalOrderStatus.AdditionalPaymentCompleted, updated.Status);
    }

    [Fact]
    public async Task ConfirmAdditionalPaymentAsync_InvalidStatus_ThrowsConflict()
    {
        var order = await CreateOrderAsync("FL", AppraisalOrderStatus.AppraisalInProgress);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ConfirmAdditionalPaymentAsync(order.Id));
        Assert.Equal("ORDER_NOT_AWAITING_PAYMENT", ex.ErrorCode);
    }

    [Fact]
    public async Task ConfirmAdditionalPaymentAsync_NoAppraiser_ThrowsConflict()
    {
        var order = await CreateOrderAsync("FL", AppraisalOrderStatus.AdditionalPaymentRequested);
        // No appraiser

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ConfirmAdditionalPaymentAsync(order.Id));
        Assert.Equal("APPRAISER_NOT_ASSIGNED", ex.ErrorCode);
    }

    [Fact]
    public async Task ConfirmAdditionalPaymentAsync_AppraiserNotFoundInDb_ThrowsNotFound()
    {
        var order = await CreateOrderAsync("FL");
        // SelectAppraiser with non-existent ID, then override status
        order.SelectAppraiser(9999, DateTime.UtcNow); // non-existent appraiser ID
        // CS0618: deliberate state machine bypass for test setup
        order.ChangeStatus(AppraisalOrderStatus.AdditionalPaymentRequested, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.ConfirmAdditionalPaymentAsync(order.Id));
        Assert.Equal("APPRAISER_NOT_FOUND", ex.ErrorCode);
    }

    // ── RejectOrderAsync (CA/CO admin odbijanje) ────────────────────────────────
    // Test matrix:
    //  Scenario                           | Expected                       | Type
    //  Validan status (OrderSentToAppraiser)| Vraća dto, kreira task        | Happy path
    //  Validan status (AppraisalInProgress) | Vraća dto                    | State transition
    //  Pogrešan status (Draft)             | ConflictException ORDER_NOT.. | Negative/State
    //  Bez vještaka na narudžbi            | Prazan rejectedName, nastavlja | Edge case
    //  Automatski reassign uspijeva        | autoReassigned=true u poruci   | Happy + reassign
    //  Audit event sniman                  | audit.RecordAsync pozvan       | Side-effect

    [Fact]
    public async Task RejectOrderAsync_WhenOrderSentToAppraiser_ShouldReturnResultAndCreateRejectedTask()
    {
        // Arrange: order mora proći kroz DocumentationApproved → AppraiserSelected → OrderSentToAppraiser
        var order    = await CreateOrderAsync("FL", AppraisalOrderStatus.DocumentationApproved);
        var appraiser = await AddAppraiserAsync();
        order.SelectAppraiser(appraiser.Id, DateTime.UtcNow);           // DocumentationApproved → AppraiserSelected
        // CS0618: bypass za direktno postavljanje test statusa
        order.ChangeStatus(AppraisalOrderStatus.OrderSentToAppraiser, DateTime.UtcNow); // → OrderSentToAppraiser
        await _db.SaveChangesAsync();

        _selectionService.SelectForOrderAsync(
            Arg.Any<AppraisalOrder>(),
            Arg.Any<IReadOnlyList<int>?>(),
            Arg.Any<CancellationToken>())
            .Returns((Appraiser?)null); // no auto-reassign

        // Act
        var result = await _sut.RejectOrderAsync(order.Id, "Greška u narudžbi", null);

        // Assert
        result.Should().NotBeNull();
        result.OrderId.Should().Be(order.Id);

        var tasks = _db.TaskItems.Where(t => t.AppraisalOrderId == order.Id).ToList();
        tasks.Should().Contain(t => t.TaskType == TaskItemType.AppraiserRejected);
    }

    [Fact]
    public async Task RejectOrderAsync_WhenAppraisalInProgress_ShouldSucceedAfterStateMachineFix()
    {
        // Regresijski test: AppraisalInProgress → AppraiserRejected je SADA validan
        // nakon state machine fixa (dodat prijelaz u OrderStateMachine.cs).
        // Prethodno je ova kombinacija bacala InvalidStateTransitionException.
        var order     = await CreateOrderAsync("FL", AppraisalOrderStatus.DocumentationApproved);
        var appraiser = await AddAppraiserAsync();
        order.SelectAppraiser(appraiser.Id, DateTime.UtcNow);
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        _selectionService.SelectForOrderAsync(
            Arg.Any<AppraisalOrder>(), Arg.Any<IReadOnlyList<int>?>(), Arg.Any<CancellationToken>())
            .Returns((Appraiser?)null);

        var result = await _sut.RejectOrderAsync(order.Id, "Razlog", null);

        result.Should().NotBeNull();
        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        updated.Status.Should().Be(AppraisalOrderStatus.AppraiserRejected,
            "AppraisalInProgress → AppraiserRejected je validan nakon state machine fixa");
    }

    [Fact]
    public async Task RejectOrderAsync_WhenOrderInWrongStatus_ShouldThrowConflict()
    {
        // State: Draft narudžba ne može biti odbijena
        var order = await CreateOrderAsync("FL", AppraisalOrderStatus.Draft);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.RejectOrderAsync(order.Id, "Razlog", null));

        ex.ErrorCode.Should().Be("ORDER_NOT_WITH_APPRAISER");
    }

    [Fact]
    public async Task RejectOrderAsync_WithRejectionComment_ShouldIncludeItInTaskDescription()
    {
        // Verifikacija da se komentar prenosi u task description
        var order     = await CreateOrderAsync("FL", AppraisalOrderStatus.DocumentationApproved);
        var appraiser = await AddAppraiserAsync();
        order.SelectAppraiser(appraiser.Id, DateTime.UtcNow);
        order.ChangeStatus(AppraisalOrderStatus.OrderSentToAppraiser, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        _selectionService.SelectForOrderAsync(
            Arg.Any<AppraisalOrder>(), Arg.Any<IReadOnlyList<int>?>(), Arg.Any<CancellationToken>())
            .Returns((Appraiser?)null);

        await _sut.RejectOrderAsync(order.Id, "Operativni razlozi", "Detaljno obrazloženje");

        var task = _db.TaskItems
            .First(t => t.AppraisalOrderId == order.Id && t.TaskType == TaskItemType.AppraiserRejected);
        task.Description.Should().Contain("Operativni razlozi: Detaljno obrazloženje");
    }

    [Fact]
    public async Task RejectOrderAsync_WhenNoAppraiserAssigned_ShouldStillSucceed()
    {
        // Edge case: narudžba nema dodijeljen vještak (AppraiserId == null)
        var order = await CreateOrderAsync("FL", AppraisalOrderStatus.OrderSentToAppraiser);
        // namjerno NE postavljamo AppraiserId

        _selectionService.SelectForOrderAsync(
            Arg.Any<AppraisalOrder>(), Arg.Any<IReadOnlyList<int>?>(), Arg.Any<CancellationToken>())
            .Returns((Appraiser?)null);

        var result = await _sut.RejectOrderAsync(order.Id, "Razlog", null);

        result.Should().NotBeNull();
    }

    [Fact]
    public async Task RejectOrderAsync_ShouldRecordAuditEvent()
    {
        // Side-effect: audit mora biti sniman
        var order     = await CreateOrderAsync("FL", AppraisalOrderStatus.DocumentationApproved);
        var appraiser = await AddAppraiserAsync();
        order.SelectAppraiser(appraiser.Id, DateTime.UtcNow);
        order.ChangeStatus(AppraisalOrderStatus.OrderSentToAppraiser, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        _selectionService.SelectForOrderAsync(
            Arg.Any<AppraisalOrder>(), Arg.Any<IReadOnlyList<int>?>(), Arg.Any<CancellationToken>())
            .Returns((Appraiser?)null);

        await _sut.RejectOrderAsync(order.Id, "Razlog", null);

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.OrderRejectedByAppraiser),
            Arg.Any<CancellationToken>());
    }

    public void Dispose() => _db.Dispose();
}
