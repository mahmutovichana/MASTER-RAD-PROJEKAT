using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence;

public sealed class ApplicationDbContextFactory : IDesignTimeDbContextFactory<ApplicationDbContext>
{
    public ApplicationDbContext CreateDbContext(string[] args)
    {
        var connectionString = ConnectionHelper.BuildConnection(key =>
            Environment.GetEnvironmentVariable(key.Replace(":", "__")));
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseSqlServer(connectionString)
            .Options;
        return new ApplicationDbContext(options);
    }
}
