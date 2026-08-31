using System.Diagnostics.CodeAnalysis;
using CK = RBBH.CollateralAppraisal.Application.Common.Constants.CodebookKeys;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Hosting;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.IdentityModel.Tokens;
using RBBH.CollateralAppraisal.Application.Appraisers;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Branches;
using RBBH.CollateralAppraisal.Application.Codebooks.Interfaces;
using RBBH.CollateralAppraisal.Application.Codebooks.Import;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Application.Reports;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Common;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using AppClock = RBBH.CollateralAppraisal.Application.Common.Interfaces.IClock;
using InfraClock = RBBH.CollateralAppraisal.Infrastructure.Common.SystemClock;
using InfraRateLimiter = RBBH.CollateralAppraisal.Infrastructure.Common.InMemoryDistributedRateLimiter;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Roles.Interfaces;
using RBBH.CollateralAppraisal.Application.Security.Interfaces;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Infrastructure.Appraisers;
using RBBH.CollateralAppraisal.Infrastructure.Codebooks.Import;
using RBBH.CollateralAppraisal.Infrastructure.Codebooks.Import.Mappers;
using RBBH.CollateralAppraisal.Infrastructure.Audit;
using RBBH.CollateralAppraisal.Infrastructure.Branches;
using RBBH.CollateralAppraisal.Infrastructure.Auth;
using RBBH.CollateralAppraisal.Infrastructure.Codebooks;
using RBBH.CollateralAppraisal.Infrastructure.Notifications;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using RBBH.CollateralAppraisal.Infrastructure.Roles;
using RBBH.CollateralAppraisal.Infrastructure.Security;
using RBBH.CollateralAppraisal.Infrastructure.Storage;
using RBBH.CollateralAppraisal.Infrastructure.Users;

namespace RBBH.CollateralAppraisal.Infrastructure;

