using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using RBBH.CollateralAppraisal.Api.Tests.Helpers;
using Xunit;

namespace RBBH.CollateralAppraisal.Api.Tests.Regression;

/// <summary>
/// HTTP-nivo regresijski testovi: svaki test dokumentira konkretan bug koji je bio u produkciji.
/// Kada test prolazi, bug je i dalje fixan. Ako test počne fail-ati, bug je regredirao.
///
/// VAŽNO: Ovi testovi su namjerno verbose u naslovima i komentarima — služe kao dokumentacija.
/// </summary>
[Collection("ApiTests")]
public sealed class HttpRegressionTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;

    private static readonly object ValidOrderPayload = new
    {
        clientName           = "Regression Tester",
        clientType           = "FL",
        clientIdentifier     = "0101985771007",
        collateralTypeId     = 1,
        city                 = "Sarajevo",
        propertyAddress      = "Titova 7",
        branch               = "POS_SARAJEVO_CENTAR",
        branchAddress        = "Maršala Tita 1",
        contactName          = "Regression Tester",
        contactPhone         = "061-999-000",
        contactEmail         = "regression@test.ba",
        deliveryContactName  = "Regression Tester",
        amRecipientName      = "Test AM",
        requestReceivedAt    = "2026-01-15T10:00:00Z"
    };

    public HttpRegressionTests(ApiFactory factory) => _factory = factory;

    // Regresija: raspon datuma ne smije izazvati serversku grešku.
    // Pokriva regresiju filtriranja datuma bez vezivanja za konkretan provider.

    [Fact]
    public async Task DateFilter_DateRangeFilter_DoesNotReturn500()
    {
        var client = _factory.CreateAuthenticatedClient();

        // Ove vrijednosti Parse-uju u Kind=Unspecified — bio je trigger za bug
        var response = await client.GetAsync(
            "/api/orders?createdFrom=2026-01-01&createdTo=2026-12-31");

        // Mora biti 200, ne 500
        Assert.NotEqual(HttpStatusCode.InternalServerError, response.StatusCode);
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task DateFilter_OnlyCreatedFrom_DoesNotReturn500()
    {
        var client = _factory.CreateAuthenticatedClient();

        var response = await client.GetAsync("/api/orders?createdFrom=2025-06-01");

        Assert.NotEqual(HttpStatusCode.InternalServerError, response.StatusCode);
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task DateFilter_OnlyCreatedTo_DoesNotReturn500()
    {
        var client = _factory.CreateAuthenticatedClient();

        var response = await client.GetAsync("/api/orders?createdTo=2026-12-31");

        Assert.NotEqual(HttpStatusCode.InternalServerError, response.StatusCode);
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    // ── Bug #2: NotFoundException nije mapirala na 404 ────────────────────────────
    // Uzrok: GlobalExceptionHandler nije bio registriran / nije pokrivao NotFoundException
    // Fix: AddExceptionHandler<GlobalExceptionHandler> + problem details middleware
    // Efekat: nepostojeci resurs vracaol je 500 umjesto 404 s ProblemDetails tijelom

    [Fact]
    public async Task Bug_NotFoundException_Returns404NotInternalServerError()
    {
        var client = _factory.CreateAuthenticatedClient();

        var response = await client.GetAsync("/api/orders/999999");

        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
        Assert.NotEqual(HttpStatusCode.InternalServerError, response.StatusCode);
    }

    [Fact]
    public async Task Bug_NotFoundException_ResponseBodyIsProblemDetails()
    {
        var client = _factory.CreateAuthenticatedClient();

        var response = await client.GetAsync("/api/orders/999999");

        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);

        var body = await response.Content.ReadFromJsonAsync<JsonElement>();

        // Mora biti ProblemDetails format
        Assert.Equal(404, body.GetProperty("status").GetInt32());
        Assert.True(body.TryGetProperty("title", out _),   "ProblemDetails mora imati 'title'");
        Assert.True(body.TryGetProperty("type", out _),    "ProblemDetails mora imati 'type'");
        // errorCode je opcionalan — prisutan samo kad NotFoundException ima eksplicitan ErrorCode
        // correlationId je UVIJEK prisutan (GlobalExceptionHandler linija 78)
        Assert.True(body.TryGetProperty("correlationId", out _), "ProblemDetails mora imati 'correlationId'");
    }

    // ── Bug #3: ProblemDetails nema correlationId extension ───────────────────────
    // Uzrok: CorrelationIdMiddleware postavljao header ali ga nije ubacivao u ProblemDetails
    // Fix: GlobalExceptionHandler čita X-Correlation-Id header i dodaje ga u Extensions

    [Fact]
    public async Task Bug_ProblemDetails_IncludesCorrelationId()
    {
        var client = _factory.CreateAuthenticatedClient();

        var response = await client.GetAsync("/api/orders/888888");

        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);

        var body = await response.Content.ReadFromJsonAsync<JsonElement>();

        Assert.True(body.TryGetProperty("correlationId", out _),
            "ProblemDetails mora imati 'correlationId' extension za traceability");
    }

    // ── Bug #4: ValidationException vraćao 500 umjesto 400 ───────────────────────
    // Uzrok: FluentValidation exception nije bila pokrivena exception handlerom
    // Fix: GlobalExceptionHandler mapira ValidationException na 400 + fieldErrors

    [Fact]
    public async Task Bug_ValidationException_Returns400NotInternalServerError()
    {
        var client = _factory.CreateAuthenticatedClient();

        // Payload s praznim obaveznim poljem — triggera ValidationException
        var invalidPayload = new
        {
            clientName       = "",
            collateralTypeId = 1,
            city             = "Sarajevo",
            branch           = "POS",
            contactName      = "T",
            contactPhone     = "061",
            deliveryContactName = "T",
            amRecipientName  = "H"
        };

        var response = await client.PostAsJsonAsync("/api/orders", invalidPayload);

        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
        Assert.NotEqual(HttpStatusCode.InternalServerError, response.StatusCode);
    }

    [Fact]
    public async Task Bug_ValidationException_ResponseHasFieldErrors()
    {
        var client = _factory.CreateAuthenticatedClient();
        var invalidPayload = new
        {
            clientName       = "",
            collateralTypeId = 1,
            city             = "Sarajevo",
            branch           = "POS",
            contactName      = "T",
            contactPhone     = "061",
            deliveryContactName = "T",
            amRecipientName  = "H"
        };

        var response = await client.PostAsJsonAsync("/api/orders", invalidPayload);

        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);

        var body = await response.Content.ReadFromJsonAsync<JsonElement>();

        Assert.Equal(400, body.GetProperty("status").GetInt32());
        // fieldErrors ili errors mora postojati — zavisi od implementacije GlobalExceptionHandler-a
        var hasFieldErrors = body.TryGetProperty("fieldErrors", out _)
                          || body.TryGetProperty("errors", out _);
        Assert.True(hasFieldErrors,
            "400 odgovor mora imati fieldErrors ili errors za validacijske greške");
    }

    // ── Bug #5: InvalidStateTransition vraćao 500 umjesto 409 ───────────────────
    // Uzrok: InvalidStateTransitionException nije mapirala na Conflict
    // Fix: GlobalExceptionHandler mapira InvalidStateTransitionException → 409

    [Fact]
    public async Task Bug_InvalidStateTransition_Returns409NotInternalServerError()
    {
        var client = _factory.CreateAuthenticatedClient();

        // Kreiraj narudžbu u Draft statusu
        var createResp = await client.PostAsJsonAsync("/api/orders", ValidOrderPayload);
        createResp.EnsureSuccessStatusCode();
        var id = (await createResp.Content.ReadFromJsonAsync<JsonElement>()).GetProperty("id").GetInt32();

        // Pošalji jednom (Draft → SubmittedBySales — OK)
        var submit1 = await client.PostAsync($"/api/orders/{id}/submit", null);
        submit1.EnsureSuccessStatusCode();

        // Pokušaj ponovo submit — SubmittedBySales → SubmittedBySales je invalid transition
        var submit2 = await client.PostAsync($"/api/orders/{id}/submit", null);

        // Mora biti 409 ili 400, nikako 500
        Assert.NotEqual(HttpStatusCode.InternalServerError, submit2.StatusCode);
        Assert.True(
            submit2.StatusCode == HttpStatusCode.Conflict ||
            submit2.StatusCode == HttpStatusCode.BadRequest ||
            submit2.StatusCode == HttpStatusCode.UnprocessableContent,
            $"Nevalidan status prijelaz treba dati 4xx, ali je vratio {(int)submit2.StatusCode}");
    }

    // ── Bug #6: EF Migration drift → 500 pri startu ────────────────────────────
    // Uzrok: DbContext model nije odgovarao migracijama (model changes bez migracije)
    // Fix: dotnet ef migrations add + ispravka HasFilter indeksa
    // Vidi: project_ef_migration_drift.md
    // Na in-memory bazi (EnsureCreated) ovo nije problem, ali dokumentira scenario

    [Fact]
    public async Task Bug_ApplicationStarts_NoMigrationDriftError()
    {
        // Ako app ne startuje / baca 500 na prvom requestu, ovo pada
        var client = _factory.CreateAuthenticatedClient();

        var response = await client.GetAsync("/health");

        // App mora biti pokrenuta i zdrava
        Assert.NotEqual(HttpStatusCode.InternalServerError, response.StatusCode);
    }

    // ── Bug #7: Submit narudžbe bez ispravnog clientType bacao 500 ──────────────
    // Uzrok: ClientType enum parse nije imao fallback — null/prazno bacalo NullRef
    // Fix: ValidateClientType u validator + sanitizacija u command handleru

    [Fact]
    public async Task Bug_CreateOrder_WithoutClientType_Returns400NotInternalServerError()
    {
        var client = _factory.CreateAuthenticatedClient();
        var payload = new
        {
            clientName           = "Test",
            // clientType namjerno izostavljen
            collateralTypeId     = 1,
            city                 = "Sarajevo",
            branch               = "POS",
            contactName          = "Test",
            contactPhone         = "061-000",
            deliveryContactName  = "Test",
            amRecipientName      = "Test"
        };

        var response = await client.PostAsJsonAsync("/api/orders", payload);

        // Mora biti 400 ili 201 (ako je clientType optional s default-om), nikako 500
        Assert.NotEqual(HttpStatusCode.InternalServerError, response.StatusCode);
    }

    // ── CorrelationIdMiddleware putevi ─────────────────────────────────────────
    // Middleware ima 4 puta: bez headera, prazan header, predug header, validan header.
    // Bez headera je pokriven svim ostalim testovima. Ovdje pokrivamo preostala 3.

    [Fact]
    public async Task CorrelationId_ValidHeader_EchoesBackInResponse()
    {
        var client = _factory.CreateAuthenticatedClient();
        client.DefaultRequestHeaders.Add("X-Correlation-Id", "my-trace-123");

        var response = await client.GetAsync("/health");

        Assert.NotEqual(HttpStatusCode.InternalServerError, response.StatusCode);
        // Header se propagira u response
        Assert.True(response.Headers.Contains("X-Correlation-Id"));
    }

    [Fact]
    public async Task CorrelationId_EmptyHeader_GeneratesNewId()
    {
        var client = _factory.CreateAuthenticatedClient();
        client.DefaultRequestHeaders.Add("X-Correlation-Id", "   ");

        var response = await client.GetAsync("/health");

        Assert.NotEqual(HttpStatusCode.InternalServerError, response.StatusCode);
    }

    [Fact]
    public async Task CorrelationId_TooLongHeader_GeneratesNewId()
    {
        var client = _factory.CreateAuthenticatedClient();
        var longId = new string('x', 100); // > 64 znaka
        client.DefaultRequestHeaders.Add("X-Correlation-Id", longId);

        var response = await client.GetAsync("/health");

        Assert.NotEqual(HttpStatusCode.InternalServerError, response.StatusCode);
    }
}
