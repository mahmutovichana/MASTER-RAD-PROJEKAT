using RBBH.TestAutomation.Api.Jobs;
using Hangfire;
using Hangfire.Console;
using Hangfire.InMemory;
using Hangfire.SqlServer;

namespace RBBH.TestAutomation.Api.Services.Schedules;

public static class ScheduleServiceRegistration
{
    public static void AddScheduleServices(this IServiceCollection services, IConfiguration cfg)
    {
        var useMock = string.IsNullOrWhiteSpace(cfg.GetConnectionString("Default"));

        if (useMock)
        {
            // Mock mod: InMemory Hangfire storage da /hangfire ruta postoji za pregled.
            // ScheduleService nije registrovan — UI koristi MockScheduleService.
            services.AddHangfire(config => config
                .SetDataCompatibilityLevel(CompatibilityLevel.Version_180)
                .UseSimpleAssemblyNameTypeSerializer()
                .UseRecommendedSerializerSettings()
                .UseInMemoryStorage());

            services.AddSingleton<IScheduleService, MockScheduleService>();
            return;
        }

        var connStr = cfg.GetConnectionString("Default")
            ?? throw new InvalidOperationException("ConnectionStrings:Default nije konfigurisan.");

        services.AddHangfire(config => config
            .SetDataCompatibilityLevel(CompatibilityLevel.Version_180)
            .UseSimpleAssemblyNameTypeSerializer()
            .UseRecommendedSerializerSettings()
            .UseSqlServerStorage(connStr, new SqlServerStorageOptions
            {
                QueuePollInterval = TimeSpan.FromSeconds(15),
                SlidingInvisibilityTimeout = TimeSpan.FromMinutes(5),
                UseRecommendedIsolationLevel = true,
                DisableGlobalLocks = true,
            })
            // Live log output u Dashboard-u (Hangfire Console).
            .UseConsole()
            // Retention: 7 dana uspjesni, 30 dana neuspjeli.
            .UseFilter(new RetentionPolicyAttribute()));

        services.AddHangfireServer(opts =>
        {
            opts.Queues      = ["critical", "default", "low"];
            opts.WorkerCount = 5;
        });

        services.AddScoped<GroupTestJob>();
        services.AddScoped<IScheduleService, ScheduleService>();
    }
}
