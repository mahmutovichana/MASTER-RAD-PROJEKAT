namespace RBBH.CollateralAppraisal.Application.Users.Models;

/// <summary>
/// Jedna dodijeljena rola u sklopu UserRolesDetailDto.
/// IsSupported=false označava rolu koja nije poznata aplikaciji (ne daje permission-e).
/// CanRemove i RemoveBlockedReason su UI pomoćna polja — backend uvijek sam validira.
/// </summary>
public sealed class UserAssignedRoleDto
{
    public string Role { get; init; } = string.Empty;

    /// <summary>Čitljiv naziv role, npr. "Administrator", "Unosnik podataka".</summary>
    public string Label { get; init; } = string.Empty;

    /// <summary>True ako je rola poznata aplikaciji (postoji u AppRoles.All).</summary>
    public bool IsSupported { get; init; }

    /// <summary>True za sistemske role koje ne mogu biti trajno obrisane/promijenjene van aplikacije.</summary>
    public bool IsSystemRole { get; init; }

    /// <summary>
    /// UI hint: može li se rola ukloniti ovom korisniku.
    /// False primjeri: korisnik je jedini Administrator, rola je zaključana, korisnik je neaktivan.
    /// NIJE zamjena za backend validaciju — remove endpoint mora sam provjeriti.
    /// </summary>
    public bool CanRemove { get; init; }

    /// <summary>Razlog blokade uklanjanja, npr. "Nije moguće ukloniti posljednjeg Administratora."</summary>
    public string? RemoveBlockedReason { get; init; }
}
