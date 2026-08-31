using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Domain.Audit;
using RBBH.CollateralAppraisal.Infrastructure.Audit;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Audit;

public sealed class FileAuditSinkTests
{
    private static string LogFilePath(DateTime timestamp) => Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData),
        "audit-logs",
        $"audit-{timestamp:yyyy-MM-dd}.jsonl");

    [Fact]
    public async Task WriteAsync_ValidLog_AppendsJsonLineToFile()
    {
        var sut = new FileAuditSink(Substitute.For<ILogger<FileAuditSink>>());
        var timestamp = DateTime.UtcNow;
        var marker = $"FILE_SINK_MARKER_{Guid.NewGuid()}";
        var log = AuditLog.Create(TestAuditLogData.Make(timestampUtc: timestamp, action: marker));

        await sut.WriteAsync(log);

        var lines = File.ReadAllLines(LogFilePath(timestamp));
        Assert.Contains(lines, l => l.Contains(marker));
    }

    [Fact]
    public async Task WriteAsync_CancelledToken_DoesNotThrow()
    {
        var sut = new FileAuditSink(Substitute.For<ILogger<FileAuditSink>>());
        var log = AuditLog.Create(TestAuditLogData.Make(action: "FILE_SINK_CANCELLED"));
        using var cts = new CancellationTokenSource();
        cts.Cancel();

        await sut.WriteAsync(log, cts.Token);
    }
}
