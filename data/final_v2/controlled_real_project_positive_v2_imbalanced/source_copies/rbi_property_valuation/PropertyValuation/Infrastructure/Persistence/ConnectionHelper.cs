using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Configuration;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence;

public static class ConnectionHelper
{
    public static bool IsConfigured(IConfiguration configuration)
    {
        ArgumentNullException.ThrowIfNull(configuration);
        return !string.IsNullOrWhiteSpace(configuration["Database:ServerName"])
            || !string.IsNullOrWhiteSpace(configuration["Database:Name"]);
    }

    public static string BuildConnection(IConfiguration configuration)
    {
        ArgumentNullException.ThrowIfNull(configuration);

        return BuildConnection(key => configuration[key]);
    }

    public static string BuildConnection(Func<string, string?> readSetting)
    {
        ArgumentNullException.ThrowIfNull(readSetting);
        var integratedSecurity = bool.TryParse(readSetting("Database:IntegratedSecurity"), out var parsed)
            && parsed;
        var builder = new SqlConnectionStringBuilder
        {
            DataSource = Required(readSetting, "Database:ServerName"),
            InitialCatalog = Required(readSetting, "Database:Name"),
            IntegratedSecurity = integratedSecurity,
            Encrypt = true,
            TrustServerCertificate = string.Equals(
                readSetting("ASPNETCORE_ENVIRONMENT"),
                "Development",
                StringComparison.OrdinalIgnoreCase),
            MultipleActiveResultSets = true,
            ConnectTimeout = 15,
            ConnectRetryCount = 3,
            ConnectRetryInterval = 5,
            Pooling = true,
            MinPoolSize = 5,
            MaxPoolSize = 100
        };

        if (!integratedSecurity)
        {
            builder.UserID = Required(readSetting, "Database:User");
            builder.Password = Required(readSetting, "Database:Password");
        }

        return builder.ConnectionString;
    }

    private static string Required(Func<string, string?> readSetting, string key) =>
        string.IsNullOrWhiteSpace(readSetting(key))
            ? throw new InvalidOperationException($"Required database setting '{key}' is missing or empty.")
            : readSetting(key)!;
}
