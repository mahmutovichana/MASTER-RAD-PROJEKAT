using Microsoft.AspNetCore.Authorization;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Extensions;

/// <summary>
/// Registruje sve permission-based policy-je za autorizaciju endpointa.
///
/// Kako dodati novu permission:
/// 1. Dodaj konstantu u AppPermissions.cs.
/// 2. Dodaj permission u AppPermissions.All niz.
/// 3. Policy se automatski registruje ovdje.
/// 4. Zaštiti endpoint: .RequireAuthorization(AppPolicies.NovaPermission)
///
/// Policy provjera:
/// - Korisnik mora biti autentificiran.
/// - Korisnik mora imati "permission" claim sa datom vrijednošću.
/// - Permission claim-ovi se dodaju putem PermissionClaimsTransformation.
///
/// 401 → korisnik nije prijavljen.
/// 403 → korisnik je prijavljen, ali nema potrebnu permission.
/// </summary>
public static class AuthorizationExtensions
{
    public static IServiceCollection AddPermissionPolicies(
        this IServiceCollection services)
    {
        services.AddAuthorization(ConfigurePolicies);
        return services;
    }

    private static void ConfigurePolicies(AuthorizationOptions options)
    {
        foreach (var permission in AppPermissions.All)
        {
            options.AddPolicy(permission, policy =>
            {
                policy.RequireAuthenticatedUser();
                policy.RequireClaim("permission", permission);
            });
        }
    }
}
