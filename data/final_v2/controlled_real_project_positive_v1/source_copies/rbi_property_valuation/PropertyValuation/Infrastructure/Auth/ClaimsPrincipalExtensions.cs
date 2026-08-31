using System.Security.Claims;

namespace RBBH.CollateralAppraisal.Infrastructure.Auth;

/// <summary>
/// Extension metode za ClaimsPrincipal — standardizovano čitanje claim-ova.
/// Podržava flat JWT claim-ove i standardne Keycloak claim-ove.
///
/// KEYCLOAK CLAIM FORMAT — za Ernad:
/// Keycloak može slati role u dva formata:
///
/// 1. Flat format (podržan): svaka rola je poseban claim:
///    "role": "Administrator"
///    "role": "Unosnik"
///
/// 2. Nested realm_access format (NYI — provjeriti):
///    { "realm_access": { "roles": ["Administrator", "Unosnik"] } }
///    Ako Keycloak koristi ovaj format, Ernad mora:
///    a) Provjeriti stvarni JWT token iz Keycloak realma.
///    b) Dodati podršku u GetRoles() za parsiranje realm_access.roles JSON claim-a.
///    c) Alternativno: konfigurirati Keycloak da mapira role kao flat claim-ove.
///
/// 3. resource_access format (za client-specifične role):
///    { "resource_access": { "collateral-appraisal-api": { "roles": ["Administrator"] } } }
///    Ako su uloge per-client, Ernad dodaje parsiranje za "collateral-appraisal-api" resource.
///
/// Preporučena Keycloak konfiguracija: protocol mapper koji flatten-uje role u "role" claim.
/// </summary>
public static class ClaimsPrincipalExtensions
{
    /// <summary>
    /// Vraća UserId iz sub ili NameIdentifier claim-a.
    /// </summary>
    public static string? GetUserId(this ClaimsPrincipal principal) =>
        principal.FindFirst(ClaimTypes.NameIdentifier)?.Value
        ?? principal.FindFirst("sub")?.Value;

    /// <summary>
    /// Vraća username iz preferred_username, Name ili email claim-a.
    /// </summary>
    public static string? GetUsername(this ClaimsPrincipal principal) =>
        principal.FindFirst("preferred_username")?.Value
        ?? principal.FindFirst(ClaimTypes.Name)?.Value
        ?? principal.FindFirst(ClaimTypes.Email)?.Value;

    /// <summary>
    /// Vraća sve role korisnika. Podržava dva Keycloak formata:
    /// 1. Flat claim-ovi: role / roles / ClaimTypes.Role (preferiran — realm-roles-flat mapper).
    /// 2. Nested realm_access.roles JSON claim (Keycloak default) — parsira se kao fallback,
    ///    da autorizacija radi i ako flat mapper nije konfigurisan.
    /// </summary>
    public static IReadOnlyList<string> GetRoles(this ClaimsPrincipal principal)
    {
        var roles = principal.FindAll(ClaimTypes.Role)
            .Concat(principal.FindAll("role"))
            .Concat(principal.FindAll("roles"))
            .Select(c => c.Value)
            .Concat(ParseRealmAccessRoles(principal))
            .Where(v => !string.IsNullOrWhiteSpace(v))
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .ToList();

        return roles.AsReadOnly();
    }

    /// <summary>
    /// Parsira nested Keycloak claim: { "realm_access": { "roles": ["Administrator", ...] } }.
    /// </summary>
    private static IEnumerable<string> ParseRealmAccessRoles(ClaimsPrincipal principal)
    {
        var realmAccess = principal.FindFirst("realm_access")?.Value;
        if (string.IsNullOrWhiteSpace(realmAccess))
            return [];

        try
        {
            using var doc = System.Text.Json.JsonDocument.Parse(realmAccess);
            if (doc.RootElement.TryGetProperty("roles", out var rolesEl)
                && rolesEl.ValueKind == System.Text.Json.JsonValueKind.Array)
            {
                return rolesEl.EnumerateArray()
                    .Select(e => e.GetString() ?? string.Empty)
                    .ToList();
            }
        }
        catch (System.Text.Json.JsonException)
        {
            // Neispravan JSON u realm_access — ignoriši, oslanjamo se na flat claim-ove.
        }

        return [];
    }

    /// <summary>
    /// Vraća true ako korisnik ima danu permission kao claim.
    /// Permission-e su dodane u principal od strane <see cref="PermissionClaimsTransformation"/>.
    /// </summary>
    public static bool HasPermission(this ClaimsPrincipal principal, string permission) =>
        principal.HasClaim("permission", permission);
}
