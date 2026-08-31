using Microsoft.Extensions.Configuration;

namespace RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;

public sealed class E2EConfig
{
    public string BaseUrl               { get; init; } = "http://localhost:5001";
    public string ApiUrl                { get; init; } = "http://localhost:5000";
    public string KeycloakUrl           { get; init; } = "http://localhost:8080";
    public string KeycloakRealm         { get; init; } = "rbbh";
    public string KeycloakClientId      { get; init; } = "collateral-appraisal-web";
    public bool   Headless              { get; init; } = true;
    public int    SlowMo                { get; init; } = 0;
    public int    Timeout               { get; init; } = 15000;
    public int    WorkflowTestTimeoutMs { get; init; } = 90000;
    public Dictionary<string, UserCredentials> Users { get; init; } = [];

    public UserCredentials GetUser(string role) =>
        Users.TryGetValue(role, out var u) ? u
            : throw new InvalidOperationException(
                $"Korisnik za ulogu '{role}' nije konfigurisan u appsettings.e2e.json. " +
                $"Dostupne uloge: {string.Join(", ", Users.Keys)}");

    public static E2EConfig Load()
    {
        var cfg = new ConfigurationBuilder()
            .SetBasePath(AppContext.BaseDirectory)
            .AddJsonFile("appsettings.e2e.json", optional: false)
            // CI override: E2E__BaseUrl, E2E__ApiUrl itd. kao environment varijable
            .AddEnvironmentVariables()
            .Build();

        var config = new E2EConfig();
        cfg.GetSection("E2E").Bind(config);
        return config;
    }
}

public sealed class UserCredentials
{
    public string Username { get; init; } = "";
    public string Password { get; init; } = "";
    public string Role     { get; init; } = "";
}
