using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Options;

namespace RBBH.TestAutomation.Api.Auth;

/// <summary>
/// HTTP-level auth handler za mock mod.
///
/// U .NET 8+ Blazor, [Authorize] atributi se provjeravaju na HTTP endpoint nivou
/// (endpoint routing) — nije dovoljno samo MockAuthenticationStateProvider (koji
/// radi na Blazor nivou). Ovaj handler uvijek vraća Success s istim principalom
/// koji bi izgradio MockAuthenticationStateProvider, pa HTTP autorizacija prolazi.
/// </summary>
public sealed class MockHttpAuthHandler(
    IOptionsMonitor<AuthenticationSchemeOptions> options,
    ILoggerFactory logger,
    UrlEncoder encoder,
    IUserContext userContext)
    : AuthenticationHandler<AuthenticationSchemeOptions>(options, logger, encoder)
{
    protected override Task<AuthenticateResult> HandleAuthenticateAsync()
    {
        var principal = MockAuthenticationStateProvider.BuildPrincipal(userContext);
        var ticket    = new AuthenticationTicket(principal, Scheme.Name);
        return Task.FromResult(AuthenticateResult.Success(ticket));
    }
}
