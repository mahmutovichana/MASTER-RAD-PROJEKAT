using RBBH.CollateralAppraisal.Application.Roles.Interfaces;

namespace RBBH.CollateralAppraisal.Infrastructure.Roles;

/// <summary>
/// Lokalna zamjena kada Keycloak nije konfigurisan. Poslovne role ostaju u
/// aplikacijskoj bazi, dok se vanjski pozivi namjerno preskaču.
/// </summary>
public sealed class NullKeycloakRoleSyncService : IKeycloakRoleSyncService
{
    public Task CreateRoleAsync(string roleName, string? description, CancellationToken ct = default) => Task.CompletedTask;
    public Task UpdateRoleAsync(string roleName, string? description, CancellationToken ct = default) => Task.CompletedTask;
    public Task DeleteRoleAsync(string roleName, CancellationToken ct = default) => Task.CompletedTask;
    public Task<bool> RoleExistsAsync(string roleName, CancellationToken ct = default) => Task.FromResult(false);
    public Task<int> GetRoleUserCountAsync(string roleName, CancellationToken ct = default) => Task.FromResult(0);
    public Task AssignRoleToUserAsync(string userId, string roleName, CancellationToken ct = default) => Task.CompletedTask;
    public Task RemoveRoleFromUserAsync(string userId, string roleName, CancellationToken ct = default) => Task.CompletedTask;
    public Task<IReadOnlyList<string>> GetUserRealmRolesAsync(string userId, CancellationToken ct = default) =>
        Task.FromResult<IReadOnlyList<string>>(Array.Empty<string>());
}
