using System.Reflection;

namespace RBBH.CollateralAppraisal.Api.Modules;

/// <summary>
/// Auto-discovery za <see cref="IEndpointModule"/> implementacije.
/// </summary>
public static class EndpointModuleExtensions
{
    /// <summary>
    /// Pronalazi sve konkretne klase koje implementiraju <see cref="IEndpointModule"/>
    /// u datim sklopovima, instancira ih (bezparametarski konstruktor) i poziva
    /// <see cref="IEndpointModule.MapEndpoints"/>.
    /// </summary>
    public static IEndpointRouteBuilder MapFeatureEndpoints(
        this IEndpointRouteBuilder app,
        params IEnumerable<Assembly> assemblies)
    {
        var moduleTypes = assemblies
            .SelectMany(a => a.GetTypes())
            .Where(t => t is { IsClass: true, IsAbstract: false }
                     && typeof(IEndpointModule).IsAssignableFrom(t)
                     && t.GetConstructor(Type.EmptyTypes) is not null);

        foreach (var moduleType in moduleTypes)
        {
            var module = (IEndpointModule)Activator.CreateInstance(moduleType)!;
            module.MapEndpoints(app);
        }

        return app;
    }
}
