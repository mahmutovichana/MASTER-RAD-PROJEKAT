using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Roles.Requests;
using RBBH.CollateralAppraisal.Domain.Audit;
using RBBH.CollateralAppraisal.Infrastructure.Audit;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Infrastructure.Tests.Audit;

public class AuditQueryServiceTests
{
    [Fact]
    public async Task QueryAsync_FiltersByActorRole_MatchesActiveRoleOrActorRole()
    {
        await using var db = CreateDbContext();

        // ActiveRole != ActorRole (korisnik sa više rola, akcija izvršena pod "SM")
        db.AuditLogs.Add(AuditLog.Create(MakeData(
            actorRole: "AM", activeRole: "SM", action: "DOCUMENT_DOWNLOADED")));

        // Korisnik sa jednom rolom — ActorRole == ActiveRole
        db.AuditLogs.Add(AuditLog.Create(MakeData(
            actorRole: "KolateralAdministrator", activeRole: "KolateralAdministrator", action: "ORDER_SUBMITTED")));

        await db.SaveChangesAsync();

        var service = new AuditQueryService(db);

        var bySm = await service.QueryAsync(new AuditQueryRequest(ActorRole: "SM"));
        Assert.Single(bySm.Items);
        Assert.Equal("DOCUMENT_DOWNLOADED", bySm.Items[0].Action);

        var byCa = await service.QueryAsync(new AuditQueryRequest(ActorRole: "KolateralAdministrator"));
        Assert.Single(byCa.Items);
        Assert.Equal("ORDER_SUBMITTED", byCa.Items[0].Action);

        var byUnknown = await service.QueryAsync(new AuditQueryRequest(ActorRole: "Vjestak"));
        Assert.Empty(byUnknown.Items);
    }

    [Fact]
    public async Task QueryAsync_ProjectsActorFullNameAndActiveRole()
    {
        await using var db = CreateDbContext();
        db.AuditLogs.Add(AuditLog.Create(MakeData(
            actorRole: "AM", activeRole: "AM", action: "DOCUMENT_DOWNLOADED", fullName: "Haris Hadžić")));
        await db.SaveChangesAsync();

        var service = new AuditQueryService(db);

        var result = await service.QueryAsync(new AuditQueryRequest());

        var item = Assert.Single(result.Items);
        Assert.Equal("Haris Hadžić", item.ActorFullName);
        Assert.Equal("AM", item.ActiveRole);
    }

    [Fact]
    public async Task QueryAsync_FiltersByModuleAndAction_ForDocumentDownloadEvents()
    {
        await using var db = CreateDbContext();
        db.AuditLogs.Add(AuditLog.Create(MakeData(action: "DOCUMENT_DOWNLOADED", module: "Documents")));
        db.AuditLogs.Add(AuditLog.Create(MakeData(action: "ORDER_SUBMITTED", module: "AppraisalOrders")));
        await db.SaveChangesAsync();

        var service = new AuditQueryService(db);

        var result = await service.QueryAsync(new AuditQueryRequest(Module: "Documents", Action: "DOCUMENT_DOWNLOADED"));

        Assert.Single(result.Items);
        Assert.Equal("DOCUMENT_DOWNLOADED", result.Items[0].Action);
    }

    private static ApplicationDbContext CreateDbContext()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;

        return new ApplicationDbContext(options);
    }

    private static AuditLogData MakeData(
        string actorRole = "AM",
        string? activeRole = null,
        string action = "DOCUMENT_DOWNLOADED",
        string module = "Documents",
        string? fullName = "Test Korisnik") => new(
        TimestampUtc:            DateTime.UtcNow,
        ActorUserId:             "user-1",
        ActorUsername:           "test.user",
        ActorEmail:              null,
        ActorFullName:           fullName,
        ActorRole:               actorRole,
        ActiveRole:              activeRole ?? actorRole,
        Action:                  action,
        OperationType:           "Read",
        Module:                  module,
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
