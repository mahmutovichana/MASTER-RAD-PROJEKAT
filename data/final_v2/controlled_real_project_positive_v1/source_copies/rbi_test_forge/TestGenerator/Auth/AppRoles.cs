namespace RBBH.TestAutomation.Api.Auth;

/// <summary>
/// Konstante za sve role u TAG aplikaciji.
///
/// VAŽNO: String vrijednosti moraju biti IDENTIČNE nazivima rola u Keycloak realmu
/// i SQL Server bazi. Jedna tipografska greška = auth ne radi.
///
/// Konvencija: C# ime je PascalCase bez razmaka.
/// </summary>
public static class AppRoles
{
    /// <summary>
    /// Administrator aplikacije — pun pristup svim modulima.
    /// Može kreirati/brisati korisnike, upravljati rolama, pregledati Audit Log.
    /// </summary>
    public const string Administrator = "Administrator";

    /// <summary>
    /// QA Lead — upravljanje svim QA modulima, grupama, scenarijima, rasporedima.
    /// </summary>
    public const string QALead = "QA Lead";

    /// <summary>
    /// QA Inzenjer — kreiranje i uređivanje scenarija, grupe testova, generator.
    /// </summary>
    public const string QAInzenjer = "QA Inzenjer";

    /// <summary>
    /// Developer — pregled scenarija i generisanje test fajlova.
    /// </summary>
    public const string Developer = "Developer";

    /// <summary>
    /// DevOps Inzenjer — zakazivanje i pokretanje testova, CI integracija.
    /// </summary>
    public const string DevOpsInzenjer = "DevOps Inzenjer";

    /// <summary>
    /// Sve role u sistemu — koristi se u dropdownima za upravljanje rolama.
    /// </summary>
    public static readonly string[] All =
    [
        Administrator,
        QALead,
        QAInzenjer,
        Developer,
        DevOpsInzenjer,
    ];

    /// <summary>
    /// Provjerava da li korisnik ima traženu rolu.
    /// </summary>
    /// <param name="userRoles">Niz rola prijavljenog korisnika (iz UserInfo.Roles).</param>
    /// <param name="requiredRole">Rola koja se traži — koristiti konstante iz AppRoles.</param>
    /// <returns>True ako korisnik ima traženu rolu, inače false.</returns>
    public static bool HasRole(string[]? userRoles, string requiredRole)
    {
        if (userRoles is null || userRoles.Length == 0)
            return false;

        return userRoles.Contains(requiredRole, StringComparer.OrdinalIgnoreCase);
    }

    /// <summary>
    /// Provjerava da li korisnik ima barem jednu od navedenih rola.
    /// </summary>
    /// <param name="userRoles">Niz rola prijavljenog korisnika.</param>
    /// <param name="anyOfRoles">Rola je dovoljna — korisnik mora imati barem jednu.</param>
    /// <returns>True ako korisnik ima barem jednu od navedenih rola.</returns>
    public static bool HasAnyRole(string[]? userRoles, params string[] anyOfRoles)
    {
        if (userRoles is null || userRoles.Length == 0)
            return false;

        return anyOfRoles.Any(r => HasRole(userRoles, r));
    }
}
