using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using RBBH.CollateralAppraisal.Api.Tests.Helpers;
using Xunit;

namespace RBBH.CollateralAppraisal.Api.Tests.Codebooks;

[Collection("ApiTests")]
public sealed class CodebookEndpointsTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;
    private const string BaseUrl = "/api/codebooks/tipovi_kolaterala/values";

    public CodebookEndpointsTests(ApiFactory f) => _factory = f;

    // ── Authorization: active values (CodebooksView) ──────────────────────────

    [Fact]
    public async Task GetActiveValues_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient().GetAsync($"{BaseUrl}/active");
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task GetActiveValues_NoPermission_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-noperm").GetAsync($"{BaseUrl}/active");
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task GetActiveValues_WithPermission_Returns200()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am").GetAsync($"{BaseUrl}/active");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
        var body = await r.Content.ReadFromJsonAsync<JsonElement>();
        Assert.True(body.ValueKind == JsonValueKind.Array);
    }

    // ── Admin list (CodebooksManage) ──────────────────────────────────────────

    [Fact]
    public async Task GetAllValues_AM_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am").GetAsync(BaseUrl);
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task GetAllValues_Admin_Returns200()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin").GetAsync(BaseUrl);
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    // ── Create value ──────────────────────────────────────────────────────────

    [Fact]
    public async Task CreateValue_AM_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am")
            .PostAsJsonAsync(BaseUrl, new { code = "TEST", label = "Test", sortOrder = 99 });
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task CreateValue_Admin_Returns201()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .PostAsJsonAsync(BaseUrl, new { code = "NOVA_OPCIJA", label = "Nova opcija", sortOrder = 50 });
        Assert.Equal(HttpStatusCode.Created, r.StatusCode);
    }

    [Fact]
    public async Task CreateValue_DuplicateCode_Returns409()
    {
        var client = _factory.CreateAuthenticatedClient("test-admin");
        var body = new { code = "DUPLIKAT_TEST", label = "Duplikat", sortOrder = 1 };

        await client.PostAsJsonAsync(BaseUrl, body); // first
        var r = await client.PostAsJsonAsync(BaseUrl, body); // duplicate
        Assert.Equal(HttpStatusCode.Conflict, r.StatusCode);
    }

    // ── Get by ID ─────────────────────────────────────────────────────────────

    [Fact]
    public async Task GetById_Admin_Returns200()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin").GetAsync($"{BaseUrl}/1");
        // ID 1 is the seeded CollateralType value
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    [Fact]
    public async Task GetById_NotFound_Returns404()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin").GetAsync($"{BaseUrl}/99999");
        Assert.Equal(HttpStatusCode.NotFound, r.StatusCode);
    }

    // ── Update ────────────────────────────────────────────────────────────────

    [Fact]
    public async Task UpdateValue_Admin_Returns200()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .PutAsJsonAsync($"{BaseUrl}/1", new { label = "Ažuriran naziv", sortOrder = 1 });
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    [Fact]
    public async Task UpdateValue_AM_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am")
            .PutAsJsonAsync($"{BaseUrl}/1", new { label = "Pokušaj AM", sortOrder = 1 });
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    // ── Deactivate / Activate ─────────────────────────────────────────────────

    [Fact]
    public async Task DeactivateValue_Admin_Returns200()
    {
        // Create a new value to deactivate (don't deactivate the seeded one — other tests use it)
        var client = _factory.CreateAuthenticatedClient("test-admin");
        var created = await client.PostAsJsonAsync(BaseUrl,
            new { code = "ZA_DEACTIVATE", label = "Za deaktivaciju", sortOrder = 99 });
        var body = await created.Content.ReadFromJsonAsync<JsonElement>();
        var id = body.GetProperty("id").GetInt32();

        var r = await client.PostAsJsonAsync($"{BaseUrl}/{id}/deactivate", new { });
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    [Fact]
    public async Task ActivateValue_Admin_Returns200()
    {
        var client = _factory.CreateAuthenticatedClient("test-admin");
        var created = await client.PostAsJsonAsync(BaseUrl,
            new { code = "ZA_ACTIVATE", label = "Za aktivaciju", sortOrder = 98 });
        var body = await created.Content.ReadFromJsonAsync<JsonElement>();
        var id = body.GetProperty("id").GetInt32();

        await client.PostAsJsonAsync($"{BaseUrl}/{id}/deactivate", new { });
        var r = await client.PostAsJsonAsync($"{BaseUrl}/{id}/activate", new { });
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    // ── Usage check ───────────────────────────────────────────────────────────

    [Fact]
    public async Task GetUsage_Admin_Returns200()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin").GetAsync($"{BaseUrl}/1/usage");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }
}
