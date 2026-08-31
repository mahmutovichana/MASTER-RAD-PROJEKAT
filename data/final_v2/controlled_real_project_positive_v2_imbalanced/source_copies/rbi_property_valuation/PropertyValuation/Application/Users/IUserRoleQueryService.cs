using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Users.Models;

namespace RBBH.CollateralAppraisal.Application.Users;

/// <summary>
/// Servis za read-only pregled korisnika i njihovih rola s izračunatim permission-ima.
///
/// Odgovornosti:
/// - poziva IUserRoleProvider za sirove podatke,
/// - računa EffectivePermissions putem RolePermissionMatrix,
/// - uklanja duple permission-e,
/// - označava nepoznate role kao IsSupported=false,
/// - popunjava CanRemove i RemoveBlockedReason na osnovu poslovnih pravila,
/// - popunjava CanManageRoles za listu korisnika.
///
/// NE mijenja role, NE dodijeljuje role, NE briše role.
/// Implementacija: UserRoleQueryService (Infrastructure/Users/).
/// </summary>
public interface IUserRoleQueryService
{
    /// <summary>
    /// Paginirana lista korisnika s izračunatim EffectivePermissions i CanManageRoles.
    /// Baca ValidationException ako je Role filter nepoznat.
    /// </summary>
    Task<PagedResult<UserRoleListItemDto>> GetUsersWithRolesAsync(
        UserRoleListRequest request,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Detaljan prikaz jednog korisnika sa svim rolama, CanRemove indikatorima i EffectivePermissions.
    /// Vraća null ako korisnik ne postoji (endpoint treba vratiti 404).
    /// </summary>
    Task<UserRolesDetailDto?> GetUserRolesAsync(
        string userId,
        CancellationToken cancellationToken = default);
}
