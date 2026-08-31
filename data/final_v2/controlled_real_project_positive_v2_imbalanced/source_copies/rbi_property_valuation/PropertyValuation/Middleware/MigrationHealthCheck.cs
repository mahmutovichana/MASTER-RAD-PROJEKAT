using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Api.Middleware;

/// <summary>
/// Health check koji provjerava da li su sve EF Core migracije primijenjene.
/// Ako postoje neprimijenjene migracije, health status je Unhealthy.
///
/// NAPOMENA: Ovaj check je SAMO dijagnostički — ne primjenjuje migracije.
/// Migracije se primjenjuju automatski pri startupu u WebApplicationExtensions.ApplyMigrationsAsync(),
/// prije nego što Kestrel počne prihvatati veze. U normalnom scenariju ovaj check će uvijek
/// biti Healthy jer migracije su već primijenjene pri pokretanju.
/// </summary>
public sealed class MigrationHealthCheck : IHealthCheck
{
    private readonly ApplicationDbContext _db;
    private readonly ILogger<MigrationHealthCheck> _logger;

    public MigrationHealthCheck(ApplicationDbContext db, ILogger<MigrationHealthCheck> logger)
    {
        _db     = db;
        _logger = logger;
    }

    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            if (!_db.Database.IsRelational())
                return HealthCheckResult.Healthy("Lokalna in-memory baza ne zahtijeva migracije.");

            var pending = await _db.Database.GetPendingMigrationsAsync(cancellationToken);
            var pendingList = pending.ToList();

            if (pendingList.Count == 0)
                return HealthCheckResult.Healthy("Sve migracije su primijenjene.");

            _logger.LogWarning(
                "Postoji {Count} ne-primijenjenih migracija: {Migrations}",
                pendingList.Count, string.Join(", ", pendingList));

            return HealthCheckResult.Unhealthy(
                $"{pendingList.Count} migracija nije primijenjeno: {string.Join(", ", pendingList)}",
                data: new Dictionary<string, object> { ["pendingMigrations"] = pendingList });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Migration health check nije uspio.");
            return HealthCheckResult.Degraded("Nije moguće provjeriti migracije — baza možda nije dostupna.");
        }
    }
}
