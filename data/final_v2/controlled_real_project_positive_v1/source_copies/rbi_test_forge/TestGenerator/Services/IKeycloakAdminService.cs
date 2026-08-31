namespace RBBH.TestAutomation.Api.Services;

public interface IKeycloakAdminService
{
    /// <summary>Vraća sve korisnike s njihovim rolama u jednom pozivu.</summary>
    Task<IReadOnlyList<UserWithRolesDto>> GetUsersWithRolesAsync(CancellationToken ct = default);

    /// <summary>Dodjeljuje rolu korisniku.</summary>
    Task AssignRoleAsync(string userId, string roleName, CancellationToken ct = default);

    /// <summary>Uklanja rolu od korisnika.</summary>
    Task RemoveRoleAsync(string userId, string roleName, CancellationToken ct = default);
}

public sealed record KeycloakUserDto(
    string Id,
    string Username,
    string FullName,
    string Email,
    bool Enabled
);

public sealed record UserWithRolesDto(KeycloakUserDto User, List<string> Roles);
