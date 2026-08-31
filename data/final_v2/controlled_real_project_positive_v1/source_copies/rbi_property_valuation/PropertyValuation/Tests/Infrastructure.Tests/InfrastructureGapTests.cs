// Infrastructure gap testovi — klase ekvivalencije za 0% servise
// Pokriva: BranchQueryService, CollateralTypeUsageChecker, DocumentTypeUsageChecker, UserRoleQueryService
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Security.Interfaces;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Application.Users.Models;
using RBBH.CollateralAppraisal.Domain.Branches;
using RBBH.CollateralAppraisal.Domain.Documents;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Branches;
using RBBH.CollateralAppraisal.Infrastructure.Codebooks.UsageCheckers;
using RBBH.CollateralAppraisal.Infrastructure.Tests.Helpers;
using RBBH.CollateralAppraisal.Infrastructure.Users;
using Xunit;

namespace RBBH.CollateralAppraisal.Infrastructure.Tests;

// ══════════════════════════════════════════════════════════════════════════════
// BranchQueryService
// ══════════════════════════════════════════════════════════════════════════════

public sealed class BranchQueryServiceTests
{
    // ── GetCitiesAsync ────────────────────────────────────────────────────────

    [Fact]
    public async Task GetCitiesAsync_EmptyDb_ReturnsEmptyList()
    {
        await using var db = TestDbFactory.Create();
        var svc = new BranchQueryService(db);
        var result = await svc.GetCitiesAsync();
        Assert.Empty(result);
    }

    [Fact]
    public async Task GetCitiesAsync_WithCities_ReturnsSortedByName()
    {
        await using var db = TestDbFactory.Create();
        db.Cities.AddRange(City.Create("Zenica"), City.Create("Banja Luka"), City.Create("Sarajevo"));
        await db.SaveChangesAsync();

        var svc = new BranchQueryService(db);
        var result = await svc.GetCitiesAsync();

        Assert.Equal(3, result.Count);
        Assert.Equal("Banja Luka", result[0].Name);
        Assert.Equal("Sarajevo",   result[1].Name);
        Assert.Equal("Zenica",     result[2].Name);
    }

    // ── GetBranchesAsync ──────────────────────────────────────────────────────

    [Fact]
    public async Task GetBranchesAsync_NoFilter_ReturnsAllBranches()
    {
        await using var db = TestDbFactory.Create();
        var city = City.Create("Sarajevo");
        db.Cities.Add(city);
        await db.SaveChangesAsync();

        db.Branches.AddRange(
            Branch.Create("CODE_A", "Branch A", "Addr A", city.Id),
            Branch.Create("CODE_B", "Branch B", "Addr B", city.Id));
        await db.SaveChangesAsync();

        var svc = new BranchQueryService(db);
        var result = await svc.GetBranchesAsync();

        Assert.Equal(2, result.Count);
    }

    [Fact]
    public async Task GetBranchesAsync_WithCityIdFilter_ReturnsOnlyThatCity()
    {
        await using var db = TestDbFactory.Create();
        var city1 = City.Create("Sarajevo");
        var city2 = City.Create("Mostar");
        db.Cities.AddRange(city1, city2);
        await db.SaveChangesAsync();

        db.Branches.AddRange(
            Branch.Create("CODE_SA", "Branch SA", "Addr SA", city1.Id),
            Branch.Create("CODE_MO", "Branch MO", "Addr MO", city2.Id));
        await db.SaveChangesAsync();

        var svc = new BranchQueryService(db);
        var result = await svc.GetBranchesAsync(cityId: city2.Id);

        Assert.Single(result);
        Assert.Equal("Branch MO", result[0].Name);
    }

    // ── GetBranchByIdAsync ────────────────────────────────────────────────────

    [Fact]
    public async Task GetBranchByIdAsync_Found_ReturnsBranchDto()
    {
        await using var db = TestDbFactory.Create();
        var city = City.Create("Tuzla");
        db.Cities.Add(city);
        await db.SaveChangesAsync();

        var branch = Branch.Create("CODE_T", "Branch T", "Addr T", city.Id);
        db.Branches.Add(branch);
        await db.SaveChangesAsync();

        var svc = new BranchQueryService(db);
        var result = await svc.GetBranchByIdAsync(branch.Id);

        Assert.NotNull(result);
        Assert.Equal("Branch T", result!.Name);
        Assert.Equal(city.Id, result.CityId);
    }

    [Fact]
    public async Task GetBranchByIdAsync_NotFound_ReturnsNull()
    {
        await using var db = TestDbFactory.Create();
        var svc = new BranchQueryService(db);
        var result = await svc.GetBranchByIdAsync(999);
        Assert.Null(result);
    }
}

