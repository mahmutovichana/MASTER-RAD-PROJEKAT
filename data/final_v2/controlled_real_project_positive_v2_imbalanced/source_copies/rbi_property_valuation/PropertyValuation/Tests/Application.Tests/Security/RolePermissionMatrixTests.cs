using RBBH.CollateralAppraisal.Application.Security;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Security;

public class RolePermissionMatrixTests
{
    [Fact]
    public void PermissionsByRole_ContainsEntryForEveryRole()
    {
        foreach (var role in AppRoles.All)
        {
            Assert.True(
                RolePermissionMatrix.PermissionsByRole.ContainsKey(role),
                $"Rola '{role}' nema definisan skup permission-a u RolePermissionMatrix.");
        }
    }

    [Fact]
    public void PermissionsByRole_ContainsOnlyKnownPermissions()
    {
        var knownPermissions = new HashSet<string>(AppPermissions.All);

        foreach (var (role, permissions) in RolePermissionMatrix.PermissionsByRole)
        {
            foreach (var permission in permissions)
            {
                Assert.True(
                    knownPermissions.Contains(permission),
                    $"Permission '{permission}' za rolu '{role}' ne postoji u AppPermissions.All.");
            }
        }
    }

    [Fact]
    public void PermissionsByRole_HasNoDuplicatePermissionsPerRole()
    {
        foreach (var (role, permissions) in RolePermissionMatrix.PermissionsByRole)
        {
            Assert.True(
                permissions.Length == permissions.Distinct().Count(),
                $"Rola '{role}' ima duplirane permission-e u RolePermissionMatrix.");
        }
    }

    [Theory]
    [InlineData(AppRoles.AM)]
    [InlineData(AppRoles.SM)]
    [InlineData(AppRoles.UB)]
    [InlineData(AppRoles.KolateralAdministrator)]
    [InlineData(AppRoles.KolateralOficir)]
    [InlineData(AppRoles.PravnaSluzba)]
    [InlineData(AppRoles.Vjestak)]
    [InlineData(AppRoles.Protokol)]
    public void BusinessRoles_AllHaveNotificationsView(string role)
    {
        Assert.True(RolePermissionMatrix.RoleHasPermission(role, AppPermissions.NotificationsView));
    }

    [Fact]
    public void RoleHasPermission_ReturnsTrueForAssignedPermission()
    {
        Assert.True(RolePermissionMatrix.RoleHasPermission(AppRoles.Administrator, AppPermissions.AdminAccess));
    }

    [Fact]
    public void RoleHasPermission_ReturnsFalseForUnassignedPermission()
    {
        Assert.False(RolePermissionMatrix.RoleHasPermission(AppRoles.Unosnik, AppPermissions.AdminAccess));
    }

    [Fact]
    public void RoleHasPermission_ReturnsFalseForUnknownRole()
    {
        Assert.False(RolePermissionMatrix.RoleHasPermission("NepostojecaRola", AppPermissions.NotificationsView));
    }

    [Fact]
    public void GetPermissionsForRoles_ReturnsUnionWithoutDuplicates()
    {
        var permissions = RolePermissionMatrix
            .GetPermissionsForRoles([AppRoles.AM, AppRoles.KolateralOficir])
            .ToList();

        // Oba imaju OrdersView i NotificationsView — unija ih sadrži samo jednom.
        Assert.Equal(permissions.Count, permissions.Distinct().Count());
        Assert.Contains(AppPermissions.OrdersView, permissions);
        Assert.Contains(AppPermissions.OpinionsSubmitCo, permissions);       // samo CO
        Assert.Contains(AppPermissions.OrdersDownloadAppraisal, permissions); // samo Prodaja (AM)
    }

    [Fact]
    public void GetPermissionsForRoles_IgnoresUnknownRoles()
    {
        var permissions = RolePermissionMatrix.GetPermissionsForRoles(["NepostojecaRola"]).ToList();

        Assert.Empty(permissions);
    }

    [Fact]
    public void GetPermissionsForRoles_WithEmptyInput_ReturnsEmpty()
    {
        Assert.Empty(RolePermissionMatrix.GetPermissionsForRoles([]));
    }

    [Theory]
    [InlineData(AppRoles.KolateralOficir, AppPermissions.OpinionsSubmitCo, AppPermissions.OpinionsSubmitLegal)]
    [InlineData(AppRoles.PravnaSluzba, AppPermissions.OpinionsSubmitLegal, AppPermissions.OpinionsSubmitCo)]
    public void Roles_HaveExactlyTheirOwnOpinionSubmitPermission(string role, string ownPermission, string otherPermission)
    {
        Assert.True(RolePermissionMatrix.RoleHasPermission(role, ownPermission));
        Assert.False(RolePermissionMatrix.RoleHasPermission(role, otherPermission));
    }

    // ── Narudžbe procjene — inicijacija i radni tok (US-1, US-2) ───────────────

    [Theory]
    [InlineData(AppRoles.AM)]
    [InlineData(AppRoles.SM)]
    [InlineData(AppRoles.UB)]
    public void RoleHasPermission_OrdersCreate_AllowedForSalesRoles(string role)
    {
        Assert.True(RolePermissionMatrix.RoleHasPermission(role, AppPermissions.OrdersCreate));
    }

    [Theory]
    [InlineData(AppRoles.KolateralAdministrator)]
    [InlineData(AppRoles.Verifikator)]
    [InlineData(AppRoles.Unosnik)]
    [InlineData(AppRoles.Administrator)]
    public void RoleHasPermission_OrdersCreate_DeniedForNonSalesRoles(string role)
    {
        Assert.False(RolePermissionMatrix.RoleHasPermission(role, AppPermissions.OrdersCreate));
    }

    [Fact]
    public void AmSmUb_ShareIdenticalPermissionSet()
    {
        // Zahtjev: sve tri role moraju biti mapirane na ISTE Prodaja permissione.
        var am = RolePermissionMatrix.PermissionsByRole[AppRoles.AM];
        var sm = RolePermissionMatrix.PermissionsByRole[AppRoles.SM];
        var ub = RolePermissionMatrix.PermissionsByRole[AppRoles.UB];

        Assert.Equal(am.OrderBy(p => p), sm.OrderBy(p => p));
        Assert.Equal(am.OrderBy(p => p), ub.OrderBy(p => p));
    }

    [Theory]
    [InlineData(AppRoles.AM)]
    [InlineData(AppRoles.SM)]
    [InlineData(AppRoles.UB)]
    public void SalesRoles_HaveNamedSalesPermissionCatalog(string role)
    {
        Assert.True(RolePermissionMatrix.RoleHasPermission(role, AppPermissions.SalesDashboardView));
        Assert.True(RolePermissionMatrix.RoleHasPermission(role, AppPermissions.SalesOrderCreate));
        Assert.True(RolePermissionMatrix.RoleHasPermission(role, AppPermissions.SalesOrderView));
        Assert.True(RolePermissionMatrix.RoleHasPermission(role, AppPermissions.SalesOrderEditDraft));
        Assert.True(RolePermissionMatrix.RoleHasPermission(role, AppPermissions.SalesOrderSubmit));
        Assert.True(RolePermissionMatrix.RoleHasPermission(role, AppPermissions.SalesOrderDetailsView));
    }
}
