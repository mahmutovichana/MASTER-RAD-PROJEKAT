using Microsoft.Extensions.Diagnostics.HealthChecks;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Api.Middleware;

/// <summary>
/// Health check koji provjerava konekciju na konfiguriranu bazu putem EF Core.
/// Ne zahtijeva dodatni NuGet paket — koristi postojeći DbContext.
/// </summary>
public sealed class DatabaseHealthCheck : IHealthCheck
{
    private readonly ApplicationDbContext _db;

    public DatabaseHealthCheck(ApplicationDbContext db) => _db = db;

    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            var canConnect = await _db.Database.CanConnectAsync(cancellationToken);
            return canConnect
                ? HealthCheckResult.Healthy("Konekcija prema bazi je uspješna.")
                : HealthCheckResult.Unhealthy("Baza nije dostupna.");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("Greška pri provjeri baze: " + ex.Message);
        }
    }
}
