using System.Security.Claims;
using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Caching.Memory;
using RBBH.CollateralAppraisal.Application.Roles.Interfaces;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Infrastructure.Auth;

/// <summary>
/// Claims transformation koja se izvršava na svakom autentificiranom zahtjevu.
///
/// Logika:
/// 1. Čita role iz JWT tokena.
/// 2. Za sistemske role → statički RolePermissionMatrix (brzo, bez DB).
/// 3. Za custom role → IMemoryCache (TTL 5 min) → DB fallback.
/// 4. Dodaje sve permission-e kao "permission" claim-ove.
///
/// Cache invalidacija: pozovi InvalidateRoleCache(roleName) kada se promijene permissioni.
/// </summary>
public class PermissionClaimsTransformation : IClaimsTransformation
{
    private const string PermissionClaimType = "permission";
    private const string TransformedMarker   = "permissions_transformed";
    private static readonly TimeSpan CacheTtl = TimeSpan.FromMinutes(5);
    private const string CacheKeyPrefix = "role_perms_";

    private readonly IRoleDefinitionService _roleDefinitionService;
    private readonly IMemoryCache _cache;

    public PermissionClaimsTransformation(
        IRoleDefinitionService roleDefinitionService,
        IMemoryCache cache)
    {
        _roleDefinitionService = roleDefinitionService;
        _cache                 = cache;
    }

    public async Task<ClaimsPrincipal> TransformAsync(ClaimsPrincipal principal)
    {
        if (principal.Identity?.IsAuthenticated != true)
            return principal;

        // Izbjegavamo dupliranje ako je transformation već pokrenuta
        if (principal.HasClaim(TransformedMarker, "true"))
            return principal;

        var roles = principal.GetRoles();
        if (roles.Count == 0)
            return principal;

        var permissions = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

        // Sistemske role — statička matrica (uvijek brzo, bez DB ili cache)
        var systemRoles = roles.Where(RolePermissionMatrix.PermissionsByRole.ContainsKey).ToList();
        foreach (var p in RolePermissionMatrix.GetPermissionsForRoles(systemRoles))
            permissions.Add(p);

        // Custom role — IMemoryCache (5 min TTL) sa DB fallback-om
        var customRoles = roles.Except(systemRoles, StringComparer.OrdinalIgnoreCase).ToList();
        foreach (var role in customRoles)
        {
            var cachedPerms = await _cache.GetOrCreateAsync(
                $"{CacheKeyPrefix}{role}",
                async entry =>
                {
                    entry.AbsoluteExpirationRelativeToNow = CacheTtl;
                    return await _roleDefinitionService.GetPermissionCodesForRoleAsync(role);
                });

            if (cachedPerms is not null)
                foreach (var p in cachedPerms)
                    permissions.Add(p);
        }

        var claimsIdentity = new ClaimsIdentity();
        foreach (var permission in permissions)
            claimsIdentity.AddClaim(new Claim(PermissionClaimType, permission));

        claimsIdentity.AddClaim(new Claim(TransformedMarker, "true"));
        principal.AddIdentity(claimsIdentity);

        return principal;
    }

    /// <summary>
    /// Invalidira cache za konkretnu rolu. Poziva se kada se promijene permissioni.
    /// </summary>
    public static void InvalidateRoleCache(IMemoryCache cache, string roleName)
        => cache.Remove($"{CacheKeyPrefix}{roleName}");
}
