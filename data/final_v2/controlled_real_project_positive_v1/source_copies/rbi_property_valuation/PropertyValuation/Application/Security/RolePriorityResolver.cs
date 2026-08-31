namespace RBBH.CollateralAppraisal.Application.Security;

/// <summary>
/// Određuje prioritet kada korisnik ima više rola.
///
/// Koristi se za:
///   1. Redirect nakon prijave — korisnik se preusmjerava prema najautoritativnijoj roli.
///   2. Prikaz primarne role u UI-u.
///   3. Logging primarne role u audit zapise.
///
/// Redoslijed prioriteta (viši broj = viši prioritet):
///   Administrator (100) > Verifikator (50) > Unosnik (10) > Nepoznate role (0)
///
/// Sistem je proširiv: nove role se dodaju ovdje bez promjene logike koja ga koristi.
/// </summary>
public static class RolePriorityResolver
{
    private static readonly IReadOnlyDictionary<string, int> _priorities =
        new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase)
        {
            [AppRoles.Administrator] = 100,
            [AppRoles.Verifikator]   = 50,
            [AppRoles.KolateralOficir]        = 45,
            [AppRoles.KolateralAdministrator] = 40,
            [AppRoles.PravnaSluzba]           = 35,
            [AppRoles.AM]                     = 20,
            [AppRoles.SM]                     = 20,
            [AppRoles.UB]                     = 20,
            [AppRoles.Unosnik]       = 10,
            [AppRoles.Vjestak]                = 8,
            [AppRoles.Protokol]               = 5,
        };

    /// <summary>
    /// Vraća rolu sa najvišim prioritetom iz datog skupa rola.
    /// Null ako je skup prazan ili nema poznatih rola.
    /// </summary>
    public static string? GetPrimaryRole(IEnumerable<string> roles)
    {
        return roles
            .OrderByDescending(GetPriority)
            .FirstOrDefault();
    }

    /// <summary>
    /// Vraća fallback dashboard rutu prema prioritetu rola.
    /// Ovo je FALLBACK — normalni UX flow za 2+ role je /select-role.
    /// </summary>
    public static string GetRedirectPath(IEnumerable<string> roles)
    {
        var primary = GetPrimaryRole(roles);
        if (primary is null) return DashboardRoutes.AccessDenied;
        return DashboardRoutes.GetRoute(primary) ?? DashboardRoutes.AccessDenied;
    }

    /// <summary>Vraća numerički prioritet za datu rolu. 0 za nepoznate role.</summary>
    public static int GetPriority(string role) =>
        _priorities.TryGetValue(role, out var p) ? p : 0;

    /// <summary>Sortira role po prioritetu opadajuće (najvažnija prva).</summary>
    public static IEnumerable<string> SortByPriority(IEnumerable<string> roles) =>
        roles.OrderByDescending(GetPriority);
}