// ══════════════════════════════════════════════════════════════════════════════
// CollateralTypeUsageChecker
// ══════════════════════════════════════════════════════════════════════════════

public sealed class CollateralTypeUsageCheckerTests
{
    [Fact]
    public async Task CheckAsync_NoUsage_ReturnsNull()
    {
        await using var db = TestDbFactory.Create();
        var checker = new CollateralTypeUsageChecker(db);
        Assert.Equal(RBBH.CollateralAppraisal.Application.Common.Constants.CodebookKeys.CollateralTypes, checker.CodebookKey);
        var result = await checker.CheckAsync(42);
        Assert.Null(result);
    }

    [Fact]
    public async Task CheckAsync_CollateralTypeUsed_ReturnsLocation()
    {
        await using var db = TestDbFactory.Create();
        var order = MakeOrder(collateralTypeId: 7);
        db.AppraisalOrders.Add(order);
        await db.SaveChangesAsync();

        var checker = new CollateralTypeUsageChecker(db);
        var result = await checker.CheckAsync(7);

        Assert.NotNull(result);
        Assert.Equal("Narudžbe", result!.Module);
        Assert.Equal(1, result.Count);
    }

    [Fact]
    public async Task CheckAsync_CombinedCollateralTypeUsed_ReturnsLocation()
    {
        await using var db = TestDbFactory.Create();
        var order = MakeOrder(collateralTypeId: 1, combinedCollateralTypeId: 9);
        db.AppraisalOrders.Add(order);
        await db.SaveChangesAsync();

        var checker = new CollateralTypeUsageChecker(db);
        var result = await checker.CheckAsync(9);

        Assert.NotNull(result);
        Assert.Equal(1, result!.Count);
    }

    private static AppraisalOrder MakeOrder(int? collateralTypeId = null, int? combinedCollateralTypeId = null)
        => AppraisalOrder.Create(
            "PN-001", "Test", "Klijent", "FL", null,
            null, null, null, null, null, null, null,
            collateralTypeId, combinedCollateralTypeId,
            "user-1", "AM", null, null, null);
}

// ══════════════════════════════════════════════════════════════════════════════
// DocumentTypeUsageChecker
// ══════════════════════════════════════════════════════════════════════════════

public sealed class DocumentTypeUsageCheckerTests
{
    [Fact]
    public async Task CheckAsync_NoUsage_ReturnsNull()
    {
        await using var db = TestDbFactory.Create();
        var checker = new DocumentTypeUsageChecker(db);
        Assert.Equal(RBBH.CollateralAppraisal.Application.Common.Constants.CodebookKeys.DocumentTypes, checker.CodebookKey);
        var result = await checker.CheckAsync(99);
        Assert.Null(result);
    }

    [Fact]
    public async Task CheckAsync_DocumentTypeUsed_ReturnsLocation()
    {
        await using var db = TestDbFactory.Create();
        var doc = Document.Create(1, documentTypeId: 3, "file.pdf", "file.pdf", "application/pdf", 1024, "/path", null);
        db.Documents.Add(doc);
        await db.SaveChangesAsync();

        var checker = new DocumentTypeUsageChecker(db);
        var result = await checker.CheckAsync(3);

        Assert.NotNull(result);
        Assert.Equal("Dokumenti", result!.Module);
        Assert.Equal(1, result.Count);
    }
}

// ══════════════════════════════════════════════════════════════════════════════
// UserRoleQueryService — klase ekvivalencije
// ══════════════════════════════════════════════════════════════════════════════

public sealed class UserRoleQueryServiceTests
{
    private readonly IUserRoleProvider _provider = Substitute.For<IUserRoleProvider>();
    private readonly IUserPermissionService _permSvc = Substitute.For<IUserPermissionService>();

    private UserRoleQueryService MakeSvc() => new(_provider, _permSvc);

    // ── GetUsersWithRolesAsync ────────────────────────────────────────────────

    [Fact]
    public async Task GetUsersWithRolesAsync_MapsAndReturnsPagedResult()
    {
        var raw = new PagedResult<UserRoleSourceItem>
        {
            Items = [new() { UserId = "u1", Username = "user1", Roles = [AppRoles.Unosnik] }],
            TotalCount = 1, Page = 1, PageSize = 20
        };
        _provider.GetUsersWithRolesAsync(Arg.Any<UserRoleListRequest>(), Arg.Any<CancellationToken>())
                 .Returns(Task.FromResult(raw));
        _permSvc.CurrentUserHasPermission(Arg.Any<string>()).Returns(true);

        var result = await MakeSvc().GetUsersWithRolesAsync(new UserRoleListRequest());

        Assert.Single(result.Items);
        Assert.Equal("user1", result.Items[0].Username);
        Assert.True(result.Items[0].CanManageRoles);
    }

