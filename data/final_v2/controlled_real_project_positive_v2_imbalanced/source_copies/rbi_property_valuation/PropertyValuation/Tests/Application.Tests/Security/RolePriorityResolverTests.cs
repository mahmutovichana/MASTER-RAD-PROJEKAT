using RBBH.CollateralAppraisal.Application.Security;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Security;

public sealed class RolePriorityResolverTests
{
    [Fact]
    public void GetPriority_ReturnsExpectedValuesForKnownRoles()
    {
        Assert.Equal(100, RolePriorityResolver.GetPriority(AppRoles.Administrator));
        Assert.Equal(50,  RolePriorityResolver.GetPriority(AppRoles.Verifikator));
        Assert.Equal(10,  RolePriorityResolver.GetPriority(AppRoles.Unosnik));
    }

    [Fact]
    public void GetPriority_ForUnknownRole_ReturnsZero()
    {
        Assert.Equal(0, RolePriorityResolver.GetPriority("NepoznataRola"));
    }

    [Fact]
    public void GetPrimaryRole_WithMultipleRoles_ReturnsHighestPriority()
    {
        var roles = new[] { AppRoles.Unosnik, AppRoles.Administrator, AppRoles.Verifikator };

        Assert.Equal(AppRoles.Administrator, RolePriorityResolver.GetPrimaryRole(roles));
    }

    [Fact]
    public void GetPrimaryRole_WithEmptyCollection_ReturnsNull()
    {
        Assert.Null(RolePriorityResolver.GetPrimaryRole([]));
    }

    [Fact]
    public void GetRedirectPath_ForAdministrator_ReturnsAdminDashboard()
    {
        var path = RolePriorityResolver.GetRedirectPath([AppRoles.Administrator]);

        Assert.Equal(DashboardRoutes.Admin, path);
    }

    [Fact]
    public void GetRedirectPath_ForEmptyRoles_ReturnsAccessDenied()
    {
        var path = RolePriorityResolver.GetRedirectPath([]);

        Assert.Equal(DashboardRoutes.AccessDenied, path);
    }

    [Fact]
    public void GetRedirectPath_ForUnknownRole_ReturnsAccessDenied()
    {
        var path = RolePriorityResolver.GetRedirectPath(["NepoznataRola"]);

        Assert.Equal(DashboardRoutes.AccessDenied, path);
    }

    [Fact]
    public void SortByPriority_OrdersRolesDescendingByPriority()
    {
        var roles = new[] { AppRoles.Unosnik, AppRoles.Administrator, AppRoles.Verifikator };

        var sorted = RolePriorityResolver.SortByPriority(roles).ToList();

        Assert.Equal(
            [AppRoles.Administrator, AppRoles.Verifikator, AppRoles.Unosnik],
            sorted);
    }
}
