using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using RBBH.TestAutomation.Core.Infrastructure;

namespace RBBH.TestAutomation.Api.Health;

/// <summary>
/// Provjerava da app može otvoriti konekciju na bazu (TestForgeDbContext).
/// Pravi vlastiti scope (DbContext je Scoped, health check radi iz root providera).
/// </summary>
public sealed class DatabaseHealthCheck(IServiceScopeFactory scopeFactory) : IHealthCheck
{
    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context, CancellationToken cancellationToken = default)
    {
        try
        {
            using var scope = scopeFactory.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<TestForgeDbContext>();
            return await db.Database.CanConnectAsync(cancellationToken)
                ? HealthCheckResult.Healthy("Baza dostupna")
                : HealthCheckResult.Unhealthy("Baza nedostupna (CanConnect=false)");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("Greška pri konekciji na bazu", ex);
        }
    }
}

/// <summary>
/// Provjerava da je Keycloak realm dohvatljiv (OIDC discovery dokument).
/// Gađa interni Authority (keycloak:8080) — isti koji app koristi za login.
/// </summary>
public sealed class KeycloakHealthCheck(IHttpClientFactory httpFactory, IConfiguration config)
    : IHealthCheck
{
    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context, CancellationToken cancellationToken = default)
    {
        var authority = config["OpenIDConnectSettings:Authority"];
        if (string.IsNullOrWhiteSpace(authority))
            return HealthCheckResult.Healthy("Keycloak je namjerno isključen; koristi se lokalna autentifikacija.");

        try
        {
            var http = httpFactory.CreateClient();
            http.Timeout = TimeSpan.FromSeconds(5);
            var url = $"{authority.TrimEnd('/')}/.well-known/openid-configuration";
            var resp = await http.GetAsync(url, cancellationToken);
            return resp.IsSuccessStatusCode
                ? HealthCheckResult.Healthy("Keycloak realm dostupan")
                : HealthCheckResult.Unhealthy($"Keycloak vratio HTTP {(int)resp.StatusCode}");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("Keycloak nedostupan", ex);
        }
    }
}
