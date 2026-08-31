using Microsoft.EntityFrameworkCore;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Application.Users.Models;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Orders;

public sealed class OrderQueryServiceTests : IDisposable
{
    private readonly ApplicationDbContext _db;
    private readonly ICurrentUserService  _currentUser;
    private readonly IUserRoleProvider    _userRoleProvider;
    private readonly OrderQueryService    _sut;

    public OrderQueryServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db               = new ApplicationDbContext(options);
        _currentUser      = Substitute.For<ICurrentUserService>();
        _userRoleProvider = Substitute.For<IUserRoleProvider>();
        _currentUser.Permissions.Returns(Array.Empty<string>());

        _sut = new OrderQueryService(_db, _currentUser, _userRoleProvider);
    }

    public void Dispose() => _db.Dispose();

    private AppraisalOrder SeedOrder(
        string orderNumber = "2026-000001",
        string? city = "Sarajevo",
        int? collateralTypeId = null,
        int? combinedTypeId = null)
    {
        var order = AppraisalOrder.Create(
            orderNumber, "Procjena - " + orderNumber, "Petar Petrović", "FL", "0101985100123",
            "Petar Petrović", "061-123-456", "petar@test.ba",
            city, "POS_SARAJEVO_CENTAR", "Titova 1", "Obala 1",
            collateralTypeId, combinedTypeId,
            "user-am-1", "AM", "Amina AM",
            "Amina Dostavljač", "Amar Primalac");
        _db.AppraisalOrders.Add(order);
        _db.SaveChanges();
        return order;
    }

    // ── Basic mapping ──────────────────────────────────────────────────────

    [Fact]
    public async Task GetByIdAsync_NonExistentOrder_ThrowsNotFoundException()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.GetByIdAsync(999));

        Assert.Equal("APPRAISAL_ORDER_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task GetByIdAsync_WithCity_TitleIncludesLocation()
    {
        var order = SeedOrder(city: "Sarajevo");

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.Equal($"Procjena nekretnine — {order.ClientName}, Sarajevo", dto.Title);
        Assert.Equal("Draft", dto.Status);
        Assert.Equal(0, dto.StatusCode);
    }

    [Fact]
    public async Task GetByIdAsync_NoCity_TitleOmitsLocation()
    {
        var order = SeedOrder(city: null);

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.Equal($"Procjena nekretnine — {order.ClientName}", dto.Title);
    }

    [Fact]
    public async Task GetByIdAsync_WithCollateralTypes_ResolvesLabelsFromCodebook()
    {
        var collateral = CodebookValue.Create("tipovi_kolaterala", "APP_STAN", "Stan", null, 10, "system-seed");
        var combined   = CodebookValue.Create("kombinovani_tipovi_kolaterala", "APP_STAN_I_GARAZA", "Stan i garaža", null, 10, "system-seed");
        _db.CodebookValues.Add(collateral);
        _db.CodebookValues.Add(combined);
        _db.SaveChanges();

        var order = SeedOrder(collateralTypeId: collateral.Id, combinedTypeId: combined.Id);

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.Equal("Stan", dto.CollateralTypeLabel);
        Assert.Equal("Stan i garaža", dto.CombinedCollateralTypeLabel);
    }

    [Fact]
    public async Task GetByIdAsync_NoCollateralTypes_LabelsAreNull()
    {
        var order = SeedOrder();

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.Null(dto.CollateralTypeId);
        Assert.Null(dto.CollateralTypeLabel);
        Assert.Null(dto.CombinedCollateralTypeId);
        Assert.Null(dto.CombinedCollateralTypeLabel);
    }

    // ── ResolveDisplayNameAsync ────────────────────────────────────────────

    [Fact]
    public async Task GetByIdAsync_CoApprovedByUserId_ResolvesDisplayNameFromProvider()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
#pragma warning restore CS0618
        order.ApproveByCO("co-user-1", DateTime.UtcNow);
        _db.SaveChanges();

        _userRoleProvider.GetUserWithRolesAsync("co-user-1", Arg.Any<CancellationToken>())
            .Returns(new UserRoleSourceItem { UserId = "co-user-1", Username = "co.user", DisplayName = "Marko Marković", IsActive = true });

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.Equal("Marko Marković", dto.CoApprovedByName);
    }

    [Fact]
    public async Task GetByIdAsync_CoApprovedByUserId_NoDisplayName_FallsBackToUsername()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
