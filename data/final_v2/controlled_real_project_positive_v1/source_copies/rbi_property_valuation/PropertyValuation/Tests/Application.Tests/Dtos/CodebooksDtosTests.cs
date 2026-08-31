using RBBH.CollateralAppraisal.Application.Codebooks.Models;
using RBBH.CollateralAppraisal.Application.Codebooks.Requests;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Dtos;

public sealed class CodebooksDtosTests
{
    [Fact]
    public void CodebookDto_StoresAllProperties()
    {
        var dto = new CodebookDto(
            Id: 1,
            Code: "relation_basis",
            Name: "Osnov odnosa",
            Description: "opis",
            Category: "Klijenti",
            IsActive: true,
            IsSystem: true,
            ValueCount: 3,
            CreatedAt: new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc),
            CreatedByUserId: null,
            UpdatedAt: null,
            UpdatedByUserId: null);

        Assert.Equal("relation_basis", dto.Code);
        Assert.Equal(3, dto.ValueCount);
        Assert.True(dto.IsSystem);
    }

    [Fact]
    public void CodebookListItemDto_StoresAllProperties()
    {
        var dto = new CodebookListItemDto(
            Id: 1,
            Code: "relation_basis",
            Name: "Osnov odnosa",
            Description: null,
            Category: null,
            IsActive: true,
            IsSystem: true,
            ValueCount: 3,
            ActiveValueCount: 2,
            CreatedAt: new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc),
            UpdatedAt: null,
            UpdatedByUserId: null);

        Assert.Equal(3, dto.ValueCount);
        Assert.Equal(2, dto.ActiveValueCount);
    }

    [Fact]
    public void CodebookOptionDto_StoresAllProperties()
    {
        var dto = new CodebookOptionDto(Id: 1, Code: "VLASNIK", Label: "Vlasnik", SortOrder: 1);

        Assert.Equal("VLASNIK", dto.Code);
        Assert.Equal("Vlasnik", dto.Label);
        Assert.Equal(1, dto.SortOrder);
    }

    [Fact]
    public void CodebookValueDto_StoresAllProperties()
    {
        var dto = new CodebookValueDto(
            Id: 1,
            CodebookKey: "relation_basis",
            Code: "VLASNIK",
            Label: "Vlasnik",
            Description: null,
            SortOrder: 1,
            IsActive: true,
            IsSystem: false,
            IsCritical: false,
            CreatedAt: new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc),
            CreatedByUserId: "user-1",
            UpdatedAt: null,
            UpdatedByUserId: null,
            DeactivatedAt: null,
            DeactivatedByUserId: null,
            DeactivationReason: null);

        Assert.Equal("relation_basis", dto.CodebookKey);
        Assert.Equal("VLASNIK", dto.Code);
        Assert.True(dto.IsActive);
    }

    [Fact]
    public void CodebookUsageLocation_StoresModuleEntityAndCount()
    {
        var location = new CodebookUsageLocation
        {
            Module     = "Limits",
            EntityName = "LimitRequest",
            Count      = 5
        };

        Assert.Equal("Limits",       location.Module);
        Assert.Equal("LimitRequest", location.EntityName);
        Assert.Equal(5,              location.Count);
    }

    [Fact]
    public void CodebookUsageResult_NotInUseAndReliable_CanDeleteAndRecommendsDelete()
    {
        var result = new CodebookUsageResult { IsInUse = false, UsageCount = 0, IsReliable = true };

        Assert.True(result.CanDelete);
        Assert.True(result.CanDeactivate);
        Assert.Equal("Delete", result.RecommendedAction);
    }

    [Fact]
    public void CodebookUsageResult_InUse_CannotDeleteAndRecommendsDeactivate()
    {
        var result = new CodebookUsageResult { IsInUse = true, UsageCount = 3, IsReliable = true };

        Assert.False(result.CanDelete);
        Assert.True(result.CanDeactivate);
        Assert.Equal("Deactivate", result.RecommendedAction);
    }

    [Fact]
    public void CodebookUsageResult_Unreliable_CannotDeleteEvenIfNotInUse()
    {
        var result = new CodebookUsageResult { IsInUse = false, UsageCount = 0, IsReliable = false };

        Assert.False(result.CanDelete);
        Assert.Equal("Delete", result.RecommendedAction);
    }

    [Fact]
    public void CodebookUsageResult_DefaultIsReliableTrue()
    {
        var result = new CodebookUsageResult();

        Assert.True(result.IsReliable);
        Assert.Empty(result.Locations);
    }

    [Fact]
    public void CreateCodebookRequest_StoresAllProperties()
    {
        var request = new CreateCodebookRequest(Code: "relation_basis", Name: "Osnov odnosa", Description: "opis", Category: "Klijenti");

        Assert.Equal("relation_basis", request.Code);
        Assert.Equal("Osnov odnosa",   request.Name);
    }

    [Fact]
    public void UpdateCodebookRequest_StoresAllProperties()
    {
        var request = new UpdateCodebookRequest(Name: "Novi naziv", Description: null, Category: null);

        Assert.Equal("Novi naziv", request.Name);
    }

    [Fact]
    public void DeactivateCodebookRequest_DefaultsReasonToNull()
    {
        var request = new DeactivateCodebookRequest();

        Assert.Null(request.Reason);
    }

    [Fact]
    public void CodebookQueryRequest_DefaultsApplyExpectedPagingAndSort()
    {
        var request = new CodebookQueryRequest();

        Assert.Equal(1,  request.Page);
        Assert.Equal(50, request.PageSize);
        Assert.True(request.SortAsc);
        Assert.Null(request.Search);
    }

    [Fact]
    public void CreateCodebookValueRequest_StoresAllProperties()
    {
        var request = new CreateCodebookValueRequest(Code: "VLASNIK", Label: "Vlasnik", Description: null, SortOrder: 1);

        Assert.Equal("VLASNIK", request.Code);
        Assert.Equal("Vlasnik", request.Label);
        Assert.Equal(1, request.SortOrder);
    }

    [Fact]
    public void DeactivateCodebookValueRequest_DefaultsReasonToNull()
    {
        var request = new DeactivateCodebookValueRequest();

        Assert.Null(request.Reason);
    }

    [Fact]
    public void UpdateCodebookValueRequest_StoresAllProperties()
    {
        var request = new UpdateCodebookValueRequest(Label: "Novi label", Description: "Novi opis", SortOrder: 5);

        Assert.Equal("Novi label", request.Label);
        Assert.Equal("Novi opis",  request.Description);
        Assert.Equal(5,            request.SortOrder);
    }

    // ── CodebookDto extended coverage ──────────────────────────────────────────

    [Fact]
    public void CodebookDto_AllFieldsPopulated_StoresCorrectValues()
    {
        var created = new DateTime(2026, 1, 15, 10, 0, 0, DateTimeKind.Utc);
        var updated = new DateTime(2026, 6, 10, 14, 30, 0, DateTimeKind.Utc);

        var dto = new CodebookDto(
            Id: 42,
            Code: "collateral_type",
            Name: "Tip kolaterala",
            Description: "Definise tipove kolaterala",
            Category: "Procjene",
            IsActive: false,
            IsSystem: false,
            ValueCount: 15,
            CreatedAt: created,
            CreatedByUserId: "admin-1",
            UpdatedAt: updated,
            UpdatedByUserId: "admin-2");

        Assert.Equal(42, dto.Id);
        Assert.Equal("collateral_type", dto.Code);
        Assert.Equal("Tip kolaterala", dto.Name);
        Assert.Equal("Definise tipove kolaterala", dto.Description);
        Assert.Equal("Procjene", dto.Category);
        Assert.False(dto.IsActive);
        Assert.False(dto.IsSystem);
        Assert.Equal(15, dto.ValueCount);
        Assert.Equal(created, dto.CreatedAt);
        Assert.Equal("admin-1", dto.CreatedByUserId);
        Assert.Equal(updated, dto.UpdatedAt);
        Assert.Equal("admin-2", dto.UpdatedByUserId);
    }

    [Fact]
    public void CodebookDto_NullOptionalFields_StoresNull()
    {
        var dto = new CodebookDto(
            Id: 1,
            Code: "test",
            Name: "Test",
            Description: null,
            Category: null,
            IsActive: true,
            IsSystem: true,
            ValueCount: 0,
            CreatedAt: DateTime.UtcNow,
            CreatedByUserId: null,
            UpdatedAt: null,
            UpdatedByUserId: null);

        Assert.Null(dto.Description);
        Assert.Null(dto.Category);
        Assert.Null(dto.CreatedByUserId);
        Assert.Null(dto.UpdatedAt);
        Assert.Null(dto.UpdatedByUserId);
        Assert.Equal(0, dto.ValueCount);
    }

    // ── CodebookListItemDto extended coverage ──────────────────────────────────

    [Fact]
    public void CodebookListItemDto_AllFieldsPopulated_StoresCorrectValues()
    {
        var created = new DateTime(2026, 3, 1, 0, 0, 0, DateTimeKind.Utc);
        var updated = new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc);

        var dto = new CodebookListItemDto(
            Id: 10,
            Code: "region",
            Name: "Regija",
            Description: "Geografske regije",
            Category: "Lokacija",
            IsActive: true,
            IsSystem: false,
            ValueCount: 7,
            ActiveValueCount: 5,
            CreatedAt: created,
            UpdatedAt: updated,
            UpdatedByUserId: "user-5");

        Assert.Equal(10, dto.Id);
        Assert.Equal("region", dto.Code);
        Assert.Equal("Regija", dto.Name);
        Assert.Equal("Geografske regije", dto.Description);
        Assert.Equal("Lokacija", dto.Category);
        Assert.True(dto.IsActive);
        Assert.False(dto.IsSystem);
        Assert.Equal(7, dto.ValueCount);
        Assert.Equal(5, dto.ActiveValueCount);
        Assert.Equal(created, dto.CreatedAt);
        Assert.Equal(updated, dto.UpdatedAt);
        Assert.Equal("user-5", dto.UpdatedByUserId);
    }

    [Fact]
    public void CodebookListItemDto_InactiveCodebook_StoresFalse()
    {
        var dto = new CodebookListItemDto(
            Id: 2, Code: "old_code", Name: "Stari", Description: null,
            Category: null, IsActive: false, IsSystem: false,
            ValueCount: 0, ActiveValueCount: 0,
            CreatedAt: DateTime.UtcNow, UpdatedAt: null, UpdatedByUserId: null);

        Assert.False(dto.IsActive);
        Assert.Equal(0, dto.ActiveValueCount);
    }

    // ── CodebookValueDto extended coverage ─────────────────────────────────────

    [Fact]
    public void CodebookValueDto_AllFieldsPopulated_StoresCorrectValues()
    {
        var created = new DateTime(2026, 1, 1, 0, 0, 0, DateTimeKind.Utc);
        var updated = new DateTime(2026, 3, 1, 0, 0, 0, DateTimeKind.Utc);
        var deactivated = new DateTime(2026, 5, 1, 0, 0, 0, DateTimeKind.Utc);

        var dto = new CodebookValueDto(
            Id: 50,
            CodebookKey: "collateral_type",
            Code: "STAN",
            Label: "Stan",
            Description: "Stambeni prostor",
            SortOrder: 3,
            IsActive: false,
            IsSystem: true,
            IsCritical: true,
            CreatedAt: created,
            CreatedByUserId: "admin-1",
            UpdatedAt: updated,
            UpdatedByUserId: "admin-2",
            DeactivatedAt: deactivated,
            DeactivatedByUserId: "admin-3",
            DeactivationReason: "Zamijenjen novim kodom");

        Assert.Equal(50, dto.Id);
        Assert.Equal("collateral_type", dto.CodebookKey);
        Assert.Equal("STAN", dto.Code);
        Assert.Equal("Stan", dto.Label);
        Assert.Equal("Stambeni prostor", dto.Description);
        Assert.Equal(3, dto.SortOrder);
        Assert.False(dto.IsActive);
        Assert.True(dto.IsSystem);
        Assert.True(dto.IsCritical);
        Assert.Equal(created, dto.CreatedAt);
        Assert.Equal("admin-1", dto.CreatedByUserId);
        Assert.Equal(updated, dto.UpdatedAt);
        Assert.Equal("admin-2", dto.UpdatedByUserId);
        Assert.Equal(deactivated, dto.DeactivatedAt);
        Assert.Equal("admin-3", dto.DeactivatedByUserId);
        Assert.Equal("Zamijenjen novim kodom", dto.DeactivationReason);
    }

    [Fact]
    public void CodebookValueDto_NullOptionalFields_StoresNull()
    {
        var dto = new CodebookValueDto(
            Id: 1, CodebookKey: "test", Code: "T", Label: "Test",
            Description: null, SortOrder: 0,
            IsActive: true, IsSystem: false, IsCritical: false,
            CreatedAt: DateTime.UtcNow, CreatedByUserId: null,
            UpdatedAt: null, UpdatedByUserId: null,
            DeactivatedAt: null, DeactivatedByUserId: null, DeactivationReason: null);

        Assert.Null(dto.Description);
        Assert.Null(dto.CreatedByUserId);
        Assert.Null(dto.UpdatedAt);
        Assert.Null(dto.UpdatedByUserId);
        Assert.Null(dto.DeactivatedAt);
        Assert.Null(dto.DeactivatedByUserId);
        Assert.Null(dto.DeactivationReason);
    }

    [Fact]
    public void CodebookValueDto_CriticalAndSystemFlags_IndependentlyControlled()
    {
        var dto1 = new CodebookValueDto(
            Id: 1, CodebookKey: "k", Code: "C", Label: "L",
            Description: null, SortOrder: 0,
            IsActive: true, IsSystem: true, IsCritical: false,
            CreatedAt: DateTime.UtcNow, CreatedByUserId: null,
            UpdatedAt: null, UpdatedByUserId: null,
            DeactivatedAt: null, DeactivatedByUserId: null, DeactivationReason: null);

        var dto2 = new CodebookValueDto(
            Id: 2, CodebookKey: "k", Code: "C2", Label: "L2",
            Description: null, SortOrder: 1,
            IsActive: true, IsSystem: false, IsCritical: true,
            CreatedAt: DateTime.UtcNow, CreatedByUserId: null,
            UpdatedAt: null, UpdatedByUserId: null,
            DeactivatedAt: null, DeactivatedByUserId: null, DeactivationReason: null);

        Assert.True(dto1.IsSystem);
        Assert.False(dto1.IsCritical);
        Assert.False(dto2.IsSystem);
        Assert.True(dto2.IsCritical);
    }

    // ── CodebookUsageResult extended coverage ─────────────────────────────────

    [Fact]
    public void CodebookUsageResult_WithLocations_StoresLocations()
    {
        var locations = new List<CodebookUsageLocation>
        {
            new() { Module = "Orders", EntityName = "AppraisalOrder", Count = 10 },
            new() { Module = "Codebooks", EntityName = "CodebookValue", Count = 3 }
        };

        var result = new CodebookUsageResult
        {
            IsInUse = true,
            UsageCount = 13,
            IsReliable = true,
            Locations = locations
        };

        Assert.Equal(2, result.Locations.Count);
        Assert.Equal(13, result.UsageCount);
        Assert.True(result.IsInUse);
    }
}
