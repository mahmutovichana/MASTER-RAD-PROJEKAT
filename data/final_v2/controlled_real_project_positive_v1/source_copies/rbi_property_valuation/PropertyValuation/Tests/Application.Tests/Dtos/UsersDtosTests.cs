using RBBH.CollateralAppraisal.Application.Users.Models;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Dtos;

public sealed class UsersDtosTests
{
    [Fact]
    public void MeDto_StoresAllProperties()
    {
        var dto = new MeDto(
            UserId: "user-1",
            Username: "ivan",
            DisplayName: "Ivan Ivić",
            Email: "ivan@test.ba",
            Roles: ["AM"],
            Permissions: ["orders.create"],
            DefaultRoute: "/",
            AvailableModules: ["Orders"],
            UserStatus: "Active");

        Assert.Equal("ivan", dto.Username);
        Assert.Equal("Active", dto.UserStatus);
        Assert.Contains("AM", dto.Roles);
        Assert.Contains("orders.create", dto.Permissions);
    }

    [Fact]
    public void UserAssignedRoleDto_DefaultsToEmptyStrings()
    {
        var dto = new UserAssignedRoleDto();

        Assert.Equal(string.Empty, dto.Role);
        Assert.Equal(string.Empty, dto.Label);
        Assert.False(dto.IsSupported);
        Assert.False(dto.IsSystemRole);
        Assert.False(dto.CanRemove);
        Assert.Null(dto.RemoveBlockedReason);
    }

    [Fact]
    public void UserAssignedRoleDto_SetsRemoveBlockedReason()
    {
        var dto = new UserAssignedRoleDto
        {
            Role = "Administrator",
            Label = "Administrator",
            IsSupported = true,
            IsSystemRole = true,
            CanRemove = false,
            RemoveBlockedReason = "Nije moguće ukloniti posljednjeg Administratora."
        };

        Assert.False(dto.CanRemove);
        Assert.Equal("Nije moguće ukloniti posljednjeg Administratora.", dto.RemoveBlockedReason);
    }

    [Fact]
    public void UserRoleListItemDto_DefaultsToEmptyCollections()
    {
        var dto = new UserRoleListItemDto();

        Assert.Equal(string.Empty, dto.UserId);
        Assert.Empty(dto.Roles);
        Assert.Empty(dto.EffectivePermissions);
        Assert.False(dto.CanManageRoles);
    }

    [Fact]
    public void UserRoleListItemDto_SetsRolesAndPermissions()
    {
        var dto = new UserRoleListItemDto
        {
            UserId = "user-1",
            Username = "ivan",
            IsActive = true,
            Roles = ["AM", "SM"],
            EffectivePermissions = ["orders.create", "orders.submit"],
            CanManageRoles = true
        };

        Assert.Equal(2, dto.Roles.Count);
        Assert.True(dto.CanManageRoles);
    }

    [Fact]
    public void UserRolesDetailDto_DefaultsToEmptyCollections()
    {
        var dto = new UserRolesDetailDto();

        Assert.Empty(dto.Roles);
        Assert.Empty(dto.EffectivePermissions);
    }

    // ── UserRoleListRequest computed properties ─────────────────────────────────

    [Fact]
    public void UserRoleListRequest_Defaults_ValidatePageAndPageSize()
    {
        var request = new UserRoleListRequest();

        Assert.Equal(1,  request.ValidatedPage);
        Assert.Equal(20, request.ValidatedPageSize);
        Assert.Equal(0,  request.Offset);
    }

    [Theory]
    [InlineData(0, 1)]
    [InlineData(-5, 1)]
    [InlineData(1, 1)]
    [InlineData(3, 3)]
    public void UserRoleListRequest_ValidatedPage_ClampsToAtLeastOne(int page, int expected)
    {
        var request = new UserRoleListRequest { Page = page };

        Assert.Equal(expected, request.ValidatedPage);
    }

    [Theory]
    [InlineData(0, 20)]
    [InlineData(-1, 20)]
    [InlineData(101, 20)]
    [InlineData(50, 50)]
    [InlineData(100, 100)]
    public void UserRoleListRequest_ValidatedPageSize_FallsBackTo20WhenOutOfRange(int pageSize, int expected)
    {
        var request = new UserRoleListRequest { PageSize = pageSize };

        Assert.Equal(expected, request.ValidatedPageSize);
    }

    [Fact]
    public void UserRoleListRequest_Offset_ComputedFromValidatedPageAndPageSize()
    {
        var request = new UserRoleListRequest { Page = 3, PageSize = 10 };

        Assert.Equal(20, request.Offset);
    }

