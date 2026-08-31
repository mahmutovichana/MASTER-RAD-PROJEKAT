using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using RBBH.CollateralAppraisal.Api.Tests.Helpers;
using Xunit;

namespace RBBH.CollateralAppraisal.Api.Tests.Security;

/// <summary>
/// Testovi koji verificiraju da svaki endpoint ispravno primjenjuje autorizaciju.
/// Scenariji: bez tokena → 401, pogrešne permissije → 403, ispravan token → ne-4xx.
/// </summary>
[Collection("ApiTests")]
public sealed class AuthorizationTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;

    private static readonly object MinimalOrderPayload = new
    {
        clientName           = "Test Klijent",
        clientType           = "FL",
        clientIdentifier     = "0101985771007",
        collateralTypeId     = 1,
        city                 = "Sarajevo",
        propertyAddress      = "Test adresa 1",
        branch               = "POS_SARAJEVO_CENTAR",
        branchAddress        = "Maršala Tita 1",
        contactName          = "Test Klijent",
        contactPhone         = "061-000-001",
        contactEmail         = "test@test.ba",
        deliveryContactName  = "Test Klijent",
        amRecipientName      = "Haris H",
        requestReceivedAt    = "2026-01-15T10:00:00Z"
    };

    public AuthorizationTests(ApiFactory factory) => _factory = factory;

    // ── Anonimni pristup ──────────────────────────────────────────────────────────

    [Fact]
    public async Task GetOrders_NoToken_Returns401()
    {
        var client = _factory.CreateAnonymousClient();

        var response = await client.GetAsync("/api/orders");

        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task CreateOrder_NoToken_Returns401()
    {
        var client = _factory.CreateAnonymousClient();

        var response = await client.PostAsJsonAsync("/api/orders", MinimalOrderPayload);

        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task GetOrderById_NoToken_Returns401()
    {
        var client = _factory.CreateAnonymousClient();

        var response = await client.GetAsync("/api/orders/1");

        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task DeleteOrder_NoToken_Returns401()
    {
        var client = _factory.CreateAnonymousClient();

        var response = await client.DeleteAsync("/api/orders/1");

        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task SubmitOrder_NoToken_Returns401()
    {
        var client = _factory.CreateAnonymousClient();

        var response = await client.PostAsync("/api/orders/1/submit", null);

        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    // ── Korisnik bez permissija → 403 ─────────────────────────────────────────────

    [Fact]
    public async Task GetOrders_NoPermissions_Returns403()
    {
        // "test-noperm" token → autentificiran ali bez permissions
        var client = _factory.CreateAuthenticatedClient("test-noperm");

        var response = await client.GetAsync("/api/orders");

        Assert.Equal(HttpStatusCode.Forbidden, response.StatusCode);
    }

    [Fact]
    public async Task CreateOrder_NoPermissions_Returns403()
    {
        var client = _factory.CreateAuthenticatedClient("test-noperm");

        var response = await client.PostAsJsonAsync("/api/orders", MinimalOrderPayload);

        Assert.Equal(HttpStatusCode.Forbidden, response.StatusCode);
    }

    // ── Health endpoint je anoniman ────────────────────────────────────────────────

    [Theory]
    [InlineData("/health")]
    [InlineData("/health/ready")]
    [InlineData("/health/live")]
    public async Task HealthEndpoints_NoToken_Returns200(string path)
    {
        var client = _factory.CreateAnonymousClient();

        var response = await client.GetAsync(path);

        // 200 OK ili 503 ako neki health check ne prođe — ali nikad 401/403
        Assert.NotEqual(HttpStatusCode.Unauthorized, response.StatusCode);
        Assert.NotEqual(HttpStatusCode.Forbidden,    response.StatusCode);
    }

    // ── AM permissioni → može kreirati narudžbu ────────────────────────────────────

    [Fact]
    public async Task CreateOrder_WithAmToken_Returns201()
    {
        // "test-am" ima orders.create, orders.submit itd.
        var client = _factory.CreateAuthenticatedClient("test-am");

        var response = await client.PostAsJsonAsync("/api/orders", MinimalOrderPayload);

        // AM može kreirati narudžbu
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
    }

    [Fact]
    public async Task GetOrders_WithAmToken_Returns200()
    {
        var client = _factory.CreateAuthenticatedClient("test-am");

        var response = await client.GetAsync("/api/orders");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    // ── Pogrešan format tokena ─────────────────────────────────────────────────────

    [Fact]
    public async Task GetOrders_InvalidTokenFormat_Returns401()
    {
        // Token koji ne počinje sa "Bearer test-" — handler vraća NoResult(), a
        // platforma vraća 401 jer nije pronađen nijedan uspješan handler.
        var client = _factory.CreateAnonymousClient();
        client.DefaultRequestHeaders.Add("Authorization", "Bearer invalid-jwt-token");

        var response = await client.GetAsync("/api/orders");

        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }
}
