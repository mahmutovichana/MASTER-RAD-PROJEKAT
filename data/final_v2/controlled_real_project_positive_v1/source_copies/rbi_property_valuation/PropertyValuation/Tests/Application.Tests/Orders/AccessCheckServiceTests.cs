#pragma warning disable CS0618
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

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

public sealed class AccessCheckServiceTests : IDisposable
{
    private readonly ApplicationDbContext _db;
    private readonly AccessCheckService _sut;

    public AccessCheckServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db = new ApplicationDbContext(options);
        var user = Substitute.For<ICurrentUserService>();
        user.UserId.Returns("co-user");
        user.Role.Returns("KolateralOficir");
        user.Roles.Returns(["KolateralOficir"]);
        user.IsAuthenticated.Returns(true);

        _sut = new AccessCheckService(
            _db, user,
            Substitute.For<INotificationProvider>(),
            Substitute.For<IAuditService>(),
            Substitute.For<ILogger<AccessCheckService>>());
    }

    private async Task<AppraisalOrder> SeedAsync(AppraisalOrderStatus status = AppraisalOrderStatus.AccessCheckRequested)
    {
        var order = AppraisalOrder.Create("NP-AC-1", "Test", "Klijent", "FL",
            null, null, null, null, "Sarajevo", null, null, null,
            null, null, "sales-user", "AM", null, null, null);
        order.ChangeStatus(status, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        if (status == AppraisalOrderStatus.AccessCheckRequested)
        {
            _db.TaskItems.Add(TaskItem.Create(order.Id, TaskItemType.AccessCheckCO,
                "Provjera pristupa", null, "KolateralOficir"));
            await _db.SaveChangesAsync();
        }

        return order;
    }

    [Fact]
    public async Task ApproveAccessAsync_ValidOrder_SetsApprovedStatus()
    {
        var order = await SeedAsync();
        var result = await _sut.ApproveAccessAsync(order.Id, "Pristup uredan");
        Assert.Contains("Approved", result.Status);
    }

    [Fact]
    public async Task RejectAccessAsync_ValidOrder_SetsRejectedStatus()
    {
        var order = await SeedAsync();
        var result = await _sut.RejectAccessAsync(order.Id, "Neuredan pristup");
        Assert.Contains("Rejected", result.Status);
    }

    [Fact]
    public async Task ApproveAccessAsync_WrongStatus_ThrowsConflict()
    {
        var order = await SeedAsync(AppraisalOrderStatus.Draft);
        await Assert.ThrowsAsync<ConflictException>(() => _sut.ApproveAccessAsync(order.Id, "ok"));
    }

    [Fact]
    public async Task ApproveAccessAsync_NotFound_ThrowsNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.ApproveAccessAsync(99999, "ok"));
    }

    // ── Additional ApproveAccessAsync tests ──────────────────────────────────

    [Fact]
    public async Task ApproveAccessAsync_CompletesAccessCheckTask()
    {
        var order = await SeedAsync();
        await _sut.ApproveAccessAsync(order.Id, "Pristup uredan");

        var task = await _db.TaskItems
            .FirstAsync(t => t.AppraisalOrderId == order.Id && t.TaskType == TaskItemType.AccessCheckCO);
        Assert.Equal(TaskItemStatus.Completed, task.Status);
        Assert.Equal("co-user", task.CompletedByUserId);
    }

    [Fact]
    public async Task ApproveAccessAsync_CreatesSelectAppraiserTask()
    {
        var order = await SeedAsync();
        await _sut.ApproveAccessAsync(order.Id, "Pristup uredan");

        var selectTask = await _db.TaskItems
            .FirstOrDefaultAsync(t => t.AppraisalOrderId == order.Id && t.TaskType == TaskItemType.SelectAppraiser);
        Assert.NotNull(selectTask);
        Assert.Contains("Odabir vještaka", selectTask!.Title);
    }

    [Fact]
    public async Task ApproveAccessAsync_WithNullComment_UsesDefaultComment()
    {
        var order = await SeedAsync();
        var result = await _sut.ApproveAccessAsync(order.Id, null);

        var task = await _db.TaskItems
            .FirstAsync(t => t.AppraisalOrderId == order.Id && t.TaskType == TaskItemType.AccessCheckCO);
        Assert.Contains("uredan", task.Comment!);
    }

    [Fact]
    public async Task ApproveAccessAsync_SetsCoDocumentationReviewStartedAt()
    {
        var order = await SeedAsync();
        await _sut.ApproveAccessAsync(order.Id, "ok");

        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        Assert.NotNull(updated.CoDocumentationReviewStartedAt);
    }

    // ── RejectAccessAsync tests ──────────────────────────────────────────────

    [Fact]
    public async Task RejectAccessAsync_WrongStatus_ThrowsConflict()
    {
        var order = await SeedAsync(AppraisalOrderStatus.Draft);
        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.RejectAccessAsync(order.Id, "Nepotpuno"));
        Assert.Equal("ACCESS_CHECK_INVALID_STATUS", ex.ErrorCode);
    }

    [Fact]
    public async Task RejectAccessAsync_NotFound_ThrowsNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.RejectAccessAsync(99999, "Nepotpuno"));
    }

    [Fact]
    public async Task RejectAccessAsync_EmptyComment_ThrowsValidation()
    {
        var order = await SeedAsync();
        await Assert.ThrowsAsync<ValidationException>(() => _sut.RejectAccessAsync(order.Id, ""));
    }

    [Fact]
    public async Task RejectAccessAsync_WhitespaceComment_ThrowsValidation()
    {
        var order = await SeedAsync();
        await Assert.ThrowsAsync<ValidationException>(() => _sut.RejectAccessAsync(order.Id, "   "));
    }

    [Fact]
    public async Task RejectAccessAsync_CompletesAccessCheckTask()
    {
        var order = await SeedAsync();
        await _sut.RejectAccessAsync(order.Id, "Nepotpuno");

        var task = await _db.TaskItems
            .FirstAsync(t => t.AppraisalOrderId == order.Id && t.TaskType == TaskItemType.AccessCheckCO);
        Assert.Equal(TaskItemStatus.Completed, task.Status);
    }

    [Fact]
    public async Task RejectAccessAsync_CreatesReviewDocumentationTask()
    {
        var order = await SeedAsync();
        await _sut.RejectAccessAsync(order.Id, "Nepotpuno");

        var reviewTask = await _db.TaskItems
            .FirstOrDefaultAsync(t => t.AppraisalOrderId == order.Id && t.TaskType == TaskItemType.ReviewDocumentation);
        Assert.NotNull(reviewTask);
        Assert.Contains("Pregled dokumentacije", reviewTask!.Title);
    }

    [Fact]
    public async Task RejectAccessAsync_NoActiveTask_ThrowsConflict()
    {
        var order = AppraisalOrder.Create("NP-AC-NT", "Test", "Klijent", "FL",
            null, null, null, null, "Sarajevo", null, null, null,
            null, null, "sales-user", "AM", null, null, null);
        order.ChangeStatus(AppraisalOrderStatus.AccessCheckRequested, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();
        // No task seeded

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.RejectAccessAsync(order.Id, "Nepotpuno"));
        Assert.Equal("ACCESS_CHECK_TASK_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task ApproveAccessAsync_NoActiveTask_ThrowsConflict()
    {
        var order = AppraisalOrder.Create("NP-AC-NT2", "Test", "Klijent", "FL",
            null, null, null, null, "Sarajevo", null, null, null,
            null, null, "sales-user", "AM", null, null, null);
        order.ChangeStatus(AppraisalOrderStatus.AccessCheckRequested, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();
        // No task seeded

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ApproveAccessAsync(order.Id, "ok"));
        Assert.Equal("ACCESS_CHECK_TASK_NOT_FOUND", ex.ErrorCode);
    }

    // ── Auth ─────────────────────────────────────────────────────────────────

    [Fact]
    public async Task ApproveAccessAsync_NotAuthenticated_ThrowsForbidden()
    {
        var userSub = Substitute.For<ICurrentUserService>();
        userSub.IsAuthenticated.Returns(false);
        userSub.UserId.Returns((string?)null);

        var sut = new AccessCheckService(
            _db, userSub,
            Substitute.For<INotificationProvider>(),
            Substitute.For<IAuditService>(),
            Substitute.For<ILogger<AccessCheckService>>());

        var order = await SeedAsync();
        await Assert.ThrowsAsync<ForbiddenException>(() => sut.ApproveAccessAsync(order.Id, "ok"));
    }

    [Fact]
    public async Task RejectAccessAsync_NotAuthenticated_ThrowsForbidden()
    {
        var userSub = Substitute.For<ICurrentUserService>();
        userSub.IsAuthenticated.Returns(false);
        userSub.UserId.Returns((string?)null);

        var sut = new AccessCheckService(
            _db, userSub,
            Substitute.For<INotificationProvider>(),
            Substitute.For<IAuditService>(),
            Substitute.For<ILogger<AccessCheckService>>());

        var order = await SeedAsync();
        await Assert.ThrowsAsync<ForbiddenException>(() => sut.RejectAccessAsync(order.Id, "Nepotpuno"));
    }

    // ── Notification edge cases ──────────────────────────────────────────────

    [Fact]
    public async Task ApproveAccessAsync_OrderWithCreator_NotifiesCreator()
    {
        var order = AppraisalOrder.Create("NP-AC-CR", "Test", "Klijent", "FL",
            null, null, null, null, "Sarajevo", null, null, null,
            null, null, "creator-user-id", "AM", null, null, null);
        order.ChangeStatus(AppraisalOrderStatus.AccessCheckRequested, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        _db.TaskItems.Add(TaskItem.Create(order.Id, TaskItemType.AccessCheckCO,
            "Provjera pristupa", null, "KolateralOficir"));
        await _db.SaveChangesAsync();

        var result = await _sut.ApproveAccessAsync(order.Id, "ok");

        // Approve should succeed
        Assert.Contains("Approved", result.Status);
    }

    [Fact]
    public async Task RejectAccessAsync_OrderWithoutCreator_FallsBackToRoleNotification()
    {
        var order = AppraisalOrder.Create("NP-AC-NC", "Test", "Klijent", "FL",
            null, null, null, null, "Sarajevo", null, null, null,
            null, null, "  ", "AM", null, null, null);
        order.ChangeStatus(AppraisalOrderStatus.AccessCheckRequested, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        _db.TaskItems.Add(TaskItem.Create(order.Id, TaskItemType.AccessCheckCO,
            "Provjera pristupa", null, "KolateralOficir"));
        await _db.SaveChangesAsync();

        var result = await _sut.RejectAccessAsync(order.Id, "Nepotpuno");

        Assert.Contains("Rejected", result.Status);
    }

    public void Dispose() => _db.Dispose();
}
