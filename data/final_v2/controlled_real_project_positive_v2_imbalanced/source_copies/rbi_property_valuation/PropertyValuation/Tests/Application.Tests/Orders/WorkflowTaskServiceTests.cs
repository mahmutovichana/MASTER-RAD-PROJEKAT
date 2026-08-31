using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Tests.Helpers;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

public sealed class WorkflowTaskServiceTests : IDisposable
{
    private readonly ApplicationDbContext   _db;
    private readonly ICurrentUserService    _user;
    private readonly IAuditService          _audit;
    private readonly INotificationProvider  _notify;
    private readonly WorkflowTaskService    _sut;

    public WorkflowTaskServiceTests()
    {
        var opts = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w =>
                w.Ignore(Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;

        _db     = new ApplicationDbContext(opts);
        _user   = Substitute.For<ICurrentUserService>();
        _audit  = Substitute.For<IAuditService>();
        _notify = Substitute.For<INotificationProvider>();

        _user.UserId.Returns("user-ca-1");
        _user.IsAuthenticated.Returns(true);
        _user.Roles.Returns([AppRoles.KolateralAdministrator]);

        _sut = new WorkflowTaskService(
            _db, _user, _audit, _notify,
            Substitute.For<ILogger<WorkflowTaskService>>());
    }

    public void Dispose() => _db.Dispose();

    // ── Helpers ───────────────────────────────────────────────────────────────

    private async Task<AppraisalOrder> SeedOrderAsync(AppraisalOrderStatus status = AppraisalOrderStatus.SubmittedBySales)
    {
        var order = AppraisalOrder.Create(
            "PN-T-001", "Task Test", "Klijent", "FL", "0101985100129",
            "Kontakt", "061000000", null,
            "Sarajevo", "POS_SARAJEVO_CENTAR", "Adresa", "Obala 1",
            1, null, "user-am-1", AppRoles.AM, "Amar",
            "Dostava", "AM",
            workflowType: RBBH.CollateralAppraisal.Domain.Orders.WorkflowType.FizickaLica);
        order.ChangeStatus(status, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();
        return order;
    }

    private async Task<TaskItem> SeedTaskAsync(
        int orderId, TaskItemType type = TaskItemType.AcceptCAOrder,
        string assignedRole = AppRoles.KolateralAdministrator,
        string? assignedUserId = null)
    {
        var task = TaskItem.Create(orderId, type, "Test Task", null, assignedRole, assignedUserId: assignedUserId);
        _db.TaskItems.Add(task);
        await _db.SaveChangesAsync();
        return task;
    }

    // ══════════════════════════════════════════════════════════════════
    // GetMyTasksAsync
    // ══════════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetMyTasks_WhenNoTasks_ShouldReturnEmpty()
    {
        var result = await _sut.GetMyTasksAsync();

        result.Items.Should().BeEmpty();
        result.TotalCount.Should().Be(0);
    }

    [Fact]
    public async Task GetMyTasks_ShouldReturnRoleMatchedOpenTasks()
    {
        var order = await SeedOrderAsync();
        await SeedTaskAsync(order.Id, TaskItemType.AcceptCAOrder, AppRoles.KolateralAdministrator);

        var result = await _sut.GetMyTasksAsync();

        result.Items.Should().HaveCount(1);
    }

    [Fact]
    public async Task GetMyTasks_ShouldExcludeCompletedTasks()
    {
        var order = await SeedOrderAsync();
        var task  = await SeedTaskAsync(order.Id);
        task.Complete("user-ca-1", "Done", DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var result = await _sut.GetMyTasksAsync();

        result.Items.Should().BeEmpty("completed tasks ne smiju biti prikazani");
    }

    [Fact]
    public async Task GetMyTasks_Pagination_ShouldReturnCorrectPage()
    {
        var order = await SeedOrderAsync();
        for (var i = 0; i < 5; i++)
            await SeedTaskAsync(order.Id);

        var page1 = await _sut.GetMyTasksAsync(page: 1, pageSize: 2);
        var page2 = await _sut.GetMyTasksAsync(page: 2, pageSize: 2);

        page1.Items.Should().HaveCount(2);
        page2.Items.Should().HaveCount(2);
        page1.TotalCount.Should().Be(5);
    }

    // ══════════════════════════════════════════════════════════════════
    // AcceptTaskAsync
    // ══════════════════════════════════════════════════════════════════

    [Fact]
    public async Task AcceptTask_WhenNotFound_ShouldThrowNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.AcceptTaskAsync(99999));
    }

    [Fact]
    public async Task AcceptTask_WhenAlreadyLocked_ShouldThrowValidation()
    {
        var order = await SeedOrderAsync();
        var task  = await SeedTaskAsync(order.Id);
        task.Accept("some-other-user", DateTime.UtcNow); // zaključava ga
        await _db.SaveChangesAsync();

        await Assert.ThrowsAsync<ValidationException>(
            () => _sut.AcceptTaskAsync(task.Id));
    }

    [Fact]
    public async Task AcceptTask_WhenAlreadyCompleted_ShouldThrowValidation()
    {
        var order = await SeedOrderAsync();
        var task  = await SeedTaskAsync(order.Id);
        task.Complete("user-ca-1", "Done", DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await Assert.ThrowsAsync<ValidationException>(
            () => _sut.AcceptTaskAsync(task.Id));
    }

    [Fact]
    public async Task AcceptTask_ValidTask_ShouldLockAndReturnDto()
    {
        var order = await SeedOrderAsync();
        var task  = await SeedTaskAsync(order.Id);

        var result = await _sut.AcceptTaskAsync(task.Id);

        result.Should().NotBeNull();
        result.Id.Should().Be(task.Id);

        var updated = await _db.TaskItems.FirstAsync(t => t.Id == task.Id);
        updated.IsLocked.Should().BeTrue();
        updated.AssignedUserId.Should().Be("user-ca-1");
    }

    [Fact]
    public async Task AcceptTask_CaAcceptCAOrder_ShouldTransitionOrderToAcceptedByCA()
    {
        // Specijalni slučaj: CA prihvata AcceptCAOrder task → narudžba prelazi u AcceptedByCA
        var order = await SeedOrderAsync(AppraisalOrderStatus.SubmittedBySales);
        var task  = await SeedTaskAsync(order.Id, TaskItemType.AcceptCAOrder);

        await _sut.AcceptTaskAsync(task.Id);

        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        // WorkflowTaskService acceptuje task i odmah prelazi u DocumentationReviewInProgress
        updated.Status.Should().BeOneOf(
            AppraisalOrderStatus.AcceptedByCA,
            AppraisalOrderStatus.DocumentationReviewInProgress);
    }

    // ══════════════════════════════════════════════════════════════════
    // CompleteTaskAsync
    // ══════════════════════════════════════════════════════════════════

    [Fact]
    public async Task CompleteTask_WhenNotFound_ShouldThrowNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.CompleteTaskAsync(99999, null));
    }

