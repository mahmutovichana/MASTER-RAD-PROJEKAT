using NSubstitute;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Domain.Enums;
using RBBH.TestAutomation.Core.Repositories;

namespace UnitTests.TestForge;

/// <summary>
/// Provjerava da GroupRepository emituje audit zapise kroz ITestForgeAuditWriter
/// za CREATE/UPDATE/DELETE. Writer je mockovan (NSubstitute) — provjeravamo poziv,
/// ne stvarni upis u audit_log (to radi DapperTestForgeAuditWriter nad pravom bazom).
/// </summary>
public class GroupRepositoryAuditTests
{
    private static TestGroup MakeGroup(string naziv, Guid? parentId = null) =>
        new() { Id = Guid.NewGuid(), Naziv = naziv, Tag = TestTag.Smoke, ParentGroupId = parentId };

    [Fact]
    public async Task AddAsync_WritesCreateAudit()
    {
        await using var db = TestForgeFixture.CreateInMemory();
        var audit = Substitute.For<ITestForgeAuditWriter>();
        var repo = new GroupRepository(db, audit);
        var g = MakeGroup("Root");

        await repo.AddAsync(g, "user-1", "User One");

        await audit.Received(1).WriteAsync(
            TestForgeAuditEntities.Group, g.Id, TestForgeAuditActions.Create,
            "user-1", "User One", Arg.Is<object?>(o => o == null), Arg.Any<object>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task UpdateAsync_WritesUpdateAudit_WithOldAndNew()
    {
        await using var db = TestForgeFixture.CreateInMemory();
        var audit = Substitute.For<ITestForgeAuditWriter>();
        var repo = new GroupRepository(db, audit);
        var g = MakeGroup("Old name");
        await repo.AddAsync(g, "u", "U");

        g.Naziv = "New name";
        await repo.UpdateAsync(g, "user-2", "User Two");

        await audit.Received(1).WriteAsync(
            TestForgeAuditEntities.Group, g.Id, TestForgeAuditActions.Update,
            "user-2", "User Two", Arg.Any<object>(), Arg.Any<object>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task DeleteAsync_WritesDeleteAudit()
    {
        await using var db = TestForgeFixture.CreateInMemory();
        var audit = Substitute.For<ITestForgeAuditWriter>();
        var repo = new GroupRepository(db, audit);
        var g = MakeGroup("Root");
        await repo.AddAsync(g, "u", "U");

        await repo.DeleteAsync(g.Id, "user-3", "User Three");

        await audit.Received(1).WriteAsync(
            TestForgeAuditEntities.Group, g.Id, TestForgeAuditActions.Delete,
            "user-3", "User Three", Arg.Any<object>(), Arg.Is<object?>(o => o == null), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task FailedAdd_DoesNotWriteAudit()
    {
        await using var db = TestForgeFixture.CreateInMemory();
        var audit = Substitute.For<ITestForgeAuditWriter>();
        var repo = new GroupRepository(db, audit);
        // 3-nivo grupa baca prije SaveChanges → audit se NE smije emitovati.
        var root = MakeGroup("Root");
        await repo.AddAsync(root, "u", "U");
        var child = MakeGroup("Child", root.Id);
        await repo.AddAsync(child, "u", "U");
        audit.ClearReceivedCalls();

        var grandchild = MakeGroup("Grandchild", child.Id);
        await Assert.ThrowsAsync<InvalidOperationException>(() => repo.AddAsync(grandchild, "u", "U"));

        await audit.DidNotReceive().WriteAsync(
            Arg.Any<string>(), Arg.Any<Guid>(), Arg.Any<string>(), Arg.Any<string>(),
            Arg.Any<string>(), Arg.Any<object>(), Arg.Any<object>(), Arg.Any<CancellationToken>());
    }
}
