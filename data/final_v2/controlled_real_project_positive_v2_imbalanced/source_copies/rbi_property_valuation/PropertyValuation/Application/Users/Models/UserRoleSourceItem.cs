namespace RBBH.CollateralAppraisal.Application.Users.Models;

/// <summary>
/// Sirovi podatak koji dolazi iz IUserRoleProvider izvora (lokalna baza, Keycloak, vanjska baza).
/// Provider vraća ove podatke bez interpretacije permission-a.
/// Effective permissions se računaju u IUserRoleQueryService putem RolePermissionMatrix.
/// </summary>
public sealed class UserRoleSourceItem
{
    public string UserId { get; init; } = string.Empty;
    public string Username { get; init; } = string.Empty;
    public string? DisplayName { get; init; }
    public string? Email { get; init; }
    public bool IsActive { get; init; }

    /// <summary>
    /// Role korisnika iz izvora. Može sadržavati nepoznate role — IUserRoleQueryService ih označava kao IsSupported=false.
    /// Null se tretira kao prazna lista.
    /// </summary>
    public IReadOnlyList<string> Roles { get; init; } = [];
}
