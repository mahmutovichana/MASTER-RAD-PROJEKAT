using System.Security.Claims;
using Microsoft.AspNetCore.Http;
using NSubstitute;
using RBBH.CollateralAppraisal.Infrastructure.Auth;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Auth;

public sealed class CurrentUserServiceTests
{
    private static CurrentUserService CreateService(ClaimsPrincipal? user)
    {
        var accessor = Substitute.For<IHttpContextAccessor>();
        accessor.HttpContext.Returns(user is null ? null : new DefaultHttpContext { User = user });

        return new CurrentUserService(accessor);
    }

    private static ClaimsPrincipal AuthenticatedPrincipal(params Claim[] claims)
        => new(new ClaimsIdentity(claims, "TestAuth"));

    private static ClaimsPrincipal UnauthenticatedPrincipal(params Claim[] claims)
        => new(new ClaimsIdentity(claims));

    [Fact]
    public void UserId_FromNameIdentifierClaim_ReturnsValue()
    {
        var sut = CreateService(AuthenticatedPrincipal(new Claim(ClaimTypes.NameIdentifier, "user-1")));

        Assert.Equal("user-1", sut.UserId);
    }

    [Fact]
    public void UserId_FromSubClaim_WhenNameIdentifierMissing_ReturnsValue()
    {
        var sut = CreateService(AuthenticatedPrincipal(new Claim("sub", "user-2")));

        Assert.Equal("user-2", sut.UserId);
    }

    [Fact]
    public void UserId_NoHttpContext_ReturnsNull()
    {
        var sut = CreateService(null);

        Assert.Null(sut.UserId);
    }

    [Fact]
    public void Username_FromPreferredUsernameClaim_ReturnsValue()
    {
        var sut = CreateService(AuthenticatedPrincipal(
            new Claim("preferred_username", "jdoe"),
            new Claim(ClaimTypes.Name, "John Doe")));

        Assert.Equal("jdoe", sut.Username);
    }

    [Fact]
    public void Username_FromNameClaim_WhenPreferredUsernameMissing_ReturnsValue()
    {
        var sut = CreateService(AuthenticatedPrincipal(new Claim(ClaimTypes.Name, "John Doe")));

        Assert.Equal("John Doe", sut.Username);
    }

    [Fact]
    public void Email_FromClaimTypesEmail_ReturnsValue()
    {
        var sut = CreateService(AuthenticatedPrincipal(new Claim(ClaimTypes.Email, "john@test.ba")));

        Assert.Equal("john@test.ba", sut.Email);
    }

    [Fact]
    public void Email_FromEmailClaim_WhenClaimTypesEmailMissing_ReturnsValue()
    {
        var sut = CreateService(AuthenticatedPrincipal(new Claim("email", "jane@test.ba")));

        Assert.Equal("jane@test.ba", sut.Email);
    }

    [Fact]
    public void Role_ReturnsFirstRole()
    {
        var sut = CreateService(AuthenticatedPrincipal(
            new Claim(ClaimTypes.Role, "Administrator"),
            new Claim(ClaimTypes.Role, "Prodaja")));

        Assert.Equal("Administrator", sut.Role);
    }

    [Fact]
    public void Role_NoRoles_ReturnsNull()
    {
        var sut = CreateService(AuthenticatedPrincipal());

        Assert.Null(sut.Role);
    }

    [Fact]
    public void Roles_ReturnsAllRoles()
    {
        var sut = CreateService(AuthenticatedPrincipal(
            new Claim(ClaimTypes.Role, "Administrator"),
            new Claim(ClaimTypes.Role, "Prodaja")));

        Assert.Equal(2, sut.Roles.Count);
        Assert.Contains("Administrator", sut.Roles);
        Assert.Contains("Prodaja", sut.Roles);
    }

    [Fact]
    public void Roles_NoHttpContext_ReturnsEmpty()
    {
        var sut = CreateService(null);

        Assert.Empty(sut.Roles);
    }

    [Fact]
    public void Permissions_ReturnsValuesSortedAlphabetically()
    {
        var sut = CreateService(AuthenticatedPrincipal(
            new Claim("permission", "orders.view"),
            new Claim("permission", "orders.create")));

        Assert.Equal(["orders.create", "orders.view"], sut.Permissions);
    }

    [Fact]
    public void Permissions_NoHttpContext_ReturnsEmpty()
    {
        var sut = CreateService(null);

        Assert.Empty(sut.Permissions);
    }

    [Fact]
    public void IsAuthenticated_AuthenticatedPrincipal_ReturnsTrue()
    {
        var sut = CreateService(AuthenticatedPrincipal());

        Assert.True(sut.IsAuthenticated);
    }

    [Fact]
    public void IsAuthenticated_UnauthenticatedPrincipal_ReturnsFalse()
    {
        var sut = CreateService(UnauthenticatedPrincipal());

        Assert.False(sut.IsAuthenticated);
    }

