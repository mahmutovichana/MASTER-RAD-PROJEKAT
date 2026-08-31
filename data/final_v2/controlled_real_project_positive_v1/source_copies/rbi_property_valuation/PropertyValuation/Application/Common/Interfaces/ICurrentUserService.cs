namespace RBBH.CollateralAppraisal.Application.Common.Interfaces;

public interface ICurrentUserService
{
    string? UserId          { get; }
    string? Username        { get; }
    string? Email           { get; }

    /// <summary>
    /// Puno ime korisnika (npr. "Haris Hadžić") — iz "name" claim-a (Keycloak full-name
    /// mapper), uz fallback na given_name+family_name, pa na <see cref="Username"/>.
    /// Koristi se za "Ime AM/SM/UB" polje i CreatedByName na narudžbi.
    /// </summary>
    string? FullName        { get; }

    /// <summary>
    /// Primarna (prva) rola korisnika — koristi se za audit log ActorRole polje.
    /// Za autorizacijske provjere koristiti <see cref="Roles"/>.
    /// </summary>
    string? Role            { get; }

    /// <summary>
    /// Sve role korisnika — koristi se za izračun permission-a putem RolePermissionMatrix.
    /// Podržava korisnike sa više rola.
    /// </summary>
    IReadOnlyList<string> Roles { get; }

    /// <summary>
    /// Efektivne permission-e korisnika — izračunate od strane PermissionClaimsTransformation
    /// i dodane kao "permission" claim-ovi u ClaimsPrincipal.
    /// </summary>
    IReadOnlyList<string> Permissions { get; }

    bool IsAuthenticated    { get; }
}