[ExcludeFromCodeCoverage]
public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // ── Baza podataka ─────────────────────────────────────────────────────
        // U Testing okruženju (WebApplicationFactory) preskačemo SQL Server provider —
        // factory registruje vlastiti in-memory DbContext bez konflikta providera.
        var env = services
            .FirstOrDefault(d => d.ServiceType == typeof(IWebHostEnvironment))
            ?.ImplementationInstance as IWebHostEnvironment;
        var configuredKeycloak = configuration.GetValue<bool>("Keycloak:Enabled") &&
            !string.IsNullOrWhiteSpace(configuration["Keycloak:Authority"]) &&
            !string.IsNullOrWhiteSpace(configuration["Keycloak:Audience"]);

        if (env?.IsEnvironment("Testing") != true)
        {
            var connectionString = ConnectionHelper.IsConfigured(configuration)
                ? ConnectionHelper.BuildConnection(configuration)
                : null;
            if (env?.IsDevelopment() != true && string.IsNullOrWhiteSpace(connectionString))
                throw new InvalidOperationException(
                    "SQL Server nije konfigurisan. Postavite Database__ServerName i Database__Name.");

            services.AddDbContext<ApplicationDbContext>(options =>
            {
                if (env?.IsDevelopment() == true && string.IsNullOrWhiteSpace(connectionString))
                {
                    options.UseInMemoryDatabase("collateral-appraisal-local");
                    return;
                }

                options.UseSqlServer(
                        connectionString,
                        sqlOptions => sqlOptions
                            .EnableRetryOnFailure(3, TimeSpan.FromSeconds(5), null)
                            .MigrationsAssembly(
                            typeof(ApplicationDbContext).Assembly.FullName));
            });
        }

        services.AddHttpContextAccessor();
        services.AddMemoryCache();
        services.AddSingleton<IClock, RBBH.CollateralAppraisal.Infrastructure.Common.SystemClock>();
        services.AddSingleton<IDistributedRateLimiter, InfraRateLimiter>();

        // ── Autentifikacija / Claims ───────────────────────────────────────────
        services.AddScoped<ICurrentUserService, CurrentUserService>();
        services.AddScoped<IClaimsTransformation, PermissionClaimsTransformation>();
        services.AddScoped<IUserPermissionService, UserPermissionService>();

        // ── Skladište fajlova (dokumentacija narudžbi, US 92) ──────────────────
        services.Configure<FileStorageOptions>(configuration.GetSection(FileStorageOptions.SectionName));
        services.AddSingleton<IFileStorageProvider, LocalFileStorageProvider>();

        // ── Notifikacije ──────────────────────────────────────────────────────
        services.AddScoped<IRoleManagementNotificationService, NullRoleManagementNotificationService>();

        // ── Role management (Keycloak assign/remove/transfer) ─────────────────
        services.AddScoped<IRoleManagementService, RoleManagementService>();

        // ── Role Definitions (SQL Server + Keycloak sync) ─────────────────────
        services.AddScoped<IRoleDefinitionService, RoleDefinitionService>();
        services.AddScoped<IPermissionCatalogService, PermissionCatalogService>();
        if (configuredKeycloak)
            services.AddScoped<IKeycloakRoleSyncService, KeycloakRoleSyncService>();
        else
            services.AddSingleton<IKeycloakRoleSyncService, NullKeycloakRoleSyncService>();

        // ── User Suspension ───────────────────────────────────────────────────
        services.AddScoped<IUserSuspensionService, UserSuspensionService>();

        // ── Narudžbe procjene (US-1, US-2) — fizički split (I-1) ────────────────
        // Sub-servisi dostupni direktno za buduću granularnu injekciju
        services.AddScoped<IOrderCreateService,  OrderCreateService>();
        services.AddScoped<IOrderSubmitService,  OrderSubmitService>();
        // Facade implementira IAppraisalOrderService i delegira na sub-servise
        services.AddScoped<IAppraisalOrderService, AppraisalOrderService>();
        services.AddScoped<IProtocolService, ProtocolService>();
        services.AddScoped<IWorkflowTaskService, WorkflowTaskService>();
        services.AddScoped<ICaDocumentReviewService, CaDocumentReviewService>();
        services.AddScoped<IAccessCheckService, AccessCheckService>();
        services.AddScoped<IOrderTitleGenerator, OrderTitleGenerator>();
        services.AddScoped<IOrderNumberGenerator, OrderNumberGenerator>();
        // IOrderApprovalService je registrovan kroz OrderApprovalFeatureModule (AddFeatureModules).

        // ── Vještaci — master-data, odabir i workflow (Faza C/D) — fizički split (I-2) ─
        services.AddScoped<IAppraiserService, AppraiserService>();
        services.AddScoped<IAppraiserSelectionService, AppraiserSelectionService>();
        services.AddScoped<IFlAppraiserSelectionService, FlAppraiserSelectionService>();
        services.AddScoped<IPlAppraiserSelectionService, PlAppraiserSelectionService>();
        services.AddScoped<IAppraiserOrderLifecycleService, AppraiserAssignmentService>();
        services.AddScoped<IAppraiserAssignmentService, AppraiserAssignmentService>();
        services.AddScoped<IQuoteRequestService, QuoteRequestService>();
        services.AddScoped<IInvoiceWorkflowService, InvoiceWorkflowService>();
        services.AddScoped<IReportService, Reports.ReportService>();
        if (env?.IsDevelopment() == true && !ConnectionHelper.IsConfigured(configuration))
            services.AddSingleton<IDistributedJobLock, InMemoryJobLock>();
        else
            services.AddScoped<IDistributedJobLock, SqlServerJobLock>();
        services.AddHostedService<AppraiserTimeoutService>();
        // Provjera 24h roka prihvatanja — blokira vještaka i dodjeljuje sljedećeg.
        services.AddHostedService<AppraiserAcceptanceTimeoutService>();

        // ── Import/Export šifarnika ──────────────────────────────────────────
        services.AddScoped<ICodebookImportExportService, CodebookImportExportService>();
        services.AddScoped<ICodebookMapper, AppraiserMapper>();
        services.AddScoped<ICodebookMapper>(_ => new CodebookValueMapper(CK.CollateralTypes, CK.CollateralTypes));
        services.AddScoped<ICodebookMapper>(_ => new CodebookValueMapper(CK.PropertyTypes, CK.PropertyTypes));
        services.AddScoped<ICodebookMapper>(_ => new CodebookValueMapper(CK.Cities, CK.Cities));
        services.AddScoped<ICodebookMapper>(_ => new CodebookValueMapper(CK.Branches, CK.Branches));
        services.AddScoped<ICodebookMapper>(_ => new CodebookValueMapper(CK.CombinedCollateralTypes, CK.CombinedCollateralTypes));
        services.AddScoped<ICodebookMapper>(_ => new CodebookValueMapper(CK.DocumentationSupplementReasons, CK.DocumentationSupplementReasons));
        services.AddScoped<ICodebookMapper, ProtocolOrderMapper>();

        // ── Izvještaji ─────────────────────────────────────────────────────────
        services.AddScoped<IReportService, Reports.ReportService>();

        // ── Poslovnice i gradovi ──────────────────────────────────────────────
        services.AddScoped<IBranchQueryService, BranchQueryService>();

        // ── Šifarnici ─────────────────────────────────────────────────────────
        services.AddScoped<ICodebookService, CodebookService>();
        services.AddScoped<ICodebookValueService, CodebookValueService>();
        services.AddScoped<ICodebookUsageService, CodebookUsageService>();
        services.AddScoped<ICodebookUsageChecker, Codebooks.UsageCheckers.CollateralTypeUsageChecker>();
        services.AddScoped<ICodebookUsageChecker, Codebooks.UsageCheckers.DocumentTypeUsageChecker>();
        services.AddScoped<ICodebookCacheInvalidator, NullCodebookCacheInvalidator>();

        // ── Audit ─────────────────────────────────────────────────────────────
        services.AddScoped<IAuditValueSanitizer, AuditValueSanitizer>();
        services.AddScoped<DatabaseAuditSink>();
        services.AddScoped<FileAuditSink>();
        services.AddScoped<IAuditSink, FallbackAuditSink>();
        services.AddSingleton<AuditLogQueue>();
        services.AddSingleton<IAuditLogQueue>(sp => sp.GetRequiredService<AuditLogQueue>());
        services.AddHostedService<AuditLogQueueWorker>();
        services.AddScoped<IAuditService, AuditService>();
        services.AddScoped<IAuditQueryService, AuditQueryService>();

        // ── Korisnici i role (Keycloak read) ──────────────────────────────────
        if (configuredKeycloak)
            services.AddScoped<IUserRoleProvider, KeycloakUserRoleProvider>();
        else
            services.AddSingleton<IUserRoleProvider, LocalUserRoleProvider>();
        services.AddScoped<IUserRoleQueryService, UserRoleQueryService>();

        // ── Keycloak Admin HTTP client ────────────────────────────────────────
        services.Configure<KeycloakOptions>(configuration.GetSection(KeycloakOptions.SectionName));
        services.Configure<KeycloakAdminOptions>(configuration.GetSection(KeycloakAdminOptions.SectionName));
        var authority = configuration[$"{KeycloakOptions.SectionName}:Authority"] ?? string.Empty;
        var realmMarker = authority.LastIndexOf("/realms/", StringComparison.OrdinalIgnoreCase);
        var derivedBaseUrl = realmMarker > 0 ? authority[..realmMarker] : string.Empty;
        var derivedRealm = realmMarker > 0 ? authority[(realmMarker + 8)..].TrimEnd('/') : string.Empty;
        services.PostConfigure<KeycloakAdminOptions>(options =>
        {
            if (string.IsNullOrWhiteSpace(options.BaseUrl)) options.BaseUrl = derivedBaseUrl;
            if (string.IsNullOrWhiteSpace(options.Realm)) options.Realm = derivedRealm;
        });
        services.AddHttpClient("KeycloakAdmin", client =>
        {
            var baseUrl = configuration[$"{KeycloakAdminOptions.SectionName}:BaseUrl"];
            if (string.IsNullOrWhiteSpace(baseUrl)) baseUrl = derivedBaseUrl;
            if (!string.IsNullOrEmpty(baseUrl))
                client.BaseAddress = new Uri(baseUrl);
            client.DefaultRequestHeaders.Add("Accept", "application/json");
        });

        // ── JWT Bearer autentifikacija ────────────────────────────────────────
        var keycloak = configuration.GetSection(KeycloakOptions.SectionName).Get<KeycloakOptions>()
            ?? new KeycloakOptions();

        var keycloakEnabled = configuredKeycloak;

        if (keycloakEnabled)
        {
            services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
                .AddJwtBearer(options =>
            {
                options.Authority             = keycloak.Authority;
                options.Audience              = keycloak.Audience;
                options.RequireHttpsMetadata  = keycloak.RequireHttpsMetadata;
                options.AutomaticRefreshInterval = TimeSpan.FromMinutes(10);
                options.RefreshInterval       = TimeSpan.FromSeconds(10);

                var validIssuers = new[] { keycloak.Authority }
                    .Concat(keycloak.ValidIssuers)
                    .Where(i => !string.IsNullOrWhiteSpace(i))
                    .Distinct()
                    .ToArray();
                if (validIssuers.Length > 0)
                {
                    options.TokenValidationParameters.ValidIssuers = validIssuers;
                }

                options.Events = new JwtBearerEvents
                {
                    OnAuthenticationFailed = context =>
                    {
                        if (context.Exception is SecurityTokenExpiredException)
                            context.Response.Headers["Token-Expired"] = "true";
                        return Task.CompletedTask;
                    }
                };
            });
        }
        else
        {
            services.AddAuthentication(LocalDevelopmentAuthenticationHandler.SchemeName)
                .AddScheme<LocalDevelopmentAuthenticationOptions, LocalDevelopmentAuthenticationHandler>(
                    LocalDevelopmentAuthenticationHandler.SchemeName,
                    options => options.Enabled = env?.IsDevelopment() == true);
        }

        services.AddSingleton(new AuthenticationStartupStatus(
            keycloakEnabled,
            keycloakEnabled
                ? "Keycloak autentifikacija je uključena."
                : env?.IsDevelopment() == true
                    ? "Keycloak nije konfigurisan; koristi se lokalni razvojni administrator."
                    : "Keycloak nije konfigurisan; zaštićeni endpointi vraćaju 401."));

        return services;
    }
}
