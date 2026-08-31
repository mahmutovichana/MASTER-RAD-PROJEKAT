using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using RBBH.CollateralAppraisal.Application.Common.Modules;
using RBBH.CollateralAppraisal.Application.Notifications;

namespace RBBH.CollateralAppraisal.Infrastructure.Notifications;

/// <summary>
/// Registruje servise notifikacionog modula (US 92/93/94).
/// Proof-of-concept za <see cref="IFeatureModule"/> auto-discovery —
/// vidi docs/backend/feature-module-pattern.md.
/// </summary>
[System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage]
public sealed class NotificationsFeatureModule : IFeatureModule
{
    public void RegisterServices(IServiceCollection services, IConfiguration configuration)
    {
        services.AddScoped<IEmailProvider, LogEmailProvider>();
        services.AddScoped<INotificationService, NotificationService>();
    }
}
