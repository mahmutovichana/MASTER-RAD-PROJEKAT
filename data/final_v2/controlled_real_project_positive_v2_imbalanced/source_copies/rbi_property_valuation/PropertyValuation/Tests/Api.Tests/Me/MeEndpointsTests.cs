using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using RBBH.CollateralAppraisal.Api.Tests.Helpers;
using Xunit;

namespace RBBH.CollateralAppraisal.Api.Tests.Me;

[Collection("ApiTests")]
public sealed class MeEndpointsTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;

    public MeEndpointsTests(ApiFactory factory) => _factory = factory;

    // ── GET /api/me ───────────────────────────────────────────────────────────

    [Fact]
    public async Task GetMe_WithAmToken_Returns200WithActiveStatus()
    {
        var client = _factory.CreateAuthenticatedClient("test-am");
        var response = await client.GetAsync("/api/me");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var body = await response.Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal("Active", body.GetProperty("userStatus").GetString());
        Assert.Equal("AM", body.GetProperty("roles").EnumerateArray().First().GetString());
    }

    [Fact]
    public async Task GetMe_WithNoPermToken_Returns200WithNoRoleStatus()
    {
        var client = _factory.CreateAuthenticatedClient("test-noperm");
        var response = await client.GetAsync("/api/me");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var body = await response.Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal("NoRole", body.GetProperty("userStatus").GetString());
    }

    [Fact]
    public async Task GetMe_NoToken_Returns401()
    {
        var client = _factory.CreateAnonymousClient();
        var response = await client.GetAsync("/api/me");
        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    // ── POST /api/me/active-role ──────────────────────────────────────────────

    [Fact]
    public async Task SetActiveRole_EmptyRoleCode_Returns400()
    {
        var client = _factory.CreateAuthenticatedClient("test-am");
        var response = await client.PostAsJsonAsync("/api/me/active-role", new { roleCode = "" });
        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }

    [Fact]
    public async Task SetActiveRole_ValidOwnedRole_Returns200WithDashboardRoute()
    {
        var client = _factory.CreateAuthenticatedClient("test-am");
        var response = await client.PostAsJsonAsync("/api/me/active-role", new { roleCode = "AM" });
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var body = await response.Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal("AM", body.GetProperty("roleCode").GetString());
        Assert.NotEmpty(body.GetProperty("dashboardRoute").GetString()!);
    }

    [Fact]
    public async Task SetActiveRole_RoleNotOwned_Returns403()
    {
        // test-noperm nema role u tokenu — ne može tražiti AM rolu
        var client = _factory.CreateAuthenticatedClient("test-noperm");
        var response = await client.PostAsJsonAsync("/api/me/active-role", new { roleCode = "Administrator" });
        Assert.Equal(HttpStatusCode.Forbidden, response.StatusCode);
    }

    [Fact]
    public async Task SetActiveRole_UnknownRole_Returns400()
    {
        // test-admin ima role, ali "NepostojecaRola" nije u AppRoles — nema dashboardRoute
        var client = _factory.CreateAuthenticatedClient("test-admin");
        var response = await client.PostAsJsonAsync("/api/me/active-role", new { roleCode = "Administrator" });
        // Administrator ima dashboardRoute — treba proći
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task SetActiveRole_NullRoleCode_Returns400()
    {
        var client = _factory.CreateAuthenticatedClient("test-am");
        var response = await client.PostAsJsonAsync("/api/me/active-role", new { roleCode = (string?)null });
        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }

    [Fact]
    public async Task GetMe_WithAdminToken_Returns200WithModules()
    {
        var client = _factory.CreateAuthenticatedClient("test-admin");
        var response = await client.GetAsync("/api/me");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var body = await response.Content.ReadFromJsonAsync<System.Text.Json.JsonElement>();
        Assert.Equal("Active", body.GetProperty("userStatus").GetString());
    }

    [Fact]
    public async Task GetMe_WithVerifikatorRole_Returns200_WithNoRoleStatus()
    {
        // Verifikator uklonjen iz AppRoles.All (A-5 refactoring) — filtrira se kao nepoznata rola.
        // GetMe vraća NoRole jer rola nije u AppRoles.All listi.
        var client = _factory.CreateAuthenticatedClient("test-verifikator");
        var response = await client.GetAsync("/api/me");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var body = await response.Content.ReadFromJsonAsync<System.Text.Json.JsonElement>();
        Assert.Equal("NoRole", body.GetProperty("userStatus").GetString());
    }

    [Fact]
    public async Task GetMe_WithUnosnikRole_Returns200()
    {
        var client = _factory.CreateAuthenticatedClient("test-unosnik");
        var response = await client.GetAsync("/api/me");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task GetMe_WithUbRole_Returns200()
    {
        var client = _factory.CreateAuthenticatedClient("test-ub");
        var response = await client.GetAsync("/api/me");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task GetMe_WithKolateralAdminRole_Returns200()
    {
        var client = _factory.CreateAuthenticatedClient("test-kola");
        var response = await client.GetAsync("/api/me");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task GetMe_WithVjestakRole_Returns200WithDefaultModules()
    {
        // AppRoles.Vjestak nije u GetModulesForRole switch → default case "_"
        var client = _factory.CreateAuthenticatedClient("test-vjestak");
        var response = await client.GetAsync("/api/me");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task GetMe_WithMultipleRoles_Returns200WithSelectRoleStatus()
    {
        // test-multi-role ima AM + SM → "SelectRole" status
        var client = _factory.CreateAuthenticatedClient("test-multi-role");
        var response = await client.GetAsync("/api/me");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var body = await response.Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal("SelectRole", body.GetProperty("userStatus").GetString());
    }

    [Fact]
    public async Task GetMe_WithUnknownExternalRole_Returns200WithNoRoleStatus()
    {
        // test-unknown-role ima "CustomExternalRole" — filtrira se iz AppRoles.All → NoRole
        var client = _factory.CreateAuthenticatedClient("test-unknown-role");
        var response = await client.GetAsync("/api/me");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var body = await response.Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal("NoRole", body.GetProperty("userStatus").GetString());
    }

    [Fact]
    public async Task SetActiveRole_OwnedRoleWithNoDashboardRoute_Returns400()
    {
        // test-unknown-role ima "CustomExternalRole" koju posjeduje, ali nema dashboard rutu
        var client = _factory.CreateAuthenticatedClient("test-unknown-role");
        var response = await client.PostAsJsonAsync("/api/me/active-role", new { roleCode = "CustomExternalRole" });
        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }
}
