using System.Security.Claims;
using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Tests.Helpers;

/// <summary>
/// Lažni JWT handler koji ne validira nikakav potpis — prihvata bearer tokene oblika
/// "test-{userId}" i gradi ClaimsPrincipal s potrebnim permission claimovima.
///
/// Format tokena:
///   "test-admin"  → korisnik s SVIM permissionima (simulacija super-admina / integracijski setup)
///   "test-am"     → korisnik s AM permissionima (orders.create, orders.submit, orders.view-own, ...)
///   "test-noperm" → autentificirani korisnik bez ijednog permissiona
///   "test-{id}"   → generički — daje sve perms (default za pogodnost u testovima)
/// </summary>
public sealed class TestAuthHandler : AuthenticationHandler<AuthenticationSchemeOptions>
{
    public const string SchemeName = "Test";

    // Predefined user IDs za testove
    public const string AdminUserId  = "test-admin-user-id";
    public const string AmUserId     = "test-am-user-id";
    public const string NoPermUserId = "test-noperm-user-id";

    // Permission-e za AM ulogu (podskup svih perms)
    private static readonly string[] AmPermissions =
    [
        AppPermissions.OrdersCreate,
        AppPermissions.OrdersViewOwn,
        AppPermissions.OrdersUpdateDraft,
        AppPermissions.OrdersSubmit,
        AppPermissions.OrdersCancel,
        AppPermissions.DocumentsUpload,
        AppPermissions.DocumentsView,
        AppPermissions.NotificationsView,
        AppPermissions.CodebooksView,
    ];

    public TestAuthHandler(
        IOptionsMonitor<AuthenticationSchemeOptions> options,
        ILoggerFactory logger,
        UrlEncoder encoder)
        : base(options, logger, encoder) { }

    protected override Task<AuthenticateResult> HandleAuthenticateAsync()
    {
        var authHeader = Request.Headers.Authorization.ToString();
        if (!authHeader.StartsWith("Bearer test-", StringComparison.OrdinalIgnoreCase))
            return Task.FromResult(AuthenticateResult.NoResult());

        var token = authHeader["Bearer ".Length..].Trim();

        var (userId, permissions) = token switch
        {
            "test-admin"  => (AdminUserId,  AppPermissions.All),
            "test-am"     => (AmUserId,     AmPermissions),
            "test-noperm" => (NoPermUserId, Array.Empty<string>()),
            _             => (token,        AppPermissions.All),   // default: sve perms
        };

        // Rola za uobičajene tokene
        var roleForToken = token switch
        {
            "test-admin"        => AppRoles.Administrator,
            "test-am"           => AppRoles.AM,
            "test-sm"           => AppRoles.SM,
            "test-verifikator"  => AppRoles.Verifikator,
            "test-unosnik"      => AppRoles.Unosnik,
            "test-ub"           => AppRoles.UB,
            "test-kola"         => AppRoles.KolateralAdministrator,
            "test-vjestak"      => AppRoles.Vjestak,
            "test-unknown-role" => "CustomExternalRole",   // nije u DashboardRoutes
            _                   => null
        };

        // Višestruke role za test-multi-role
        var extraRole = token == "test-multi-role" ? AppRoles.SM : null;

        var claims = new List<Claim>
        {
            new(ClaimTypes.NameIdentifier, userId),
            new("sub",                    userId),
            new("preferred_username",     userId),
            new("permissions_transformed", "true"),
        };

        if (roleForToken is not null)
            claims.Add(new Claim("role", roleForToken));

        // test-multi-role ima AM + SM
        if (token == "test-multi-role")
        {
            claims.Add(new Claim("role", AppRoles.AM));
            claims.Add(new Claim("role", AppRoles.SM));
        }

        if (extraRole is not null)
            claims.Add(new Claim("role", extraRole));

        foreach (var perm in permissions)
            claims.Add(new Claim("permission", perm));

        var identity  = new ClaimsIdentity(claims, SchemeName);
        var principal = new ClaimsPrincipal(identity);
        var ticket    = new AuthenticationTicket(principal, SchemeName);

        return Task.FromResult(AuthenticateResult.Success(ticket));
    }
}
