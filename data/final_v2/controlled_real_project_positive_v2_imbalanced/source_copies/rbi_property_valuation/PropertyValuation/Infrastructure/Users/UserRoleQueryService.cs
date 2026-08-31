using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Security.Interfaces;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Application.Users.Models;

namespace RBBH.CollateralAppraisal.Infrastructure.Users;

/// <summary>
/// Implementacija IUserRoleQueryService.
/// Poziva IUserRoleProvider za sirove podatke, računa EffectivePermissions putem RolePermissionMatrix
/// i određuje CanManageRoles na osnovu permissiona pregledatelja.
/// Ne mijenja role, ne dodjeljuje, ne briše.
/// </summary>
public class UserRoleQueryService : IUserRoleQueryService
{
    private readonly IUserRoleProvider _userRoleProvider;
    private readonly IUserPermissionService _permissionService;

    private static readonly IReadOnlyDictionary<string, string> _roleLabels =
        new Dictionary<string, string>
        {
            [AppRoles.Administrator] = "Administrator",
            [AppRoles.Unosnik]       = "Unosnik podataka",
            [AppRoles.Verifikator]   = "Verifikator podataka"
        };

    public UserRoleQueryService(
        IUserRoleProvider userRoleProvider,
        IUserPermissionService permissionService)
    {
        _userRoleProvider = userRoleProvider;
        _permissionService = permissionService;
    }

    public async Task<PagedResult<UserRoleListItemDto>> GetUsersWithRolesAsync(
        UserRoleListRequest request,
        CancellationToken cancellationToken = default)
    {
        var raw = await _userRoleProvider.GetUsersWithRolesAsync(request, cancellationToken);

        var canManageRoles =
            _permissionService.CurrentUserHasPermission(AppPermissions.RolesAssign) ||
            _permissionService.CurrentUserHasPermission(AppPermissions.RolesRemove);

        var items = raw.Items
            .Select(u => MapToListItemDto(u, canManageRoles))
            .ToList();

        return new PagedResult<UserRoleListItemDto>
        {
            Items = items,
            TotalCount = raw.TotalCount,
            Page = raw.Page,
            PageSize = raw.PageSize
        };
    }

    public async Task<UserRolesDetailDto?> GetUserRolesAsync(
        string userId,
        CancellationToken cancellationToken = default)
    {
        var raw = await _userRoleProvider.GetUserWithRolesAsync(userId, cancellationToken);
        if (raw is null) return null;

        var effectivePermissions = RolePermissionMatrix
            .GetPermissionsForRoles(raw.Roles)
            .OrderBy(p => p)
            .ToList()
            .AsReadOnly();

        var sortedRoles = RolePriorityResolver.SortByPriority(raw.Roles).ToList();
        var roles = sortedRoles
            .Select(role => new UserAssignedRoleDto
            {
                Role                = role,
                Label               = _roleLabels.GetValueOrDefault(role, role),
                IsSupported         = AppRoles.All.Contains(role),
                IsSystemRole        = AppRoles.All.Contains(role, StringComparer.OrdinalIgnoreCase),
                CanRemove           = true,
                RemoveBlockedReason = null
            })
            .ToList()
            .AsReadOnly();

        return new UserRolesDetailDto
        {
            UserId = raw.UserId,
            Username = raw.Username,
            DisplayName = raw.DisplayName,
            Email = raw.Email,
            IsActive = raw.IsActive,
            Roles = roles,
            EffectivePermissions = effectivePermissions
        };
    }

    private static UserRoleListItemDto MapToListItemDto(UserRoleSourceItem user, bool canManageRoles)
    {
        var effectivePermissions = RolePermissionMatrix
            .GetPermissionsForRoles(user.Roles)
            .OrderBy(p => p)
            .ToList()
            .AsReadOnly();

        return new UserRoleListItemDto
        {
            UserId = user.UserId,
            Username = user.Username,
            DisplayName = user.DisplayName,
            Email = user.Email,
            IsActive = user.IsActive,
            Roles = user.Roles,
            EffectivePermissions = effectivePermissions,
            CanManageRoles = canManageRoles
        };
    }
}
