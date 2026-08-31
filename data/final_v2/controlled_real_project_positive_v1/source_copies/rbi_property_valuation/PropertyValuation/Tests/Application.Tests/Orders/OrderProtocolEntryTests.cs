using RBBH.CollateralAppraisal.Domain.Orders;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

public sealed class OrderProtocolEntryTests
{
    // ── Happy path ────────────────────────────────────────────────────────────

    [Fact]
    public void Create_GeneratesCorrectProtocolNumber()
    {
        var now      = new DateTime(2026, 6, 9, 10, 0, 0, DateTimeKind.Utc);
        var protocol = OrderProtocolEntry.Create(1, 2026, 1, "user-1", now);

        Assert.Equal("2026/00001", protocol.ProtocolNumber);
    }

    [Fact]
    public void Create_PadsSequenceTo5Digits()
    {
        var now = DateTime.UtcNow;

        Assert.Equal("2026/00042", OrderProtocolEntry.Create(1, 2026, 42,    "u", now).ProtocolNumber);
        Assert.Equal("2026/00999", OrderProtocolEntry.Create(1, 2026, 999,   "u", now).ProtocolNumber);
        Assert.Equal("2026/10000", OrderProtocolEntry.Create(1, 2026, 10000, "u", now).ProtocolNumber);
    }

    [Fact]
    public void Create_SetsStatusToActive()
    {
        var protocol = OrderProtocolEntry.Create(1, 2026, 1, "user-1", DateTime.UtcNow);
        Assert.Equal(ProtocolStatus.Active, protocol.Status);
    }

    [Fact]
    public void Create_SetsYearAndSequence()
    {
        var protocol = OrderProtocolEntry.Create(5, 2026, 7, "user-99", DateTime.UtcNow);

        Assert.Equal(5,        protocol.OrderId);
        Assert.Equal(2026,     protocol.ProtocolYear);
        Assert.Equal(7,        protocol.ProtocolSequence);
        Assert.Equal("user-99", protocol.GeneratedByUserId);
    }

    // ── Cancel ────────────────────────────────────────────────────────────────

    [Fact]
    public void Cancel_ChangesStatusToCancelled()
    {
        var now      = DateTime.UtcNow;
        var protocol = OrderProtocolEntry.Create(1, 2026, 1, "user-1", now);

        protocol.Cancel(now.AddMinutes(5));

        Assert.Equal(ProtocolStatus.Cancelled, protocol.Status);
    }
}
