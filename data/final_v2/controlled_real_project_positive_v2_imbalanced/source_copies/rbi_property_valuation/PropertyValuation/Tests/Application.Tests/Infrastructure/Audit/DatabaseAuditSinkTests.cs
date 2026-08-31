using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Domain.Audit;
using RBBH.CollateralAppraisal.Infrastructure.Audit;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Audit;

public sealed class DatabaseAuditSinkTests : IDisposable
{
    private readonly ApplicationDbContext _db;
    private readonly DatabaseAuditSink    _sut;

    public DatabaseAuditSinkTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db  = new ApplicationDbContext(options);
        _sut = new DatabaseAuditSink(_db);
    }

    public void Dispose() => _db.Dispose();

    [Fact]
    public async Task WriteAsync_PersistsAuditLogToDatabase()
    {
        var log = AuditLog.Create(TestAuditLogData.Make(action: "DB_SINK_TEST", entityKey: "42"));

        await _sut.WriteAsync(log);

        var saved = await _db.AuditLogs.SingleAsync();
        Assert.Equal("DB_SINK_TEST", saved.Action);
        Assert.Equal("42", saved.EntityKey);
    }
}
