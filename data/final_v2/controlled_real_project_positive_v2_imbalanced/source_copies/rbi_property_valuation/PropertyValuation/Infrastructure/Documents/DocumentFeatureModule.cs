using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using RBBH.CollateralAppraisal.Application.Common.Modules;
using RBBH.CollateralAppraisal.Application.Documents;

namespace RBBH.CollateralAppraisal.Infrastructure.Documents;

[System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage]
public sealed class DocumentFeatureModule : IFeatureModule
{
    public void RegisterServices(IServiceCollection services, IConfiguration configuration)
    {
        services.AddScoped<IDocumentService, DocumentService>();
        services.AddScoped<ISharedDocumentService, SharedDocumentService>();
        services.AddScoped<IOrderDocumentGenerator, OrderDocumentGeneratorService>();
    }
}