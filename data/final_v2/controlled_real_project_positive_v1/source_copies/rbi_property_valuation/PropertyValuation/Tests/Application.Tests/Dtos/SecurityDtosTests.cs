using RBBH.CollateralAppraisal.Application.Security.DTOs;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Dtos;

public sealed class SecurityDtosTests
{
    [Fact]
    public void AssignRoleRequest_StoresUserIdAndRoleName()
    {
        var request = new AssignRoleRequest(UserId: "user-1", RoleName: "AM");

        Assert.Equal("user-1", request.UserId);
        Assert.Equal("AM",     request.RoleName);
    }

    [Fact]
    public void RemoveRoleRequest_StoresUserIdAndRoleName()
    {
        var request = new RemoveRoleRequest(UserId: "user-1", RoleName: "AM");

        Assert.Equal("user-1", request.UserId);
        Assert.Equal("AM",     request.RoleName);
    }

    [Fact]
    public void TransferAdminRoleRequest_StoresSourceTargetAndReason()
    {
        var request = new TransferAdminRoleRequest(
            SourceUserId: "user-1",
            TargetUserId: "user-2",
            Reason: "Predaja administracije novom korisniku");

        Assert.Equal("user-1", request.SourceUserId);
        Assert.Equal("user-2", request.TargetUserId);
        Assert.Equal("Predaja administracije novom korisniku", request.Reason);
    }
}
