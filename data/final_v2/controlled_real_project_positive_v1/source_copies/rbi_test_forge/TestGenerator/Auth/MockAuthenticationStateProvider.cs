using System.Security.Claims;
using Microsoft.AspNetCore.Components.Authorization;

namespace RBBH.TestAutomation.Api.Auth;

/// <summary>
/// Development AuthenticationStateProvider za mock mod.
///
/// Mock mod nema Keycloak, pa <see cref="MockUserContext"/> sam po sebi ne proizvodi
/// <see cref="ClaimsPrincipal"/>. Bez principala <c>&lt;AuthorizeRouteView&gt;</c> i
/// <c>[Authorize(Roles = ...)]</c> nemaju izvor rola i route-level zaštita ne radi lokalno.
///
/// Ovaj provider projektuje aktivnog mock korisnika u autentificiran principal s role
/// claimovima, tako da se <c>[Authorize]</c> ponaša identično u mock i OIDC modu.
///
/// Role se dodaju kao <see cref="ClaimTypes.Role"/> (za <c>IsInRole</c> i
/// <c>[Authorize(Roles=...)]</c>) i kao <c>"roles"</c> (radi paritета s
/// <c>RoleClaimType="roles"</c> iz OIDC grane u Program.cs).
/// </summary>
public sealed class MockAuthenticationStateProvider : AuthenticationStateProvider
{
    private readonly AuthenticationState _state;

    public MockAuthenticationStateProvider(IUserContext userContext)
    {
        _state = new AuthenticationState(BuildPrincipal(userContext));
    }

    public override Task<AuthenticationState> GetAuthenticationStateAsync() =>
        Task.FromResult(_state);

    internal static ClaimsPrincipal BuildPrincipal(IUserContext ctx)
    {
        var claims = new List<Claim>
        {
            new("sub", ctx.UserId),
            new(ClaimTypes.NameIdentifier, ctx.UserId),
            new("name", ctx.FullName),
            new(ClaimTypes.Name, ctx.FullName),
            new("email", ctx.Email),
            new(ClaimTypes.Email, ctx.Email),
        };

        foreach (var role in ctx.Roles)
        {
            claims.Add(new Claim(ClaimTypes.Role, role));
            claims.Add(new Claim("roles", role));
        }

        var identity = new ClaimsIdentity(
            claims,
            authenticationType: "Mock",
            nameType: ClaimTypes.Name,
            roleType: ClaimTypes.Role);

        return new ClaimsPrincipal(identity);
    }
}