#pragma warning restore CS0618
        order.ApproveByCO("co-user-1", DateTime.UtcNow);
        _db.SaveChanges();

        _userRoleProvider.GetUserWithRolesAsync("co-user-1", Arg.Any<CancellationToken>())
            .Returns(new UserRoleSourceItem { UserId = "co-user-1", Username = "co.user", DisplayName = null, IsActive = true });

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.Equal("co.user", dto.CoApprovedByName);
    }

    [Fact]
    public async Task GetByIdAsync_CoApprovedByUserId_ProviderReturnsNull_FallsBackToUserId()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
#pragma warning restore CS0618
        order.ApproveByCO("co-user-1", DateTime.UtcNow);
        _db.SaveChanges();

        _userRoleProvider.GetUserWithRolesAsync("co-user-1", Arg.Any<CancellationToken>())
            .Returns((UserRoleSourceItem?)null);

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.Equal("co-user-1", dto.CoApprovedByName);
    }

    [Fact]
    public async Task GetByIdAsync_CoApprovedByUserId_ProviderThrows_FallsBackToUserId()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
#pragma warning restore CS0618
        order.ApproveByCO("co-user-1", DateTime.UtcNow);
        _db.SaveChanges();

        _userRoleProvider.GetUserWithRolesAsync("co-user-1", Arg.Any<CancellationToken>())
            .Returns(Task.FromException<UserRoleSourceItem?>(new InvalidOperationException("Keycloak nije dostupan")));

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.Equal("co-user-1", dto.CoApprovedByName);
    }

    [Fact]
    public async Task GetByIdAsync_NoCoApprovedByUserId_DisplayNameIsNullAndProviderNotCalled()
    {
        var order = SeedOrder();

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.Null(dto.CoApprovedByName);
        await _userRoleProvider.DidNotReceive().GetUserWithRolesAsync(Arg.Any<string>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task GetByIdAsync_OriginalReceivedByUserId_ResolvesDisplayNameFromProvider()
    {
        var order = SeedOrder();
#pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.ReadyForProcedure, DateTime.UtcNow);
#pragma warning restore CS0618
        order.ConfirmOriginalReceived("am-user-1", DateTime.UtcNow);
        _db.SaveChanges();

        _userRoleProvider.GetUserWithRolesAsync("am-user-1", Arg.Any<CancellationToken>())
            .Returns(new UserRoleSourceItem { UserId = "am-user-1", Username = "am.user", DisplayName = "Amina AM", IsActive = true });

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.Equal("Amina AM", dto.OriginalReceivedByName);
        Assert.Equal("Completed", dto.Status);
        Assert.NotNull(dto.OriginalReceivedAt);
    }

    [Fact]
    public async Task GetByIdAsync_AfterRecordAppraiserReminder_ReturnsCountAndTimestamp()
    {
        var order = SeedOrder();
        var now   = DateTime.UtcNow;
        order.RecordAppraiserReminder(now);
        _db.SaveChanges();

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.Equal(1, dto.AppraiserReminderCount);
        Assert.Equal(now, dto.AppraiserReminderLastSentAt);
    }

    // ── Capabilities ───────────────────────────────────────────────────────

    [Fact]
    public async Task GetByIdAsync_AppraisalReceivedWithPermissions_CanApproveFinalAndDownloadFinalTrue()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, DateTime.UtcNow);
        #pragma warning restore CS0618
        order.SetFinalAppraisalDocument(documentId: 5, DateTime.UtcNow);
        _db.SaveChanges();
        _currentUser.Permissions.Returns(new[] { AppPermissions.OrdersApproveFinal, AppPermissions.OrdersDownloadAppraisal });

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.Equal("AppraisalReceived", dto.Status);
        Assert.True(dto.Capabilities.CanApproveFinal);
        Assert.True(dto.Capabilities.CanDownloadFinal);
    }

    [Fact]
    public async Task GetByIdAsync_DraftStatus_CanApproveFinalFalseEvenWithPermission()
    {
        var order = SeedOrder();
        _currentUser.Permissions.Returns(new[] { AppPermissions.OrdersApproveFinal });

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.False(dto.Capabilities.CanApproveFinal);
    }

    [Fact]
    public async Task GetByIdAsync_NoFinalDocument_CanDownloadFinalFalseEvenWithPermission()
    {
        var order = SeedOrder();
        _currentUser.Permissions.Returns(new[] { AppPermissions.OrdersDownloadAppraisal });

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.False(dto.Capabilities.CanDownloadFinal);
    }

    [Fact]
    public async Task GetByIdAsync_ReadyForProcedureWithPermission_CanConfirmOriginalTrue()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, DateTime.UtcNow);
        #pragma warning restore CS0618
        order.SetFinalAppraisalDocument(5, DateTime.UtcNow);
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
#pragma warning restore CS0618
        order.ApproveByCO("co-user-1", DateTime.UtcNow);
        _db.SaveChanges();
        _currentUser.Permissions.Returns(new[] { AppPermissions.OrdersConfirmOriginal });

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.Equal("ReadyForProcedure", dto.Status);
        Assert.True(dto.Capabilities.CanConfirmOriginal);
    }

    [Fact]
    public async Task GetByIdAsync_OriginalReceivedAtNullEligibleStatusWithPermission_CanRemindAppraiserTrue()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, DateTime.UtcNow);
        #pragma warning restore CS0618
        order.SetFinalAppraisalDocument(5, DateTime.UtcNow);
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
#pragma warning restore CS0618
        order.ApproveByCO("co-user-1", DateTime.UtcNow);
        _db.SaveChanges();
        _currentUser.Permissions.Returns(new[] { AppPermissions.OrdersRemindAppraiser });

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.True(dto.Capabilities.CanRemindAppraiser);
    }

    [Fact]
    public async Task GetByIdAsync_OriginalReceivedAtSet_CanRemindAppraiserFalse()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, DateTime.UtcNow);
        #pragma warning restore CS0618
        order.SetFinalAppraisalDocument(5, DateTime.UtcNow);
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
#pragma warning restore CS0618
        order.ApproveByCO("co-user-1", DateTime.UtcNow);
        order.ConfirmOriginalReceived("am-user-1", DateTime.UtcNow);
        _db.SaveChanges();
        _currentUser.Permissions.Returns(new[] { AppPermissions.OrdersRemindAppraiser });

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.False(dto.Capabilities.CanRemindAppraiser);
    }

    [Fact]
    public async Task GetByIdAsync_CancelledStatus_CanRemindAppraiserFalse()
    {
        var order = SeedOrder();
        order.ChangeStatus(AppraisalOrderStatus.Cancelled, DateTime.UtcNow);
        _db.SaveChanges();
        _currentUser.Permissions.Returns(new[] { AppPermissions.OrdersRemindAppraiser });

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.False(dto.Capabilities.CanRemindAppraiser);
    }

    [Fact]
    public async Task GetByIdAsync_WithoutAnyPermissions_AllCapabilitiesFalse()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, DateTime.UtcNow);
        #pragma warning restore CS0618
        order.SetFinalAppraisalDocument(5, DateTime.UtcNow);
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
#pragma warning restore CS0618
        order.ApproveByCO("co-user-1", DateTime.UtcNow);
        _db.SaveChanges();

        var dto = await _sut.GetByIdAsync(order.Id);

        Assert.False(dto.Capabilities.CanApproveFinal);
        Assert.False(dto.Capabilities.CanDownloadFinal);
        Assert.False(dto.Capabilities.CanConfirmOriginal);
        Assert.False(dto.Capabilities.CanRemindAppraiser);
    }
}
