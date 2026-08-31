using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using RBBH.CollateralAppraisal.Application.Common.Modules;
using RBBH.CollateralAppraisal.Application.Opinions;

namespace RBBH.CollateralAppraisal.Infrastructure.Opinions;

[System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage]
public sealed class OpinionFeatureModule : IFeatureModule
{
    public void RegisterServices(IServiceCollection services, IConfiguration configuration)
    {
        services.AddScoped<IOpinionService, OpinionService>();
    }
}