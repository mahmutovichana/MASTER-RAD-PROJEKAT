using RBBH.CollateralAppraisal.Api.Middleware;
using RBBH.CollateralAppraisal.Application;
using RBBH.CollateralAppraisal.Application.Common.Modules;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Infrastructure;
using RBBH.CollateralAppraisal.Infrastructure.Notifications;

namespace RBBH.CollateralAppraisal.Api.Extensions;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddApiServices(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddApplication();
        services.AddInfrastructure(configuration);

        // Notification provider — EmailNotificationProvider šalje emailove preko SMTP-a;
        // ako "Smtp:Host" nije konfigurisan, samo loguje (npr. lokalni dev bez mail servera).
        services.AddScoped<INotificationProvider, EmailNotificationProvider>();
        services.Configure<OrderNotificationsOptions>(
            configuration.GetSection(OrderNotificationsOptions.SectionName));
        services.Configure<WorkflowSlaOptions>(
            configuration.GetSection(WorkflowSlaOptions.SectionName));
        services.Configure<SmtpOptions>(
            configuration.GetSection(SmtpOptions.SectionName));

        // ── Feature modul auto-discovery (IFeatureModule) ───────────────────────
        // Svaki feature (T2-T8) registruje vlastite servise kroz IFeatureModule
        // implementaciju u Application/Infrastructure/Api — bez izmjene ovog fajla.
        // Vidi docs/backend/feature-module-pattern.md.
        services.AddFeatureModules(
            configuration,
            typeof(RBBH.CollateralAppraisal.Application.DependencyInjection).Assembly,
            typeof(RBBH.CollateralAppraisal.Infrastructure.DependencyInjection).Assembly,
            typeof(Program).Assembly);

        // Globalni handler za izuzetke — mapira poslovne exception-e na ProblemDetails
        services.AddExceptionHandler<GlobalExceptionHandler>();
        services.AddProblemDetails();

        // ── Health checks ─────────────────────────────────────────────────────
        services.AddHealthChecks()
            .AddCheck<DatabaseHealthCheck>(
                "database",
                tags: ["database"],
                failureStatus: Microsoft.Extensions.Diagnostics.HealthChecks.HealthStatus.Unhealthy)
            .AddCheck<MigrationHealthCheck>(
                "migrations",
                tags: ["database", "startup"],
                failureStatus: Microsoft.Extensions.Diagnostics.HealthChecks.HealthStatus.Unhealthy)
            .AddCheck<FileStorageHealthCheck>(
                "file-storage",
                tags: ["storage"],
                failureStatus: Microsoft.Extensions.Diagnostics.HealthChecks.HealthStatus.Degraded)
            .AddCheck<KeycloakHealthCheck>(
                "keycloak",
                tags: ["auth"],
                failureStatus: Microsoft.Extensions.Diagnostics.HealthChecks.HealthStatus.Degraded);

        // ── CORS ──────────────────────────────────────────────────────────────
        var allowedOrigins = configuration.GetSection("AllowedOrigins").Get<string[]>() ?? [];
        services.AddCors(options =>
        {
            options.AddDefaultPolicy(policy =>
                policy.WithOrigins(allowedOrigins)
                      .AllowAnyHeader()
                      .WithMethods("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS")
                      // React and API run on separate local origins. The shared HTTP
                      // client uses the antiforgery/session cookie together with the
                      // Keycloak bearer token, so the browser requires this header.
                      .AllowCredentials());
        });

        // Registruje sve permission-based policy-je iz AppPermissions.All
        services.AddPermissionPolicies();

        return services;
    }
}
