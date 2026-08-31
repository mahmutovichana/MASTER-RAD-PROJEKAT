using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Security.Interfaces;

namespace RBBH.CollateralAppraisal.Infrastructure.Security;

/// <summary>
/// Implementacija <see cref="IUserPermissionService"/>.
/// Izračunava permission-e trenutnog korisnika putem <see cref="RolePermissionMatrix"/>.
/// Podržava korisnike sa više rola — permission-e se sabiraju.
/// </summary>
public class UserPermissionService : IUserPermissionService
{
    private readonly ICurrentUserService _currentUser;

    public UserPermissionService(ICurrentUserService currentUser)
    {
        _currentUser = currentUser;
    }

    public bool CurrentUserHasPermission(string permission) =>
        RolePermissionMatrix
            .GetPermissionsForRoles(_currentUser.Roles)
            .Contains(permission);
}
