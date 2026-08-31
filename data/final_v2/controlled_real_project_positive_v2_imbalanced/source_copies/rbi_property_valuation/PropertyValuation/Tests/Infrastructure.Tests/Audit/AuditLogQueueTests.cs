using Microsoft.Extensions.Logging.Abstractions;
using RBBH.CollateralAppraisal.Domain.Audit;
using RBBH.CollateralAppraisal.Infrastructure.Audit;
using Xunit;

namespace RBBH.CollateralAppraisal.Infrastructure.Tests.Audit;

public class AuditLogQueueTests
{
    [Fact]
    public async Task EnqueueAsync_ReturnsImmediately_LogBecomesAvailableToReader()
    {
        var queue = new AuditLogQueue(NullLogger<AuditLogQueue>.Instance);
        var log = AuditLog.Create(MakeData());

        await queue.EnqueueAsync(log);

        var read = await queue.Reader.ReadAsync();
        Assert.Same(log, read);
    }

    [Fact]
    public async Task EnqueueAsync_MultipleEvents_PreservesOrder()
    {
        var queue = new AuditLogQueue(NullLogger<AuditLogQueue>.Instance);
        var first = AuditLog.Create(MakeData(action: "DOCUMENT_DOWNLOADED"));
        var second = AuditLog.Create(MakeData(action: "DOCUMENT_UPLOADED"));

        await queue.EnqueueAsync(first);
        await queue.EnqueueAsync(second);

        Assert.Same(first, await queue.Reader.ReadAsync());
        Assert.Same(second, await queue.Reader.ReadAsync());
    }

    private static AuditLogData MakeData(string action = "DOCUMENT_DOWNLOADED") => new(
        TimestampUtc:            DateTime.UtcNow,
        ActorUserId:             "user-1",
        ActorUsername:           "test.user",
        ActorEmail:              null,
        ActorFullName:           "Test Korisnik",
        ActorRole:               "AM",
        ActiveRole:              "AM",
        Action:                  action,
        OperationType:           "Read",
        Module:                  "Documents",
        SourceSystem:            null,
        SourceConnectionName:    null,
        SourceDatabase:          null,
        SourceSchema:            null,
        SourceTable:             null,
        EntityType:              "Document",
        EntityKey:               "1",
        EntityDisplayName:       "test.pdf",
        OldValuesJson:           null,
        NewValuesJson:           null,
        ChangedFieldsJson:       null,
        Status:                  "Success",
        Severity:                "Info",
        Reason:                  null,
        IntegrationDirection:    null,
        ExternalRequestId:       null,
        ExternalResponseStatus:  null,
        CorrelationId:           null,
        RequestPath:             null,
        HttpMethod:              null,
        IpAddress:               null,
        UserAgent:               null);
}
