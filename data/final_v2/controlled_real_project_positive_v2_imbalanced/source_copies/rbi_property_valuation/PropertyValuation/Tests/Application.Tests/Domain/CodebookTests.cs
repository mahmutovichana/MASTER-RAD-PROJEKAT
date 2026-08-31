using RBBH.CollateralAppraisal.Domain.Codebooks;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Domain;

public sealed class CodebookTests
{
    [Fact]
    public void CreateSystem_SetsIsSystemAndIsActive()
    {
        var codebook = Codebook.CreateSystem("tipovi_nekretnina", "Tipovi nekretnina", "opis", "Nekretnine");

        Assert.True(codebook.IsSystem);
        Assert.True(codebook.IsActive);
        Assert.Equal("tipovi_nekretnina", codebook.Code);
        Assert.Equal("Tipovi nekretnina", codebook.Name);
        Assert.Equal("opis", codebook.Description);
        Assert.Equal("Nekretnine", codebook.Category);
        Assert.Null(codebook.CreatedByUserId);
    }

    [Fact]
    public void CreateCustom_SetsCreatedByUserIdAndIsSystemFalse()
    {
        var codebook = Codebook.CreateCustom("custom_kod", "Custom šifarnik", null, null, "user-1");

        Assert.False(codebook.IsSystem);
        Assert.True(codebook.IsActive);
        Assert.Equal("user-1", codebook.CreatedByUserId);
        Assert.Null(codebook.Description);
        Assert.Null(codebook.Category);
    }

    [Fact]
    public void Update_ChangesNameDescriptionCategoryAndUpdatedBy()
    {
        var codebook = Codebook.CreateCustom("custom_kod", "Stari naziv", null, null, "user-1");
        var now = DateTime.UtcNow;

        codebook.Update("Novi naziv", "Novi opis", "Nova kategorija", "user-2", now);

        Assert.Equal("Novi naziv", codebook.Name);
        Assert.Equal("Novi opis", codebook.Description);
        Assert.Equal("Nova kategorija", codebook.Category);
        Assert.Equal("user-2", codebook.UpdatedByUserId);
        Assert.Equal(now, codebook.UpdatedAt);
    }

    [Fact]
    public void Deactivate_SetsIsActiveFalseAndUpdatedBy()
    {
        var codebook = Codebook.CreateCustom("custom_kod", "Naziv", null, null, "user-1");
        var now = DateTime.UtcNow;

        codebook.Deactivate("user-2", now);

        Assert.False(codebook.IsActive);
        Assert.Equal("user-2", codebook.UpdatedByUserId);
        Assert.Equal(now, codebook.UpdatedAt);
    }

    [Fact]
    public void Activate_SetsIsActiveTrueAndUpdatedBy()
    {
        var codebook = Codebook.CreateCustom("custom_kod", "Naziv", null, null, "user-1");
        var now = DateTime.UtcNow;
        codebook.Deactivate("user-2", now);

        codebook.Activate("user-3", now.AddMinutes(1));

        Assert.True(codebook.IsActive);
        Assert.Equal("user-3", codebook.UpdatedByUserId);
        Assert.Equal(now.AddMinutes(1), codebook.UpdatedAt);
    }

    [Fact]
    public void SoftDelete_SetsDeletedAtAndDeletedByUserId()
    {
        var codebook = Codebook.CreateCustom("custom_kod", "Naziv", null, null, "user-1");
        var now = DateTime.UtcNow;

        codebook.SoftDelete("user-2", now);

        Assert.Equal(now, codebook.DeletedAt);
        Assert.Equal("user-2", codebook.DeletedByUserId);
        Assert.Equal("user-2", codebook.UpdatedByUserId);
        Assert.Equal(now, codebook.UpdatedAt);
    }
}
