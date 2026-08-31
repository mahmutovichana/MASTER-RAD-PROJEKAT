using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace RBBH.TestAutomation.Api.Services.Scenarios;

/// <summary>
/// DI registracija servisa scenarija. Drži logiku registracije izvan <c>Program.cs</c>
/// (tamo se poziva jednom linijom), pa dijeljeni fajl ostaje minimalan.
/// </summary>
public static class ScenarioServiceRegistration
{
    /// <summary>
    /// Registruje <see cref="IScenarioService"/>. Koristi <see cref="MockScenarioService"/>
    /// samo ako je <c>MockScenarios:Enabled=true</c> ili <c>MockAuth:Enabled=true</c>;
    /// inače koristi pravi <see cref="ScenarioService"/> (EF Core / SQL Server).
    /// </summary>
    public static IServiceCollection AddScenarioServices(this IServiceCollection services, IConfiguration cfg)
    {
        var useMock = cfg.GetValue<bool?>("MockScenarios:Enabled") ?? false;
        if (useMock)
            services.AddSingleton<IScenarioService, MockScenarioService>();
        else
            services.AddScoped<IScenarioService, ScenarioService>();
        return services;
    }
}
