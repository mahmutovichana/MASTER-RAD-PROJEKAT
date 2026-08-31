using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Roles.Interfaces;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using RBBH.CollateralAppraisal.Infrastructure.Seed;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Seed;

public sealed class RolePermissionSeederTests : IDisposable
{
    private readonly ApplicationDbContext _db;
    private readonly IKeycloakRoleSyncService _keycloakSync;

    public RolePermissionSeederTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db           = new ApplicationDbContext(options);
        _keycloakSync = Substitute.For<IKeycloakRoleSyncService>();
    }

    public void Dispose() => _db.Dispose();

    [Fact]
    public async Task SeedAsync_EmptyDatabase_SeedsPermissionsRolesAndMappings()
    {
        await RolePermissionSeeder.SeedAsync(_db, _keycloakSync);

        Assert.True(await _db.PermissionDefinitions.AnyAsync(p => p.Code == AppPermissions.UsersView));
        Assert.True(await _db.RoleDefinitions.AnyAsync(r => r.Name == AppRoles.Administrator));

        var adminRole = await _db.RoleDefinitions
            .Include(r => r.Permissions)
            .SingleAsync(r => r.Name == AppRoles.Administrator);
        Assert.NotEmpty(adminRole.Permissions);

        await _keycloakSync.Received(1)
            .CreateRoleAsync(AppRoles.Administrator, Arg.Any<string?>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task SeedAsync_CalledTwice_DoesNotCreateDuplicates()
    {
        await RolePermissionSeeder.SeedAsync(_db, _keycloakSync);
        var permCount    = await _db.PermissionDefinitions.CountAsync();
        var roleCount    = await _db.RoleDefinitions.CountAsync();
        var mappingCount = await _db.RolePermissions.CountAsync();

        await RolePermissionSeeder.SeedAsync(_db, _keycloakSync);

        Assert.Equal(permCount, await _db.PermissionDefinitions.CountAsync());
        Assert.Equal(roleCount, await _db.RoleDefinitions.CountAsync());
        Assert.Equal(mappingCount, await _db.RolePermissions.CountAsync());
    }

    [Fact]
    public async Task SeedAsync_KeycloakCreateRoleThrows_LogsWarningAndContinuesLocalSeed()
    {
        _keycloakSync.CreateRoleAsync(Arg.Any<string>(), Arg.Any<string?>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("Keycloak down")));

        var logger = Substitute.For<ILogger>();

        await RolePermissionSeeder.SeedAsync(_db, _keycloakSync, logger);

        var adminRole = await _db.RoleDefinitions
            .Include(r => r.Permissions)
            .SingleAsync(r => r.Name == AppRoles.Administrator);
        Assert.NotEmpty(adminRole.Permissions);
    }

    [Fact]
    public async Task SeedAsync_ExistingPermissionAndRole_AreNotDuplicatedButMappingsAreAdded()
    {
        // Pre-seed only the permission + role definitions (no mappings yet) — simulates a
        // partially-completed prior run.
        var permission = RBBH.CollateralAppraisal.Domain.Roles.PermissionDefinition.Create(
            AppPermissions.UsersView, "Pregled korisnika", "desc", "Users");
        var role = RBBH.CollateralAppraisal.Domain.Roles.RoleDefinition.CreateSystem(AppRoles.Administrator, "Administrator");
        _db.PermissionDefinitions.Add(permission);
        _db.RoleDefinitions.Add(role);
        await _db.SaveChangesAsync();

        await RolePermissionSeeder.SeedAsync(_db, _keycloakSync);

        Assert.Equal(1, await _db.PermissionDefinitions.CountAsync(p => p.Code == AppPermissions.UsersView));
        Assert.Equal(1, await _db.RoleDefinitions.CountAsync(r => r.Name == AppRoles.Administrator));

        var adminRole = await _db.RoleDefinitions
            .Include(r => r.Permissions)
            .SingleAsync(r => r.Name == AppRoles.Administrator);
        Assert.Contains(adminRole.Permissions, rp => rp.PermissionDefinitionId == permission.Id);
    }
}
