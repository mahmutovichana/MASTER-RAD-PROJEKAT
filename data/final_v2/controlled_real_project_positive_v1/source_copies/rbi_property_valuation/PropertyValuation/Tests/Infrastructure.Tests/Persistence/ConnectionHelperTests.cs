using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Configuration;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Infrastructure.Tests.Persistence;

public sealed class ConnectionHelperTests
{
    [Fact]
    public void BuildConnection_UsesDatabaseNameFromConfiguration()
    {
        const string databaseName = "PropertyValuation_Uat";
        var configuration = new ConfigurationBuilder()
            .AddInMemoryCollection(new Dictionary<string, string?>
            {
                ["Database:ServerName"] = "sql.example.local,1433",
                ["Database:Name"] = databaseName,
                ["Database:User"] = "app_user",
                ["Database:Password"] = "secret",
                ["ASPNETCORE_ENVIRONMENT"] = "Production"
            })
            .Build();

        var result = new SqlConnectionStringBuilder(ConnectionHelper.BuildConnection(configuration));

        Assert.Equal(databaseName, result.InitialCatalog);
        Assert.Equal("sql.example.local,1433", result.DataSource);
        Assert.Equal("app_user", result.UserID);
        Assert.True(result.Encrypt);
        Assert.False(result.TrustServerCertificate);
    }

    [Fact]
    public void BuildConnection_WhenConfigurationIsPartial_FailsWithExactMissingSetting()
    {
        var configuration = new ConfigurationBuilder()
            .AddInMemoryCollection(new Dictionary<string, string?>
            {
                ["Database:ServerName"] = "sql.example.local"
            })
            .Build();

        var error = Assert.Throws<InvalidOperationException>(
            () => ConnectionHelper.BuildConnection(configuration));

        Assert.Contains("Database:Name", error.Message, StringComparison.Ordinal);
    }
}
