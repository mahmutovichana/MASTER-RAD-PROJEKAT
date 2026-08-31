using System.Security.Claims;
using RBBH.CollateralAppraisal.Infrastructure.Auth;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Auth;

public sealed class ClaimsPrincipalExtensionsTests
{
    private static ClaimsPrincipal CreatePrincipal(params Claim[] claims)
        => new(new ClaimsIdentity(claims));

    [Fact]
    public void GetUserId_FromNameIdentifierClaim_ReturnsValue()
    {
        var principal = CreatePrincipal(new Claim(ClaimTypes.NameIdentifier, "user-1"));

        Assert.Equal("user-1", principal.GetUserId());
    }

    [Fact]
    public void GetUserId_FromSubClaim_FallsBackWhenNoNameIdentifier()
    {
        var principal = CreatePrincipal(new Claim("sub", "user-2"));

        Assert.Equal("user-2", principal.GetUserId());
    }

    [Fact]
    public void GetUserId_NoMatchingClaims_ReturnsNull()
    {
        var principal = CreatePrincipal();

        Assert.Null(principal.GetUserId());
    }

    [Fact]
    public void GetUsername_FromPreferredUsernameClaim_ReturnsValue()
    {
        var principal = CreatePrincipal(
            new Claim("preferred_username", "jdoe"),
            new Claim(ClaimTypes.Name, "John Doe"));

        Assert.Equal("jdoe", principal.GetUsername());
    }

    [Fact]
    public void GetUsername_FromNameClaim_FallsBackWhenNoPreferredUsername()
    {
        var principal = CreatePrincipal(new Claim(ClaimTypes.Name, "John Doe"));

        Assert.Equal("John Doe", principal.GetUsername());
    }

    [Fact]
    public void GetUsername_FromEmailClaim_FallsBackWhenNoNameOrPreferredUsername()
    {
        var principal = CreatePrincipal(new Claim(ClaimTypes.Email, "john@test.ba"));

        Assert.Equal("john@test.ba", principal.GetUsername());
    }

    [Fact]
    public void GetUsername_NoMatchingClaims_ReturnsNull()
    {
        var principal = CreatePrincipal();

        Assert.Null(principal.GetUsername());
    }

    [Fact]
    public void GetRoles_CombinesFlatClaimFormatsAndDeduplicatesCaseInsensitively()
    {
        var principal = CreatePrincipal(
            new Claim(ClaimTypes.Role, "Administrator"),
            new Claim("role", "CO"),
            new Claim("roles", "administrator")); // duplicate, different case

        var roles = principal.GetRoles();

        Assert.Equal(2, roles.Count);
        Assert.Contains("Administrator", roles, StringComparer.OrdinalIgnoreCase);
        Assert.Contains("CO", roles, StringComparer.OrdinalIgnoreCase);
    }

    [Fact]
    public void GetRoles_FiltersOutWhitespaceOnlyValues()
    {
        var principal = CreatePrincipal(
            new Claim(ClaimTypes.Role, "AM"),
            new Claim("role", "   "));

        var roles = principal.GetRoles();

        Assert.Single(roles);
        Assert.Equal("AM", roles[0]);
    }

    [Fact]
    public void GetRoles_NoClaims_ReturnsEmpty()
    {
        var principal = CreatePrincipal();

        Assert.Empty(principal.GetRoles());
    }

    [Fact]
    public void GetRoles_ParsesNestedRealmAccessRolesArray()
    {
        var principal = CreatePrincipal(
            new Claim("realm_access", """{"roles":["AM","SM"]}"""));

        var roles = principal.GetRoles();

        Assert.Equal(2, roles.Count);
        Assert.Contains("AM", roles);
        Assert.Contains("SM", roles);
    }

    [Fact]
    public void GetRoles_CombinesFlatAndRealmAccessRoles()
    {
        var principal = CreatePrincipal(
            new Claim(ClaimTypes.Role, "Administrator"),
            new Claim("realm_access", """{"roles":["AM"]}"""));

        var roles = principal.GetRoles();

        Assert.Equal(2, roles.Count);
        Assert.Contains("Administrator", roles);
        Assert.Contains("AM", roles);
    }

    [Fact]
    public void GetRoles_RealmAccessWithNullArrayEntry_IsFilteredOut()
    {
        var principal = CreatePrincipal(
            new Claim("realm_access", """{"roles":["AM",null]}"""));

        var roles = principal.GetRoles();

        Assert.Single(roles);
        Assert.Equal("AM", roles[0]);
    }

    [Fact]
    public void GetRoles_RealmAccessWithoutRolesProperty_ReturnsOnlyFlatRoles()
    {
        var principal = CreatePrincipal(
            new Claim(ClaimTypes.Role, "AM"),
            new Claim("realm_access", """{"otherProp":"value"}"""));

        var roles = principal.GetRoles();

        Assert.Single(roles);
        Assert.Equal("AM", roles[0]);
    }

    [Fact]
    public void GetRoles_RealmAccessRolesNotAnArray_ReturnsOnlyFlatRoles()
    {
        var principal = CreatePrincipal(
            new Claim(ClaimTypes.Role, "AM"),
            new Claim("realm_access", """{"roles":"AM"}"""));

        var roles = principal.GetRoles();

        Assert.Single(roles);
        Assert.Equal("AM", roles[0]);
    }

    [Fact]
    public void GetRoles_RealmAccessInvalidJson_IgnoresAndReturnsFlatRolesOnly()
    {
        var principal = CreatePrincipal(
            new Claim(ClaimTypes.Role, "AM"),
            new Claim("realm_access", "{not-valid-json"));

        var roles = principal.GetRoles();

        Assert.Single(roles);
        Assert.Equal("AM", roles[0]);
    }

    [Fact]
    public void GetRoles_RealmAccessBlank_IsIgnored()
    {
        var principal = CreatePrincipal(
            new Claim(ClaimTypes.Role, "AM"),
            new Claim("realm_access", "   "));

        var roles = principal.GetRoles();

        Assert.Single(roles);
        Assert.Equal("AM", roles[0]);
    }

    [Fact]
    public void HasPermission_ClaimPresent_ReturnsTrue()
    {
        var principal = CreatePrincipal(new Claim("permission", "orders.create"));

        Assert.True(principal.HasPermission("orders.create"));
    }

    [Fact]
    public void HasPermission_ClaimMissing_ReturnsFalse()
    {
        var principal = CreatePrincipal(new Claim("permission", "orders.create"));

        Assert.False(principal.HasPermission("orders.delete"));
    }
}
