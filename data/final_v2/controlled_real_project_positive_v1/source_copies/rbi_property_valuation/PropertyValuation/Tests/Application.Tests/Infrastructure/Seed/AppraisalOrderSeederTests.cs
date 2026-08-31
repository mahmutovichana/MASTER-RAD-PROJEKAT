using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Application.Users.Models;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using RBBH.CollateralAppraisal.Infrastructure.Seed;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Seed;

public sealed class AppraisalOrderSeederTests : IDisposable
{
    private readonly ApplicationDbContext _db;
    private readonly IFileStorageProvider _fileStorage;
    private readonly IUserRoleProvider _userRoleProvider;

    public AppraisalOrderSeederTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db               = new ApplicationDbContext(options);
        _fileStorage      = Substitute.For<IFileStorageProvider>();
        _userRoleProvider = Substitute.For<IUserRoleProvider>();

        _fileStorage.SaveAsync(Arg.Any<Stream>(), Arg.Any<string>(), Arg.Any<string>(), Arg.Any<CancellationToken>())
            .Returns(new FileStorageResult("appraisal-orders/1/finalna-procjena.pdf", 1024));
    }

    public void Dispose() => _db.Dispose();

    private Task SeedAsync(ILogger? logger = null)
        => AppraisalOrderSeeder.SeedAsync(_db, _fileStorage, _userRoleProvider, logger);

    [Fact]
    public async Task SeedAsync_EmptyDatabase_SeedsPnOrdersWithFinalAppraisalDocument()
    {
        await SeedAsync();

        var order1 = await _db.AppraisalOrders.SingleAsync(o => o.OrderNumber == "PN-2026-001");
        Assert.Equal(AppraisalOrderStatus.AppraisalReceived, order1.Status);
        Assert.NotNull(order1.FinalAppraisalDocumentId);

        var document = await _db.Documents.SingleAsync(d => d.AppraisalOrderId == order1.Id);
        Assert.Equal(order1.FinalAppraisalDocumentId, document.Id);
        Assert.Equal("application/pdf", document.ContentType);

        var order2 = await _db.AppraisalOrders.SingleAsync(o => o.OrderNumber == "PN-2026-002");
        Assert.Equal(AppraisalOrderStatus.AcceptedByCA, order2.Status);

        await _fileStorage.Received(1).SaveAsync(
            Arg.Any<Stream>(), Arg.Any<string>(), Arg.Any<string>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task SeedAsync_EmptyDatabase_SeedsDemoOrdersWithMarker()
    {
        await SeedAsync();

        var demoOrders = await _db.AppraisalOrders
            .Where(o => o.InternalNote == "Demo podaci za testiranje (seed).")
            .ToListAsync();

        Assert.Equal(12, demoOrders.Count);
        Assert.All(demoOrders, o => Assert.StartsWith("PN-", o.OrderNumber));
    }

    [Fact]
    public async Task SeedAsync_CalledTwice_DoesNotDuplicateOrdersOrDocuments()
    {
        await SeedAsync();
        var orderCountAfterFirst    = await _db.AppraisalOrders.CountAsync();
        var documentCountAfterFirst = await _db.Documents.CountAsync();

        await SeedAsync();

        Assert.Equal(orderCountAfterFirst, await _db.AppraisalOrders.CountAsync());
        Assert.Equal(documentCountAfterFirst, await _db.Documents.CountAsync());
        await _fileStorage.Received(1).SaveAsync(
            Arg.Any<Stream>(), Arg.Any<string>(), Arg.Any<string>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task SeedAsync_UserRoleProviderReturnsUser_UsesResolvedUserIdAsCreator()
    {
        _userRoleProvider.GetUsersWithRolesAsync(
                Arg.Is<UserRoleListRequest>(r => r.Role == AppRoles.AM), Arg.Any<CancellationToken>())
            .Returns(new PagedResult<UserRoleSourceItem>
            {
                Items      = [new UserRoleSourceItem { UserId = "prodaja-real-1", Username = "prodaja.real" }],
                TotalCount = 1,
                Page       = 1,
                PageSize   = 1
            });

        await SeedAsync();

        var order1 = await _db.AppraisalOrders.SingleAsync(o => o.OrderNumber == "PN-2026-001");
        Assert.Equal("prodaja-real-1", order1.CreatedByUserId);
    }

    [Fact]
    public async Task SeedAsync_UserRoleProviderThrows_FallsBackToDefaultUserIdAndLogsWarning()
    {
        _userRoleProvider.GetUsersWithRolesAsync(Arg.Any<UserRoleListRequest>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException<PagedResult<UserRoleSourceItem>>(new InvalidOperationException("down")));

        var logger = Substitute.For<ILogger>();

        await SeedAsync(logger);

        var order1 = await _db.AppraisalOrders.SingleAsync(o => o.OrderNumber == "PN-2026-001");
        Assert.Equal("seed-am-user", order1.CreatedByUserId);
        Assert.Equal("seed-ca-user", order1.AcceptedByCAUserId);
        Assert.NotEmpty(logger.ReceivedCalls());
    }

    [Fact]
    public async Task SeedAsync_UserRoleProviderReturnsEmptyResult_FallsBackToDefaultUserId()
    {
        _userRoleProvider.GetUsersWithRolesAsync(Arg.Any<UserRoleListRequest>(), Arg.Any<CancellationToken>())
            .Returns(PagedResult<UserRoleSourceItem>.Empty(1, 1));

        await SeedAsync();

        var order1 = await _db.AppraisalOrders.SingleAsync(o => o.OrderNumber == "PN-2026-001");
        Assert.Equal("seed-am-user", order1.CreatedByUserId);
    }
}
