using RBBH.CollateralAppraisal.Application.Security;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Security;

public sealed class DashboardRoutesTests
{
    [Fact]
    public void GetRoute_ForAdministrator_ReturnsAdminRoute()
    {
        Assert.Equal(DashboardRoutes.Admin, DashboardRoutes.GetRoute(AppRoles.Administrator));
    }

    [Fact]
    public void GetRoute_ForBusinessRoles_ReturnsHome()
    {
        Assert.Equal(DashboardRoutes.Home, DashboardRoutes.GetRoute(AppRoles.AM));
        Assert.Equal(DashboardRoutes.Home, DashboardRoutes.GetRoute(AppRoles.SM));
        Assert.Equal(DashboardRoutes.Home, DashboardRoutes.GetRoute(AppRoles.UB));
        Assert.Equal(DashboardRoutes.Home, DashboardRoutes.GetRoute(AppRoles.KolateralAdministrator));
        Assert.Equal(DashboardRoutes.Home, DashboardRoutes.GetRoute(AppRoles.KolateralOficir));
        Assert.Equal(DashboardRoutes.Home, DashboardRoutes.GetRoute(AppRoles.Vjestak));
        Assert.Equal(DashboardRoutes.Home, DashboardRoutes.GetRoute(AppRoles.PravnaSluzba));
        Assert.Equal(DashboardRoutes.Home, DashboardRoutes.GetRoute(AppRoles.Protokol));
    }

    [Fact]
    public void GetRoute_ForAmSmUb_AllReturnSameDashboard()
    {
        // Zahtjev: ne praviti tri dashboarda — AM/SM/UB idu na ISTI dashboard.
        var amRoute = DashboardRoutes.GetRoute(AppRoles.AM);
        var smRoute = DashboardRoutes.GetRoute(AppRoles.SM);
        var ubRoute = DashboardRoutes.GetRoute(AppRoles.UB);

        Assert.Equal(amRoute, smRoute);
        Assert.Equal(amRoute, ubRoute);
    }

    [Fact]
    public void GetRoute_ForUnknownRole_ReturnsNull()
    {
        Assert.Null(DashboardRoutes.GetRoute("NepoznataRola"));
    }

    [Fact]
    public void IsKnownRole_DistinguishesKnownFromUnknown()
    {
        Assert.True(DashboardRoutes.IsKnownRole(AppRoles.Administrator));
        Assert.True(DashboardRoutes.IsKnownRole(AppRoles.KolateralAdministrator));
        Assert.False(DashboardRoutes.IsKnownRole("NepoznataRola"));
    }

    [Fact]
    public void All_ContainsEntryForEveryAppRole()
    {
        foreach (var role in AppRoles.All)
        {
            Assert.True(DashboardRoutes.All.ContainsKey(role));
        }
    }
}
