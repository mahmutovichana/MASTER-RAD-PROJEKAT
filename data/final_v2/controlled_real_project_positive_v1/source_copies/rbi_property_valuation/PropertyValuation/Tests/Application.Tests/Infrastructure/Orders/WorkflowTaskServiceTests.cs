using Microsoft.EntityFrameworkCore;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Notifications;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Orders;

public sealed class WorkflowTaskServiceTests : IDisposable
{
    private readonly ApplicationDbContext _db;
    private readonly ICurrentUserService  _user;
    private readonly IAuditService        _audit;
    private readonly WorkflowTaskService  _sut;

    public WorkflowTaskServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db    = new ApplicationDbContext(options);
        _user  = Substitute.For<ICurrentUserService>();
        _audit = Substitute.For<IAuditService>();

        _user.UserId.Returns("user-am-1");
        _user.FullName.Returns("Test User");
        _user.Roles.Returns(["AM"]);

        _sut = new WorkflowTaskService(_db, _user, _audit, 
    Substitute.For<INotificationProvider>(),
    Substitute.For<ILogger<WorkflowTaskService>>());
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

    private TaskItem SeedTask(
        int orderId,
        TaskItemType taskType = TaskItemType.ReviewDocumentation,
        string? assignedRole = "AM",
        DateTime? dueDate = null)
    {
        var task = TaskItem.Create(orderId, taskType, "Task title", "Task desc", assignedRole, dueDate);
        _db.TaskItems.Add(task);
        _db.SaveChanges();
        return task;
    }

    // ── GetMyTasksAsync ────────────────────────────────────────────────────

    [Fact]
    public async Task GetMyTasksAsync_TaskAcceptedByCurrentUser_IsIncluded()
    {
        var order = SeedOrder();
        var task  = SeedTask(order.Id, assignedRole: "CA");
        task.Accept("user-am-1", DateTime.UtcNow);
        _db.SaveChanges();

        var result = await _sut.GetMyTasksAsync();

        Assert.Single(result.Items);
        Assert.Equal(task.Id, result.Items[0].Id);
        Assert.Equal("Accepted", result.Items[0].Status);
    }

    [Fact]
    public async Task GetMyTasksAsync_OpenTaskAssignedToUserRole_IsIncluded()
    {
        var order = SeedOrder();
        var task  = SeedTask(order.Id, assignedRole: "AM");

        var result = await _sut.GetMyTasksAsync();

        Assert.Single(result.Items);
        Assert.Equal(task.Id, result.Items[0].Id);
        Assert.Equal(order.OrderNumber, result.Items[0].OrderNumber);
    }

    [Fact]
    public async Task GetMyTasksAsync_OpenTaskAssignedToOtherRole_IsExcluded()
    {
        var order = SeedOrder();
        SeedTask(order.Id, assignedRole: "CO");

        var result = await _sut.GetMyTasksAsync();

        Assert.Empty(result.Items);
    }

    [Fact]
    public async Task GetMyTasksAsync_CancelledTask_IsExcludedEvenIfRoleMatches()
    {
        var order = SeedOrder();
        var task  = SeedTask(order.Id, assignedRole: "AM");
        task.Cancel(DateTime.UtcNow);
        _db.SaveChanges();

        var result = await _sut.GetMyTasksAsync();

        Assert.Empty(result.Items);
    }

    [Fact]
    public async Task GetMyTasksAsync_CompletedTask_IsExcludedEvenIfAssignedToUser()
    {
        var order = SeedOrder();
        var task  = SeedTask(order.Id, assignedRole: "CA");
        task.Accept("user-am-1", DateTime.UtcNow);
        task.Complete("user-am-1", "done", DateTime.UtcNow);
        _db.SaveChanges();

        var result = await _sut.GetMyTasksAsync();

        Assert.Empty(result.Items);
    }

    [Fact]
    public async Task GetMyTasksAsync_OrderingAndPaging_OrdersByDueDateAscending()
    {
        var order = SeedOrder();
        var taskA = SeedTask(order.Id, assignedRole: "AM", dueDate: new DateTime(2026, 6, 20, 0, 0, 0, DateTimeKind.Utc));
        var taskB = SeedTask(order.Id, assignedRole: "AM", dueDate: new DateTime(2026, 6, 10, 0, 0, 0, DateTimeKind.Utc));
        var taskC = SeedTask(order.Id, assignedRole: "AM", dueDate: new DateTime(2026, 6, 15, 0, 0, 0, DateTimeKind.Utc));

        var page1 = await _sut.GetMyTasksAsync(page: 1, pageSize: 2);
        var page2 = await _sut.GetMyTasksAsync(page: 2, pageSize: 2);

        Assert.Equal(3, page1.TotalCount);
        Assert.Equal(2, page1.Items.Count);
        Assert.Equal(taskB.Id, page1.Items[0].Id);
        Assert.Equal(taskC.Id, page1.Items[1].Id);
        Assert.Single(page2.Items);
        Assert.Equal(taskA.Id, page2.Items[0].Id);
    }

