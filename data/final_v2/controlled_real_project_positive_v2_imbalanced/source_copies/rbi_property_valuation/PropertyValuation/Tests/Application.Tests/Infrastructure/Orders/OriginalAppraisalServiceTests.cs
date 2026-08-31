using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Orders;

public sealed class OriginalAppraisalServiceTests : IDisposable
{
    private readonly ApplicationDbContext   _db;
    private readonly ICurrentUserService    _currentUser;
    private readonly INotificationService   _notificationService;
    private readonly IAuditService          _audit;
    private readonly OriginalAppraisalService _sut;

    public OriginalAppraisalServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db                  = new ApplicationDbContext(options);
        _currentUser         = Substitute.For<ICurrentUserService>();
        _notificationService = Substitute.For<INotificationService>();
        _audit               = Substitute.For<IAuditService>();

        _currentUser.IsAuthenticated.Returns(true);
        _currentUser.UserId.Returns("user-am-1");

        _sut = new OriginalAppraisalService(
            _db, _currentUser, _notificationService, _audit, Substitute.For<ILogger<OriginalAppraisalService>>());
    }

    public void Dispose() => _db.Dispose();

    private AppraisalOrder SeedOrder(string orderNumber = "2026-000001")
    {
        var order = AppraisalOrder.Create(
            orderNumber, "Procjena - " + orderNumber, "Petar Petrović", "FL", "0101985100123",
            "Petar Petrović", "061-123-456", "petar@test.ba",
            "Sarajevo", "POS_SARAJEVO_CENTAR", "Titova 1", "Obala 1",
            null, null,
            "user-am-1", "AM", "Amina AM",
            "Amina Dostavljač", "Amar Primalac");
        _db.AppraisalOrders.Add(order);
        _db.SaveChanges();
        return order;
    }

    // ── ConfirmOriginalReceivedAsync ──────────────────────────────────────

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_ValidOrder_UpdatesStatusAndReturnsDto()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.ReadyForProcedure, DateTime.UtcNow);
#pragma warning restore CS0618
        _db.SaveChanges();

        var dto = await _sut.ConfirmOriginalReceivedAsync(order.Id);

        Assert.Equal(order.Id, dto.OrderId);
        Assert.Equal(order.OrderNumber, dto.OrderNumber);
        Assert.Equal("Completed", dto.Status);
        Assert.Equal("user-am-1", dto.OriginalReceivedByUserId);
        Assert.Contains(order.ClientName, dto.Message);

        var reloaded = await _db.AppraisalOrders.FindAsync(order.Id);
        Assert.Equal(AppraisalOrderStatus.Completed, reloaded!.Status);
        Assert.NotNull(reloaded.OriginalReceivedAt);

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == "ORDER_ORIGINAL_RECEIVED"), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_NotAuthenticated_ThrowsForbiddenException()
    {
        _currentUser.IsAuthenticated.Returns(false);
        var order = SeedOrder();

        await Assert.ThrowsAsync<ForbiddenException>(() => _sut.ConfirmOriginalReceivedAsync(order.Id));
    }

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_OrderNotFound_ThrowsNotFoundException()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.ConfirmOriginalReceivedAsync(999));
    }

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_AlreadyReceived_ThrowsConflictExceptionWithCode()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.ReadyForProcedure, DateTime.UtcNow);
#pragma warning restore CS0618
        order.ConfirmOriginalReceived("am-user-1", DateTime.UtcNow);
        _db.SaveChanges();

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ConfirmOriginalReceivedAsync(order.Id));

        Assert.Equal("ORIGINAL_ALREADY_RECEIVED", ex.ErrorCode);
    }

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_InvalidStatus_ThrowsConflictExceptionWithCode()
    {
        var order = SeedOrder(); // Draft

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ConfirmOriginalReceivedAsync(order.Id));

        Assert.Equal("ORIGINAL_INVALID_STATUS", ex.ErrorCode);
    }

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_NoKnownCAOrCOUsers_NotificationsSentFalse()
    {
        var order = SeedOrder();
        order.ChangeStatus(AppraisalOrderStatus.ReadyForProcedure, DateTime.UtcNow);
        _db.SaveChanges();

        var dto = await _sut.ConfirmOriginalReceivedAsync(order.Id);

        Assert.False(dto.NotificationsSent);
    }

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_NotificationThrows_NotificationsSentFalseButSucceeds()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.ReadyForProcedure, DateTime.UtcNow);
#pragma warning restore CS0618
        _db.SaveChanges();

        _notificationService
            .NotifyUserAsync(Arg.Any<string>(), Arg.Any<string>(), Arg.Any<string>(),
                Arg.Any<string?>(), Arg.Any<string?>(), Arg.Any<bool>(), Arg.Any<string?>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("notification provider down")));

        var dto = await _sut.ConfirmOriginalReceivedAsync(order.Id);

        Assert.False(dto.NotificationsSent);
    }

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_AuditRecordingThrows_StillReturnsResult()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.ReadyForProcedure, DateTime.UtcNow);
#pragma warning restore CS0618
        _db.SaveChanges();

        _audit.RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("audit sink down")));

        var dto = await _sut.ConfirmOriginalReceivedAsync(order.Id);

        Assert.Equal("Completed", dto.Status);
    }

    // ── SendAppraiserReminderAsync ────────────────────────────────────────

    [Fact]
    public async Task SendAppraiserReminderAsync_ValidOrder_IncrementsCounterAndReturnsDto()
    {
        var order = SeedOrder();

        var dto = await _sut.SendAppraiserReminderAsync(order.Id);

        Assert.Equal(order.Id, dto.OrderId);
        Assert.Equal(order.OrderNumber, dto.OrderNumber);
        Assert.Equal(1, dto.ReminderCount);
        Assert.False(dto.NotificationSent);
        Assert.Contains("Reminder #1", dto.Message);

        var reloaded = await _db.AppraisalOrders.FindAsync(order.Id);
        Assert.Equal(1, reloaded!.AppraiserReminderCount);
        Assert.NotNull(reloaded.AppraiserReminderLastSentAt);

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == "ORDER_APPRAISER_REMINDER_SENT"), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task SendAppraiserReminderAsync_NotAuthenticated_ThrowsForbiddenException()
    {
        _currentUser.IsAuthenticated.Returns(false);
        var order = SeedOrder();

        await Assert.ThrowsAsync<ForbiddenException>(() => _sut.SendAppraiserReminderAsync(order.Id));
    }

    [Fact]
    public async Task SendAppraiserReminderAsync_OrderNotFound_ThrowsNotFoundException()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.SendAppraiserReminderAsync(999));
    }

    [Fact]
    public async Task SendAppraiserReminderAsync_OriginalAlreadyReceived_ThrowsConflictExceptionWithCode()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.ReadyForProcedure, DateTime.UtcNow);
