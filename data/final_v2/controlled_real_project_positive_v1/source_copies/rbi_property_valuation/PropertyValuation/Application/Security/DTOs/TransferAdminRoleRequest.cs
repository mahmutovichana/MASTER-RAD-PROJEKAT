namespace RBBH.CollateralAppraisal.Application.Security.DTOs;

/// <summary>
/// Request za prenos administratorske role na drugog korisnika.
/// Endpoint: POST /api/roles/transfer-admin
/// Policy: AppPolicies.RolesTransferAdmin
///
/// Siguran redoslijed izvršenja (EC-ROLE-24):
/// 1. Provjeri da TargetUserId postoji i da je aktivan.
/// 2. Dodaj Administrator rolu korisniku TargetUserId.
/// 3. Potvrdi da TargetUserId sada ima Administrator rolu.
/// 4. Tek onda ukloni Administrator rolu korisniku SourceUserId (ako je transfer, a ne samo dodjela).
/// 5. Auditiraj akciju sa ADMIN_ROLE_TRANSFERRED.
/// </summary>
public sealed record TransferAdminRoleRequest(
    /// <summary>ID korisnika koji predaje administratorsku rolu.</summary>
    string SourceUserId,
    /// <summary>ID korisnika koji prima administratorsku rolu.</summary>
    string TargetUserId,
    /// <summary>Razlog prenosa — obavezan radi audita i transparentnosti.</summary>
    string Reason
);
