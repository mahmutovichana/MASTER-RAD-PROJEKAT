using NSubstitute;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Infrastructure.Security;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Security;

public sealed class UserPermissionServiceTests
{
    private static UserPermissionService CreateSut(params string[] roles)
    {
        var currentUser = Substitute.For<ICurrentUserService>();
        currentUser.Roles.Returns(roles);
        return new UserPermissionService(currentUser);
    }

    [Fact]
    public void CurrentUserHasPermission_RoleHasPermission_ReturnsTrue()
    {
        var sut = CreateSut(AppRoles.Administrator);

        Assert.True(sut.CurrentUserHasPermission(AppPermissions.UsersView));
    }

    [Fact]
    public void CurrentUserHasPermission_RoleDoesNotHavePermission_ReturnsFalse()
    {
        var sut = CreateSut(AppRoles.Vjestak);

        Assert.False(sut.CurrentUserHasPermission(AppPermissions.UsersView));
    }

    [Fact]
    public void CurrentUserHasPermission_MultipleRoles_UnionsPermissions()
    {
        var sut = CreateSut(AppRoles.Unosnik, AppRoles.Verifikator);

        Assert.True(sut.CurrentUserHasPermission(AppPermissions.RecordsCreate));
        Assert.True(sut.CurrentUserHasPermission(AppPermissions.RecordsApprove));
    }

    [Fact]
    public void CurrentUserHasPermission_NoRoles_ReturnsFalse()
    {
        var sut = CreateSut();

        Assert.False(sut.CurrentUserHasPermission(AppPermissions.UsersView));
    }

    [Fact]
    public void CurrentUserHasPermission_UnknownRole_ReturnsFalse()
    {
        var sut = CreateSut("NonExistentRole");

        Assert.False(sut.CurrentUserHasPermission(AppPermissions.UsersView));
    }
}
