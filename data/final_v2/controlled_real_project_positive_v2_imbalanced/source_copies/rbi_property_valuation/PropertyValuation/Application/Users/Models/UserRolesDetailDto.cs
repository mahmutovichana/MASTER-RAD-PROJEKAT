namespace RBBH.CollateralAppraisal.Application.Users.Models;

/// <summary>
/// Detaljni prikaz korisnika, njegovih rola i effective permission-a.
/// Koristi se za GET /api/role-management/users/{userId}/roles.
/// Roles lista sadrži UserAssignedRoleDto sa CanRemove i RemoveBlockedReason poljem.
/// </summary>
public sealed class UserRolesDetailDto
{
    public string UserId { get; init; } = string.Empty;
    public string Username { get; init; } = string.Empty;
    public string? DisplayName { get; init; }
    public string? Email { get; init; }
    public bool IsActive { get; init; }
    public IReadOnlyList<UserAssignedRoleDto> Roles { get; init; } = [];

    /// <summary>Unija permission-a svih rola, bez duplikata, izračunata putem RolePermissionMatrix.</summary>
    public IReadOnlyList<string> EffectivePermissions { get; init; } = [];
}
