using RBBH.CollateralAppraisal.Domain.Codebooks;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Domain;

public sealed class CodebookValueTests
{
    private static CodebookValue MakeValue() =>
        CodebookValue.Create(
            codebookKey:     "relation_basis",
            code:            "VLASNIK",
            label:           "Vlasnik",
            description:     "opis",
            sortOrder:       1,
            createdByUserId: "user-1");

    [Fact]
    public void Create_SetsIsActiveTrue()
    {
        var value = MakeValue();

        Assert.True(value.IsActive);
        Assert.Equal("relation_basis", value.CodebookKey);
        Assert.Equal("VLASNIK",        value.Code);
        Assert.Equal("Vlasnik",        value.Label);
        Assert.Equal("opis",           value.Description);
        Assert.Equal(1,                value.SortOrder);
        Assert.Equal("user-1",         value.CreatedByUserId);
        Assert.False(value.IsSystem);
        Assert.False(value.IsCritical);
    }

    [Fact]
    public void Create_WithSystemAndCriticalFlags()
    {
        var value = CodebookValue.Create(
            "relation_basis", "VLASNIK", "Vlasnik", null, 1, "user-1",
            isSystem: true, isCritical: true);

        Assert.True(value.IsSystem);
        Assert.True(value.IsCritical);
    }

    [Fact]
    public void Deactivate_SetsIsActiveFalseAndDeactivationFields()
    {
        var value = MakeValue();
        var now   = DateTime.UtcNow;

        value.Deactivate(now, "user-2", "Nije više u upotrebi");

        Assert.False(value.IsActive);
        Assert.Equal(now,                     value.DeactivatedAt);
        Assert.Equal("user-2",                value.DeactivatedByUserId);
        Assert.Equal("Nije više u upotrebi",  value.DeactivationReason);
        Assert.Equal("user-2",                value.UpdatedByUserId);
        Assert.Equal(now,                     value.UpdatedAt);
    }

    [Fact]
    public void Activate_SetsIsActiveTrueAndPreservesDeactivationHistory()
    {
        var value = MakeValue();
        var now   = DateTime.UtcNow;
        value.Deactivate(now, "user-2", "Nije više u upotrebi");

        value.Activate(now.AddMinutes(1), "user-3");

        Assert.True(value.IsActive);
        Assert.Equal("user-3", value.UpdatedByUserId);
        Assert.Equal(now.AddMinutes(1), value.UpdatedAt);
        // Historijski trag deaktivacije ostaje sačuvan
        Assert.Equal(now,                    value.DeactivatedAt);
        Assert.Equal("user-2",               value.DeactivatedByUserId);
        Assert.Equal("Nije više u upotrebi", value.DeactivationReason);
    }

    [Fact]
    public void SoftDelete_SetsDeletedAtAndDeletedByUserId()
    {
        var value = MakeValue();
        var now   = DateTime.UtcNow;

        value.SoftDelete(now, "user-2");

        Assert.Equal(now,      value.DeletedAt);
        Assert.Equal("user-2", value.DeletedByUserId);
        Assert.Equal("user-2", value.UpdatedByUserId);
        Assert.Equal(now,      value.UpdatedAt);
    }

    [Fact]
    public void UpdateDetails_ChangesLabelDescriptionAndSortOrder()
    {
        var value = MakeValue();
        var now   = DateTime.UtcNow;

        value.UpdateDetails("Novi label", "Novi opis", 5, "user-2", now);

        Assert.Equal("Novi label", value.Label);
        Assert.Equal("Novi opis",  value.Description);
        Assert.Equal(5,            value.SortOrder);
        Assert.Equal("user-2",     value.UpdatedByUserId);
        Assert.Equal(now,          value.UpdatedAt);
    }
}