    [Fact]
    public async Task GetUsersWithRolesAsync_NoManagePermission_CanManageRolesFalse()
    {
        var raw = new PagedResult<UserRoleSourceItem>
        {
            Items = [new() { UserId = "u1", Username = "user1", Roles = [] }],
            TotalCount = 1, Page = 1, PageSize = 20
        };
        _provider.GetUsersWithRolesAsync(Arg.Any<UserRoleListRequest>(), Arg.Any<CancellationToken>())
                 .Returns(Task.FromResult(raw));
        _permSvc.CurrentUserHasPermission(Arg.Any<string>()).Returns(false);

        var result = await MakeSvc().GetUsersWithRolesAsync(new UserRoleListRequest());

        Assert.False(result.Items[0].CanManageRoles);
    }

    // ── GetUserRolesAsync ─────────────────────────────────────────────────────

    [Fact]
    public async Task GetUserRolesAsync_UserNotFound_ReturnsNull()
    {
        _provider.GetUserWithRolesAsync("unknown", Arg.Any<CancellationToken>())
                 .Returns(Task.FromResult<UserRoleSourceItem?>(null));

        var result = await MakeSvc().GetUserRolesAsync("unknown");

        Assert.Null(result);
    }

    [Fact]
    public async Task GetUserRolesAsync_UserFound_ReturnsDetailWithEffectivePermissions()
    {
        var raw = new UserRoleSourceItem
        {
            UserId = "u1", Username = "admin", Roles = [AppRoles.Administrator],
            IsActive = true
        };
        _provider.GetUserWithRolesAsync("u1", Arg.Any<CancellationToken>())
                 .Returns(Task.FromResult<UserRoleSourceItem?>(raw));

        var result = await MakeSvc().GetUserRolesAsync("u1");

        Assert.NotNull(result);
        Assert.Equal("u1", result!.UserId);
        Assert.NotEmpty(result.EffectivePermissions);
    }

    [Fact]
    public async Task GetUserRolesAsync_UnknownRole_MarkedAsUnsupported()
    {
        var raw = new UserRoleSourceItem
        {
            UserId = "u2", Username = "strange", Roles = ["some-external-role"], IsActive = true
        };
        _provider.GetUserWithRolesAsync("u2", Arg.Any<CancellationToken>())
                 .Returns(Task.FromResult<UserRoleSourceItem?>(raw));

        var result = await MakeSvc().GetUserRolesAsync("u2");

        Assert.NotNull(result);
        Assert.Single(result!.Roles);
        Assert.False(result.Roles[0].IsSupported);
    }
}

// ══════════════════════════════════════════════════════════════════════════════
// ApplicationDbContext DbSet properties
// ══════════════════════════════════════════════════════════════════════════════

public sealed class ApplicationDbContextTests
{
    [Fact]
    public void AllDbSetProperties_AreAccessible()
    {
        using var db = TestDbFactory.Create();
        // Pristup svim DbSet propertiima koji nisu pokriven srodnim testovima
        _ = db.Cities;
        _ = db.Branches;
        _ = db.SharedDocuments;
        _ = db.OrderDeclinedAppraisers;
        _ = db.QuoteRequests;
        _ = db.DocumentTemplates;
        _ = db.AuditOutbox;
    }
}

// ══════════════════════════════════════════════════════════════════════════════
// Domain entity metode koje nisu pokrili API testovi
// ══════════════════════════════════════════════════════════════════════════════

public sealed class DomainEntityTests
{
    [Fact]
    public void Branch_Update_ChangesProperties()
    {
        var b = Branch.Create("CODE_A", "Old Name", "Old Addr", 1);
        b.Update("New Name", "New Addr", 2);
        Assert.Equal("New Name", b.Name);
        Assert.Equal("New Addr", b.Address);
        Assert.Equal(2, b.CityId);
    }

    [Fact]
    public void City_UpdateName_ChangesName()
    {
        var c = City.Create("Sarajevo");
        c.UpdateName("Banja Luka");
        Assert.Equal("Banja Luka", c.Name);
    }

    [Fact]
    public void Branch_Update_InvalidName_Throws()
    {
        var b = Branch.Create("CODE", "Name", "Addr", 1);
        Assert.Throws<ArgumentException>(() => b.Update("", "Addr", 1));
    }

    [Fact]
    public void City_UpdateName_Empty_Throws()
    {
        var c = City.Create("Sarajevo");
        Assert.Throws<ArgumentException>(() => c.UpdateName(""));
    }
}