    [Theory]
    [InlineData(null, null)]
    [InlineData("", null)]
    [InlineData("   ", null)]
    [InlineData("  ivan  ", "ivan")]
    [InlineData("ivan", "ivan")]
    public void UserRoleListRequest_NormalizedSearch_TrimsOrReturnsNull(string? search, string? expected)
    {
        var request = new UserRoleListRequest { Search = search };

        Assert.Equal(expected, request.NormalizedSearch);
    }

    [Fact]
    public void UserRoleListRequest_HasUnknownRoleFilter_FalseWhenRoleNotSet()
    {
        var request = new UserRoleListRequest();

        Assert.False(request.HasUnknownRoleFilter);
    }

    [Fact]
    public void UserRoleListRequest_HasUnknownRoleFilter_FalseForKnownRole()
    {
        var request = new UserRoleListRequest { Role = "AM" };

        Assert.False(request.HasUnknownRoleFilter);
    }

    [Fact]
    public void UserRoleListRequest_HasUnknownRoleFilter_TrueForUnknownRole()
    {
        var request = new UserRoleListRequest { Role = "NepoznataRola" };

        Assert.True(request.HasUnknownRoleFilter);
    }

    // ── MeDto extended coverage ───────────────────────────────────────────────

    [Fact]
    public void MeDto_AllFieldsPopulated_StoresCorrectValues()
    {
        var roles = new List<string> { "AM", "SM", "UB" };
        var permissions = new List<string> { "orders.create", "orders.submit", "orders.cancel" };
        var modules = new List<string> { "Orders", "Codebooks", "Users" };

        var dto = new MeDto(
            UserId: "user-42",
            Username: "marko",
            DisplayName: "Marko Markovic",
            Email: "marko@firma.ba",
            Roles: roles,
            Permissions: permissions,
            DefaultRoute: "/orders",
            AvailableModules: modules,
            UserStatus: "Active");

        Assert.Equal("user-42", dto.UserId);
        Assert.Equal("marko", dto.Username);
        Assert.Equal("Marko Markovic", dto.DisplayName);
        Assert.Equal("marko@firma.ba", dto.Email);
        Assert.Equal(3, dto.Roles.Count);
        Assert.Contains("AM", dto.Roles);
        Assert.Contains("SM", dto.Roles);
        Assert.Contains("UB", dto.Roles);
        Assert.Equal(3, dto.Permissions.Count);
        Assert.Contains("orders.create", dto.Permissions);
        Assert.Contains("orders.submit", dto.Permissions);
        Assert.Contains("orders.cancel", dto.Permissions);
        Assert.Equal("/orders", dto.DefaultRoute);
        Assert.Equal(3, dto.AvailableModules.Count);
        Assert.Contains("Orders", dto.AvailableModules);
        Assert.Contains("Codebooks", dto.AvailableModules);
        Assert.Contains("Users", dto.AvailableModules);
        Assert.Equal("Active", dto.UserStatus);
    }

    [Fact]
    public void MeDto_NullOptionalFields_StoresNull()
    {
        var dto = new MeDto(
            UserId: null,
            Username: null,
            DisplayName: null,
            Email: null,
            Roles: [],
            Permissions: [],
            DefaultRoute: null,
            AvailableModules: [],
            UserStatus: "NoRole");

        Assert.Null(dto.UserId);
        Assert.Null(dto.Username);
        Assert.Null(dto.DisplayName);
        Assert.Null(dto.Email);
        Assert.Empty(dto.Roles);
        Assert.Empty(dto.Permissions);
        Assert.Null(dto.DefaultRoute);
        Assert.Empty(dto.AvailableModules);
        Assert.Equal("NoRole", dto.UserStatus);
    }

    [Theory]
    [InlineData("Active")]
    [InlineData("Suspended")]
    [InlineData("NoRole")]
    [InlineData("UnknownRole")]
    public void MeDto_UserStatus_AcceptsAllValidValues(string status)
    {
        var dto = new MeDto(
            UserId: "u", Username: "u", DisplayName: "u", Email: null,
            Roles: [], Permissions: [], DefaultRoute: null,
            AvailableModules: [], UserStatus: status);

        Assert.Equal(status, dto.UserStatus);
    }

    // ── UserRolesDetailDto extended coverage ──────────────────────────────────

