using System.Reflection;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace RBBH.CollateralAppraisal.Application.Common.Modules;

/// <summary>
/// Auto-discovery za <see cref="IFeatureModule"/> implementacije.
/// </summary>
public static class FeatureModuleExtensions
{
    /// <summary>
    /// Pronalazi sve konkretne klase koje implementiraju <see cref="IFeatureModule"/>
    /// u datim sklopovima, instancira ih (bezparametarski konstruktor) i poziva
    /// <see cref="IFeatureModule.RegisterServices"/>.
    /// </summary>
    public static IServiceCollection AddFeatureModules(
        this IServiceCollection services,
        IConfiguration configuration,
        params IEnumerable<Assembly> assemblies)
    {
        var moduleTypes = assemblies
            .SelectMany(a => a.GetTypes())
            .Where(t => t is { IsClass: true, IsAbstract: false }
                     && typeof(IFeatureModule).IsAssignableFrom(t)
                     && t.GetConstructor(Type.EmptyTypes) is not null);

        foreach (var moduleType in moduleTypes)
        {
            var module = (IFeatureModule)Activator.CreateInstance(moduleType)!;
            module.RegisterServices(services, configuration);
        }

        return services;
    }
}
