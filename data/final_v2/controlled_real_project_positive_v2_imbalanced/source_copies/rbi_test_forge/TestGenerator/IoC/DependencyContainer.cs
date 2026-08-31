using RBBH.TestAutomation.Api.Auth;
using RBBH.TestAutomation.Api.Services;
using RBBH.TestAutomation.Api.Services.ApiKeys;
using RBBH.TestAutomation.Api.Services.Auth;
using RBBH.TestAutomation.Api.Services.Notifications;
using RBBH.TestAutomation.Api.Services.Run;
using Microsoft.EntityFrameworkCore;
using RBBH.TestAutomation.Core.Generation;
using RBBH.TestAutomation.Core.Infrastructure;
using RBBH.TestAutomation.Core.Repositories;

namespace RBBH.TestAutomation.Api.IoC
{
    public class DependencyContainer
    {
        /// <summary>
        /// Registracija autentikacijskih i pratećih servisa za Keycloak OIDC tok.
        /// React klijent koristi sigurni server-side cookie; tokeni se ne čuvaju u browser storage-u.
        /// </summary>
        public static void RegisterService(IServiceCollection services, bool useInMemoryDatabase)
        {
            // Typed pristup podacima prijavljenog korisnika — čita iz OIDC cookie principal-a.
            services.AddScoped<IUserContext, KeycloakUserContext>();

            // Keycloak Admin REST klijent — čita/dodjeljuje role (service account realm-admin).
            services.AddHttpClient("KeycloakAdmin");
            services.AddScoped<IKeycloakAdminService, KeycloakAdminService>();

            // ── Nezavisni servisi ────────────────────────────────────────────
            // Idle timeout — Scoped, per-circuit timer.
            services.AddScoped<IdleTimeoutService>();

            // Audit log — Singleton store (globalni pregled) + Scoped logger.
            // Upisuje se iz OIDC events u Program.cs (login/logout).
            // DbAuditLogStore perzistira u SQL Server (security_audit_log) — preživi
            // restart; mock/dev tok (Program.cs else-grana) koristi InMemoryAuditLogStore.
            if (useInMemoryDatabase)
                services.AddSingleton<IAuditLogStore, InMemoryAuditLogStore>();
            else
                services.AddSingleton<IAuditLogStore, DbAuditLogStore>();
            services.AddScoped<SecurityEventLogger>();

            // Live runner — izvršava REST scenarije uživo (HTTP) i vraća prolaz/pad.
            // Zaseban HTTP klijent (ne dijeli token handler s backend pozivima).
            services.AddHttpClient("ScenarioRunner");
            services.AddScoped<IScenarioRunner, ScenarioRunner>();
            services.AddScoped<IGroupTestExecutor, GroupTestExecutor>();

            // Dijeljeno run-stanje (header Pokreni ↔ sidebar indikator ↔ Scenariji tab).
            services.AddScoped<TestRunStateService>();

            // Pravi xUnit runner (opcija A) — kompajlira generisani projekt i pokreće `dotnet test`.
            services.AddScoped<IXUnitTestRunner, XUnitTestRunner>();

            // Notifikacijski servisi (email, Slack, Teams).
            services.AddSingleton<EmailSender>();
            services.AddSingleton<SlackSender>();
            services.AddSingleton<TeamsSender>();
            services.AddScoped<INotificationService, NotificationService>();
        }

        public static void RegisterTestForge(IServiceCollection services, IConfiguration configuration)
        {
            var connectionString = configuration.GetConnectionString("Default");
            var useInMemory = string.IsNullOrWhiteSpace(connectionString);

            services.AddDbContext<TestForgeDbContext>(opts =>
            {
                if (useInMemory)
                    opts.UseInMemoryDatabase("test-automation-local");
                else
                    opts.UseSqlServer(connectionString, sql =>
                        sql.EnableRetryOnFailure(3, TimeSpan.FromSeconds(5), null));
            });

            if (useInMemory)
                services.AddSingleton<ITestForgeAuditWriter, InMemoryTestForgeAuditWriter>();
            else
                services.AddScoped<ITestForgeAuditWriter, DapperTestForgeAuditWriter>();

            services.AddScoped<IGroupRepository, GroupRepository>();
            services.AddScoped<IScenarioRepository, ScenarioRepository>();
            services.AddScoped<IRunRepository, RunRepository>();
            services.AddScoped<IRunHistoryService, RunHistoryService>();
            services.AddScoped<IApiKeyService, ApiKeyService>();
        }
    }
}
