using RBBH.CollateralAppraisal.Application.Roles.Models;
using RBBH.CollateralAppraisal.Application.Roles.Requests;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Dtos;

public sealed class RolesDtosTests
{
    [Fact]
    public void RoleDefinitionDto_StoresPermissionsList()
    {
        var permission = new PermissionDefinitionDto(
            Id: 1, Code: "orders.create", DisplayName: "Kreiraj narudžbu", Description: null, Module: "Orders", IsActive: true);

        var dto = new RoleDefinitionDto(
            Id: 1,
            Name: "AM",
            DisplayName: "Account Manager",
            Description: null,
            IsSystem: true,
            IsActive: true,
            IsDeleted: false,
            CreatedAt: new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc),
            CreatedByUserId: null,
            UpdatedAt: new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc),
            UpdatedByUserId: null,
            Permissions: [permission]);

        Assert.Equal("AM", dto.Name);
        Assert.Single(dto.Permissions);
        Assert.Equal("orders.create", dto.Permissions[0].Code);
    }

    [Fact]
    public void RoleDefinitionListItemDto_StoresCounts()
    {
        var dto = new RoleDefinitionListItemDto(
            Id: 1, Name: "AM", DisplayName: "Account Manager", Description: null,
            IsSystem: true, IsActive: true, PermissionCount: 6, UserCount: 4);

        Assert.Equal(6, dto.PermissionCount);
        Assert.Equal(4, dto.UserCount);
    }

    [Fact]
    public void PermissionDefinitionDto_StoresAllProperties()
    {
        var dto = new PermissionDefinitionDto(
            Id: 1, Code: "orders.approve-final", DisplayName: "Odobri finalnu procjenu", Description: "opis", Module: "Orders", IsActive: true);

        Assert.Equal("orders.approve-final", dto.Code);
        Assert.Equal("Orders", dto.Module);
        Assert.True(dto.IsActive);
    }

    [Fact]
    public void AuditLogDto_StoresAllProperties()
    {
        var dto = new AuditLogDto(
            Id: 1,
            TimestampUtc: new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc),
            ActorUserId: "user-1",
            ActorUsername: "ivan",
            ActorEmail: null,
            ActorFullName: "Ivan Ivić",
            ActorRole: "AM",
            ActiveRole: "AM",
            Action: "ORDER_CREATED",
            OperationType: "Create",
            Module: "Orders",
            EntityType: "AppraisalOrder",
            EntityKey: "1",
            EntityDisplayName: "Narudžba #1",
            OldValuesJson: null,
            NewValuesJson: null,
            ChangedFieldsJson: null,
            Status: "Success",
            Severity: "Info",
            Reason: null,
            CorrelationId: "corr-1",
            RequestPath: "/api/orders",
            IpAddress: "127.0.0.1",
            UserAgent: "test-agent");

        Assert.Equal("ORDER_CREATED", dto.Action);
        Assert.Equal("Orders",        dto.Module);
        Assert.Equal("Success",       dto.Status);
    }

    [Fact]
    public void CreateRoleRequest_StoresAllProperties()
    {
        var request = new CreateRoleRequest(Name: "CUSTOM", DisplayName: "Custom rola", Description: null);

        Assert.Equal("CUSTOM",      request.Name);
        Assert.Equal("Custom rola", request.DisplayName);
    }

    [Fact]
    public void UpdateRoleRequest_StoresAllProperties()
    {
        var request = new UpdateRoleRequest(DisplayName: "Novi naziv", Description: "Novi opis");

        Assert.Equal("Novi naziv", request.DisplayName);
        Assert.Equal("Novi opis",  request.Description);
    }

    [Fact]
    public void AddPermissionToRoleRequest_StoresPermissionId()
    {
        var request = new AddPermissionToRoleRequest(PermissionDefinitionId: 7);

        Assert.Equal(7, request.PermissionDefinitionId);
    }

    [Fact]
    public void RoleQueryRequest_DefaultsApplyExpectedPaging()
    {
        var request = new RoleQueryRequest();

        Assert.Equal(1,  request.Page);
        Assert.Equal(20, request.PageSize);
        Assert.Null(request.Search);
        Assert.Null(request.IsActive);
    }

    [Fact]
    public void AuditQueryRequest_DefaultsApplyExpectedPaging()
    {
        var request = new AuditQueryRequest();

        Assert.Equal(1,  request.Page);
        Assert.Equal(50, request.PageSize);
        Assert.Null(request.From);
        Assert.Null(request.To);
    }

    // ── RoleDefinitionDto extended coverage ────────────────────────────────────

    [Fact]
    public void RoleDefinitionDto_AllFieldsPopulated_StoresCorrectValues()
    {
        var created = new DateTime(2026, 1, 1, 0, 0, 0, DateTimeKind.Utc);
        var updated = new DateTime(2026, 6, 15, 12, 0, 0, DateTimeKind.Utc);

        var permissions = new List<PermissionDefinitionDto>
        {
            new(Id: 1, Code: "orders.create", DisplayName: "Kreiraj narudžbu", Description: null, Module: "Orders", IsActive: true),
            new(Id: 2, Code: "orders.submit", DisplayName: "Pošalji narudžbu", Description: "Opis", Module: "Orders", IsActive: true),
            new(Id: 3, Code: "users.view", DisplayName: "Pregledaj korisnike", Description: null, Module: "Users", IsActive: false)
        };

        var dto = new RoleDefinitionDto(
            Id: 5,
            Name: "CUSTOM_ROLE",
            DisplayName: "Prilagodjena rola",
            Description: "Opis prilagodjene role",
            IsSystem: false,
            IsActive: true,
            IsDeleted: false,
            CreatedAt: created,
            CreatedByUserId: "admin-1",
            UpdatedAt: updated,
            UpdatedByUserId: "admin-2",
            Permissions: permissions);

        Assert.Equal(5, dto.Id);
        Assert.Equal("CUSTOM_ROLE", dto.Name);
        Assert.Equal("Prilagodjena rola", dto.DisplayName);
        Assert.Equal("Opis prilagodjene role", dto.Description);
        Assert.False(dto.IsSystem);
        Assert.True(dto.IsActive);
        Assert.False(dto.IsDeleted);
        Assert.Equal(created, dto.CreatedAt);
        Assert.Equal("admin-1", dto.CreatedByUserId);
        Assert.Equal(updated, dto.UpdatedAt);
        Assert.Equal("admin-2", dto.UpdatedByUserId);
        Assert.Equal(3, dto.Permissions.Count);
    }

    [Fact]
    public void RoleDefinitionDto_DeletedRole_StoresDeletedFlag()
    {
        var dto = new RoleDefinitionDto(
            Id: 10, Name: "DELETED", DisplayName: "Obrisana",
            Description: null, IsSystem: false, IsActive: false, IsDeleted: true,
            CreatedAt: DateTime.UtcNow, CreatedByUserId: null,
            UpdatedAt: DateTime.UtcNow, UpdatedByUserId: null,
            Permissions: []);

        Assert.True(dto.IsDeleted);
        Assert.False(dto.IsActive);
        Assert.Empty(dto.Permissions);
    }

    [Fact]
    public void RoleDefinitionDto_NullOptionalFields_StoresNull()
    {
        var dto = new RoleDefinitionDto(
            Id: 1, Name: "AM", DisplayName: "AM",
            Description: null, IsSystem: true, IsActive: true, IsDeleted: false,
            CreatedAt: DateTime.UtcNow, CreatedByUserId: null,
            UpdatedAt: DateTime.UtcNow, UpdatedByUserId: null,
            Permissions: []);

        Assert.Null(dto.Description);
        Assert.Null(dto.CreatedByUserId);
        Assert.Null(dto.UpdatedByUserId);
    }

    // ── RoleDefinitionListItemDto extended coverage ───────────────────────────

    [Fact]
    public void RoleDefinitionListItemDto_AllFieldsPopulated_StoresCorrectValues()
    {
        var dto = new RoleDefinitionListItemDto(
            Id: 3, Name: "CO", DisplayName: "Control Officer",
            Description: "Kontrolni oficir", IsSystem: true, IsActive: true,
            PermissionCount: 12, UserCount: 8);

        Assert.Equal(3, dto.Id);
        Assert.Equal("CO", dto.Name);
        Assert.Equal("Control Officer", dto.DisplayName);
        Assert.Equal("Kontrolni oficir", dto.Description);
        Assert.True(dto.IsSystem);
        Assert.True(dto.IsActive);
        Assert.Equal(12, dto.PermissionCount);
        Assert.Equal(8, dto.UserCount);
    }

    [Fact]
    public void RoleDefinitionListItemDto_InactiveRole_StoresCorrectly()
    {
        var dto = new RoleDefinitionListItemDto(
            Id: 99, Name: "OLD", DisplayName: "Stara rola",
            Description: null, IsSystem: false, IsActive: false,
            PermissionCount: 0, UserCount: 0);

        Assert.False(dto.IsActive);
        Assert.False(dto.IsSystem);
        Assert.Null(dto.Description);
        Assert.Equal(0, dto.PermissionCount);
        Assert.Equal(0, dto.UserCount);
    }

    // ── PermissionDefinitionDto extended coverage ─────────────────────────────

    [Fact]
    public void PermissionDefinitionDto_InactivePermission_StoresFalse()
    {
        var dto = new PermissionDefinitionDto(
            Id: 10, Code: "old.permission", DisplayName: "Stari",
            Description: "Deaktiviran", Module: "Legacy", IsActive: false);

        Assert.Equal(10, dto.Id);
        Assert.Equal("old.permission", dto.Code);
        Assert.Equal("Stari", dto.DisplayName);
        Assert.Equal("Deaktiviran", dto.Description);
        Assert.Equal("Legacy", dto.Module);
        Assert.False(dto.IsActive);
    }

    [Fact]
    public void PermissionDefinitionDto_NullDescription_StoresNull()
    {
        var dto = new PermissionDefinitionDto(
            Id: 1, Code: "test", DisplayName: "Test", Description: null, Module: "Test", IsActive: true);

        Assert.Null(dto.Description);
    }

    // ── AuditLogDto extended coverage ─────────────────────────────────────────

    [Fact]
    public void AuditLogDto_AllFieldsPopulated_StoresCorrectValues()
    {
        var timestamp = new DateTime(2026, 6, 15, 10, 30, 0, DateTimeKind.Utc);

        var dto = new AuditLogDto(
            Id: 1000,
            TimestampUtc: timestamp,
            ActorUserId: "user-42",
            ActorUsername: "marko",
            ActorEmail: "marko@firma.ba",
            ActorFullName: "Marko Markovic",
            ActorRole: "CA",
            ActiveRole: "CA",
            Action: "ORDER_APPROVED",
            OperationType: "Update",
            Module: "Orders",
            EntityType: "AppraisalOrder",
            EntityKey: "42",
            EntityDisplayName: "Narudzba #42",
            OldValuesJson: "{\"Status\":\"InProgress\"}",
            NewValuesJson: "{\"Status\":\"Approved\"}",
            ChangedFieldsJson: "[\"Status\"]",
            Status: "Success",
            Severity: "Info",
            Reason: "CO odobrenje",
            CorrelationId: "corr-42",
            RequestPath: "/api/orders/42/approve",
            IpAddress: "192.168.1.100",
            UserAgent: "Mozilla/5.0");

        Assert.Equal(1000, dto.Id);
        Assert.Equal(timestamp, dto.TimestampUtc);
        Assert.Equal("user-42", dto.ActorUserId);
        Assert.Equal("marko", dto.ActorUsername);
        Assert.Equal("marko@firma.ba", dto.ActorEmail);
        Assert.Equal("Marko Markovic", dto.ActorFullName);
        Assert.Equal("CA", dto.ActorRole);
        Assert.Equal("CA", dto.ActiveRole);
        Assert.Equal("ORDER_APPROVED", dto.Action);
        Assert.Equal("Update", dto.OperationType);
        Assert.Equal("Orders", dto.Module);
        Assert.Equal("AppraisalOrder", dto.EntityType);
        Assert.Equal("42", dto.EntityKey);
        Assert.Equal("Narudzba #42", dto.EntityDisplayName);
        Assert.Equal("{\"Status\":\"InProgress\"}", dto.OldValuesJson);
        Assert.Equal("{\"Status\":\"Approved\"}", dto.NewValuesJson);
        Assert.Equal("[\"Status\"]", dto.ChangedFieldsJson);
        Assert.Equal("Success", dto.Status);
        Assert.Equal("Info", dto.Severity);
        Assert.Equal("CO odobrenje", dto.Reason);
        Assert.Equal("corr-42", dto.CorrelationId);
        Assert.Equal("/api/orders/42/approve", dto.RequestPath);
        Assert.Equal("192.168.1.100", dto.IpAddress);
        Assert.Equal("Mozilla/5.0", dto.UserAgent);
    }

    [Fact]
    public void AuditLogDto_NullOptionalFields_StoresNull()
    {
        var dto = new AuditLogDto(
            Id: 1, TimestampUtc: DateTime.UtcNow,
            ActorUserId: null, ActorUsername: null, ActorEmail: null,
            ActorFullName: null, ActorRole: null, ActiveRole: null,
            Action: "SYSTEM_EVENT", OperationType: "System", Module: "System",
            EntityType: null, EntityKey: null, EntityDisplayName: null,
            OldValuesJson: null, NewValuesJson: null, ChangedFieldsJson: null,
            Status: "Success", Severity: "Warning",
            Reason: null, CorrelationId: null,
            RequestPath: null, IpAddress: null, UserAgent: null);

        Assert.Null(dto.ActorUserId);
        Assert.Null(dto.ActorUsername);
        Assert.Null(dto.ActorEmail);
        Assert.Null(dto.ActorFullName);
        Assert.Null(dto.ActorRole);
        Assert.Null(dto.ActiveRole);
        Assert.Null(dto.EntityType);
        Assert.Null(dto.EntityKey);
        Assert.Null(dto.EntityDisplayName);
        Assert.Null(dto.OldValuesJson);
        Assert.Null(dto.NewValuesJson);
        Assert.Null(dto.ChangedFieldsJson);
        Assert.Null(dto.Reason);
        Assert.Null(dto.CorrelationId);
        Assert.Null(dto.RequestPath);
        Assert.Null(dto.IpAddress);
        Assert.Null(dto.UserAgent);
    }
}
