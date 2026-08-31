using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Roles.Requests;
using RBBH.CollateralAppraisal.Domain.Audit;
using RBBH.CollateralAppraisal.Infrastructure.Audit;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Audit;

public sealed class AuditQueryServiceTests : IDisposable
{
    private readonly ApplicationDbContext _db;
    private readonly AuditQueryService    _sut;

    public AuditQueryServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db  = new ApplicationDbContext(options);
        _sut = new AuditQueryService(_db);
    }

    public void Dispose() => _db.Dispose();

    private void SeedLog(
        DateTime timestamp,
        string   actorUserId = "user-1",
        string   actorUsername = "ivan",
        string   action = "ORDER_CREATED",
        string   module = "Orders",
        string   entityType = "AppraisalOrder",
        string?  entityKey = "1",
        string?  entityDisplayName = null,
        string   status = "Success",
        string   severity = "Info",
        string?  reason = null,
        string?  correlationId = null)
    {
        var log = AuditLog.Create(TestAuditLogData.Make(
            timestampUtc: timestamp,
            actorUserId: actorUserId,
            actorUsername: actorUsername,
            action: action,
            module: module,
            entityType: entityType,
            entityKey: entityKey,
            entityDisplayName: entityDisplayName,
            status: status,
            severity: severity,
            reason: reason,
            correlationId: correlationId));

        _db.AuditLogs.Add(log);
        _db.SaveChanges();
    }

    [Fact]
    public async Task QueryAsync_NoFilters_ReturnsAllOrderedByTimestampDescending()
    {
        SeedLog(new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc));
        SeedLog(new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc));

        var result = await _sut.QueryAsync(new AuditQueryRequest());

        Assert.Equal(2, result.TotalCount);
        Assert.Equal(2, result.Items.Count);
        Assert.True(result.Items[0].TimestampUtc > result.Items[1].TimestampUtc);
    }

    [Fact]
    public async Task QueryAsync_ActorUserIdFilter_ReturnsOnlyMatching()
    {
        SeedLog(new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc), actorUserId: "user-1");
        SeedLog(new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc), actorUserId: "user-2");

        var result = await _sut.QueryAsync(new AuditQueryRequest(ActorUserId: "user-2"));

        var item = Assert.Single(result.Items);
        Assert.Equal("user-2", item.ActorUserId);
    }

    [Fact]
    public async Task QueryAsync_ActorUsernameFilter_PartialMatch()
    {
        SeedLog(new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc), actorUsername: "ivan.horvat");
        SeedLog(new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc), actorUsername: "petar.peric");

        var result = await _sut.QueryAsync(new AuditQueryRequest(ActorUsername: "horvat"));

        var item = Assert.Single(result.Items);
        Assert.Equal("ivan.horvat", item.ActorUsername);
    }

    [Fact]
    public async Task QueryAsync_ModuleFilter_ReturnsOnlyMatching()
    {
        SeedLog(new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc), module: "Orders");
        SeedLog(new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc), module: "Codebooks");

        var result = await _sut.QueryAsync(new AuditQueryRequest(Module: "Codebooks"));

        var item = Assert.Single(result.Items);
        Assert.Equal("Codebooks", item.Module);
    }

    [Fact]
    public async Task QueryAsync_ActionFilter_ReturnsOnlyMatching()
    {
        SeedLog(new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc), action: "ORDER_CREATED");
        SeedLog(new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc), action: "ORDER_DELETED");

        var result = await _sut.QueryAsync(new AuditQueryRequest(Action: "ORDER_DELETED"));

        var item = Assert.Single(result.Items);
        Assert.Equal("ORDER_DELETED", item.Action);
    }

    [Fact]
    public async Task QueryAsync_EntityTypeFilter_ReturnsOnlyMatching()
    {
        SeedLog(new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc), entityType: "AppraisalOrder");
        SeedLog(new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc), entityType: "Codebook");

        var result = await _sut.QueryAsync(new AuditQueryRequest(EntityType: "Codebook"));

        var item = Assert.Single(result.Items);
        Assert.Equal("Codebook", item.EntityType);
    }

    [Fact]
    public async Task QueryAsync_EntityKeyFilter_ReturnsOnlyMatching()
    {
        SeedLog(new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc), entityKey: "1");
        SeedLog(new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc), entityKey: "2");

        var result = await _sut.QueryAsync(new AuditQueryRequest(EntityKey: "2"));

        var item = Assert.Single(result.Items);
        Assert.Equal("2", item.EntityKey);
    }

    [Fact]
    public async Task QueryAsync_StatusFilter_ReturnsOnlyMatching()
    {
        SeedLog(new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc), status: "Success");
        SeedLog(new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc), status: "Failure");

        var result = await _sut.QueryAsync(new AuditQueryRequest(Status: "Failure"));

        var item = Assert.Single(result.Items);
        Assert.Equal("Failure", item.Status);
    }

    [Fact]
    public async Task QueryAsync_SeverityFilter_ReturnsOnlyMatching()
    {
        SeedLog(new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc), severity: "Info");
        SeedLog(new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc), severity: "Warning");

        var result = await _sut.QueryAsync(new AuditQueryRequest(Severity: "Warning"));

        var item = Assert.Single(result.Items);
        Assert.Equal("Warning", item.Severity);
    }

    [Fact]
    public async Task QueryAsync_DateRangeFilter_ReturnsOnlyWithinRangeInclusive()
    {
        SeedLog(new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc), action: "DAY1");
        SeedLog(new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc), action: "DAY2");
        SeedLog(new DateTime(2026, 6, 3, 10, 0, 0, DateTimeKind.Utc), action: "DAY3");

        var result = await _sut.QueryAsync(new AuditQueryRequest(
            From: new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc),
            To:   new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc)));

        var item = Assert.Single(result.Items);
        Assert.Equal("DAY2", item.Action);
    }

    [Fact]
    public async Task QueryAsync_SearchFilter_MatchesAction()
    {
        SeedLog(new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc), action: "ORDER_CREATED");
        SeedLog(new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc), action: "ORDER_DELETED");

        var result = await _sut.QueryAsync(new AuditQueryRequest(Search: "created"));

        var item = Assert.Single(result.Items);
        Assert.Equal("ORDER_CREATED", item.Action);
    }

    [Fact]
    public async Task QueryAsync_SearchFilter_MatchesEntityDisplayName()
    {
        SeedLog(new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc), entityDisplayName: "Narudžba #123");
        SeedLog(new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc), entityDisplayName: "Narudžba #456");

        var result = await _sut.QueryAsync(new AuditQueryRequest(Search: "#123"));

        var item = Assert.Single(result.Items);
        Assert.Equal("Narudžba #123", item.EntityDisplayName);
    }

    [Fact]
    public async Task QueryAsync_SearchFilter_MatchesReason()
    {
        SeedLog(new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc), reason: "Workflow transition");
        SeedLog(new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc), reason: "Manual override");

        var result = await _sut.QueryAsync(new AuditQueryRequest(Search: "override"));

        var item = Assert.Single(result.Items);
        Assert.Equal("Manual override", item.Reason);
    }

    [Fact]
    public async Task QueryAsync_SearchFilter_MatchesCorrelationId()
    {
        SeedLog(new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc), correlationId: "corr-aaa");
        SeedLog(new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc), correlationId: "corr-bbb");

        var result = await _sut.QueryAsync(new AuditQueryRequest(Search: "bbb"));

        var item = Assert.Single(result.Items);
        Assert.Equal("corr-bbb", item.CorrelationId);
    }

    [Fact]
    public async Task QueryAsync_PageSizeBelowMinimum_ClampedToOne()
    {
        SeedLog(new DateTime(2026, 6, 1, 8, 0, 0, DateTimeKind.Utc));
        SeedLog(new DateTime(2026, 6, 2, 8, 0, 0, DateTimeKind.Utc));
        SeedLog(new DateTime(2026, 6, 3, 8, 0, 0, DateTimeKind.Utc));

        var result = await _sut.QueryAsync(new AuditQueryRequest(PageSize: 0));

        Assert.Equal(3, result.TotalCount);
        Assert.Equal(1, result.PageSize);
        Assert.Single(result.Items);
    }

    [Fact]
    public async Task QueryAsync_PageBelowMinimum_ClampedToOne()
    {
        SeedLog(new DateTime(2026, 6, 1, 8, 0, 0, DateTimeKind.Utc));

        var result = await _sut.QueryAsync(new AuditQueryRequest(Page: 0));

        Assert.Equal(1, result.Page);
    }

    [Fact]
    public async Task QueryAsync_Paging_ReturnsRequestedPage()
    {
        SeedLog(new DateTime(2026, 6, 1, 8, 0, 0, DateTimeKind.Utc), action: "A1");
        SeedLog(new DateTime(2026, 6, 2, 8, 0, 0, DateTimeKind.Utc), action: "A2");
        SeedLog(new DateTime(2026, 6, 3, 8, 0, 0, DateTimeKind.Utc), action: "A3");

        var result = await _sut.QueryAsync(new AuditQueryRequest(Page: 2, PageSize: 1));

        Assert.Equal(3, result.TotalCount);
        var item = Assert.Single(result.Items);
        Assert.Equal("A2", item.Action);
    }
}