    [Fact]
    public async Task CompleteTask_WhenAssignedToDifferentUser_ShouldThrowForbidden()
    {
        var order = await SeedOrderAsync();
        var task  = await SeedTaskAsync(order.Id, assignedUserId: "some-other-user");
        task.Accept("some-other-user", DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await Assert.ThrowsAsync<ForbiddenException>(
            () => _sut.CompleteTaskAsync(task.Id, "komentar"));
    }

    [Fact]
    public async Task CompleteTask_WhenAlreadyCompleted_ShouldThrowValidation()
    {
        var order = await SeedOrderAsync();
        var task  = await SeedTaskAsync(order.Id, assignedUserId: "user-ca-1");
        task.Accept("user-ca-1", DateTime.UtcNow);
        task.Complete("user-ca-1", "Završeno", DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await Assert.ThrowsAsync<ValidationException>(
            () => _sut.CompleteTaskAsync(task.Id, null));
    }

    [Fact]
    public async Task CompleteTask_UploadFinalAppraisalWithoutVisitDate_ShouldThrowValidation()
    {
        var order = await SeedOrderAsync(AppraisalOrderStatus.AppraisalInProgress);
        var task  = await SeedTaskAsync(order.Id, TaskItemType.UploadFinalAppraisal,
            AppRoles.Vjestak, "user-ca-1");
        task.Accept("user-ca-1", DateTime.UtcNow);
        await _db.SaveChangesAsync();

        // VisitDate nije postavljen na narudžbi
        await Assert.ThrowsAsync<ValidationException>(
            () => _sut.CompleteTaskAsync(task.Id, null));
    }

    [Fact]
    public async Task CompleteTask_ValidTask_ShouldMarkCompleted()
    {
        var order = await SeedOrderAsync();
        var task  = await SeedTaskAsync(order.Id, assignedUserId: "user-ca-1");
        task.Accept("user-ca-1", DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var result = await _sut.CompleteTaskAsync(task.Id, "Komentar završetka");

        result.Should().NotBeNull();
        var updated = await _db.TaskItems.FirstAsync(t => t.Id == task.Id);
        updated.Status.Should().Be(TaskItemStatus.Completed);
    }
}
