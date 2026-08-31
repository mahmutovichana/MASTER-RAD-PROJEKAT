using RBBH.CollateralAppraisal.Domain.Roles;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Domain;

public sealed class RoleDefinitionTests
{
    [Fact]
    public void CreateSystem_SetsIsSystemAndIsActive()
    {
        var role = RoleDefinition.CreateSystem("AM", "Account Manager", "opis");

        Assert.True(role.IsSystem);
        Assert.True(role.IsActive);
        Assert.Equal("AM", role.Name);
        Assert.Equal("Account Manager", role.DisplayName);
        Assert.Equal("opis", role.Description);
        Assert.Null(role.CreatedByUserId);
        Assert.Empty(role.Permissions);
    }

    [Fact]
    public void CreateCustom_SetsCreatedByUserIdAndIsSystemFalse()
    {
        var role = RoleDefinition.CreateCustom("CUSTOM", "Custom rola", null, "user-1");

        Assert.False(role.IsSystem);
        Assert.True(role.IsActive);
        Assert.Equal("user-1", role.CreatedByUserId);
        Assert.Null(role.Description);
    }

    [Fact]
    public void Update_ChangesDisplayNameDescriptionAndUpdatedBy()
    {
        var role = RoleDefinition.CreateCustom("CUSTOM", "Stari naziv", null, "user-1");
        var now = DateTime.UtcNow;

        role.Update("Novi naziv", "Novi opis", "user-2", now);

        Assert.Equal("Novi naziv", role.DisplayName);
        Assert.Equal("Novi opis", role.Description);
        Assert.Equal("user-2", role.UpdatedByUserId);
        Assert.Equal(now, role.UpdatedAt);
        Assert.Equal("CUSTOM", role.Name);
    }

    [Fact]
    public void Deactivate_SetsIsActiveFalseAndUpdatedBy()
    {
        var role = RoleDefinition.CreateCustom("CUSTOM", "Naziv", null, "user-1");
        var now = DateTime.UtcNow;

        role.Deactivate("user-2", now);

        Assert.False(role.IsActive);
        Assert.Equal("user-2", role.UpdatedByUserId);
        Assert.Equal(now, role.UpdatedAt);
    }

    [Fact]
    public void Activate_SetsIsActiveTrueAndUpdatedBy()
    {
        var role = RoleDefinition.CreateCustom("CUSTOM", "Naziv", null, "user-1");
        var now = DateTime.UtcNow;
        role.Deactivate("user-2", now);

        role.Activate("user-3", now.AddMinutes(1));

        Assert.True(role.IsActive);
        Assert.Equal("user-3", role.UpdatedByUserId);
        Assert.Equal(now.AddMinutes(1), role.UpdatedAt);
    }

    [Fact]
    public void SoftDelete_SetsDeletedAtAndDeletedByUserId()
    {
        var role = RoleDefinition.CreateCustom("CUSTOM", "Naziv", null, "user-1");
        var now = DateTime.UtcNow;

        role.SoftDelete("user-2", now);

        Assert.Equal(now, role.DeletedAt);
        Assert.Equal("user-2", role.DeletedByUserId);
        Assert.Equal("user-2", role.UpdatedByUserId);
        Assert.Equal(now, role.UpdatedAt);
    }
}
