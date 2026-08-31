using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Configuration;
using RBBH.TestAutomation.Core.Infrastructure;

namespace RBBH.TestAutomation.UnitTests.Infrastructure;

public sealed class ConnectionHelperTests
{
    [Fact]
    public void BuildConnection_UsesConfiguredDatabaseNameAndSqlCredentials()
    {
        const string databaseName = "TestGenerator_Uat";
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
    public void BuildConnection_WithIntegratedSecurity_DoesNotRequireCredentials()
    {
        var configuration = new ConfigurationBuilder()
            .AddInMemoryCollection(new Dictionary<string, string?>
            {
                ["Database:ServerName"] = @"localhost\SQLEXPRESS",
                ["Database:Name"] = "TestGenerator_Local",
                ["Database:IntegratedSecurity"] = "true",
                ["ASPNETCORE_ENVIRONMENT"] = "Development"
            })
            .Build();

        var result = new SqlConnectionStringBuilder(ConnectionHelper.BuildConnection(configuration));

        Assert.True(result.IntegratedSecurity);
        Assert.True(result.TrustServerCertificate);
    }
}
