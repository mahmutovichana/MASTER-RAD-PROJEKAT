using System.Security.Claims;
using RBBH.TestAutomation.Api.Auth;
using NSubstitute;
using Xunit;

namespace UnitTests.Auth;

/// <summary>
/// Verifikacija da mock principal nosi role claimove kako bi route-level
/// [Authorize(Roles=...)] radio identično kao u OIDC modu (US #4 — kontrola pristupa).
/// </summary>
public class MockAuthenticationStateProviderTests
{
    private static IUserContext UserWithRoles(params string[] roles)
    {
        var ctx = Substitute.For<IUserContext>();
        ctx.UserId.Returns("mock-001");
        ctx.FullName.Returns("Mock Korisnik");
        ctx.Email.Returns("mock@rbi.local");
        ctx.Roles.Returns(roles);
        return ctx;
    }

    [Fact]
    public async Task State_Is_Authenticated()
    {
        var provider = new MockAuthenticationStateProvider(UserWithRoles(AppRoles.Administrator));

        var state = await provider.GetAuthenticationStateAsync();

        Assert.True(state.User.Identity?.IsAuthenticated);
    }

    [Fact]
    public async Task Admin_User_IsInRole_Administrator()
    {
        var provider = new MockAuthenticationStateProvider(UserWithRoles(AppRoles.Administrator));

        var state = await provider.GetAuthenticationStateAsync();

        Assert.True(state.User.IsInRole(AppRoles.Administrator));
    }

    [Fact]
    public async Task QAInzenjer_User_Not_IsInRole_Administrator()
    {
        var provider = new MockAuthenticationStateProvider(UserWithRoles(AppRoles.QAInzenjer));

        var state = await provider.GetAuthenticationStateAsync();

        Assert.False(state.User.IsInRole(AppRoles.Administrator));
        Assert.True(state.User.IsInRole(AppRoles.QAInzenjer));
    }

    [Fact]
    public async Task Roles_Are_Exposed_As_Both_ClaimTypes()
    {
        var provider = new MockAuthenticationStateProvider(UserWithRoles(AppRoles.QALead));

        var state = await provider.GetAuthenticationStateAsync();
        var user = state.User;

        // ClaimTypes.Role — za IsInRole / [Authorize(Roles=...)]
        Assert.Contains(user.FindAll(ClaimTypes.Role), c => c.Value == AppRoles.QALead);
        // "roles" — paritet s RoleClaimType iz OIDC grane
        Assert.Contains(user.FindAll("roles"), c => c.Value == AppRoles.QALead);
    }
}
