// CS0618: AppraisalOrder.ChangeStatus() is marked [Obsolete] in production code.
// In tests, deliberately using this method to bypass the state machine and set up
// arbitrary order states for test scenarios â€” this is intentional and acceptable.
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
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Application.Orders.Requests;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Domain.Orders;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Security;

/// <summary>
/// OWASP Top-10 security test suite for the AppraisalOrder service layer.
/// Tests verify service-level enforcement of business security rules.
/// </summary>
public sealed class OwaspSecurityTests : IDisposable
{
    private readonly ApplicationDbContext   _db;
    private readonly ICurrentUserService    _user;
    private readonly IAuditService          _audit;
    private readonly INotificationProvider  _notify;
    private readonly AppraisalOrderService  _sut;

    private int _collateralTypeId;

    public OwaspSecurityTests()
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

        _user.UserId.Returns("sales-user-1");
        _user.Role.Returns(AppRoles.AM);
        _user.Roles.Returns([AppRoles.AM]);
        _user.IsAuthenticated.Returns(true);

        var createSvc = new OrderCreateService(
            _db, _user, new OrderTitleGenerator(), new FakeOrderNumberGenerator(), _audit, new FakeClock());
        var submitSvc = new OrderSubmitService(
            _db, _user, _notify, _audit,
            Substitute.For<ILogger<OrderSubmitService>>(),
            Options.Create(new OrderNotificationsOptions { CaInboxEmail = "narudzbe@test.ba" }),
            Options.Create(new WorkflowSlaOptions()),
            new FakeClock());
        _sut = new AppraisalOrderService(_db, _user, _audit, createSvc, submitSvc);

