using RBBH.CollateralAppraisal.Application.Security.DTOs;

namespace RBBH.CollateralAppraisal.Application.Security.Interfaces;

/// <summary>
/// Upravljanje rolama korisnika — dodjela, uklanjanje i prenos administratorske role.
///
/// Poslovna pravila koja ovaj servis mora provjeriti:
/// BR-ROLE-02: Samo Administrator može dodjeljivati i uklanjati role.
/// BR-ROLE-03: Samo Administrator može prenijeti administratorsku rolu.
/// BR-ROLE-04: Sistem ne smije ostati bez najmanje jednog aktivnog Administratora.
/// BR-ROLE-11: Sve izmjene rola moraju biti auditirane.
/// BR-ROLE-12: Pokušaj uklanjanja posljednjeg Administratora mora biti blokiran i auditiran.
///
/// Implementirano: Infrastructure/Auth/RoleManagementService.cs (Keycloak Admin API).
/// </summary>
public interface IRoleManagementService
{
    /// <summary>
    /// Dodjeljuje rolu korisniku.
    /// Baca <see cref="Common.Exceptions.NotFoundException"/> ako korisnik ili rola ne postoje.
    /// Baca <see cref="Common.Exceptions.ConflictException"/> ako korisnik već ima tu rolu.
    /// </summary>
    Task AssignRoleAsync(AssignRoleRequest request, CancellationToken ct = default);

    /// <summary>
    /// Uklanja rolu korisniku.
    /// Baca <see cref="Common.Exceptions.ConflictException"/> ako bi uklanjanje narušilo minimum Administratora.
    /// </summary>
    Task RemoveRoleAsync(RemoveRoleRequest request, CancellationToken ct = default);

    /// <summary>
    /// Prenosi Administrator rolu sa trenutnog korisnika na ciljnog korisnika.
    /// Slijed mora biti siguran: prvo dodaj B, pa ukloni A (nikad obrnuto).
    /// Baca <see cref="Common.Exceptions.ConflictException"/> ako bi rezultiralo 0 aktivnih Administratora.
    /// </summary>
    Task TransferAdminRoleAsync(TransferAdminRoleRequest request, CancellationToken ct = default);
}
