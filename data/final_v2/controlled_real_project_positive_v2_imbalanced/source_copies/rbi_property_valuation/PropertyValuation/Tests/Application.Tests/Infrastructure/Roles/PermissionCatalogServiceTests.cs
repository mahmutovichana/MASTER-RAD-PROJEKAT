using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Domain.Roles;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using RBBH.CollateralAppraisal.Infrastructure.Roles;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Roles;

public sealed class PermissionCatalogServiceTests : IDisposable
{
    private readonly ApplicationDbContext  _db;
    private readonly PermissionCatalogService _sut;

    public PermissionCatalogServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db  = new ApplicationDbContext(options);
        _sut = new PermissionCatalogService(_db);
    }

    public void Dispose() => _db.Dispose();

    private void SeedPermission(string code, string displayName, string module)
    {
        _db.PermissionDefinitions.Add(PermissionDefinition.Create(code, displayName, "Opis", module));
        _db.SaveChanges();
    }

    [Fact]
    public async Task GetAllAsync_ReturnsPermissionsOrderedByModuleThenDisplayName()
    {
        SeedPermission("orders.view", "View Orders", "Orders");
        SeedPermission("codebooks.view", "View Codebooks", "Codebooks");
        SeedPermission("orders.create", "Create Orders", "Orders");

        var result = await _sut.GetAllAsync();

        Assert.Equal(3, result.Count);
        Assert.Equal("Codebooks", result[0].Module);
        Assert.Equal("Orders", result[1].Module);
        Assert.Equal("Create Orders", result[1].DisplayName);
        Assert.Equal("Orders", result[2].Module);
        Assert.Equal("View Orders", result[2].DisplayName);
    }

    [Fact]
    public async Task GetByModuleAsync_ReturnsOnlyMatchingModuleOrderedByDisplayName()
    {
        SeedPermission("orders.view", "View Orders", "Orders");
        SeedPermission("orders.create", "Create Orders", "Orders");
        SeedPermission("codebooks.view", "View Codebooks", "Codebooks");

        var result = await _sut.GetByModuleAsync("Orders");

        Assert.Equal(2, result.Count);
        Assert.All(result, p => Assert.Equal("Orders", p.Module));
        Assert.Equal("Create Orders", result[0].DisplayName);
        Assert.Equal("View Orders", result[1].DisplayName);
    }

    [Fact]
    public async Task GetByModuleAsync_NoMatches_ReturnsEmpty()
    {
        SeedPermission("orders.view", "View Orders", "Orders");

        var result = await _sut.GetByModuleAsync("NonExistent");

        Assert.Empty(result);
    }
}
