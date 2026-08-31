using RBBH.CollateralAppraisal.Domain.Orders;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Domain;

public sealed class TaskItemTests
{
    private static TaskItem MakeTask() =>
        TaskItem.Create(
            orderId:      1,
            type:         TaskItemType.AcceptCAOrder,
            title:        "Prihvati narudžbu",
            description:  "opis",
            assignedRole: "CA");

    [Fact]
    public void Create_SetsStatusToOpen()
    {
        var task = MakeTask();

        Assert.Equal(TaskItemStatus.Open, task.Status);
        Assert.Equal(1,                   task.AppraisalOrderId);
        Assert.Equal(TaskItemType.AcceptCAOrder, task.TaskType);
        Assert.Equal("Prihvati narudžbu", task.Title);
        Assert.Equal("opis",              task.Description);
        Assert.Equal("CA",                task.AssignedRole);
        Assert.False(task.IsLocked);
    }

    [Fact]
    public void Create_WithDueDate_SetsDueDate()
    {
        var dueDate = DateTime.UtcNow.AddDays(7);

        var task = TaskItem.Create(1, TaskItemType.ReviewDocumentation, "Naslov", null, "CA", dueDate);

        Assert.Equal(dueDate, task.DueDate);
    }

    [Fact]
    public void Accept_SetsStatusAcceptedAndLocksTask()
    {
        var task = MakeTask();
        var now  = DateTime.UtcNow;

        task.Accept("user-1", now);

        Assert.Equal(TaskItemStatus.Accepted, task.Status);
        Assert.Equal("user-1", task.AcceptedByUserId);
        Assert.Equal(now,      task.AcceptedAt);
        Assert.Equal("user-1", task.AssignedUserId);
        Assert.True(task.IsLocked);
        Assert.Equal(now,      task.UpdatedAt);
    }

    [Fact]
    public void Complete_SetsStatusCompletedWithComment()
    {
        var task = MakeTask();
        var now  = DateTime.UtcNow;
        task.Accept("user-1", now);

        task.Complete("user-1", "Završeno", now.AddMinutes(5));

        Assert.Equal(TaskItemStatus.Completed, task.Status);
        Assert.Equal("user-1",   task.CompletedByUserId);
        Assert.Equal(now.AddMinutes(5), task.CompletedAt);
        Assert.Equal("Završeno", task.Comment);
    }

    [Fact]
    public void Return_SetsStatusReturnedAndUnlocksTask()
    {
        var task = MakeTask();
        var now  = DateTime.UtcNow;
        task.Accept("user-1", now);

        task.Return("Nedostaje dokumentacija", now.AddMinutes(5));

        Assert.Equal(TaskItemStatus.Returned, task.Status);
        Assert.Equal("Nedostaje dokumentacija", task.Comment);
        Assert.False(task.IsLocked);
    }

    [Fact]
    public void Cancel_SetsStatusCancelled()
    {
        var task = MakeTask();
        var now  = DateTime.UtcNow;

        task.Cancel(now);

        Assert.Equal(TaskItemStatus.Cancelled, task.Status);
        Assert.Equal(now, task.UpdatedAt);
    }
}
