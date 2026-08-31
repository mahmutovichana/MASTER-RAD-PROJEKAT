using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using RBBH.CollateralAppraisal.Api.Tests.Helpers;
using Xunit;

namespace RBBH.CollateralAppraisal.Api.Tests.Branches;

[Collection("ApiTests")]
public sealed class BranchEndpointsTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;
    public BranchEndpointsTests(ApiFactory f) => _factory = f;

    // ── GET /api/branches/cities ──────────────────────────────────────────────

    [Fact]
    public async Task GetCities_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient().GetAsync("/api/branches/cities");
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task GetCities_Authenticated_Returns200WithArray()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am").GetAsync("/api/branches/cities");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
        var body = await r.Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal(JsonValueKind.Array, body.ValueKind);
    }

    [Fact]
    public async Task GetCities_NoPermTokenButAuthenticated_Returns200()
    {
        // BranchEndpoints koristi samo RequireAuthorization() bez policy-a
        // — svaki autenticirani korisnik smije pristupiti
        var r = await _factory.CreateAuthenticatedClient("test-noperm").GetAsync("/api/branches/cities");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    // ── GET /api/branches — lista poslovnica ──────────────────────────────────

    [Fact]
    public async Task GetBranches_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient().GetAsync("/api/branches");
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task GetBranches_Authenticated_Returns200()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am").GetAsync("/api/branches");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
        var body = await r.Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal(JsonValueKind.Array, body.ValueKind);
    }

    [Fact]
    public async Task GetBranches_WithCityFilter_Returns200()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am")
            .GetAsync("/api/branches?city=Sarajevo");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    // ── GET /api/branches/{id} ────────────────────────────────────────────────

    [Fact]
    public async Task GetBranchById_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient().GetAsync("/api/branches/1");
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task GetBranchById_NotFound_Returns404()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am").GetAsync("/api/branches/99999");
        Assert.Equal(HttpStatusCode.NotFound, r.StatusCode);
    }
}
