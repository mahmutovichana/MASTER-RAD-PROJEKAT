using Microsoft.AspNetCore.Components.Authorization;
using Microsoft.AspNetCore.Components.Server;

namespace RBBH.TestAutomation.Api.Auth;

/// <summary>
/// Server-side AuthenticationStateProvider za OIDC (Keycloak) mod.
///
/// Zašto baš ovaj tip:
/// Aplikacija renderuje InteractiveServer (SignalR circuit). Nakon što se circuit
/// uspostavi, HttpContext više nije direktno dostupan, pa provider koji čita
/// HttpContext.User na svaki poziv ne bi radio u živom circuitu. Bazni
/// <see cref="ServerAuthenticationStateProvider"/> (kroz <c>IHostEnvironmentAuthenticationStateProvider</c>)
/// preuzme principal iz cookie-ja tokom statičkog SSR pasa i drži ga za životni
/// vijek circuita; revalidacija periodično provjerava da je sesija i dalje validna.
///
/// Refresh access tokena radi <c>CookieOidcRefresher</c> (na cookie validaciji),
/// pa ovdje samo potvrđujemo da je korisnik i dalje autentificiran.
/// </summary>
internal sealed class OidcRevalidatingAuthenticationStateProvider
    : RevalidatingServerAuthenticationStateProvider
{
    public OidcRevalidatingAuthenticationStateProvider(ILoggerFactory loggerFactory)
        : base(loggerFactory)
    {
    }

    protected override TimeSpan RevalidationInterval => TimeSpan.FromMinutes(30);

    protected override Task<bool> ValidateAuthenticationStateAsync(
        AuthenticationState authenticationState,
        CancellationToken cancellationToken)
    {
        // Cookie/OIDC refresh se rješava u CookieOidcRefresher-u; ovdje je dovoljno
        // provjeriti da identitet i dalje postoji (sign-out ga poništi).
        var isAuthenticated = authenticationState.User.Identity?.IsAuthenticated == true;
        return Task.FromResult(isAuthenticated);
    }
}
