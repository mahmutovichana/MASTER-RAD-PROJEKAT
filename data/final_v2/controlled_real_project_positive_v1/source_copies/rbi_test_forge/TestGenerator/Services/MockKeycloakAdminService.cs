using RBBH.TestAutomation.Api.Auth;

namespace RBBH.TestAutomation.Api.Services;

/// <summary>
/// Dev implementacija — radi bez Keycloak-a.
/// Registruje se kao Singleton da promjene rola opstaju između navigacija.
/// </summary>
public sealed class MockKeycloakAdminService : IKeycloakAdminService
{
    private static readonly List<KeycloakUserDto> _users =
    [
        new("mock-admin-001", "admin",        "Admin Korisnik",    "admin@tag.local",        true),
        new("mock-qal-001",   "qalead1",      "QA Lead Jedan",     "qalead1@tag.local",      true),
        new("mock-qal-002",   "qalead2",      "QA Lead Dva",       "qalead2@tag.local",      true),
        new("mock-qae-001",   "qaengineer1",  "QA Inzenjer Jedan", "qaengineer1@tag.local",  true),
        new("mock-qae-002",   "qaengineer2",  "QA Inzenjer Dva",   "qaengineer2@tag.local",  true),
        new("mock-dev-001",   "developer1",   "Developer Jedan",   "developer1@tag.local",   true),
        new("mock-dev-002",   "developer2",   "Developer Dva",     "developer2@tag.local",   true),
        new("mock-ops-001",   "devops1",      "DevOps Jedan",      "devops1@tag.local",      true),
        new("mock-ops-002",   "devops2",      "DevOps Dva",        "devops2@tag.local",      true),
    ];

    // Singleton state — promjene opstaju tokom životnog vijeka procesa
    private static readonly Dictionary<string, List<string>> _roles = new()
    {
        ["mock-admin-001"] = [AppRoles.Administrator],
        ["mock-qal-001"]   = [AppRoles.QALead],
        ["mock-qal-002"]   = [AppRoles.QALead],
        ["mock-qae-001"]   = [AppRoles.QAInzenjer],
        ["mock-qae-002"]   = [AppRoles.QAInzenjer],
        ["mock-dev-001"]   = [AppRoles.Developer],
        ["mock-dev-002"]   = [AppRoles.Developer],
        ["mock-ops-001"]   = [AppRoles.DevOpsInzenjer],
        ["mock-ops-002"]   = [AppRoles.DevOpsInzenjer],
    };

    private static readonly Lock _lock = new();

    public Task<IReadOnlyList<UserWithRolesDto>> GetUsersWithRolesAsync(CancellationToken ct = default)
    {
        lock (_lock)
        {
            IReadOnlyList<UserWithRolesDto> result = _users
                .Select(u => new UserWithRolesDto(u, new List<string>(_roles.GetValueOrDefault(u.Id, []))))
                .ToList();
            return Task.FromResult(result);
        }
    }

    public Task AssignRoleAsync(string userId, string roleName, CancellationToken ct = default)
    {
        lock (_lock)
        {
            if (!_roles.TryGetValue(userId, out var roles))
            {
                roles = [];
                _roles[userId] = roles;
            }
            if (!roles.Contains(roleName, StringComparer.OrdinalIgnoreCase))
                roles.Add(roleName);
        }
        return Task.CompletedTask;
    }

    public Task RemoveRoleAsync(string userId, string roleName, CancellationToken ct = default)
    {
        lock (_lock)
        {
            if (_roles.TryGetValue(userId, out var roles))
                roles.RemoveAll(r => string.Equals(r, roleName, StringComparison.OrdinalIgnoreCase));
        }
        return Task.CompletedTask;
    }
}
