#pragma warning disable CS0618
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

public sealed class OriginalAppraisalServiceTests : IDisposable
{
    private readonly ApplicationDbContext _db;
    private readonly OriginalAppraisalService _sut;

    public OriginalAppraisalServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db = new ApplicationDbContext(options);
        var user = Substitute.For<ICurrentUserService>();
        user.UserId.Returns("am-user");
        user.FullName.Returns("AM User");
        user.Role.Returns("AM");
        user.Roles.Returns(["AM"]);
        user.IsAuthenticated.Returns(true);

        _sut = new OriginalAppraisalService(
            _db, user,
            Substitute.For<INotificationService>(),
            Substitute.For<IAuditService>(),
            Substitute.For<ILogger<OriginalAppraisalService>>());
    }

    private async Task<AppraisalOrder> SeedAsync(AppraisalOrderStatus status = AppraisalOrderStatus.ReadyForProcedure)
    {
        var order = AppraisalOrder.Create("NP-OA-1", "Test", "Klijent", "FL",
            null, null, null, null, "Sarajevo", null, null, null,
            null, null, "am-user", "AM", null, null, null);
        order.ChangeStatus(status, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();
        return order;
    }

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_ValidOrder_SetsCompleted()
    {
        var order = await SeedAsync();
        var result = await _sut.ConfirmOriginalReceivedAsync(order.Id);
        Assert.Equal("Completed", result.Status);
        Assert.NotEqual(default, result.OriginalReceivedAt);
    }

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_NotFound_ThrowsNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.ConfirmOriginalReceivedAsync(99999));
    }

    [Fact]
    public async Task SendAppraiserReminderAsync_ValidOrder_IncrementsCount()
    {
        var order = await SeedAsync(AppraisalOrderStatus.AppraisalInProgress);
        var result = await _sut.SendAppraiserReminderAsync(order.Id);
        Assert.Equal(1, result.ReminderCount);
        Assert.NotEqual(default, result.LastReminderAt);
    }

    [Fact]
    public async Task SendAppraiserReminderAsync_NotFound_ThrowsNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.SendAppraiserReminderAsync(99999));
    }

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_WrongStatus_ThrowsConflict()
    {
        var order = await SeedAsync(AppraisalOrderStatus.Draft);
        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ConfirmOriginalReceivedAsync(order.Id));
        Assert.Equal("ORIGINAL_INVALID_STATUS", ex.ErrorCode);
    }

    [Fact]
    public async Task ConfirmOriginalReceivedAsync_AlreadyCompleted_ThrowsConflict()
    {
        var order = await SeedAsync(AppraisalOrderStatus.Completed);
        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ConfirmOriginalReceivedAsync(order.Id));
        Assert.Equal("ORIGINAL_ALREADY_RECEIVED", ex.ErrorCode);
    }

    [Fact]
    public async Task SendAppraiserReminderAsync_OriginalReceived_ThrowsConflict()
    {
        var order = await SeedAsync(AppraisalOrderStatus.ReadyForProcedure);
        order.ConfirmOriginalReceived("user-1", DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.SendAppraiserReminderAsync(order.Id));
        Assert.Equal("APPRAISER_REMINDER_NOT_ALLOWED", ex.ErrorCode);
    }

    [Fact]
    public async Task SendAppraiserReminderAsync_MultipleReminders_CountIncrements()
    {
        var order = await SeedAsync(AppraisalOrderStatus.AppraisalInProgress);

        var r1 = await _sut.SendAppraiserReminderAsync(order.Id);
        var r2 = await _sut.SendAppraiserReminderAsync(order.Id);

        Assert.Equal(1, r1.ReminderCount);
        Assert.Equal(2, r2.ReminderCount);
    }

    public void Dispose() => _db.Dispose();

    // ── Dodatni testovi za coverage gapove ────────────────────────────────────

    [Fact]
    public async Task DeliverOriginal_WhenWrongStatus_ShouldThrowConflict()
    {
        var order = await SeedAsync(AppraisalOrderStatus.Draft);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.DeliverOriginalToOfficeAsync(order.Id));

        Assert.Equal("ORIGINAL_DELIVERY_INVALID_STATUS", ex.ErrorCode);
    }

    [Fact]
    public async Task DeliverOriginal_WhenCOApproved_ShouldSucceed()
    {
        var order = await SeedAsync(AppraisalOrderStatus.COApproved);
        _db.TaskItems.Add(TaskItem.Create(
            order.Id, TaskItemType.DeliverOriginalToOffice, "Dostava", null, AppRoles.Vjestak));
        await _db.SaveChangesAsync();

        var result = await _sut.DeliverOriginalToOfficeAsync(order.Id);

        Assert.NotNull(result);
    }

    [Fact]
    public async Task ConfirmOriginal_WhenWrongStatus_ShouldThrowConflict()
    {
        var order = await SeedAsync(AppraisalOrderStatus.Draft);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ConfirmOriginalReceivedAsync(order.Id));

        Assert.Equal("ORIGINAL_INVALID_STATUS", ex.ErrorCode);
    }

    [Fact]
    public async Task SendReminder_WhenOriginalAlreadyReceived_ShouldThrowConflict()
    {
        var order = await SeedAsync(AppraisalOrderStatus.ReadyForProcedure);
        _db.Entry(order).Property("OriginalReceivedAt").CurrentValue = DateTime.UtcNow;
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SendAppraiserReminderAsync(order.Id));

        Assert.Equal("APPRAISER_REMINDER_NOT_ALLOWED", ex.ErrorCode);
    }

    [Fact]
    public async Task SendReminder_WhenValidOrder_ShouldSucceedWithoutAppraiser()
    {
        // Edge case: AppraiserId je null — samo DB record bez notifikacije
        var order = await SeedAsync(AppraisalOrderStatus.ReadyForProcedure);

        var result = await _sut.SendAppraiserReminderAsync(order.Id);

        Assert.NotNull(result);
    }
}
