using RBBH.CollateralAppraisal.Application.Security;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Security;

public sealed class AppRolesTests
{
    [Fact]
    public void All_ContainsActiveRoles_ExcludesUnimplementedRoles()
    {
        // Unosnik i Verifikator namjerno izostavljeni iz All — Records modul nije implementiran.
        Assert.Equal(
            [
                AppRoles.Administrator,
                AppRoles.AM,
                AppRoles.SM,
                AppRoles.UB,
                AppRoles.KolateralAdministrator,
                AppRoles.KolateralOficir,
                AppRoles.Vjestak,
                AppRoles.PravnaSluzba,
                AppRoles.Protokol,
                AppRoles.Likvidatura,
                AppRoles.SpecijalniRacuni,
                AppRoles.Racunovodstvo
            ],
            AppRoles.All);
    }

    [Fact]
    public void All_DoesNotContainUnimplementedRoles()
    {
        Assert.DoesNotContain(AppRoles.Unosnik,    AppRoles.All);
        Assert.DoesNotContain(AppRoles.Verifikator, AppRoles.All);
    }

    [Theory]
    [InlineData(AppRoles.AM)]
    [InlineData(AppRoles.SM)]
    [InlineData(AppRoles.UB)]
    public void IsSalesRole_TrueForAmSmUb(string role)
    {
        Assert.True(AppRoles.IsSalesRole(role));
    }

    [Theory]
    [InlineData(AppRoles.KolateralAdministrator)]
    [InlineData(AppRoles.Unosnik)]
    [InlineData(AppRoles.ProdajaSegment)]
    [InlineData(null)]
    public void IsSalesRole_FalseForNonSalesRoles(string? role)
    {
        Assert.False(AppRoles.IsSalesRole(role));
    }
}
