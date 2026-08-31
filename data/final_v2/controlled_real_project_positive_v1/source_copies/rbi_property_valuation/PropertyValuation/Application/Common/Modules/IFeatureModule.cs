using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace RBBH.CollateralAppraisal.Application.Common.Modules;

/// <summary>
/// Feature modul koji registruje vlastite servise u DI kontejner.
///
/// Svaki feature (T2-T8) implementira ovaj interfejs u svom sloju (obično
/// Infrastructure) za servise koje taj feature uvodi. <see cref="FeatureModuleExtensions.AddFeatureModules"/>
/// pronalazi sve implementacije reflection-om i poziva <see cref="RegisterServices"/> —
/// nije potrebno mijenjati centralni <c>DependencyInjection.cs</c>.
///
/// Implementacija mora imati public bezparametarski konstruktor.
/// Vidi docs/backend/feature-module-pattern.md.
/// </summary>
public interface IFeatureModule
{
    void RegisterServices(IServiceCollection services, IConfiguration configuration);
}
