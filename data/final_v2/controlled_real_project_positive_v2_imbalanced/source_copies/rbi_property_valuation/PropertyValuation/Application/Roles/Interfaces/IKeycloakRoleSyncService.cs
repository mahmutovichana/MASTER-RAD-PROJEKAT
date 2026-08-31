namespace RBBH.CollateralAppraisal.Application.Roles.Interfaces;

/// <summary>
/// Sinhronizacija definicija rola i korisničkih role mappinga između SQL Server i Keycloak.
///
/// Sve metode su idempotentne gdje je moguće (create not fails if exists, delete not fails if missing).
/// </summary>
public interface IKeycloakRoleSyncService
{
    // ── Role definicije ───────────────────────────────────────────────────────

    /// <summary>Kreira realm rolu u Keycloak-u. Ne baca grešku ako rola već postoji (idempotentno).</summary>
    Task CreateRoleAsync(string roleName, string? description, CancellationToken ct = default);

    /// <summary>Ažurira opis realm role u Keycloak-u.</summary>
    Task UpdateRoleAsync(string roleName, string? description, CancellationToken ct = default);

    /// <summary>Briše realm rolu iz Keycloak-a. Ne baca grešku ako rola ne postoji (idempotentno).</summary>
    Task DeleteRoleAsync(string roleName, CancellationToken ct = default);

    /// <summary>Vraća true ako rola postoji u Keycloak-u.</summary>
    Task<bool> RoleExistsAsync(string roleName, CancellationToken ct = default);

    /// <summary>Vraća broj korisnika koji imaju datu rolu u Keycloak-u.</summary>
    Task<int> GetRoleUserCountAsync(string roleName, CancellationToken ct = default);

    // ── Korisnik–rola mappinzi ─────────────────────────────────────────────────

    /// <summary>Dodjeljuje realm rolu korisniku u Keycloak-u.</summary>
    Task AssignRoleToUserAsync(string userId, string roleName, CancellationToken ct = default);

    /// <summary>Uklanja realm rolu od korisnika u Keycloak-u.</summary>
    Task RemoveRoleFromUserAsync(string userId, string roleName, CancellationToken ct = default);

    /// <summary>Vraća listu realm rola koje korisnik ima u Keycloak-u.</summary>
    Task<IReadOnlyList<string>> GetUserRealmRolesAsync(string userId, CancellationToken ct = default);
}
