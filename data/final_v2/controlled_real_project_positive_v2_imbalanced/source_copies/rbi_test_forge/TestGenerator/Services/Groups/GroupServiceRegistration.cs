using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace RBBH.TestAutomation.Api.Services.Groups;

/// <summary>
/// DI registracija servisa grupa. Drži logiku registracije izvan <c>Program.cs</c>
/// (tamo se poziva jednom linijom), pa dijeljeni fajl ostaje minimalan i bez seam konflikta.
/// </summary>
public static class GroupServiceRegistration
{
    /// <summary>
    /// Registruje <see cref="IGroupService"/>. U mock modu
    /// (<c>MockGroups:Enabled</c>, fallback na <c>MockAuth:Enabled</c>) koristi
    /// <see cref="MockGroupService"/> kao <c>Singleton</c> — stanje opstaje kroz sesiju
    /// procesa (isto kao <c>MockSifarnikService</c>). Inače se registruje realna EF Core
    /// implementacija <c>GroupService</c> (<c>Scoped</c>) — UI ostaje isti u oba moda.
    /// </summary>
    public static IServiceCollection AddGroupServices(this IServiceCollection services, IConfiguration cfg)
    {
        var useMock = cfg.GetValue<bool?>("MockGroups:Enabled") ?? false;
        if (useMock)
            services.AddSingleton<IGroupService, MockGroupService>();
        else
            services.AddScoped<IGroupService, GroupService>();
        return services;
    }
}
