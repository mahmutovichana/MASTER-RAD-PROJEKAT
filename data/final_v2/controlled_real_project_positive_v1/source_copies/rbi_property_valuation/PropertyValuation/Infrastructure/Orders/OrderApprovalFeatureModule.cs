using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using RBBH.CollateralAppraisal.Application.Common.Modules;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

[System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage]
public sealed class OrderApprovalFeatureModule : IFeatureModule
{
    public void RegisterServices(IServiceCollection services, IConfiguration configuration)
    {
        services.AddScoped<IOrderApprovalService, OrderApprovalService>();
        services.AddScoped<IOrderQueryService, OrderQueryService>();
    }
}
