using Microsoft.AspNetCore.Diagnostics.HealthChecks;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

public static class HealthEndpoints
{
    public static IEndpointRouteBuilder MapHealthEndpoints(this IEndpointRouteBuilder app)
    {
        // Spec (Backend Upute §24.1): /api/health provjerava API, /api/health/db provjerava bazu.
        app.MapHealthChecks("/api/health").AllowAnonymous();
        app.MapHealthChecks("/api/health/db", new HealthCheckOptions
        {
            Predicate = check => check.Tags.Contains("database")
        }).AllowAnonymous();

        app.MapHealthChecks("/api/health/storage", new HealthCheckOptions
        {
            Predicate = check => check.Tags.Contains("storage")
        }).AllowAnonymous();

        app.MapHealthChecks("/api/health/auth", new HealthCheckOptions
        {
            Predicate = check => check.Tags.Contains("auth")
        }).AllowAnonymous();

        // Standardni liveness/readiness aliasi (orchestratori, nginx).
        app.MapHealthChecks("/health").AllowAnonymous();
        app.MapHealthChecks("/health/ready").AllowAnonymous();
        app.MapHealthChecks("/health/live").AllowAnonymous();

        return app;
    }
}
