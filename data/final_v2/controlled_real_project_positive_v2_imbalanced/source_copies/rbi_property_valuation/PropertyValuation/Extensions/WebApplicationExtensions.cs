using Microsoft.AspNetCore.HttpOverrides;
using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Api.Endpoints;
using RBBH.CollateralAppraisal.Api.Middleware;
using RBBH.CollateralAppraisal.Api.Modules;
using RBBH.CollateralAppraisal.Application.Common.Constants;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Roles.Interfaces;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using RBBH.CollateralAppraisal.Infrastructure.Seed;

namespace RBBH.CollateralAppraisal.Api.Extensions;

public static class WebApplicationExtensions
{
    public static async Task ApplyMigrationsAsync(this WebApplication app)
    {
        using var scope = app.Services.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();

        var isRelational = db.Database.IsRelational();
        if (!isRelational)
        {
            await db.Database.EnsureCreatedAsync();
            await SeedTestDataAsync(db);
        }
        else if (db.Database.GetMigrations().Any())
            await db.Database.MigrateAsync();
        else
            await db.Database.EnsureCreatedAsync();

        var loggerFactory = scope.ServiceProvider.GetService<ILoggerFactory>();

        // Idempotentno popunjavanje poslovnica i gradova.
        await BranchSeeder.SeedAsync(db);

        // Idempotentno popunjavanje šifarnika referentnim vrijednostima.
        var codebookLogger = loggerFactory?.CreateLogger("CodebookSeeder");
        await CodebookSeeder.SeedAsync(db, codebookLogger);

        // Idempotentno punjenje rola, permissiona i role-permission veza.
        // Greška seedera NE smije srušiti API — loguje se i nastavlja.
        var roleLogger   = loggerFactory?.CreateLogger("RolePermissionSeeder");
        var keycloakSync = scope.ServiceProvider.GetRequiredService<IKeycloakRoleSyncService>();
        try
        {
            await RolePermissionSeeder.SeedAsync(db, keycloakSync, roleLogger);
        }
        catch (Exception ex)
        {
            roleLogger?.LogError(ex,
                "RolePermissionSeeder nije uspio. Tabele vjerovatno još ne postoje (migracije nisu primijenjene). " +
                "Provjerite SQL Server šemu i ponovo pokrenite aplikaciju.");
            // Nastavljamo — API ostaje aktivan, seed će biti pokrenut pri sljedećem startupu
        }

        // Demo narudžbe se seeduju SAMO u Development i Staging okruženjima.
        // U produkciji bi insertovale lažne narudžbe u pravo bankarsko okruženje.
        if (app.Environment.IsDevelopment() || app.Environment.IsEnvironment("Staging"))
        {
            var appraiserLogger = loggerFactory?.CreateLogger("AppraiserSeeder");
            try
            {
                await AppraiserSeeder.SeedAsync(db, appraiserLogger);
            }
            catch (Exception ex)
            {
                appraiserLogger?.LogError(ex, "AppraiserSeeder nije uspio.");
            }

            var orderLogger = loggerFactory?.CreateLogger("AppraisalOrderSeeder");
            try
            {
                var fileStorage      = scope.ServiceProvider.GetRequiredService<IFileStorageProvider>();
                var userRoleProvider = scope.ServiceProvider.GetRequiredService<IUserRoleProvider>();
                await AppraisalOrderSeeder.SeedAsync(db, fileStorage, userRoleProvider, orderLogger);
            }
            catch (Exception ex)
            {
                orderLogger?.LogError(ex, "AppraisalOrderSeeder nije uspio.");
            }
        }

        // Idempotentno punjenje šablona dokumenata (narudžbenica, izjava, urneci za procjenu).
        var templateLogger = loggerFactory?.CreateLogger("DocumentTemplateSeeder");
        try
        {
            var fileStorage = scope.ServiceProvider.GetRequiredService<IFileStorageProvider>();
            await DocumentTemplateSeeder.SeedAsync(db, fileStorage, templateLogger);
        }
        catch (Exception ex)
        {
            templateLogger?.LogError(ex, "DocumentTemplateSeeder nije uspio.");
        }

        // Idempotentno punjenje dijeljenih dokumenata (cjenovnik, liste dokumentacije).
        var sharedDocLogger = loggerFactory?.CreateLogger("SharedDocumentSeeder");
        try
        {
            var fileStorage = scope.ServiceProvider.GetRequiredService<IFileStorageProvider>();
            await SharedDocumentSeeder.SeedAsync(db, fileStorage, sharedDocLogger);
        }
        catch (Exception ex)
        {
            sharedDocLogger?.LogError(ex, "SharedDocumentSeeder nije uspio.");
        }
    }

    public static WebApplication ConfigurePipeline(this WebApplication app)
    {
        // Iza reverse proxy-ja (Nginx) na zajedničkom VPS-u: app prima HTTP, a originalni
        // scheme/host stižu u X-Forwarded-* headerima. Bez ovoga UseHttpsRedirection pravi
        // redirect petlju, a generisani apsolutni URL-ovi (CORS, linkovi) su pogrešni.
        var forwardedOptions = new ForwardedHeadersOptions
        {
            ForwardedHeaders = ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto
        };
        // Proxy je u Docker mreži na nepoznatom IP-u; default trusta samo loopback, pa
        // bez čišćenja ovih lista forwarded headeri bi se ignorisali. Sigurno jer je app
        // dostupan samo Nginx-u unutar interne mreže.
        forwardedOptions.KnownIPNetworks.Clear();
        forwardedOptions.KnownProxies.Clear();
        app.UseForwardedHeaders(forwardedOptions);

        app.UseExceptionHandler();
        app.UseMiddleware<CorrelationIdMiddleware>();
        app.UseHttpsRedirection();
        app.UseCors();
        app.UseAuthentication();
        app.UseAuthorization();
        app.MapAllEndpoints();
        return app;
    }

    private static WebApplication MapAllEndpoints(this WebApplication app)
    {
        app.MapHealthEndpoints();
        app.MapMeEndpoints();
        app.MapCodebookEndpoints();
        app.MapCodebookAdminEndpoints();
        app.MapCollateralTypeEndpoints();
        app.MapUserRoleEndpoints();
        app.MapRoleManagementEndpoints();
        app.MapRoleDefinitionEndpoints();
        app.MapPermissionEndpoints();
        app.MapAuditEndpoints();
        app.MapAuthAuditEndpoints();
        // US-1, US-2: Narudžbe, protokol, taskovi
        app.MapOrderEndpoints();
        app.MapProtocolEndpoints();
        app.MapWorkflowTaskEndpoints();
        // US-93: CO odobrenje finalne procjene
        app.MapOrderApprovalEndpoints();
        // Poslovnice i gradovi
        app.MapBranchEndpoints();

        // ── Endpoint modul auto-discovery (IEndpointModule) ─────────────────────
        // Svaki feature (T2-T8) mapira vlastite rute kroz IEndpointModule
        // implementaciju u PropertyValuation/Endpoints — bez izmjene ovog fajla.
        // Vidi docs/backend/feature-module-pattern.md.
        app.MapFeatureEndpoints(typeof(Program).Assembly);
        return app;
    }

    private static async Task SeedTestDataAsync(ApplicationDbContext db)
    {
        if (db.CodebookValues.Any()) return;

        db.CodebookValues.Add(CodebookValue.Create(
            codebookKey:     CodebookKeys.CollateralTypes,
            code:            "STAN",
            label:           "Stan (test)",
            description:     null,
            sortOrder:       1,
            createdByUserId: "test-seed"));
        await db.SaveChangesAsync();
    }
}
