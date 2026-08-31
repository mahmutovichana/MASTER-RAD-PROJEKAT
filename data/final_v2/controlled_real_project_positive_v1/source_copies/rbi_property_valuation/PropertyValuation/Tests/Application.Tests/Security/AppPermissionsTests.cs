using RBBH.CollateralAppraisal.Application.Security;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Security;

public sealed class AppPermissionsTests
{
    [Fact]
    public void All_ContainsCoreOrderApprovalPermissions()
    {
        Assert.Contains(AppPermissions.OrdersApproveFinal, AppPermissions.All);
        Assert.Contains(AppPermissions.OrdersDownloadAppraisal, AppPermissions.All);
        Assert.Contains(AppPermissions.CodebooksManage, AppPermissions.All);
        Assert.Contains(AppPermissions.AdminAccess, AppPermissions.All);
    }

    [Fact]
    public void All_HasNoDuplicates()
    {
        Assert.Equal(AppPermissions.All.Length, AppPermissions.All.Distinct().Count());
    }
}
