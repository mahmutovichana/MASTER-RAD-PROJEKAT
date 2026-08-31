using RBBH.CollateralAppraisal.Domain.Audit;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Domain;

public sealed class AuditLogTests
{
    private static AuditLogData MakeData() => new(
        TimestampUtc:            new DateTime(2026, 6, 14, 10, 0, 0, DateTimeKind.Utc),
        ActorUserId:             "user-1",
        ActorUsername:           "ivan",
        ActorEmail:              null,
        ActorFullName:           "Ivan Ivić",
        ActorRole:               "AM",
        ActiveRole:              "AM",
        Action:                  "ORDER_CREATED",
        OperationType:           "Create",
        Module:                  "Orders",
        SourceSystem:            null,
        SourceConnectionName:    null,
        SourceDatabase:          null,
        SourceSchema:            null,
        SourceTable:             null,
        EntityType:              "AppraisalOrder",
        EntityKey:               "123",
        EntityDisplayName:       "Narudžba #123",
        OldValuesJson:           null,
        NewValuesJson:           null,
        ChangedFieldsJson:       null,
        Status:                  "Success",
        Severity:                "Info",
        Reason:                  null,
        IntegrationDirection:    null,
        ExternalRequestId:       null,
        ExternalResponseStatus:  null,
        CorrelationId:           "corr-1",
        RequestPath:             "/api/orders",
        HttpMethod:              "POST",
        IpAddress:               "127.0.0.1",
        UserAgent:               "test-agent");

    [Fact]
    public void Create_MapsCoreAuditData()
    {
        var log = AuditLog.Create(MakeData());

        Assert.Equal(new DateTime(2026, 6, 14, 10, 0, 0, DateTimeKind.Utc), log.TimestampUtc);
        Assert.Equal("user-1",         log.ActorUserId);
        Assert.Equal("ivan",           log.ActorUsername);
        Assert.Equal("Ivan Ivić",      log.ActorFullName);
        Assert.Equal("AM",             log.ActorRole);
        Assert.Equal("AM",             log.ActiveRole);
        Assert.Equal("ORDER_CREATED",  log.Action);
        Assert.Equal("Create",         log.OperationType);
        Assert.Equal("Orders",         log.Module);
        Assert.Equal("AppraisalOrder", log.EntityType);
        Assert.Equal("123",            log.EntityKey);
        Assert.Equal("Narudžba #123",  log.EntityDisplayName);
        Assert.Equal("Success",        log.Status);
        Assert.Equal("Info",           log.Severity);
        Assert.Equal("corr-1",         log.CorrelationId);
        Assert.Equal("/api/orders",    log.RequestPath);
        Assert.Equal("POST",           log.HttpMethod);
        Assert.Equal("127.0.0.1",      log.IpAddress);
        Assert.Equal("test-agent",     log.UserAgent);
    }

    [Fact]
    public void Create_MapsSourceSystemFields()
    {
        var data = MakeData() with
        {
            SourceSystem         = "ExternalOrdersDb",
            SourceConnectionName = "ext-conn",
            SourceDatabase       = "orders_db",
            SourceSchema         = "public",
            SourceTable          = "orders",
        };

        var log = AuditLog.Create(data);

        Assert.Equal("ExternalOrdersDb", log.SourceSystem);
        Assert.Equal("ext-conn",         log.SourceConnectionName);
        Assert.Equal("orders_db",        log.SourceDatabase);
        Assert.Equal("public",           log.SourceSchema);
        Assert.Equal("orders",           log.SourceTable);
    }

    [Fact]
    public void Create_MapsIntegrationAndChangeTrackingFields()
    {
        var data = MakeData() with
        {
            ActorEmail             = "ivan@test.ba",
            OldValuesJson          = "{\"status\":\"Draft\"}",
            NewValuesJson          = "{\"status\":\"SubmittedBySales\"}",
            ChangedFieldsJson      = "[\"Status\"]",
            Reason                 = "Workflow transition",
            IntegrationDirection   = "Outbound",
            ExternalRequestId      = "ext-req-1",
            ExternalResponseStatus = "200",
        };

        var log = AuditLog.Create(data);

        Assert.Equal("ivan@test.ba",                   log.ActorEmail);
        Assert.Equal("{\"status\":\"Draft\"}",          log.OldValuesJson);
        Assert.Equal("{\"status\":\"SubmittedBySales\"}", log.NewValuesJson);
        Assert.Equal("[\"Status\"]",                    log.ChangedFieldsJson);
        Assert.Equal("Workflow transition",             log.Reason);
        Assert.Equal("Outbound",                        log.IntegrationDirection);
        Assert.Equal("ext-req-1",                       log.ExternalRequestId);
        Assert.Equal("200",                             log.ExternalResponseStatus);
    }
}
