namespace RBBH.CollateralAppraisal.Application.Security;

/// <summary>
/// Centralna mapa rola na dashboard rute.
///
/// Proširivost: nove role dodaju se ovdje i opciono u bazi/konfiguraciji.
/// Klasa je dizajnirana da bude jedino mjesto u sistemu gdje se definiše ruta po roli.
/// </summary>
public static class DashboardRoutes
{
    public const string Admin       = "/dashboard/admin";
    public const string Home        = "/";
    public const string SelectRole  = "/select-role";
    public const string AccessDenied = "/access-denied";
    // Unosnik/Verifikator rute uklonjene (Jul 2026) — Records modul nije implementiran.
    // Dodati kad se Records modul završi.

    private static readonly IReadOnlyDictionary<string, string> _map =
        new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
        {
            [AppRoles.Administrator] = Admin,
            // Unosnik i Verifikator namjerno izostavljeni — nemaju aktivne endpointe.

            // Segment Prodaja (AM/SM/UB) i ostale poslovne role (narudžbe
            // procjene — US 92/93/94) — još nemaju dedicirani dashboard,
            // koriste opštu početnu stranicu (Home.razor grana se po roli).
            // Sve tri prodajne role idu na ISTI dashboard — isti layout/modul,
            // razlika je samo u aktivnoj roli (zahtjev: ne praviti tri dashboarda).
            [AppRoles.AM]                     = Home,
            [AppRoles.SM]                     = Home,
            [AppRoles.UB]                     = Home,
            [AppRoles.KolateralAdministrator] = Home,
            [AppRoles.KolateralOficir]        = Home,
            [AppRoles.Vjestak]                = Home,
            [AppRoles.PravnaSluzba]           = Home,
            [AppRoles.Protokol]               = Home,
            [AppRoles.Likvidatura]            = Home,
            [AppRoles.SpecijalniRacuni]       = Home,
            [AppRoles.Racunovodstvo]          = Home,
        };

    /// <summary>Vraća dashboard rutu za datu rolu. Null ako rola nije poznata.</summary>
    public static string? GetRoute(string role) =>
        _map.TryGetValue(role, out var route) ? route : null;

    /// <summary>Vraća true ako data rola ima definisanu dashboard rutu.</summary>
    public static bool IsKnownRole(string role) => _map.ContainsKey(role);

    /// <summary>Sve poznate rola → ruta mappinge (za serijalizaciju/API response).</summary>
    public static IReadOnlyDictionary<string, string> All => _map;
}
