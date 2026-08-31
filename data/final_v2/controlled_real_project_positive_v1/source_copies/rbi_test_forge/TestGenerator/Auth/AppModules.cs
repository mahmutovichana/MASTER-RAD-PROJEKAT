namespace RBBH.TestAutomation.Api.Auth;

/// <summary>
/// Definicija modula aplikacije i matrica pristupa.
/// </summary>
public static class AppModules
{
    public const string Home = "Home";
    public const string Korisnici = "Korisnici";
    public const string Role = "Role";
    public const string Sifarnici = "Sifarnici";
    public const string Grupe = "Grupe";

    /// <summary>Test scenariji — Administrator, QA Lead, QA Inženjer i Developer.</summary>
    public const string TestScenarios = "TestScenarios";
    public const string TestGenerator = "TestGenerator";
    public const string Scenariji = "Scenariji";

    /// <summary>Import API (Swagger/OpenAPI) — Administrator, QA Lead i QA Inženjer.</summary>
    public const string ApiImport = "ApiImport";

    /// <summary>Audit Log — samo Administrator.</summary>
    public const string AuditLog = "AuditLog";
    public const string Postavke = "Postavke";

    /// <summary>API Ključevi (CI/CD tokeni) — Administrator i DevOps Inženjer.</summary>
    public const string ApiKeys = "ApiKeys";

    private static readonly Dictionary<string, string[]> _accessMatrix = new()
    {
        [Home] = [],
        [Korisnici] = [AppRoles.Administrator],
        [Role] = [AppRoles.Administrator],
        [Sifarnici] = [AppRoles.Administrator, AppRoles.QALead],
        [Grupe]         = [AppRoles.Administrator, AppRoles.QALead, AppRoles.QAInzenjer],
        [TestScenarios] = [AppRoles.Administrator, AppRoles.QALead, AppRoles.QAInzenjer, AppRoles.Developer],
        [TestGenerator] = [AppRoles.Administrator, AppRoles.QALead],
        [Scenariji]     = [AppRoles.Administrator, AppRoles.QALead, AppRoles.QAInzenjer],
        [ApiImport]     = [AppRoles.Administrator, AppRoles.QALead, AppRoles.QAInzenjer],
        [AuditLog]      = [AppRoles.Administrator],
        [Postavke]      = [AppRoles.Administrator],
        [ApiKeys]       = [AppRoles.Administrator, AppRoles.DevOpsInzenjer],
    };

    public static bool CanAccess(string module, string[]? userRoles)
    {
        if (!_accessMatrix.TryGetValue(module, out var allowedRoles))
            return false;

        return allowedRoles.Length == 0 || AppRoles.HasAnyRole(userRoles, allowedRoles);
    }

    public static string[] GetAllowedRoles(string module) =>
        _accessMatrix.TryGetValue(module, out var roles) ? roles : [];
}
