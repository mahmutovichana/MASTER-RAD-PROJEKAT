using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using RBBH.CollateralAppraisal.Infrastructure.Seed;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Seed;

public sealed class CodebookSeederTests : IDisposable
{
    private readonly ApplicationDbContext _db;

    public CodebookSeederTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db = new ApplicationDbContext(options);
    }

    public void Dispose() => _db.Dispose();

    [Fact]
    public async Task SeedAsync_EmptyDatabase_SeedsCodebooksAndValues()
    {
        await CodebookSeeder.SeedAsync(_db);

        Assert.True(await _db.Codebooks.AnyAsync(c => c.Code == "tipovi_nekretnina"));
        Assert.True(await _db.CodebookValues.AnyAsync(v => v.CodebookKey == "tipovi_nekretnina" && v.Code == "STAN"));
        Assert.True(await _db.Codebooks.CountAsync() > 1);
        Assert.True(await _db.CodebookValues.CountAsync() > 1);
    }

    [Fact]
    public async Task SeedAsync_CalledTwice_DoesNotCreateDuplicates()
    {
        await CodebookSeeder.SeedAsync(_db);
        var codebookCountAfterFirst = await _db.Codebooks.CountAsync();
        var valueCountAfterFirst    = await _db.CodebookValues.CountAsync();

        await CodebookSeeder.SeedAsync(_db);

        Assert.Equal(codebookCountAfterFirst, await _db.Codebooks.CountAsync());
        Assert.Equal(valueCountAfterFirst, await _db.CodebookValues.CountAsync());
    }

    [Fact]
    public async Task SeedAsync_ExistingValueNotInSeed_IsLeftUntouched()
    {
        _db.CodebookValues.Add(CodebookValue.Create("tipovi_nekretnina", "CUSTOM_VALUE", "Custom", null, 99, "user-1"));
        await _db.SaveChangesAsync();

        await CodebookSeeder.SeedAsync(_db);

        var custom = await _db.CodebookValues
            .SingleAsync(v => v.CodebookKey == "tipovi_nekretnina" && v.Code == "CUSTOM_VALUE");
        Assert.True(custom.IsActive);
    }

    [Fact]
    public async Task SeedAsync_ExistingActiveSpValue_IsDeactivated()
    {
        _db.CodebookValues.Add(CodebookValue.Create(
            "tipovi_klijenata", "SP", "Samostalni poduzetnik", null, 30, "seed"));
        await _db.SaveChangesAsync();

        await CodebookSeeder.SeedAsync(_db);

        var sp = await _db.CodebookValues
            .IgnoreQueryFilters()
            .SingleAsync(v => v.CodebookKey == "tipovi_klijenata" && v.Code == "SP");
        Assert.False(sp.IsActive);
    }

    [Fact]
    public async Task SeedAsync_NoSpValue_DoesNotCreateOne()
    {
        await CodebookSeeder.SeedAsync(_db);

        Assert.False(await _db.CodebookValues.AnyAsync(v => v.CodebookKey == "tipovi_klijenata" && v.Code == "SP"));
    }

    [Fact]
    public async Task SeedAsync_WithLogger_LogsSeedingProgress()
    {
        var logger = Substitute.For<ILogger>();

        await CodebookSeeder.SeedAsync(_db, logger);

        Assert.NotEmpty(logger.ReceivedCalls());
    }
}