    [Fact]
    public void UserRolesDetailDto_AllFieldsPopulated_StoresCorrectValues()
    {
        var role1 = new UserAssignedRoleDto
        {
            Role = "AM",
            Label = "Account Manager",
            IsSupported = true,
            IsSystemRole = true,
            CanRemove = true,
            RemoveBlockedReason = null
        };

        var role2 = new UserAssignedRoleDto
        {
            Role = "Administrator",
            Label = "Administrator",
            IsSupported = true,
            IsSystemRole = true,
            CanRemove = false,
            RemoveBlockedReason = "Posljednji administrator"
        };

        var dto = new UserRolesDetailDto
        {
            UserId = "user-10",
            Username = "ana",
            DisplayName = "Ana Anic",
            Email = "ana@firma.ba",
            IsActive = true,
            Roles = [role1, role2],
            EffectivePermissions = ["orders.create", "orders.submit", "users.view"]
        };

        Assert.Equal("user-10", dto.UserId);
        Assert.Equal("ana", dto.Username);
        Assert.Equal("Ana Anic", dto.DisplayName);
        Assert.Equal("ana@firma.ba", dto.Email);
        Assert.True(dto.IsActive);
        Assert.Equal(2, dto.Roles.Count);
        Assert.Equal("AM", dto.Roles[0].Role);
        Assert.True(dto.Roles[0].CanRemove);
        Assert.Equal("Administrator", dto.Roles[1].Role);
        Assert.False(dto.Roles[1].CanRemove);
        Assert.Equal("Posljednji administrator", dto.Roles[1].RemoveBlockedReason);
        Assert.Equal(3, dto.EffectivePermissions.Count);
    }

    [Fact]
    public void UserRolesDetailDto_InactiveUser_StoresFalse()
    {
        var dto = new UserRolesDetailDto
        {
            UserId = "user-suspended",
            Username = "suspended",
            DisplayName = null,
            Email = null,
            IsActive = false,
            Roles = [],
            EffectivePermissions = []
        };

        Assert.False(dto.IsActive);
        Assert.Null(dto.DisplayName);
        Assert.Null(dto.Email);
        Assert.Empty(dto.Roles);
        Assert.Empty(dto.EffectivePermissions);
    }

    // ── UserAssignedRoleDto extended coverage ─────────────────────────────────

    [Fact]
    public void UserAssignedRoleDto_SupportedNonSystemRole_StoresCorrectFlags()
    {
        var dto = new UserAssignedRoleDto
        {
            Role = "CUSTOM_ROLE",
            Label = "Prilagodjena rola",
            IsSupported = true,
            IsSystemRole = false,
            CanRemove = true,
            RemoveBlockedReason = null
        };

        Assert.Equal("CUSTOM_ROLE", dto.Role);
        Assert.Equal("Prilagodjena rola", dto.Label);
        Assert.True(dto.IsSupported);
        Assert.False(dto.IsSystemRole);
        Assert.True(dto.CanRemove);
        Assert.Null(dto.RemoveBlockedReason);
    }

    [Fact]
    public void UserAssignedRoleDto_UnsupportedRole_StoresCorrectFlags()
    {
        var dto = new UserAssignedRoleDto
        {
            Role = "LEGACY",
            Label = "Legacy rola",
            IsSupported = false,
            IsSystemRole = false,
            CanRemove = false,
            RemoveBlockedReason = "Rola nije podrzana"
        };

        Assert.False(dto.IsSupported);
        Assert.False(dto.CanRemove);
        Assert.Equal("Rola nije podrzana", dto.RemoveBlockedReason);
    }

    // ── UserRoleListItemDto extended coverage ─────────────────────────────────

    [Fact]
    public void UserRoleListItemDto_AllFieldsPopulated_StoresCorrectValues()
    {
        var dto = new UserRoleListItemDto
        {
            UserId = "user-50",
            Username = "petar",
            DisplayName = "Petar Petrovic",
            Email = "petar@firma.ba",
            IsActive = true,
            Roles = ["AM", "CA", "CO"],
            EffectivePermissions = ["orders.create", "orders.approve-final", "users.view", "codebooks.manage"],
            CanManageRoles = true
        };

        Assert.Equal("user-50", dto.UserId);
        Assert.Equal("petar", dto.Username);
        Assert.Equal("Petar Petrovic", dto.DisplayName);
        Assert.Equal("petar@firma.ba", dto.Email);
        Assert.True(dto.IsActive);
        Assert.Equal(3, dto.Roles.Count);
        Assert.Contains("CA", dto.Roles);
        Assert.Equal(4, dto.EffectivePermissions.Count);
        Assert.True(dto.CanManageRoles);
    }

    [Fact]
    public void UserRoleListItemDto_InactiveUser_NullDisplayNameAndEmail()
    {
        var dto = new UserRoleListItemDto
        {
            UserId = "user-inactive",
            Username = "inactive",
            DisplayName = null,
            Email = null,
            IsActive = false,
            Roles = [],
            EffectivePermissions = [],
            CanManageRoles = false
        };

        Assert.False(dto.IsActive);
        Assert.Null(dto.DisplayName);
        Assert.Null(dto.Email);
        Assert.False(dto.CanManageRoles);
    }
}
