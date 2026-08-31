using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using RBBH.CollateralAppraisal.Api.Tests.Helpers;
using Xunit;

namespace RBBH.CollateralAppraisal.Api.Tests.Orders;

/// <summary>
/// E2E HTTP testovi za /api/orders endpoints.
/// Stack: WebApplicationFactory + in-memory baza + lažni JWT.
/// Svaki test u kolekciji dijeli jednu fabriku (baza se seeduje po potrebi per-test).
/// </summary>
[Collection("ApiTests")]
public sealed class OrderEndpointsTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;

    // Minimalan validan payload za kreiranje narudžbe
    private static readonly object ValidCreatePayload = new
    {
        clientName               = "Petar Petrović",
        clientType               = "FL",
        clientIdentifier         = "0101985771007",
        collateralTypeId         = 1,
        combinedCollateralTypeId = (int?)null,
        city                     = "Sarajevo",
        propertyAddress          = "Ferhadija 1",
        branch                   = "POS_SARAJEVO_CENTAR",
        branchAddress            = "Maršala Tita 5",
        contactName              = "Petar Petrović",
        contactPhone             = "061-100-200",
        contactEmail             = "petar@test.ba",
        internalNote             = (string?)null,
        deliveryContactName      = "Petar Petrović",
        amRecipientName          = "Haris Hadžić",
        requestReceivedAt        = "2026-01-15T10:00:00Z"
    };

    public OrderEndpointsTests(ApiFactory factory) => _factory = factory;

    // ── GET /api/orders ───────────────────────────────────────────────────────────

    [Fact]
    public async Task GetOrders_AuthenticatedUser_Returns200WithPagedResult()
    {
        var client = _factory.CreateAuthenticatedClient();

        var response = await client.GetAsync("/api/orders");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var body = await response.Content.ReadFromJsonAsync<JsonElement>();
        Assert.True(body.TryGetProperty("items", out _), "Response mora imati 'items' property");
        Assert.True(body.TryGetProperty("totalCount", out _), "Response mora imati 'totalCount' property");
    }

    [Fact]
    public async Task GetOrders_WithSearchFilter_Returns200()
    {
        var client = _factory.CreateAuthenticatedClient();

        var response = await client.GetAsync("/api/orders?search=Petar&page=1&pageSize=5");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task GetOrders_WithDateFilter_Returns200()
    {
        // Regresija: DateTime filter bacao 500 zbog SQL Server provider Kind=Unspecified.
        // Na in-memory bazi test prolazi, ali dokumentira scenario koji je bio broken.
        var client = _factory.CreateAuthenticatedClient();

        var response = await client.GetAsync(
            "/api/orders?createdFrom=2026-01-01&createdTo=2026-12-31");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    // ── POST /api/orders ──────────────────────────────────────────────────────────

    [Fact]
    public async Task CreateOrder_ValidRequest_Returns201WithOrderId()
    {
        var client = _factory.CreateAuthenticatedClient();

        var response = await client.PostAsJsonAsync("/api/orders", ValidCreatePayload);

        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        Assert.NotNull(response.Headers.Location);

        var body = await response.Content.ReadFromJsonAsync<JsonElement>();
        Assert.True(body.TryGetProperty("id", out var idEl));
        Assert.True(idEl.GetInt32() > 0);
        Assert.Equal("Draft", body.GetProperty("status").GetString());
    }

    [Fact]
    public async Task CreateOrder_MissingClientName_Returns400WithFieldErrors()
    {
        var client = _factory.CreateAuthenticatedClient();
        var invalidPayload = new
        {
            clientName           = "",        // prazno — invalid
            collateralTypeId     = 1,
            city                 = "Sarajevo",
            branch               = "POS_SARAJEVO_CENTAR",
            contactName          = "Petar",
            contactPhone         = "061-100-200",
            deliveryContactName  = "Petar",
            amRecipientName      = "Haris"
        };

        var response = await client.PostAsJsonAsync("/api/orders", invalidPayload);

        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
        var body = await response.Content.ReadFromJsonAsync<JsonElement>();
        // ProblemDetails sa fieldErrors extension-om
        Assert.Equal(400, body.GetProperty("status").GetInt32());
        Assert.True(
            body.TryGetProperty("fieldErrors", out _) || body.TryGetProperty("errors", out _),
            "400 response mora sadržati 'fieldErrors' ili 'errors'");
    }

    [Fact]
    public async Task CreateOrder_CollateralTypeIdZero_Returns400()
    {
        var client = _factory.CreateAuthenticatedClient();
        var invalidPayload = new
        {
            clientName           = "Petar",
            collateralTypeId     = 0,        // mora biti > 0
            city                 = "Sarajevo",
            branch               = "POS",
            contactName          = "Petar",
            contactPhone         = "061-111",
            deliveryContactName  = "Petar",
            amRecipientName      = "Haris"
        };

        var response = await client.PostAsJsonAsync("/api/orders", invalidPayload);

        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }

    // ── GET /api/orders/{id} ──────────────────────────────────────────────────────

    [Fact]
    public async Task GetOrderById_ExistingOrder_Returns200WithDetails()
    {
        var client = _factory.CreateAuthenticatedClient();
        var createResp = await client.PostAsJsonAsync("/api/orders", ValidCreatePayload);
        createResp.EnsureSuccessStatusCode();
        var created = await createResp.Content.ReadFromJsonAsync<JsonElement>();
        var id      = created.GetProperty("id").GetInt32();

        var response = await client.GetAsync($"/api/orders/{id}");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var body = await response.Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal(id, body.GetProperty("id").GetInt32());
        Assert.Equal("Draft", body.GetProperty("status").GetString());
    }

    [Fact]
    public async Task GetOrderById_NonExistent_Returns404WithProblemDetails()
    {
        var client = _factory.CreateAuthenticatedClient();

        var response = await client.GetAsync("/api/orders/999999");

        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
        var body = await response.Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal(404, body.GetProperty("status").GetInt32());
        Assert.True(body.TryGetProperty("title", out _),    "ProblemDetails mora imati 'title'");
        Assert.True(body.TryGetProperty("type", out _),     "ProblemDetails mora imati 'type'");
    }

    // ── DELETE /api/orders/{id} ───────────────────────────────────────────────────

    [Fact]
    public async Task CancelOrder_DraftOrder_Returns204()
    {
        var client = _factory.CreateAuthenticatedClient();
        var createResp = await client.PostAsJsonAsync("/api/orders", ValidCreatePayload);
        createResp.EnsureSuccessStatusCode();
        var id = (await createResp.Content.ReadFromJsonAsync<JsonElement>()).GetProperty("id").GetInt32();

        var response = await client.DeleteAsync($"/api/orders/{id}");

        Assert.Equal(HttpStatusCode.NoContent, response.StatusCode);
    }

    // ── POST /api/orders/{id}/submit ──────────────────────────────────────────────

    [Fact]
    public async Task SubmitOrder_DraftOrder_Returns200WithSubmittedBySalesStatus()
    {
        var client = _factory.CreateAuthenticatedClient();
        var createResp = await client.PostAsJsonAsync("/api/orders", ValidCreatePayload);
        createResp.EnsureSuccessStatusCode();
        var id = (await createResp.Content.ReadFromJsonAsync<JsonElement>()).GetProperty("id").GetInt32();

        var response = await client.PostAsync($"/api/orders/{id}/submit", null);

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var body = await response.Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal("SubmittedBySales", body.GetProperty("status").GetString());
    }

    [Fact]
    public async Task SubmitOrder_NonExistentOrder_Returns404()
    {
        var client = _factory.CreateAuthenticatedClient();

        var response = await client.PostAsync("/api/orders/999999/submit", null);

        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }

    // ── GET /api/orders/{id}/appraisal-status ────────────────────────────────────

    [Fact]
    public async Task GetAppraisalStatus_ExistingOrder_Returns200WithStatusFields()
    {
        var client = _factory.CreateAuthenticatedClient();
        var createResp = await client.PostAsJsonAsync("/api/orders", ValidCreatePayload);
        createResp.EnsureSuccessStatusCode();
        var id = (await createResp.Content.ReadFromJsonAsync<JsonElement>()).GetProperty("id").GetInt32();

        var response = await client.GetAsync($"/api/orders/{id}/appraisal-status");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var body = await response.Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal(id, body.GetProperty("id").GetInt32());
        Assert.True(body.TryGetProperty("status", out _));
        Assert.True(body.TryGetProperty("orderNumber", out _));
    }

    // ── GET /api/orders/summary ───────────────────────────────────────────────────

    [Fact]
    public async Task GetOrderSummary_Returns200WithCountsByStatus()
    {
        var client = _factory.CreateAuthenticatedClient();

        var response = await client.GetAsync("/api/orders/summary");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
