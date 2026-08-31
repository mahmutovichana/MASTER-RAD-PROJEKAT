using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using RBBH.CollateralAppraisal.Api.Tests.Helpers;
using Xunit;

namespace RBBH.CollateralAppraisal.Api.Tests.Appraisers;

[Collection("ApiTests")]
public sealed class AppraiserEndpointsTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;
    public AppraiserEndpointsTests(ApiFactory f) => _factory = f;

    // ── GET /api/appraisers ───────────────────────────────────────────────────

    [Fact]
    public async Task ListAppraisers_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient().GetAsync("/api/appraisers");
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task ListAppraisers_AM_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am").GetAsync("/api/appraisers");
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task ListAppraisers_Admin_Returns200WithPagedResult()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin").GetAsync("/api/appraisers");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
        var body = await r.Content.ReadFromJsonAsync<JsonElement>();
        // AppraiserService.GetListAsync vraća PagedResult (Object sa items[])
        Assert.True(body.TryGetProperty("items", out var items) &&
                    items.ValueKind == JsonValueKind.Array);
    }

    [Fact]
    public async Task ListAppraisers_WithFilters_Returns200()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .GetAsync("/api/appraisers?city=Sarajevo&active=true&page=1&pageSize=5");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    // ── POST /api/appraisers ──────────────────────────────────────────────────

    [Fact]
    public async Task CreateAppraiser_AM_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am")
            .PostAsJsonAsync("/api/appraisers", new
            {
                name = "Test Vještak", city = "Sarajevo", legalForm = "Individual",
                contactEmail = "v@test.ba", contactPhone = "061123456"
            });
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task CreateAppraiser_Admin_Returns201()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .PostAsJsonAsync("/api/appraisers", new
            {
                name = "Test Vještak API", city = "Sarajevo", legalForm = "Individual",
                contactEmail = "v@test.ba", contactPhone = "061123456", clientScope = "Sve"
            });
        Assert.Equal(HttpStatusCode.Created, r.StatusCode);
    }

    // ── GET /api/appraisers/{id} ──────────────────────────────────────────────

    [Fact]
    public async Task GetAppraiser_NotFound_Returns404()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin").GetAsync("/api/appraisers/99999");
        Assert.Equal(HttpStatusCode.NotFound, r.StatusCode);
    }

    [Fact]
    public async Task GetAppraiser_ExistingId_Returns200()
    {
        // Kreiraj vještaka pa dohvati
        var client = _factory.CreateAuthenticatedClient("test-admin");
        var created = await client.PostAsJsonAsync("/api/appraisers", new
        {
            name = "Vještak Za Get", city = "Tuzla", legalForm = "Individual",
            contactEmail = "get@test.ba", contactPhone = "062000000", clientScope = "Sve"
        });
        var body = await created.Content.ReadFromJsonAsync<JsonElement>();
        var id = body.GetProperty("id").GetInt32();

        var r = await client.GetAsync($"/api/appraisers/{id}");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    // ── PUT /api/appraisers/{id} ──────────────────────────────────────────────

    [Fact]
    public async Task UpdateAppraiser_Admin_Returns200()
    {
        var client = _factory.CreateAuthenticatedClient("test-admin");
        var created = await client.PostAsJsonAsync("/api/appraisers", new
        {
            name = "Vještak Za Update", city = "Mostar", legalForm = "Individual",
            contactEmail = "upd@test.ba", contactPhone = "063000000", clientScope = "Sve"
        });
        var body = await created.Content.ReadFromJsonAsync<JsonElement>();
        var id = body.GetProperty("id").GetInt32();

        var r = await client.PutAsJsonAsync($"/api/appraisers/{id}", new
        {
            name = "Ažurirani Vještak", city = "Mostar", legalForm = "Individual",
            contactEmail = "upd@test.ba", contactPhone = "063000001", clientScope = "Sve"
        });
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    // ── POST /api/appraisers/{id}/on-leave ────────────────────────────────────

    [Fact]
    public async Task SetOnLeave_Admin_Returns200()
    {
        var client = _factory.CreateAuthenticatedClient("test-admin");
        var created = await client.PostAsJsonAsync("/api/appraisers", new
        {
            name = "Vještak Na Odmor", city = "Zenica", legalForm = "Individual",
            contactEmail = "leave@test.ba", contactPhone = "064000000", clientScope = "Sve"
        });
        var body = await created.Content.ReadFromJsonAsync<JsonElement>();
        var id = body.GetProperty("id").GetInt32();

        var r = await client.PostAsJsonAsync($"/api/appraisers/{id}/on-leave", new { value = true });
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    // ── POST /api/appraisers/{id}/blacklist ───────────────────────────────────

    [Fact]
    public async Task SetBlacklisted_Admin_Returns200()
    {
        var client = _factory.CreateAuthenticatedClient("test-admin");
        var created = await client.PostAsJsonAsync("/api/appraisers", new
        {
            name = "Vještak Blacklist", city = "Bijeljina", legalForm = "Individual",
            contactEmail = "bl@test.ba", contactPhone = "065000000", clientScope = "Sve"
        });
        var body = await created.Content.ReadFromJsonAsync<JsonElement>();
        var id = body.GetProperty("id").GetInt32();

        var r = await client.PostAsJsonAsync($"/api/appraisers/{id}/blacklist", new { value = true });
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    // ── DELETE /api/appraisers/{id} (deactivate) ─────────────────────────────

    [Fact]
    public async Task DeactivateAppraiser_Admin_Returns204()
    {
        var client = _factory.CreateAuthenticatedClient("test-admin");
        var created = await client.PostAsJsonAsync("/api/appraisers", new
        {
            name = "Vještak Za Deactivate", city = "Trebinje", legalForm = "Individual",
            contactEmail = "deact@test.ba", contactPhone = "066000000", clientScope = "Sve"
        });
        var body = await created.Content.ReadFromJsonAsync<JsonElement>();
        var id = body.GetProperty("id").GetInt32();

        var r = await client.DeleteAsync($"/api/appraisers/{id}");
        Assert.Equal(HttpStatusCode.NoContent, r.StatusCode);
    }

    // ── GET /api/orders/{orderId}/appraiser-candidates ────────────────────────

    [Fact]
    public async Task GetCandidates_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient()
            .GetAsync("/api/orders/1/appraiser-candidates");
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task GetCandidates_AM_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am")
            .GetAsync("/api/orders/1/appraiser-candidates");
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task GetCandidates_Admin_NonExistentOrder_Returns404()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .GetAsync("/api/orders/99999/appraiser-candidates");
        Assert.Equal(HttpStatusCode.NotFound, r.StatusCode);
    }

    // ── POST /api/orders/{orderId}/send-to-appraiser ──────────────────────────

    [Fact]
    public async Task SendToAppraiser_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient()
            .PostAsJsonAsync("/api/orders/1/send-to-appraiser", new { });
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task SendToAppraiser_AM_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am")
            .PostAsJsonAsync("/api/orders/1/send-to-appraiser", new { });
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task SendToAppraiser_Admin_NonExistentOrder_Returns404()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .PostAsJsonAsync("/api/orders/99999/send-to-appraiser", new { });
        Assert.Equal(HttpStatusCode.NotFound, r.StatusCode);
    }

    // ── POST /api/orders/{orderId}/accept-by-appraiser ────────────────────────

    [Fact]
    public async Task AcceptByAppraiser_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient()
            .PostAsJsonAsync("/api/orders/1/accept-by-appraiser", new { });
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task AcceptByAppraiser_NonExistentOrder_Returns404()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .PostAsJsonAsync("/api/orders/99999/accept-by-appraiser", new { });
        Assert.Equal(HttpStatusCode.NotFound, r.StatusCode);
    }

    // ── POST /api/orders/{orderId}/reject-by-appraiser ───────────────────────

    [Fact]
    public async Task RejectByAppraiser_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient()
            .PostAsJsonAsync("/api/orders/1/reject-by-appraiser",
                new { reason = 1, comment = (string?)null });
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task RejectByAppraiser_NonExistentOrder_Returns404()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .PostAsJsonAsync("/api/orders/99999/reject-by-appraiser",
                new { reason = 1, comment = (string?)null });
        Assert.Equal(HttpStatusCode.NotFound, r.StatusCode);
    }
}
