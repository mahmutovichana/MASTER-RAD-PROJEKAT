using RBBH.CollateralAppraisal.Domain.Roles;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Domain;

public sealed class RolePermissionTests
{
    [Fact]
    public void Create_InitializesJoinEntityWithCreatedAt()
    {
        var before = DateTime.UtcNow;

        var rolePermission = RolePermission.Create(roleId: 1, permissionId: 2, userId: "user-1");

        var after = DateTime.UtcNow;

        Assert.Equal(1, rolePermission.RoleDefinitionId);
        Assert.Equal(2, rolePermission.PermissionDefinitionId);
        Assert.Equal("user-1", rolePermission.CreatedByUserId);
        Assert.InRange(rolePermission.CreatedAt, before, after);
    }
}