    [Fact]
    public void IsAuthenticated_NoHttpContext_ReturnsFalse()
    {
        var sut = CreateService(null);

        Assert.False(sut.IsAuthenticated);
    }

    // ── FullName ──────────────────────────────────────────────────────────────

    [Fact]
    public void FullName_FromNameClaim_ReturnsValue()
    {
        var sut = CreateService(AuthenticatedPrincipal(
            new Claim("name", "Haris Hadzic"),
            new Claim("given_name", "Haris"),
            new Claim("family_name", "Hadzic"),
            new Claim("preferred_username", "hhadzic")));

        Assert.Equal("Haris Hadzic", sut.FullName);
    }

    [Fact]
    public void FullName_FromGivenAndFamilyName_WhenNameClaimMissing()
    {
        var sut = CreateService(AuthenticatedPrincipal(
            new Claim("given_name", "Amina"),
            new Claim("family_name", "Amiric"),
            new Claim("preferred_username", "aamiric")));

        Assert.Equal("Amina Amiric", sut.FullName);
    }

    [Fact]
    public void FullName_FromGivenNameOnly_WhenFamilyNameMissing()
    {
        var sut = CreateService(AuthenticatedPrincipal(
            new Claim("given_name", "Amina"),
            new Claim("preferred_username", "aamiric")));

        Assert.Equal("Amina", sut.FullName);
    }

    [Fact]
    public void FullName_FallbackToUsername_WhenNoNameClaims()
    {
        var sut = CreateService(AuthenticatedPrincipal(
            new Claim("preferred_username", "aamiric")));

        Assert.Equal("aamiric", sut.FullName);
    }

    [Fact]
    public void FullName_NoHttpContext_ReturnsNull()
    {
        var sut = CreateService(null);

        Assert.Null(sut.FullName);
    }

    [Fact]
    public void FullName_NoClaims_ReturnsNull()
    {
        var sut = CreateService(AuthenticatedPrincipal());

        Assert.Null(sut.FullName);
    }

    // ── Email additional ──────────────────────────────────────────────────────

    [Fact]
    public void Email_NoHttpContext_ReturnsNull()
    {
        var sut = CreateService(null);

        Assert.Null(sut.Email);
    }

    [Fact]
    public void Email_NoClaims_ReturnsNull()
    {
        var sut = CreateService(AuthenticatedPrincipal());

        Assert.Null(sut.Email);
    }

    // ── Username additional ──────────────────────────────────────────────────

    [Fact]
    public void Username_NoHttpContext_ReturnsNull()
    {
        var sut = CreateService(null);

        Assert.Null(sut.Username);
    }

    [Fact]
    public void Username_NoClaims_ReturnsNull()
    {
        var sut = CreateService(AuthenticatedPrincipal());

        Assert.Null(sut.Username);
    }

    // ── UserId additional ────────────────────────────────────────────────────

    [Fact]
    public void UserId_BothClaimsPresent_PrefersNameIdentifier()
    {
        var sut = CreateService(AuthenticatedPrincipal(
            new Claim(ClaimTypes.NameIdentifier, "user-1"),
            new Claim("sub", "user-2")));

        Assert.Equal("user-1", sut.UserId);
    }

    [Fact]
    public void UserId_UnauthenticatedPrincipal_ReturnsValue()
    {
        var sut = CreateService(UnauthenticatedPrincipal(
            new Claim(ClaimTypes.NameIdentifier, "user-1")));

        Assert.Equal("user-1", sut.UserId);
    }

    // ── Permissions additional ────────────────────────────────────────────────

    [Fact]
    public void Permissions_NoPermissionClaims_ReturnsEmpty()
    {
        var sut = CreateService(AuthenticatedPrincipal(
            new Claim(ClaimTypes.Role, "Administrator")));

        Assert.Empty(sut.Permissions);
    }

    [Fact]
    public void Permissions_SinglePermission_ReturnsSingle()
    {
        var sut = CreateService(AuthenticatedPrincipal(
            new Claim("permission", "orders.view")));

        Assert.Single(sut.Permissions);
        Assert.Equal("orders.view", sut.Permissions[0]);
    }

    // ── Roles additional ─────────────────────────────────────────────────────

    [Fact]
    public void Roles_UnauthenticatedUser_ReturnsRolesFromClaims()
    {
        var sut = CreateService(UnauthenticatedPrincipal(
            new Claim(ClaimTypes.Role, "Administrator")));

        Assert.Contains("Administrator", sut.Roles);
    }

    [Fact]
    public void Role_MultipleRoles_ReturnsFirst()
    {
        var sut = CreateService(AuthenticatedPrincipal(
            new Claim(ClaimTypes.Role, "KolateralAdministrator"),
            new Claim(ClaimTypes.Role, "KolateralOficir")));

        Assert.Equal("KolateralAdministrator", sut.Role);
    }
}
