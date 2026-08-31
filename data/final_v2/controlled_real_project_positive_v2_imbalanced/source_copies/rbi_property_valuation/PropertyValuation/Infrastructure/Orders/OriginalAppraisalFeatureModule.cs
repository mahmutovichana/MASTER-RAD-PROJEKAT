using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using RBBH.CollateralAppraisal.Application.Common.Modules;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

/// <summary>
/// DI registracija za "Preuzet original + reminder vještaku" (DPNPN-108).
/// Auto-discovery preko IFeatureModule registruje ovaj modul u Infrastructure layer-u.
/// </summary>
[System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage]
public sealed class OriginalAppraisalFeatureModule : IFeatureModule
{
    public void RegisterServices(IServiceCollection services, IConfiguration configuration)
    {
        services.AddScoped<IOriginalAppraisalService, OriginalAppraisalService>();
    }
}
