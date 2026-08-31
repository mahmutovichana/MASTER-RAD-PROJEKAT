using RBBH.CollateralAppraisal.Domain.Roles;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Domain;

public sealed class PermissionDefinitionTests
{
    [Fact]
    public void Create_InitializesPropertiesAndIsActive()
    {
        var permission = PermissionDefinition.Create(
            "orders.approve-final", "Odobri finalnu procjenu", "opis", "Orders");

        Assert.Equal("orders.approve-final", permission.Code);
        Assert.Equal("Odobri finalnu procjenu", permission.DisplayName);
        Assert.Equal("opis", permission.Description);
        Assert.Equal("Orders", permission.Module);
        Assert.True(permission.IsActive);
        Assert.Empty(permission.RolePermissions);
    }
}