#pragma warning restore CS0618
        order.ConfirmOriginalReceived("am-user-1", DateTime.UtcNow);
        _db.SaveChanges();

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.SendAppraiserReminderAsync(order.Id));

        Assert.Equal("APPRAISER_REMINDER_NOT_ALLOWED", ex.ErrorCode);
    }

    [Fact]
    public async Task SendAppraiserReminderAsync_AuditRecordingThrows_StillReturnsResult()
    {
        var order = SeedOrder();

        _audit.RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("audit sink down")));

        var dto = await _sut.SendAppraiserReminderAsync(order.Id);

        Assert.Equal(1, dto.ReminderCount);
    }

    // ── ConfirmOriginalReceivedAsync additional tests ─────────────────────────

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_AlreadyConfirmed_ThrowsConflict()
    {
        // Originalna potvrda → Completed, druga potvrda treba ConflictException
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.ReadyForProcedure, DateTime.UtcNow);
        #pragma warning restore CS0618
        _db.SaveChanges();
        await _sut.ConfirmOriginalReceivedAsync(order.Id);  // prva potvrda uspijeva

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ConfirmOriginalReceivedAsync(order.Id));
        Assert.Equal("ORIGINAL_ALREADY_RECEIVED", ex.ErrorCode);
    }

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_StatusCompleted_ThrowsConflict()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.Completed, DateTime.UtcNow);
        #pragma warning restore CS0618
        _db.SaveChanges();

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ConfirmOriginalReceivedAsync(order.Id));
        Assert.Equal("ORIGINAL_ALREADY_RECEIVED", ex.ErrorCode);
    }

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_StatusAcceptedByCA_ThrowsInvalidStatusConflict()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.AcceptedByCA, DateTime.UtcNow);
        #pragma warning restore CS0618
        _db.SaveChanges();

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ConfirmOriginalReceivedAsync(order.Id));
        Assert.Equal("ORIGINAL_INVALID_STATUS", ex.ErrorCode);
    }

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_WithCAAndCOUsers_NotificationsSentTrue()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        // Walk through valid transitions to set AcceptedByCAUserId and CoApprovedByUserId
        order.ChangeStatus(AppraisalOrderStatus.SubmittedBySales, DateTime.UtcNow);
        #pragma warning restore CS0618
        order.AcceptByCA("ca-user-1", "CA User", DateTime.UtcNow);
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
        #pragma warning restore CS0618
        // ApproveByCO transitions from AppraisalReceived to ReadyForProcedure
        order.ApproveByCO("co-user-1", DateTime.UtcNow);
        _db.SaveChanges();

        var dto = await _sut.ConfirmOriginalReceivedAsync(order.Id);

        Assert.True(dto.NotificationsSent);
    }

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_MessageContainsClientNameAndCity()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.ReadyForProcedure, DateTime.UtcNow);
        #pragma warning restore CS0618
        _db.SaveChanges();

        var dto = await _sut.ConfirmOriginalReceivedAsync(order.Id);

        Assert.Contains("Petar Petrović", dto.Message);
        Assert.Contains("Sarajevo", dto.Message);
    }

    // ── SendAppraiserReminderAsync additional tests ──────────────────────────

    [Fact]
    public async Task SendAppraiserReminderAsync_MultipleReminders_IncrementCount()
    {
        var order = SeedOrder();

        var dto1 = await _sut.SendAppraiserReminderAsync(order.Id);
        Assert.Equal(1, dto1.ReminderCount);

        var dto2 = await _sut.SendAppraiserReminderAsync(order.Id);
        Assert.Equal(2, dto2.ReminderCount);

        var dto3 = await _sut.SendAppraiserReminderAsync(order.Id);
        Assert.Equal(3, dto3.ReminderCount);

        var reloaded = await _db.AppraisalOrders.FindAsync(order.Id);
        Assert.Equal(3, reloaded!.AppraiserReminderCount);
    }

    [Fact]
    public async Task SendAppraiserReminderAsync_OriginalAlreadyReceived_ThrowsConflict()
    {
        // Postavi na ReadyForProcedure → potvrdi original → OriginalReceivedAt popunjen → reminder nije dozvoljen
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.ReadyForProcedure, DateTime.UtcNow);
        #pragma warning restore CS0618
        _db.SaveChanges();
        await _sut.ConfirmOriginalReceivedAsync(order.Id);  // popunjava OriginalReceivedAt

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.SendAppraiserReminderAsync(order.Id));
        Assert.Equal("APPRAISER_REMINDER_NOT_ALLOWED", ex.ErrorCode);
    }

    [Fact]
    public async Task SendAppraiserReminderAsync_WithAppraiser_NotificationSentTrue()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.DocumentationApproved, DateTime.UtcNow);
        #pragma warning restore CS0618
        order.SelectAppraiser(42, DateTime.UtcNow);
        _db.SaveChanges();

        var dto = await _sut.SendAppraiserReminderAsync(order.Id);

        Assert.True(dto.NotificationSent);
    }

    [Fact]
    public async Task SendAppraiserReminderAsync_WithAppraiser_NotificationThrows_NotificationSentFalse()
    {
        var order = SeedOrder();
        #pragma warning disable CS0618
        order.ChangeStatus(AppraisalOrderStatus.DocumentationApproved, DateTime.UtcNow);
        #pragma warning restore CS0618
        order.SelectAppraiser(42, DateTime.UtcNow);
        _db.SaveChanges();

        _notificationService
            .NotifyUserAsync(Arg.Any<string>(), Arg.Any<string>(), Arg.Any<string>(),
                Arg.Any<string?>(), Arg.Any<string?>(), Arg.Any<bool>(), Arg.Any<string?>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("notify down")));

        var dto = await _sut.SendAppraiserReminderAsync(order.Id);

        Assert.False(dto.NotificationSent);
    }

    [Fact]
    public async Task SendAppraiserReminderAsync_MessageContainsReminderNumber()
    {
        var order = SeedOrder();

        var dto = await _sut.SendAppraiserReminderAsync(order.Id);

        Assert.Contains("Reminder #1", dto.Message);
    }

    [Fact]
    public async Task SendAppraiserReminderAsync_EmptyUserId_ThrowsForbidden()
    {
        _currentUser.UserId.Returns("  ");

        var order = SeedOrder();
        await Assert.ThrowsAsync<ForbiddenException>(() => _sut.SendAppraiserReminderAsync(order.Id));
    }
}