    // ── AcceptTaskAsync ────────────────────────────────────────────────────

    [Fact]
    public async Task AcceptTaskAsync_OpenTask_AcceptsAndReturnsDto()
    {
        var order = SeedOrder();
        var task  = SeedTask(order.Id, assignedRole: "AM");

        var dto = await _sut.AcceptTaskAsync(task.Id);

        Assert.Equal("Accepted", dto.Status);
        Assert.Equal("user-am-1", dto.AcceptedByUserId);
        Assert.True(dto.IsLocked);
        Assert.NotNull(dto.AcceptedAt);
    }

    [Fact]
    public async Task AcceptTaskAsync_TaskNotFound_ThrowsNotFoundException()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.AcceptTaskAsync(999));
    }

    [Fact]
    public async Task AcceptTaskAsync_LockedTask_ThrowsValidationException()
    {
        var order = SeedOrder();
        var task  = SeedTask(order.Id, assignedRole: "AM");
        task.Accept("other-user", DateTime.UtcNow);
        _db.SaveChanges();

        await Assert.ThrowsAsync<ValidationException>(() => _sut.AcceptTaskAsync(task.Id));
    }

    [Fact]
    public async Task AcceptTaskAsync_NonOpenStatus_ThrowsValidationException()
    {
        var order = SeedOrder();
        var task  = SeedTask(order.Id, assignedRole: "AM");
        task.Cancel(DateTime.UtcNow);
        _db.SaveChanges();

        await Assert.ThrowsAsync<ValidationException>(() => _sut.AcceptTaskAsync(task.Id));
    }

    // ── CompleteTaskAsync ──────────────────────────────────────────────────

    [Fact]
    public async Task CompleteTaskAsync_TaskNotFound_ThrowsNotFoundException()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.CompleteTaskAsync(999, null));
    }

    [Fact]
    public async Task CompleteTaskAsync_NotAssignedUser_ThrowsForbiddenException()
    {
        var order = SeedOrder();
        var task  = SeedTask(order.Id, assignedRole: "AM");
        task.Accept("other-user", DateTime.UtcNow);
        _db.SaveChanges();

        await Assert.ThrowsAsync<ForbiddenException>(() => _sut.CompleteTaskAsync(task.Id, "komentar"));
    }

    [Fact]
    public async Task CompleteTaskAsync_NonCaTask_CompletesWithoutAudit()
    {
        var order = SeedOrder();
        var task  = SeedTask(order.Id, taskType: TaskItemType.ReviewDocumentation, assignedRole: "AM");
        task.Accept("user-am-1", DateTime.UtcNow);
        _db.SaveChanges();

        var dto = await _sut.CompleteTaskAsync(task.Id, "gotovo");

        Assert.Equal("Completed", dto.Status);
        Assert.Equal("gotovo", dto.Comment);
        Assert.Equal("user-am-1", dto.CompletedByUserId);
        await _audit.Received(1).RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>());
    }

    // CA prihvat narudžbe je vezan za AcceptTaskAsync (prihvat AcceptCAOrder taska),
    // ne za CompleteTaskAsync — prihvat pomjera narudžbu u AcceptedByCA pa odmah u
    // pregled dokumentacije (DocumentationReviewInProgress) i bilježi audit.
    [Fact]
    public async Task AcceptTaskAsync_CaAcceptanceTask_AcceptsOrderAndRecordsAudit()
    {
        var order = SeedOrder();
        order.Submit(DateTime.UtcNow);   // narudžba mora biti SubmittedBySales da CA prihvat prođe
        var task  = SeedTask(order.Id, taskType: TaskItemType.AcceptCAOrder, assignedRole: "CA");
        _db.SaveChanges();

        var dto = await _sut.AcceptTaskAsync(task.Id);

        // Prihvat task se zatvara (Completed), narudžba prelazi u pregled dokumentacije.
        Assert.Equal("Completed", dto.Status);

        var reloadedOrder = await _db.AppraisalOrders.FindAsync(order.Id);
        Assert.Equal(AppraisalOrderStatus.DocumentationReviewInProgress, reloadedOrder!.Status);
        Assert.Equal("user-am-1", reloadedOrder.AcceptedByCAUserId);

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.OrderAcceptedByCA && e.EntityKey == order.Id.ToString()),
            Arg.Any<CancellationToken>());
    }
}
