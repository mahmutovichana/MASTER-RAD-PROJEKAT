using System.Security.Claims;
using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Infrastructure.Auth;

public sealed class LocalDevelopmentAuthenticationOptions : AuthenticationSchemeOptions
{
    public bool Enabled { get; set; }
}

/// <summary>
/// Predvidljiv lokalni korisnik za razvoj bez vanjskog identity providera.
/// U produkciji handler vraća NoResult i nikada ne zaobilazi autentifikaciju.
/// </summary>
public sealed class LocalDevelopmentAuthenticationHandler
    : AuthenticationHandler<LocalDevelopmentAuthenticationOptions>
{
    public const string SchemeName = "LocalDevelopment";

    public LocalDevelopmentAuthenticationHandler(
        IOptionsMonitor<LocalDevelopmentAuthenticationOptions> options,
        ILoggerFactory logger,
        UrlEncoder encoder)
        : base(options, logger, encoder)
    {
    }

    protected override Task<AuthenticateResult> HandleAuthenticateAsync()
    {
        if (!Options.Enabled)
            return Task.FromResult(AuthenticateResult.NoResult());

        var claims = new List<Claim>
        {
            new(ClaimTypes.NameIdentifier, "local-development-user"),
            new("sub", "local-development-user"),
            new(ClaimTypes.Name, "Lokalni razvojni administrator"),
            new("name", "Lokalni razvojni administrator"),
            new("preferred_username", "local.admin"),
            new(ClaimTypes.Email, "local.admin@localhost"),
        };
        foreach (var role in AppRoles.All)
        {
            claims.Add(new Claim(ClaimTypes.Role, role));
            claims.Add(new Claim("roles", role));
        }

        var identity = new ClaimsIdentity(claims, SchemeName, ClaimTypes.Name, ClaimTypes.Role);
        return Task.FromResult(AuthenticateResult.Success(
            new AuthenticationTicket(new ClaimsPrincipal(identity), SchemeName)));
    }
}

public sealed record AuthenticationStartupStatus(bool KeycloakEnabled, string Message);
