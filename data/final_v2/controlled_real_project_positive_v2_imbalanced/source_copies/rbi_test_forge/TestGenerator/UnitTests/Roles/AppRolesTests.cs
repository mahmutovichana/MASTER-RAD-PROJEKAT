using RBBH.TestAutomation.Api.Auth;

namespace UnitTests.Roles;

/// <summary>
/// Unit testovi za <see cref="AppRoles"/> utility metode.
///
/// HasRole i HasAnyRole su korištene u svim access guardovima aplikacije —
/// greška ovdje znači da pogrešni korisnici dobiju ili izgube pristup.
/// </summary>
public class AppRolesTests
{
    // ═══════════════════════════════════════════════════════════════════════════
    // AppRoles.All
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public void All_ContainsFiveRoles()
    {
        Assert.Equal(5, AppRoles.All.Length);
    }

    [Theory]
    [InlineData(AppRoles.Administrator)]
    [InlineData(AppRoles.QALead)]
    [InlineData(AppRoles.QAInzenjer)]
    [InlineData(AppRoles.Developer)]
    [InlineData(AppRoles.DevOpsInzenjer)]
    public void All_ContainsExpectedRole(string role)
    {
        Assert.Contains(role, AppRoles.All);
    }

    [Fact]
    public void All_HasNoDuplicates()
    {
        Assert.Equal(AppRoles.All.Length, AppRoles.All.Distinct().Count());
    }

    [Fact]
    public void All_HasNoNullOrEmptyEntries()
    {
        Assert.All(AppRoles.All, r => Assert.False(string.IsNullOrWhiteSpace(r)));
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // HasRole
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public void HasRole_WhenUserHasRole_ReturnsTrue()
    {
        var roles = new[] { AppRoles.Administrator };
        Assert.True(AppRoles.HasRole(roles, AppRoles.Administrator));
    }

    [Fact]
    public void HasRole_WhenUserDoesNotHaveRole_ReturnsFalse()
    {
        var roles = new[] { AppRoles.QAInzenjer };
        Assert.False(AppRoles.HasRole(roles, AppRoles.Administrator));
    }

    [Fact]
    public void HasRole_WhenRolesIsNull_ReturnsFalse()
    {
        Assert.False(AppRoles.HasRole(null, AppRoles.Administrator));
    }

    [Fact]
    public void HasRole_WhenRolesIsEmpty_ReturnsFalse()
    {
        Assert.False(AppRoles.HasRole([], AppRoles.Administrator));
    }

    [Fact]
    public void HasRole_IsCaseInsensitive()
    {
        var roles = new[] { "administrator" }; // lowercase
        Assert.True(AppRoles.HasRole(roles, AppRoles.Administrator));
    }

    [Fact]
    public void HasRole_WhenUserHasMultipleRoles_MatchesCorrectOne()
    {
        var roles = new[] { AppRoles.QAInzenjer, AppRoles.QALead };
        Assert.True(AppRoles.HasRole(roles, AppRoles.QAInzenjer));
        Assert.True(AppRoles.HasRole(roles, AppRoles.QALead));
        Assert.False(AppRoles.HasRole(roles, AppRoles.Administrator));
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // HasAnyRole
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public void HasAnyRole_WhenUserHasOneOfRequired_ReturnsTrue()
    {
        var userRoles = new[] { AppRoles.QALead };
        Assert.True(AppRoles.HasAnyRole(userRoles, AppRoles.Administrator, AppRoles.QALead));
    }

    [Fact]
    public void HasAnyRole_WhenUserHasNoneOfRequired_ReturnsFalse()
    {
        var userRoles = new[] { AppRoles.Developer };
        Assert.False(AppRoles.HasAnyRole(userRoles, AppRoles.Administrator, AppRoles.QALead));
    }

    [Fact]
    public void HasAnyRole_WhenUserRolesIsNull_ReturnsFalse()
    {
        Assert.False(AppRoles.HasAnyRole(null, AppRoles.Administrator));
    }

    [Fact]
    public void HasAnyRole_WhenUserRolesIsEmpty_ReturnsFalse()
    {
        Assert.False(AppRoles.HasAnyRole([], AppRoles.Administrator));
    }

    [Fact]
    public void HasAnyRole_WhenUserHasAllRequired_ReturnsTrue()
    {
        var userRoles = new[] { AppRoles.Administrator, AppRoles.QAInzenjer };
        Assert.True(AppRoles.HasAnyRole(userRoles, AppRoles.Administrator, AppRoles.QAInzenjer));
    }

    [Fact]
    public void HasAnyRole_IsCaseInsensitive()
    {
        var userRoles = new[] { "qa lead" }; // lowercase
        Assert.True(AppRoles.HasAnyRole(userRoles, AppRoles.QALead));
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // AppModules.CanAccess — prošireni testovi
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public void CanAccess_Home_WhenRolesEmpty_ReturnsTrue()
    {
        // Home je dostupan svim autentificiranim korisnicima (prazan allowedRoles niz)
        Assert.True(AppModules.CanAccess(AppModules.Home, []));
    }

    [Fact]
    public void CanAccess_Home_WhenRolesNull_ReturnsTrue()
    {
        Assert.True(AppModules.CanAccess(AppModules.Home, null));
    }

    [Fact]
    public void CanAccess_UnknownModule_ReturnsFalse()
    {
        // Nepoznat modul = ne dati pristup (fail-safe)
        Assert.False(AppModules.CanAccess("NepostojeciModul", [AppRoles.Administrator]));
    }

    [Theory]
    [InlineData(AppRoles.QALead)]
    [InlineData(AppRoles.QAInzenjer)]
    [InlineData(AppRoles.Developer)]
    [InlineData(AppRoles.DevOpsInzenjer)]
    public void CanAccess_Role_WhenNonAdmin_ReturnsFalse(string role)
    {
        // Acceptance kriterij #2 — Role modul dostupan samo adminu
        Assert.False(AppModules.CanAccess(AppModules.Role, [role]));
    }

    [Fact]
    public void CanAccess_Sifarnici_WhenQALead_ReturnsTrue()
    {
        Assert.True(AppModules.CanAccess(AppModules.Sifarnici, [AppRoles.QALead]));
    }

    [Fact]
    public void CanAccess_Sifarnici_WhenQAInzenjer_ReturnsFalse()
    {
        Assert.False(AppModules.CanAccess(AppModules.Sifarnici, [AppRoles.QAInzenjer]));
    }

    [Fact]
    public void GetAllowedRoles_ForRole_ReturnsOnlyAdministrator()
    {
        var allowed = AppModules.GetAllowedRoles(AppModules.Role);
        Assert.Single(allowed);
        Assert.Equal(AppRoles.Administrator, allowed[0]);
    }

    [Fact]
    public void GetAllowedRoles_ForUnknownModule_ReturnsEmptyArray()
    {
        var allowed = AppModules.GetAllowedRoles("Nepostojeci");
        Assert.Empty(allowed);
    }
}
