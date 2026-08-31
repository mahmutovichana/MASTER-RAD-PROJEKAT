using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using RBBH.CollateralAppraisal.Application.Common.Modules;
using RBBH.CollateralAppraisal.Application.Reports;

namespace RBBH.CollateralAppraisal.Infrastructure.Reports;

[System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage]
public sealed class AppraiserDeliveryReminderFeatureModule : IFeatureModule
{
    public void RegisterServices(IServiceCollection services, IConfiguration configuration)
    {
        services.AddScoped<IAppraiserDeliveryReminderService, AppraiserDeliveryReminderService>();
    }
}
