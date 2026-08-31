using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using RBBH.CollateralAppraisal.Application.Common.Modules;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Common.Modules;

public interface ITestMarkerService;

public sealed class TestMarkerService : ITestMarkerService;

public sealed class ConcreteFeatureModule : IFeatureModule
{
    public void RegisterServices(IServiceCollection services, IConfiguration configuration)
        => services.AddSingleton<ITestMarkerService, TestMarkerService>();
}

public abstract class AbstractFeatureModule : IFeatureModule
{
    public void RegisterServices(IServiceCollection services, IConfiguration configuration) { }
}

public sealed class NoParameterlessCtorFeatureModule : IFeatureModule
{
    public NoParameterlessCtorFeatureModule(string required) { }

    public void RegisterServices(IServiceCollection services, IConfiguration configuration) { }
}

public sealed class FeatureModuleExtensionsTests
{
    [Fact]
    public void AddFeatureModules_RegistersServicesFromConcreteModuleWithParameterlessCtor()
    {
        var services       = new ServiceCollection();
        var configuration  = new ConfigurationBuilder().Build();

        services.AddFeatureModules(configuration, typeof(FeatureModuleExtensionsTests).Assembly);

        Assert.Contains(services, d => d.ServiceType == typeof(ITestMarkerService));
    }

    [Fact]
    public void AddFeatureModules_ReturnsSameServiceCollection()
    {
        var services      = new ServiceCollection();
        var configuration = new ConfigurationBuilder().Build();

        var result = services.AddFeatureModules(configuration, typeof(FeatureModuleExtensionsTests).Assembly);

        Assert.Same(services, result);
    }

    [Fact]
    public void AddFeatureModules_NoAssemblies_DoesNotThrowAndReturnsSameCollection()
    {
        var services      = new ServiceCollection();
        var configuration = new ConfigurationBuilder().Build();

        var result = services.AddFeatureModules(configuration);

        Assert.Same(services, result);
    }
}
