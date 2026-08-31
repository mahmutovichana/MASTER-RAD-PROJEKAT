using System.Security.Claims;
using Microsoft.Extensions.Caching.Memory;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Roles.Interfaces;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Infrastructure.Auth;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Auth;

public sealed class PermissionClaimsTransformationTests : IDisposable
{
    private readonly IRoleDefinitionService _roleDefinitionService;
    private readonly MemoryCache _cache;
    private readonly PermissionClaimsTransformation _sut;

    public PermissionClaimsTransformationTests()
    {
        _roleDefinitionService = Substitute.For<IRoleDefinitionService>();
        _cache = new MemoryCache(new MemoryCacheOptions());
        _sut   = new PermissionClaimsTransformation(_roleDefinitionService, _cache);
    }

    public void Dispose() => _cache.Dispose();

    private static ClaimsPrincipal CreatePrincipal(params Claim[] claims)
        => new(new ClaimsIdentity(claims, "TestAuth"));

    [Fact]
    public async Task TransformAsync_NotAuthenticated_ReturnsUnchangedPrincipal()
    {
        var principal = new ClaimsPrincipal(new ClaimsIdentity());

        var result = await _sut.TransformAsync(principal);

        Assert.Same(principal, result);
        Assert.Empty(result.FindAll("permission"));
    }

    [Fact]
    public async Task TransformAsync_AlreadyTransformed_ReturnsUnchangedPrincipal()
    {
        var principal = CreatePrincipal(
            new Claim(ClaimTypes.Role, AppRoles.Administrator),
            new Claim("permissions_transformed", "true"));

        var result = await _sut.TransformAsync(principal);

        Assert.Same(principal, result);
        Assert.Empty(result.FindAll("permission"));
    }

    [Fact]
    public async Task TransformAsync_NoRoles_ReturnsUnchangedPrincipal()
    {
        var principal = CreatePrincipal();

        var result = await _sut.TransformAsync(principal);

        Assert.Same(principal, result);
        Assert.Empty(result.FindAll("permission"));
    }

    [Fact]
    public async Task TransformAsync_SystemRole_AddsPermissionsFromMatrixWithoutCallingService()
    {
        var principal = CreatePrincipal(new Claim(ClaimTypes.Role, AppRoles.Administrator));

        var result = await _sut.TransformAsync(principal);

        var permissions = result.FindAll("permission").Select(c => c.Value).ToHashSet();
        Assert.Superset(RolePermissionMatrix.PermissionsByRole[AppRoles.Administrator].ToHashSet(), permissions);
        Assert.True(result.HasClaim("permissions_transformed", "true"));

        await _roleDefinitionService.DidNotReceive()
            .GetPermissionCodesForRoleAsync(Arg.Any<string>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task TransformAsync_CustomRole_FetchesPermissionsFromService()
    {
        _roleDefinitionService.GetPermissionCodesForRoleAsync("CustomRole", Arg.Any<CancellationToken>())
            .Returns(new List<string> { "custom.permission" });

        var principal = CreatePrincipal(new Claim(ClaimTypes.Role, "CustomRole"));

        var result = await _sut.TransformAsync(principal);

        var permissions = result.FindAll("permission").Select(c => c.Value).ToList();
        Assert.Contains("custom.permission", permissions);

        await _roleDefinitionService.Received(1)
            .GetPermissionCodesForRoleAsync("CustomRole", Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task TransformAsync_CustomRole_SecondCall_UsesCacheWithoutCallingServiceAgain()
    {
        _roleDefinitionService.GetPermissionCodesForRoleAsync("CustomRole", Arg.Any<CancellationToken>())
            .Returns(new List<string> { "custom.permission" });

        await _sut.TransformAsync(CreatePrincipal(new Claim(ClaimTypes.Role, "CustomRole")));
        await _sut.TransformAsync(CreatePrincipal(new Claim(ClaimTypes.Role, "CustomRole")));

        await _roleDefinitionService.Received(1)
            .GetPermissionCodesForRoleAsync("CustomRole", Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task TransformAsync_CustomRoleServiceReturnsNull_DoesNotAddPermissionsAndDoesNotThrow()
    {
        _roleDefinitionService.GetPermissionCodesForRoleAsync("CustomRole", Arg.Any<CancellationToken>())
            .Returns((IReadOnlyList<string>)null!);

        var principal = CreatePrincipal(new Claim(ClaimTypes.Role, "CustomRole"));

        var result = await _sut.TransformAsync(principal);

        Assert.Empty(result.FindAll("permission"));
        Assert.True(result.HasClaim("permissions_transformed", "true"));
    }

    [Fact]
    public async Task TransformAsync_SystemAndCustomRole_CombinesMatrixAndServicePermissions()
    {
        _roleDefinitionService.GetPermissionCodesForRoleAsync("CustomRole", Arg.Any<CancellationToken>())
            .Returns(new List<string> { "custom.permission" });

        var principal = CreatePrincipal(
            new Claim(ClaimTypes.Role, AppRoles.Administrator),
            new Claim(ClaimTypes.Role, "CustomRole"));

        var result = await _sut.TransformAsync(principal);

        var permissions = result.FindAll("permission").Select(c => c.Value).ToHashSet();
        Assert.Contains("custom.permission", permissions);
        Assert.Superset(RolePermissionMatrix.PermissionsByRole[AppRoles.Administrator].ToHashSet(), permissions);
    }

    [Fact]
    public void InvalidateRoleCache_RemovesEntry()
    {
        _cache.Set("role_perms_CustomRole", new List<string> { "x" });

        PermissionClaimsTransformation.InvalidateRoleCache(_cache, "CustomRole");

        Assert.False(_cache.TryGetValue("role_perms_CustomRole", out _));
    }
}
