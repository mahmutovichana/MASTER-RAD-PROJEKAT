using Microsoft.EntityFrameworkCore;
using RBBH.TestAutomation.Core.Infrastructure;

namespace UnitTests.TestForge;

public static class TestForgeFixture
{
    public static TestForgeDbContext CreateInMemory()
    {
        var opts = new DbContextOptionsBuilder<TestForgeDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;
        return new TestForgeDbContext(opts);
    }
}
