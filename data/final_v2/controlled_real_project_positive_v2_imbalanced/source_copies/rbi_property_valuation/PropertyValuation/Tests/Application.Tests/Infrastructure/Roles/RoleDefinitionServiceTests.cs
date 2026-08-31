using System.Net.Http;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Roles.Interfaces;
using RBBH.CollateralAppraisal.Application.Roles.Requests;
using RBBH.CollateralAppraisal.Domain.Roles;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using RBBH.CollateralAppraisal.Infrastructure.Roles;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Roles;

public sealed class RoleDefinitionServiceTests : IDisposable
{
    private readonly ApplicationDbContext     _db;
    private readonly ICurrentUserService      _currentUser;
    private readonly IAuditService            _audit;
    private readonly IKeycloakRoleSyncService _keycloakSync;
    private readonly IMemoryCache             _cache;
    private readonly RoleDefinitionService    _sut;

    public RoleDefinitionServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db = new ApplicationDbContext(options);

        _currentUser  = Substitute.For<ICurrentUserService>();
        _audit        = Substitute.For<IAuditService>();
        _keycloakSync = Substitute.For<IKeycloakRoleSyncService>();
        _cache        = Substitute.For<IMemoryCache>();
        _currentUser.UserId.Returns("user-1");

        _sut = new RoleDefinitionService(
            _db, _currentUser, _audit, _keycloakSync, _cache, Substitute.For<ILogger<RoleDefinitionService>>());
    }

    public void Dispose() => _db.Dispose();

    private RoleDefinition SeedRole(
        string  name = "TestRole",
        string  displayName = "Test Role",
        bool    isSystem = false,
        bool    isActive = true,
        string? description = "Opis role")
    {
        var role = isSystem
            ? RoleDefinition.CreateSystem(name, displayName, description)
            : RoleDefinition.CreateCustom(name, displayName, description, "user-1");

        if (!isActive)
            role.Deactivate("user-1", DateTime.UtcNow);

        _db.RoleDefinitions.Add(role);
        _db.SaveChanges();
        return role;
    }

    private PermissionDefinition SeedPermission(
        string code = "orders.view", string displayName = "View Orders", string module = "Orders")
    {
        var perm = PermissionDefinition.Create(code, displayName, "Opis", module);
        _db.PermissionDefinitions.Add(perm);
        _db.SaveChanges();
        return perm;
    }

    // ── GetAllAsync ──────────────────────────────────────────────────────────

    [Fact]
    public async Task GetAllAsync_NoFilters_OrdersSystemRolesFirstThenByName()
    {
        SeedRole(name: "ZZZCustom", displayName: "Custom Role", isSystem: false);
        SeedRole(name: "AAASystem", displayName: "System Role", isSystem: true);

        var result = await _sut.GetAllAsync(new RoleQueryRequest());

        Assert.Equal(2, result.TotalCount);
        Assert.Equal("AAASystem", result.Items[0].Name);
        Assert.Equal("ZZZCustom", result.Items[1].Name);
    }

    [Fact]
    public async Task GetAllAsync_SearchFilter_ReturnsOnlyMatching()
    {
        SeedRole(name: "Prodaja", displayName: "Prodaja rola");
        SeedRole(name: "Verifikator", displayName: "Verifikator rola");

        var result = await _sut.GetAllAsync(new RoleQueryRequest(Search: "verifik"));

        var item = Assert.Single(result.Items);
        Assert.Equal("Verifikator", item.Name);
    }

    [Fact]
    public async Task GetAllAsync_IsActiveFilter_ReturnsOnlyMatching()
    {
        SeedRole(name: "ActiveRole", isActive: true);
        SeedRole(name: "InactiveRole", isActive: false);

        var result = await _sut.GetAllAsync(new RoleQueryRequest(IsActive: false));

        var item = Assert.Single(result.Items);
        Assert.Equal("InactiveRole", item.Name);
    }

    [Fact]
    public async Task GetAllAsync_KeycloakUserCountThrows_DefaultsToZero()
    {
        SeedRole(name: "RoleA");
        _keycloakSync.GetRoleUserCountAsync(Arg.Any<string>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException<int>(new HttpRequestException("timeout")));

        var result = await _sut.GetAllAsync(new RoleQueryRequest());

        Assert.Equal(0, result.Items[0].UserCount);
    }

    [Fact]
    public async Task GetAllAsync_KeycloakUserCountSucceeds_PopulatesUserCount()
    {
        SeedRole(name: "RoleA");
        _keycloakSync.GetRoleUserCountAsync("RoleA", Arg.Any<CancellationToken>()).Returns(Task.FromResult(7));

        var result = await _sut.GetAllAsync(new RoleQueryRequest());

        Assert.Equal(7, result.Items[0].UserCount);
    }

    [Fact]
    public async Task GetAllAsync_Paging_ReturnsRequestedPage()
    {
        SeedRole(name: "RoleA");
        SeedRole(name: "RoleB");
        SeedRole(name: "RoleC");

        var result = await _sut.GetAllAsync(new RoleQueryRequest(Page: 2, PageSize: 1));

        Assert.Equal(3, result.TotalCount);
        Assert.Single(result.Items);
        Assert.Equal(2, result.Page);
    }

    // ── GetByIdAsync ─────────────────────────────────────────────────────────

    [Fact]
    public async Task GetByIdAsync_ExistingRole_ReturnsDtoWithPermissions()
    {
        var role = SeedRole();
        var perm = SeedPermission();
        _db.RolePermissions.Add(RolePermission.Create(role.Id, perm.Id, "user-1"));
        _db.SaveChanges();

        var dto = await _sut.GetByIdAsync(role.Id);

        Assert.Equal(role.Name, dto.Name);
        var permDto = Assert.Single(dto.Permissions);
        Assert.Equal(perm.Code, permDto.Code);
    }

    [Fact]
    public async Task GetByIdAsync_NonExistentRole_ThrowsNotFoundException()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.GetByIdAsync(999));

        Assert.Equal("ROLE_NOT_FOUND", ex.ErrorCode);
    }

    // ── CreateAsync ──────────────────────────────────────────────────────────

    [Fact]
    public async Task CreateAsync_ValidRequest_CreatesRoleAndSyncsKeycloak()
    {
        var request = new CreateRoleRequest("NewRole", "New Role", "Opis");

        var dto = await _sut.CreateAsync(request);

        Assert.Equal("NewRole", dto.Name);
        Assert.Equal("New Role", dto.DisplayName);
        Assert.False(dto.IsSystem);
        Assert.True(dto.IsActive);
        await _keycloakSync.Received(1).CreateRoleAsync("NewRole", "Opis", Arg.Any<CancellationToken>());
        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.RoleCreated), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task CreateAsync_EmptyName_ThrowsValidationException()
    {
        var request = new CreateRoleRequest("", "Display", null);

        await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(request));
    }

    [Fact]
    public async Task CreateAsync_NameWithSpaces_ThrowsValidationException()
    {
        var request = new CreateRoleRequest("Invalid Name", "Display", null);

        await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(request));
    }

    [Fact]
    public async Task CreateAsync_NameTooLong_ThrowsValidationException()
    {
        var request = new CreateRoleRequest(new string('A', 151), "Display", null);

        await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(request));
    }

    [Fact]
    public async Task CreateAsync_EmptyDisplayName_ThrowsValidationException()
    {
        var request = new CreateRoleRequest("ValidName", "", null);

        await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(request));
    }

    [Fact]
    public async Task CreateAsync_DisplayNameTooLong_ThrowsValidationException()
    {
        var request = new CreateRoleRequest("ValidName", new string('A', 251), null);

        await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(request));
    }

    [Fact]
    public async Task CreateAsync_DuplicateName_ThrowsConflictException()
    {
        SeedRole(name: "ExistingRole");
        var request = new CreateRoleRequest("existingrole", "Display", null);

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.CreateAsync(request));

        Assert.Equal("ROLE_DUPLICATE_NAME", ex.ErrorCode);
    }

    [Fact]
    public async Task CreateAsync_KeycloakSyncFails_RollsBackAndThrowsConflictException()
    {
        _keycloakSync.CreateRoleAsync(Arg.Any<string>(), Arg.Any<string?>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("keycloak down")));
        var request = new CreateRoleRequest("NewRole", "New Role", null);

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.CreateAsync(request));

        Assert.Equal("KEYCLOAK_SYNC_FAILED", ex.ErrorCode);
        Assert.False(await _db.RoleDefinitions.AnyAsync(r => r.Name == "NewRole"));
        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.KeycloakRoleSyncFailed), Arg.Any<CancellationToken>());
    }

    // ── UpdateAsync ──────────────────────────────────────────────────────────

    [Fact]
    public async Task UpdateAsync_ValidRequest_UpdatesRoleAndRecordsAudit()
    {
        var role = SeedRole(displayName: "Old Display");

        var dto = await _sut.UpdateAsync(role.Id, new UpdateRoleRequest("New Display", "New Desc"));

        Assert.Equal("New Display", dto.DisplayName);
        Assert.Equal("New Desc", dto.Description);
        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.RoleUpdated), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task UpdateAsync_NonExistentRole_ThrowsNotFoundException()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.UpdateAsync(999, new UpdateRoleRequest("Display", null)));

        Assert.Equal("ROLE_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task UpdateAsync_EmptyDisplayName_ThrowsValidationException()
    {
        var role = SeedRole();

        await Assert.ThrowsAsync<ValidationException>(
            () => _sut.UpdateAsync(role.Id, new UpdateRoleRequest("", null)));
    }

    // ── DeactivateAsync / ActivateAsync ─────────────────────────────────────

    [Fact]
    public async Task DeactivateAsync_ActiveRole_DeactivatesAndRecordsAudit()
    {
        var role = SeedRole(isActive: true);

        var dto = await _sut.DeactivateAsync(role.Id);

        Assert.False(dto.IsActive);
        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.RoleDeactivated), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task DeactivateAsync_AlreadyInactive_ThrowsConflictException()
    {
        var role = SeedRole(isActive: false);

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.DeactivateAsync(role.Id));

        Assert.Equal("ROLE_ALREADY_INACTIVE", ex.ErrorCode);
    }

    [Fact]
    public async Task DeactivateAsync_NonExistentRole_ThrowsNotFoundException()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.DeactivateAsync(999));

        Assert.Equal("ROLE_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task ActivateAsync_InactiveRole_ActivatesAndRecordsAudit()
    {
        var role = SeedRole(isActive: false);

        var dto = await _sut.ActivateAsync(role.Id);

        Assert.True(dto.IsActive);
        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.RoleReactivated), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task ActivateAsync_AlreadyActive_ThrowsConflictException()
    {
        var role = SeedRole(isActive: true);

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ActivateAsync(role.Id));

        Assert.Equal("ROLE_ALREADY_ACTIVE", ex.ErrorCode);
    }

    // ── DeleteAsync ──────────────────────────────────────────────────────────

    [Fact]
    public async Task DeleteAsync_SystemRole_ThrowsConflictException()
    {
        var role = SeedRole(isSystem: true);

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.DeleteAsync(role.Id));

        Assert.Equal("ROLE_SYSTEM_DELETE_BLOCKED", ex.ErrorCode);
    }

    [Fact]
    public async Task DeleteAsync_NonExistentRole_ThrowsNotFoundException()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.DeleteAsync(999));

        Assert.Equal("ROLE_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task DeleteAsync_KeycloakUserCountCheckThrows_ThrowsConflictExceptionAndRecordsAudit()
    {
        var role = SeedRole(isSystem: false);
        _keycloakSync.GetRoleUserCountAsync(Arg.Any<string>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException<int>(new HttpRequestException("timeout")));

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.DeleteAsync(role.Id));

        Assert.Equal("ROLE_DELETE_BLOCKED_USAGE_CHECK_FAILED", ex.ErrorCode);
        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.RoleDeleteBlockedInUse), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task DeleteAsync_RoleInUse_ThrowsConflictExceptionAndRecordsAudit()
    {
        var role = SeedRole(isSystem: false);
        _keycloakSync.GetRoleUserCountAsync(Arg.Any<string>(), Arg.Any<CancellationToken>()).Returns(Task.FromResult(5));

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.DeleteAsync(role.Id));

        Assert.Equal("ROLE_DELETE_BLOCKED_IN_USE", ex.ErrorCode);
        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.RoleDeleteBlockedInUse), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task DeleteAsync_NotInUse_SoftDeletesAndDeletesFromKeycloak()
    {
        var role = SeedRole(isSystem: false);
        _keycloakSync.GetRoleUserCountAsync(Arg.Any<string>(), Arg.Any<CancellationToken>()).Returns(Task.FromResult(0));

        await _sut.DeleteAsync(role.Id);

        Assert.NotNull(role.DeletedAt);
        await _keycloakSync.Received(1).DeleteRoleAsync(role.Name, Arg.Any<CancellationToken>());
        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.RoleSoftDeleted), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task DeleteAsync_KeycloakDeleteFails_StillSoftDeletesAndLogsAudit()
    {
        var role = SeedRole(isSystem: false);
        _keycloakSync.GetRoleUserCountAsync(Arg.Any<string>(), Arg.Any<CancellationToken>()).Returns(Task.FromResult(0));
        _keycloakSync.DeleteRoleAsync(Arg.Any<string>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("keycloak down")));

        await _sut.DeleteAsync(role.Id);

        Assert.NotNull(role.DeletedAt);
        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.KeycloakRoleSyncFailed), Arg.Any<CancellationToken>());
        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.RoleSoftDeleted), Arg.Any<CancellationToken>());
    }

    // ── AddPermissionAsync / RemovePermissionAsync ──────────────────────────

    [Fact]
    public async Task AddPermissionAsync_ValidRequest_AddsPermissionAndInvalidatesCache()
    {
        var role = SeedRole();
        var perm = SeedPermission();

        var dto = await _sut.AddPermissionAsync(role.Id, perm.Id);

        Assert.Contains(dto.Permissions, p => p.Code == perm.Code);
        _cache.Received(1).Remove(Arg.Any<object>());
        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.RolePermissionAdded), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task AddPermissionAsync_PermissionNotFound_ThrowsNotFoundException()
    {
        var role = SeedRole();

        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.AddPermissionAsync(role.Id, 999));

        Assert.Equal("PERMISSION_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task AddPermissionAsync_DuplicatePermission_ThrowsConflictException()
    {
        var role = SeedRole();
        var perm = SeedPermission();
        await _sut.AddPermissionAsync(role.Id, perm.Id);

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.AddPermissionAsync(role.Id, perm.Id));

        Assert.Equal("ROLE_PERMISSION_DUPLICATE", ex.ErrorCode);
    }

    [Fact]
    public async Task AddPermissionAsync_RoleNotFound_ThrowsNotFoundException()
    {
        var perm = SeedPermission();

        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.AddPermissionAsync(999, perm.Id));

        Assert.Equal("ROLE_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task RemovePermissionAsync_ValidRequest_RemovesPermissionAndInvalidatesCache()
    {
        var role = SeedRole();
        var perm = SeedPermission();
        await _sut.AddPermissionAsync(role.Id, perm.Id);

        var dto = await _sut.RemovePermissionAsync(role.Id, perm.Id);

        Assert.DoesNotContain(dto.Permissions, p => p.Code == perm.Code);
        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.RolePermissionRemoved), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task RemovePermissionAsync_PermissionNotAssigned_ThrowsNotFoundException()
    {
        var role = SeedRole();
        var perm = SeedPermission();

        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.RemovePermissionAsync(role.Id, perm.Id));

        Assert.Equal("ROLE_PERMISSION_NOT_FOUND", ex.ErrorCode);
    }

    // ── GetPermissionCodesForRoleAsync ───────────────────────────────────────

    [Fact]
    public async Task GetPermissionCodesForRoleAsync_ActiveRoleWithPermissions_ReturnsDistinctCodes()
    {
        var role = SeedRole(isActive: true);
        var perm = SeedPermission(code: "orders.view");
        await _sut.AddPermissionAsync(role.Id, perm.Id);

        var codes = await _sut.GetPermissionCodesForRoleAsync(role.Name);

        Assert.Equal(["orders.view"], codes);
    }

    [Fact]
    public async Task GetPermissionCodesForRoleAsync_InactiveRole_ReturnsEmpty()
    {
        var role = SeedRole(isActive: false);
        var perm = SeedPermission();
        _db.RolePermissions.Add(RolePermission.Create(role.Id, perm.Id, "user-1"));
        _db.SaveChanges();

        var codes = await _sut.GetPermissionCodesForRoleAsync(role.Name);

        Assert.Empty(codes);
    }

    [Fact]
    public async Task GetPermissionCodesForRoleAsync_NonExistentRole_ReturnsEmpty()
    {
        var codes = await _sut.GetPermissionCodesForRoleAsync("NoSuchRole");

        Assert.Empty(codes);
    }
}