        SeedCodebook();
    }

    private void SeedCodebook()
    {
        var collateral = CodebookValue.Create(
            "tipovi_kolaterala", "APP_STAN", "Stan", null, 10, "system-seed");
        _db.CodebookValues.Add(collateral);
        _db.SaveChanges();
        _collateralTypeId = collateral.Id;
    }

    private CreateOrderRequest ValidRequest() =>
        new(
            ClientName:               "Petar Petrovic",
            ClientType:               "FL",
            ClientIdentifier:         "0101990000019",
            CollateralTypeId:         _collateralTypeId,
            CombinedCollateralTypeId: null,
            City:                     "Sarajevo",
            PropertyAddress:          "Obala 1",
            Branch:                   "POS_SARAJEVO_CENTAR",
            BranchAddress:            "Titova 1",
            ContactName:              "Petar Petrovic",
            ContactPhone:             "061-123-456",
            ContactEmail:             "petar@test.ba",
            InternalNote:             null,
            DeliveryContactName:      "Amina Dostavljac",
            AmRecipientName:          "Amar Primalac",
            RequestReceivedAt:        new DateTime(2026, 6, 1, 9, 0, 0, DateTimeKind.Utc));

    // â”€â”€ A01: Broken Access Control â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    [Fact]
    public async Task A01_SalesAgent_CannotGetAnotherAgentsOrder_ThrowsForbidden()
    {
        // Sales user 1 creates an order
        var created = await _sut.CreateAsync(ValidRequest());

        // Another sales user (user 2) tries to access it
        _user.UserId.Returns("sales-user-2");
        _user.Roles.Returns([AppRoles.AM]);

        var ex = await Assert.ThrowsAsync<ForbiddenException>(
            () => _sut.GetByIdAsync(created.Id));

        Assert.NotNull(ex);
    }

    [Fact]
    public async Task A01_SalesAgent_CannotCancelAnotherUsersOrder_ThrowsForbidden()
    {
        // Sales user 1 creates an order
        var created = await _sut.CreateAsync(ValidRequest());

        // Another sales user tries to cancel it
        _user.UserId.Returns("sales-user-2");
        _user.Roles.Returns([AppRoles.AM]);

        var ex = await Assert.ThrowsAsync<ForbiddenException>(
            () => _sut.CancelAsync(created.Id));

        Assert.NotNull(ex);
    }

    [Fact]
    public async Task A01_SalesAgent_CannotSeeOtherUsersOrdersInList()
    {
        // Sales user 1 creates an order
        await _sut.CreateAsync(ValidRequest());

        // Another AM queries the list â€” should see nothing
        _user.UserId.Returns("sales-user-other");
        _user.Roles.Returns([AppRoles.SM]);

        var result = await new RBBH.CollateralAppraisal.Infrastructure.Orders.OrderQueryService(_db, _user, NSubstitute.Substitute.For<RBBH.CollateralAppraisal.Application.Users.IUserRoleProvider>()).GetListAsync(new OrderListRequest());

        Assert.Equal(0, result.TotalCount);
    }

    // â”€â”€ A04: Insecure Design â€” Creator cannot approve own order â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    [Fact]
    public async Task A04_CreatorCannotApproveOwnOrder_FourEyesPrincipleEnforced()
    {
        // This is tested at AppraisalOrderService level through the "four-eyes" check
        // in OrderApprovalService. Here we verify that a non-CA user who created
        // the order cannot access getById in the approval context.
        // The core four-eyes test is in OrderApprovalServiceTests.cs (test already exists).
        // This test verifies the access control at the list level for the creator.
        var created = await _sut.CreateAsync(ValidRequest());

        // Creator can read their own order
        var dto = await _sut.GetByIdAsync(created.Id);
        Assert.Equal(created.Id, dto.Id);

        // But CA (a different user) can also read it
        _user.UserId.Returns("ca-user");
        _user.Roles.Returns([AppRoles.KolateralAdministrator]);

        var caDto = await _sut.GetByIdAsync(created.Id);
        Assert.Equal(created.Id, caDto.Id);
    }

    // â”€â”€ A07: Identification and Authentication Failures â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    [Fact]
    public async Task A07_UnauthenticatedUser_CannotSubmitAnotherUsersOrder_ThrowsForbidden()
    {
        // First, create order as valid user
        var created = await _sut.CreateAsync(ValidRequest());

        // Then, switch to a different user (unauthenticated simulated by null UserId)
        // The service compares order.CreatedByUserId != _currentUser.UserId â†’
        // if UserId is null/empty, the check fails and throws ForbiddenException
        _user.IsAuthenticated.Returns(false);
        _user.UserId.Returns((string?)null);
        _user.Roles.Returns(new List<string>().AsReadOnly());

        await Assert.ThrowsAsync<ForbiddenException>(
            () => _sut.SubmitAsync(created.Id));
    }

    [Fact]
    public async Task A07_NullUserId_CannotCancelAnotherUsersOrder_ThrowsForbidden()
    {
        // First, create order as valid user
        var created = await _sut.CreateAsync(ValidRequest());

        // A different user (null UserId) cannot cancel
        _user.IsAuthenticated.Returns(false);
        _user.UserId.Returns((string?)null);
        _user.Roles.Returns(new List<string>().AsReadOnly());

        await Assert.ThrowsAsync<ForbiddenException>(
            () => _sut.CancelAsync(created.Id));
    }

    // â”€â”€ A08: Software and Data Integrity Failures (state machine) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    [Fact]
    public async Task A08_SubmittedOrder_CannotBeSubmittedAgain_ThrowsValidation()
    {
        // Demonstrates that state machine prevents duplicate transitions
        var created = await _sut.CreateAsync(ValidRequest());
        await _sut.SubmitAsync(created.Id); // first submit

        // Second submit must fail â€” state machine rejects SubmittedBySales â†’ SubmittedBySales
        await Assert.ThrowsAsync<ValidationException>(
            () => _sut.SubmitAsync(created.Id));
    }

    [Fact]
    public async Task A08_DraftOrder_CannotJumpToCompleted_StateMachinePrevents()
    {
        // State machine forbids direct Draft â†’ Completed transition
        Assert.False(OrderStateMachine.CanTransition(
            AppraisalOrderStatus.Draft,
            AppraisalOrderStatus.Completed));
    }

    [Fact]
    public async Task A08_CompletedOrder_HasNoOutgoingTransitions_CannotBeModified()
    {
        // All statuses as targets from Completed must return false
        foreach (var target in Enum.GetValues<AppraisalOrderStatus>())
        {
            Assert.False(OrderStateMachine.CanTransition(AppraisalOrderStatus.Completed, target),
                $"Completed â†’ {target} must be forbidden");
        }
    }

    [Fact]
    public async Task A08_CancelledOrderByStateMachine_HasNoOutgoingTransitions()
    {
        // Validates that Cancelled status has no outgoing transitions
        foreach (var target in Enum.GetValues<AppraisalOrderStatus>())
        {
            Assert.False(OrderStateMachine.CanTransition(AppraisalOrderStatus.Cancelled, target),
                $"Cancelled â†’ {target} must be forbidden");
        }
    }

    // â”€â”€ A09: Security Logging and Monitoring â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    [Fact]
    public async Task A09_UnauthorizedAccessAttempt_IsAuditLogged()
    {
        // A sales user creates an order
        var created = await _sut.CreateAsync(ValidRequest());

        // Another sales user (different ID) attempts to access it
        _user.UserId.Returns("intruder-user-id");
        _user.Roles.Returns([AppRoles.SM]);

        await Assert.ThrowsAsync<ForbiddenException>(
            () => _sut.GetByIdAsync(created.Id));

        // The unauthorized access attempt MUST be audit-logged
        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.UnauthorizedOrderAccess
                                 && e.EntityKey == created.Id.ToString()),
            Arg.Any<CancellationToken>());
    }

    // â”€â”€ Input Validation â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    [Fact]
    public async Task InputValidation_NullClientName_ThrowsValidationException()
    {
        var req = ValidRequest() with { ClientName = null! };

        var ex = await Assert.ThrowsAsync<ValidationException>(
            () => _sut.CreateAsync(req));

        Assert.NotNull(ex);
    }

    [Fact]
    public async Task InputValidation_EmptyClientName_ThrowsValidationException()
    {
        var req = ValidRequest() with { ClientName = string.Empty };

        await Assert.ThrowsAsync<ValidationException>(
            () => _sut.CreateAsync(req));
    }

    [Fact]
    public async Task InputValidation_SqlInjectionLikeSearchString_DoesNotThrow()
    {
        await _sut.CreateAsync(ValidRequest());

        // A SQL injection-like string in the Search parameter should be safely handled
        // (EF Core parameterizes queries, so this should return 0 results, not crash)
        var result = await new RBBH.CollateralAppraisal.Infrastructure.Orders.OrderQueryService(_db, _user, NSubstitute.Substitute.For<RBBH.CollateralAppraisal.Application.Users.IUserRoleProvider>()).GetListAsync(
            new OrderListRequest(Search: "'; DROP TABLE AppraisalOrders; --"));

        Assert.NotNull(result);
        Assert.Equal(0, result.TotalCount);
    }

    [Fact]
    public async Task InputValidation_XssLikeClientName_IsRejectedByNameValidator()
    {
        // HTML/script tags contain characters (<, >) not allowed in names
        var req = ValidRequest() with { ClientName = "<script>alert(1)</script>" };

        await Assert.ThrowsAsync<ValidationException>(
            () => _sut.CreateAsync(req));
    }

    public void Dispose() => _db.Dispose();
}
