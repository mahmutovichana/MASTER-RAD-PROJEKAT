namespace RBBH.CollateralAppraisal.Application.Users.Models;

/// <summary>
/// Lagani DTO za paginiranu listu korisnika i njihovih rola.
/// EffectivePermissions je unija permission-a svih rola, bez duplikata.
/// CanManageRoles je UI pomoćno polje — nije sigurnosna zaštita.
/// </summary>
public sealed class UserRoleListItemDto
{
    public string UserId { get; init; } = string.Empty;
    public string Username { get; init; } = string.Empty;
    public string? DisplayName { get; init; }
    public string? Email { get; init; }
    public bool IsActive { get; init; }
    public IReadOnlyList<string> Roles { get; init; } = [];
    public IReadOnlyList<string> EffectivePermissions { get; init; } = [];

    /// <summary>
    /// True ako trenutni admin koji pregledava listu ima roles.assign ili roles.remove.
    /// Pomaže frontendu da prikaže ili sakrije akcijske dugmiće.
    /// </summary>
    public bool CanManageRoles { get; init; }
}
