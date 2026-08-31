using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using RBBH.CollateralAppraisal.Application.Common.Modules;
using RBBH.CollateralAppraisal.Application.Reports;

namespace RBBH.CollateralAppraisal.Infrastructure.Reports;

/// <summary>
/// Registruje servise izvještaja (auto-discovery preko IFeatureModule — ne dira DependencyInjection.cs).
/// </summary>
[System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage]
public sealed class ReportsFeatureModule : IFeatureModule
{
    public void RegisterServices(IServiceCollection services, IConfiguration configuration)
    {
        services.AddScoped<IExcelReportBuilder, ClosedXmlReportBuilder>();
        services.AddScoped<IReportService, ReportService>();
    }
}
