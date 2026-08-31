namespace RBBH.TestAutomation.Api.Auth;

/// <summary>
/// Development IUserContext — simulates an authenticated user without Keycloak.
///
/// Configuration (appsettings.Development.json):
///   "MockAuth": { "Enabled": true, "ActiveUser": "qaengineer1" }
///
/// Change ActiveUser to any key in KnownUsers to switch the simulated persona.
/// The component tree updates on the next page reload — no restart needed.
///
/// Available users mirror the realm-import.json test accounts exactly,
/// so the mock and the real Keycloak use identical identifiers and roles.
/// </summary>
public sealed class MockUserContext : IUserContext
{
    private record MockUser(string Id, string FullName, string Email, string[] Roles);

    private static readonly Dictionary<string, MockUser> KnownUsers =
        new(StringComparer.OrdinalIgnoreCase)
        {
            ["admin"]        = new("mock-admin-001", "Admin Korisnik",    "admin@tag.local",        [AppRoles.Administrator]),
            ["qalead1"]      = new("mock-qal-001",   "QA Lead Jedan",     "qalead1@tag.local",      [AppRoles.QALead]),
            ["qalead2"]      = new("mock-qal-002",   "QA Lead Dva",       "qalead2@tag.local",      [AppRoles.QALead]),
            ["qaengineer1"]  = new("mock-qae-001",   "QA Inzenjer Jedan", "qaengineer1@tag.local",  [AppRoles.QAInzenjer]),
            ["qaengineer2"]  = new("mock-qae-002",   "QA Inzenjer Dva",   "qaengineer2@tag.local",  [AppRoles.QAInzenjer]),
            ["developer1"]   = new("mock-dev-001",   "Developer Jedan",   "developer1@tag.local",   [AppRoles.Developer]),
            ["developer2"]   = new("mock-dev-002",   "Developer Dva",     "developer2@tag.local",   [AppRoles.Developer]),
            ["devops1"]      = new("mock-ops-001",   "DevOps Jedan",      "devops1@tag.local",      [AppRoles.DevOpsInzenjer]),
            ["devops2"]      = new("mock-ops-002",   "DevOps Dva",        "devops2@tag.local",      [AppRoles.DevOpsInzenjer]),
        };

    private readonly MockUser _user;

    public MockUserContext(IConfiguration config)
    {
        var key = config["MockAuth:ActiveUser"] ?? "admin";
        _user = KnownUsers.GetValueOrDefault(key) ?? KnownUsers["admin"];
    }

    public string UserId         => _user.Id;
    public string FullName       => _user.FullName;
    public string Email          => _user.Email;
    public string[] Roles        => _user.Roles;
    public bool IsAuthenticated  => true;
    public string Initials       => BuildInitials(_user.FullName);

    public bool HasRole(string role)              => AppRoles.HasRole(Roles, role);
    public bool HasAnyRole(params string[] roles) => AppRoles.HasAnyRole(Roles, roles);
    public bool CanAccess(string module)          => AppModules.CanAccess(module, Roles);

    private static string BuildInitials(string fullName)
    {
        var parts = fullName.Split(' ', StringSplitOptions.RemoveEmptyEntries);
        return parts.Length switch
        {
            0 => "?",
            1 => parts[0][..1].ToUpperInvariant(),
            _ => $"{parts[0][0]}{parts[^1][0]}".ToUpperInvariant()
        };
    }
}
