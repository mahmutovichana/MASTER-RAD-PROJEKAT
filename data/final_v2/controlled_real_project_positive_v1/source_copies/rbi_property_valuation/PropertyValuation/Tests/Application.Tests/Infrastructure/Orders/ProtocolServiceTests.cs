using Microsoft.EntityFrameworkCore;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Orders;

public sealed class ProtocolServiceTests : IDisposable
{
    private readonly ApplicationDbContext _db;
    private readonly ProtocolService      _sut;

    public ProtocolServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db  = new ApplicationDbContext(options);
        var currentUser = Substitute.For<ICurrentUserService>();
        currentUser.UserId.Returns("test-user");
        _sut = new ProtocolService(_db, currentUser);
    }

    public void Dispose() => _db.Dispose();

    private AppraisalOrder SeedOrder(string orderNumber, int? collateralTypeId = null, int? combinedTypeId = null)
    {
        var order = AppraisalOrder.Create(
            orderNumber, "Procjena - " + orderNumber, "Petar Petrović", "FL", "0101985100123",
            "Petar Petrović", "061-123-456", "petar@test.ba",
            "Sarajevo", "POS_SARAJEVO_CENTAR", "Titova 1", "Obala 1",
            collateralTypeId, combinedTypeId,
            "user-am-1", "AM", "Amina AM",
            "Amina Dostavljač", "Amar Primalac");
        _db.AppraisalOrders.Add(order);
        _db.SaveChanges();
        return order;
    }

    private OrderProtocolEntry SeedProtocolEntry(int orderId, int year, int sequence, DateTime generatedAt)
    {
        var entry = OrderProtocolEntry.Create(orderId, year, sequence, "user-co-1", generatedAt);
        _db.OrderProtocolEntries.Add(entry);
        _db.SaveChanges();
        return entry;
    }

    // ── GetByOrderIdAsync ──────────────────────────────────────────────────

    [Fact]
    public async Task GetByOrderIdAsync_ExistingEntry_ReturnsDtoWithOrderData()
    {
        var order = SeedOrder("2026-000001");
        var entry = SeedProtocolEntry(order.Id, 2026, 1, new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc));

        var dto = await _sut.GetByOrderIdAsync(order.Id);

        Assert.Equal(entry.Id, dto.Id);
        Assert.Equal(order.Id, dto.OrderId);
        Assert.Equal(order.OrderNumber, dto.OrderNumber);
        Assert.Equal(order.Title, dto.OrderTitle);
        Assert.Equal(entry.ProtocolNumber, dto.ProtocolNumber);
        Assert.Equal(entry.ProtocolYear, dto.ProtocolYear);
        Assert.Equal(entry.ProtocolSequence, dto.ProtocolSequence);
        Assert.Equal("Active", dto.Status);
        Assert.Equal(entry.GeneratedAt, dto.GeneratedAt);
        Assert.Equal(entry.GeneratedByUserId, dto.GeneratedByUserId);
        Assert.Equal(order.ClientName, dto.ClientName);
        Assert.Equal(order.City, dto.City);
        Assert.Equal(order.Branch, dto.Branch);
        Assert.Equal("Draft", dto.OrderStatus);
        Assert.Equal(0, dto.OrderStatusCode);
        Assert.Equal(order.ClientType, dto.ClientType);
        Assert.Equal(order.ClientIdentifier, dto.ClientIdentifier);
        Assert.Equal(order.ContactName, dto.ContactName);
        Assert.Equal(order.ContactPhone, dto.ContactPhone);
        Assert.Equal(order.PropertyAddress, dto.PropertyAddress);
        Assert.Equal(order.BranchAddress, dto.BranchAddress);
        Assert.Equal(order.CreatedByName, dto.CreatedByName);
        Assert.Equal(order.DeliveryContactName, dto.DeliveryContactName);
        Assert.Equal(order.AmRecipientName, dto.AmRecipientName);
        Assert.Null(dto.CollateralTypeLabel);
        Assert.Null(dto.CombinedCollateralTypeLabel);
    }

    [Fact]
    public async Task GetByOrderIdAsync_NonExistentEntry_ThrowsNotFoundException()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.GetByOrderIdAsync(999));
    }

    [Fact]
    public async Task GetByOrderIdAsync_OrderHasCollateralTypes_ResolvesLabelsFromCodebook()
    {
        var collateral = CodebookValue.Create("tipovi_kolaterala", "APP_STAN", "Stan", null, 10, "system-seed");
        var combined   = CodebookValue.Create("kombinovani_tipovi_kolaterala", "APP_STAN_I_GARAZA", "Stan i garaža", null, 10, "system-seed");
        _db.CodebookValues.Add(collateral);
        _db.CodebookValues.Add(combined);
        _db.SaveChanges();

        var order = SeedOrder("2026-000001", collateralTypeId: collateral.Id, combinedTypeId: combined.Id);
        SeedProtocolEntry(order.Id, 2026, 1, DateTime.UtcNow);

        var dto = await _sut.GetByOrderIdAsync(order.Id);

        Assert.Equal("Stan", dto.CollateralTypeLabel);
        Assert.Equal("Stan i garaža", dto.CombinedCollateralTypeLabel);
    }

    // ── GetProtocolListAsync ───────────────────────────────────────────────

    [Fact]
    public async Task GetProtocolListAsync_ReturnsItemsOrderedByGeneratedAtDescending()
    {
        var order1 = SeedOrder("2026-000001");
        var order2 = SeedOrder("2026-000002");
        SeedProtocolEntry(order1.Id, 2026, 1, new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc));
        SeedProtocolEntry(order2.Id, 2026, 2, new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc));

        var result = await _sut.GetProtocolListAsync();

        Assert.Equal(2, result.TotalCount);
        Assert.Equal(order2.OrderNumber, result.Items[0].OrderNumber);
        Assert.Equal(order1.OrderNumber, result.Items[1].OrderNumber);
    }

    [Fact]
    public async Task GetProtocolListAsync_Paging_ReturnsRequestedPage()
    {
        var order1 = SeedOrder("2026-000001");
        var order2 = SeedOrder("2026-000002");
        var order3 = SeedOrder("2026-000003");
        SeedProtocolEntry(order1.Id, 2026, 1, new DateTime(2026, 6, 1, 10, 0, 0, DateTimeKind.Utc));
        SeedProtocolEntry(order2.Id, 2026, 2, new DateTime(2026, 6, 2, 10, 0, 0, DateTimeKind.Utc));
        SeedProtocolEntry(order3.Id, 2026, 3, new DateTime(2026, 6, 3, 10, 0, 0, DateTimeKind.Utc));

        var result = await _sut.GetProtocolListAsync(page: 2, pageSize: 1);

        Assert.Equal(3, result.TotalCount);
        Assert.Single(result.Items);
        Assert.Equal(order2.OrderNumber, result.Items[0].OrderNumber);
        Assert.Equal(2, result.Page);
        Assert.Equal(1, result.PageSize);
    }

    [Fact]
    public async Task GetProtocolListAsync_NoEntries_ReturnsEmptyResult()
    {
        var result = await _sut.GetProtocolListAsync();

        Assert.Empty(result.Items);
        Assert.Equal(0, result.TotalCount);
    }
}
