using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;

namespace RBBH.TestAutomation.Core.Infrastructure;

/// <summary>
/// Design-time factory — potrebna za `dotnet ef migrations` kada je DbContext u library-ju,
/// ne u web projektu.
/// </summary>
public class TestForgeDbContextFactory : IDesignTimeDbContextFactory<TestForgeDbContext>
{
    public TestForgeDbContext CreateDbContext(string[] args)
    {
        var opts = new DbContextOptionsBuilder<TestForgeDbContext>()
            .UseSqlServer(ConnectionHelper.BuildConnection(key =>
                Environment.GetEnvironmentVariable(key.Replace(":", "__"))))
            .Options;
        return new TestForgeDbContext(opts);
    }
}
