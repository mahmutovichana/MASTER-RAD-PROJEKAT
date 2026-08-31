using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using RBBH.CollateralAppraisal.Api.Tests.Helpers;
using Xunit;

namespace RBBH.CollateralAppraisal.Api.Tests.Users;

/// <summary>
/// UserRoleEndpoints testovi. Koristi IUserRoleProvider stub iz ApiFactory
/// koji vraća prazne podatke (bez pravog Keycloak-a).
/// </summary>
[Collection("ApiTests")]
public sealed class UserRoleEndpointsTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;
    public UserRoleEndpointsTests(ApiFactory f) => _factory = f;

    // ── GET /api/users — 401 / 403 / 200 ─────────────────────────────────────

    [Fact]
    public async Task ListUsers_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient().GetAsync("/api/users");
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task ListUsers_NoPermission_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-noperm").GetAsync("/api/users");
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task ListUsers_AM_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am").GetAsync("/api/users");
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task ListUsers_Admin_Returns200()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin").GetAsync("/api/users?page=1&pageSize=20");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
        var body = await r.Content.ReadFromJsonAsync<System.Text.Json.JsonElement>();
        Assert.True(body.TryGetProperty("items", out _));
    }

    [Fact]
    public async Task ListUsers_WithSearchParam_Returns200()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .GetAsync("/api/users?page=1&pageSize=10&search=test");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    [Fact]
    public async Task ListUsers_WithActiveFilter_Returns200()
    {
        // Test sa isActive filter — provjera da paginacija i filteri rade
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .GetAsync("/api/users?page=1&pageSize=20&isActive=true");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    // ── GET /api/users/{userId}/roles ─────────────────────────────────────────

    [Fact]
    public async Task GetUserRoles_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient().GetAsync("/api/users/some-id/roles");
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task GetUserRoles_NoPermission_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-noperm")
            .GetAsync("/api/users/some-id/roles");
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task GetUserRoles_UnknownUser_Returns404()
    {
        // Stub vraća null za nepoznatog korisnika → 404
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .GetAsync("/api/users/non-existent-user-id/roles");
        Assert.Equal(HttpStatusCode.NotFound, r.StatusCode);
    }

    // ── POST /api/users/{userId}/suspend ──────────────────────────────────────

    [Fact]
    public async Task SuspendUser_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient()
            .PostAsJsonAsync("/api/users/some-id/suspend", new { reason = "Test" });
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task SuspendUser_AM_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am")
            .PostAsJsonAsync("/api/users/some-id/suspend", new { reason = "Test" });
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task SuspendUser_Admin_Returns204()
    {
        // Stub IUserSuspensionService uvijek uspijeva — 204 NoContent
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .PostAsJsonAsync("/api/users/some-user-id/suspend", new { reason = "Test" });
        Assert.Equal(HttpStatusCode.NoContent, r.StatusCode);
    }

    // ── POST /api/users/{userId}/reactivate ───────────────────────────────────

    [Fact]
    public async Task ReactivateUser_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient()
            .PostAsJsonAsync("/api/users/some-id/reactivate", new { });
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task ReactivateUser_AM_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am")
            .PostAsJsonAsync("/api/users/some-id/reactivate", new { });
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task ReactivateUser_Admin_Returns204()
    {
        // Stub IUserSuspensionService uvijek uspijeva — 204 NoContent
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .PostAsJsonAsync("/api/users/some-user-id/reactivate", new { });
        Assert.Equal(HttpStatusCode.NoContent, r.StatusCode);
    }
}
