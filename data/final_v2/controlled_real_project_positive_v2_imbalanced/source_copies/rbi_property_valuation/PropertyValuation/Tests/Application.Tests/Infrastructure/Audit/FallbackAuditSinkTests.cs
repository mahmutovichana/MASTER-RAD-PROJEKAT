using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Domain.Audit;
using RBBH.CollateralAppraisal.Infrastructure.Audit;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Audit;

public sealed class FallbackAuditSinkTests : IDisposable
{
    private readonly ApplicationDbContext _db;
    private readonly string               _logFilePath;

    public FallbackAuditSinkTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db = new ApplicationDbContext(options);

        var logDir = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData),
            "audit-logs");
        _logFilePath = Path.Combine(logDir, $"audit-{DateTime.UtcNow:yyyy-MM-dd}.jsonl");
    }

    public void Dispose() => _db.Dispose();

    [Fact]
    public async Task WriteAsync_PrimarySucceeds_PersistsToDatabaseAndDoesNotWriteFile()
    {
        var primary  = new DatabaseAuditSink(_db);
        var fallback = new FileAuditSink(Substitute.For<ILogger<FileAuditSink>>());
        var sut = new FallbackAuditSink(primary, fallback, Substitute.For<ILogger<FallbackAuditSink>>());

        var marker = $"FALLBACK_PRIMARY_OK_{Guid.NewGuid()}";
        var log = AuditLog.Create(TestAuditLogData.Make(action: marker));
        await sut.WriteAsync(log);

        Assert.Equal(1, _db.AuditLogs.Count());
        if (File.Exists(_logFilePath))
            Assert.DoesNotContain(File.ReadAllLines(_logFilePath), l => l.Contains(marker));
    }

    [Fact]
    public async Task WriteAsync_PrimaryFails_FallsBackToFileSink()
    {
        // DbContext bez konfigurisanog providera - SaveChangesAsync uvijek baca InvalidOperationException
        using var unconfiguredDb = new ApplicationDbContext(new DbContextOptionsBuilder<ApplicationDbContext>().Options);
        var primary  = new DatabaseAuditSink(unconfiguredDb);
        var fallback = new FileAuditSink(Substitute.For<ILogger<FileAuditSink>>());
        var sut = new FallbackAuditSink(primary, fallback, Substitute.For<ILogger<FallbackAuditSink>>());

        var marker = $"FALLBACK_MARKER_{Guid.NewGuid()}";
        var log = AuditLog.Create(TestAuditLogData.Make(timestampUtc: DateTime.UtcNow, action: marker));
        await sut.WriteAsync(log);

        var lines = File.ReadAllLines(_logFilePath);
        Assert.Contains(lines, l => l.Contains(marker));
    }
}
