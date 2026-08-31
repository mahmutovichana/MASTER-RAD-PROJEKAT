using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Users.Models;

namespace RBBH.CollateralAppraisal.Application.Users;

/// <summary>
/// Adapter za izvor korisnika i njihovih rola.
/// Application sloj ne zna da li podatke čita lokalna baza, Keycloak ili vanjski sistem.
///
/// Aktivna implementacija:
/// - KeycloakUserRoleProvider (Infrastructure) — čita putem Keycloak Admin API
///
/// PRAVILO: Provider vraća korisničke podatke i role, ali NE računa permission-e.
/// Effective permissions se računaju u IUserRoleQueryService putem RolePermissionMatrix.
/// </summary>
public interface IUserRoleProvider
{
    /// <summary>
    /// Vraća paginiranu listu korisnika sa njihovim rolama.
    /// Podržava search (username, displayName, email), filter po roli i filter po IsActive.
    /// </summary>
    Task<PagedResult<UserRoleSourceItem>> GetUsersWithRolesAsync(
        UserRoleListRequest request,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Vraća jednog korisnika sa svim rolama.
    /// Vraća null ako korisnik ne postoji (endpoint treba vratiti 404).
    /// </summary>
    Task<UserRoleSourceItem?> GetUserWithRolesAsync(
        string userId,
        CancellationToken cancellationToken = default);
}
