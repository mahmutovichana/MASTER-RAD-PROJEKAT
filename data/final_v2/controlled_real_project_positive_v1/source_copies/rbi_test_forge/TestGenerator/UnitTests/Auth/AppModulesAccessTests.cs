using RBBH.TestAutomation.Api.Auth;
using Xunit;

namespace UnitTests.Auth;

/// <summary>
/// Verifikacija matrice pristupa (US #4 — sivi moduli po roli).
/// </summary>
public class AppModulesAccessTests
{
    [Theory]
    [InlineData(AppRoles.Administrator, AppModules.Korisnici, true)]
    [InlineData(AppRoles.Administrator, AppModules.Role, true)]
    [InlineData(AppRoles.Administrator, AppModules.AuditLog, true)]
    [InlineData(AppRoles.Administrator, AppModules.Sifarnici, true)]
    [InlineData(AppRoles.Administrator, AppModules.Home, true)]
    [InlineData(AppRoles.QAInzenjer, AppModules.Korisnici, false)]
    [InlineData(AppRoles.QAInzenjer, AppModules.Role, false)]
    [InlineData(AppRoles.QAInzenjer, AppModules.Home, true)]
    [InlineData(AppRoles.QALead, AppModules.Sifarnici, true)]
    [InlineData(AppRoles.QALead, AppModules.Role, false)]
    [InlineData(AppRoles.Developer, AppModules.Sifarnici, false)]
    [InlineData(AppRoles.QAInzenjer, AppModules.ApiImport, true)]
    [InlineData(AppRoles.QALead, AppModules.ApiImport, true)]
    [InlineData(AppRoles.Developer, AppModules.ApiImport, false)]
    [InlineData(AppRoles.DevOpsInzenjer, AppModules.ApiKeys, true)]
    [InlineData(AppRoles.Administrator, AppModules.ApiKeys, true)]
    [InlineData(AppRoles.Developer, AppModules.ApiKeys, false)]
    [InlineData(AppRoles.QALead, AppModules.ApiKeys, false)]
    public void CanAccess_MatchesExpectedMatrix(string role, string module, bool expected)
    {
        var actual = AppModules.CanAccess(module, [role]);
        Assert.Equal(expected, actual);
    }

    [Fact]
    public void All_AppRoles_Count_MatchesRealm()
    {
        Assert.Equal(5, AppRoles.All.Length);
    }
}
