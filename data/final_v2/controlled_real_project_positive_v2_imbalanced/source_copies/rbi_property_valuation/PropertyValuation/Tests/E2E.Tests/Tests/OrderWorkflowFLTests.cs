using Microsoft.Playwright;
using RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;
using Xunit;

namespace RBBH.CollateralAppraisal.E2E.Tests.Tests;

/// <summary>
/// E2E test koji pokriva KOMPLETAN tok narudžbe za FIZIČKA LICA (FL).
///
/// Scenario: Stan (APP_STAN) — bez provjere pristupa CO-a.
///
/// Tok statusa:
///   Draft → SubmittedBySales → AcceptedByCA → DocumentationReviewInProgress
///   → DocumentationApproved → AppraiserSelected → OrderSentToAppraiser
///   → AppraisalInProgress → AppraisalReceived → ReadyForProcedure
///
/// Učesnici: AM (inicira), CA (pregled + odabir vještaka),
///           Vještak (prihvata + dostavlja procjenu), CO (odobrava).
///
/// Preduvjeti:
///   - docker compose up (aplikacija mora biti pokrenuta)
///   - Popunjeni kredencijali u appsettings.e2e.json
///   - Keycloak klijent s Direct Access Grants uključen (KeycloakClientId)
///   - Seedovani šifarnici (CodebookSeeder), vještak postoji ili će biti kreiran
/// </summary>
[Collection("E2E")]
public sealed class OrderWorkflowFLTests : IClassFixture<PlaywrightFixture>, IAsyncLifetime
{
    private readonly PlaywrightFixture _fixture;
    private readonly E2EConfig         _config;
    private readonly JwtTokenHelper    _jwt;

    // Client koji se pravi u InitializeAsync po roli
    private WorkflowApiClient _amClient   = null!;
    private WorkflowApiClient _caClient   = null!;
    private WorkflowApiClient _coClient   = null!;
    private WorkflowApiClient _vjtClient  = null!;

    // Browser context za AM — za kreiranje narudžbe kroz UI i finalni pregled
    private IBrowserContext _amBrowserCtx = null!;
    private IPage           _amPage       = null!;

    public OrderWorkflowFLTests(PlaywrightFixture fixture)
    {
        _fixture = fixture;
        _config  = fixture.Config;
        _jwt     = new JwtTokenHelper(_config);
    }

    public async Task InitializeAsync()
    {
        // JWT tokeni za sve role (ROPC)
        var amToken  = await _jwt.GetTokenAsync(_config.GetUser("AM"));
        var caToken  = await _jwt.GetTokenAsync(_config.GetUser("CA"));
        var coToken  = await _jwt.GetTokenAsync(_config.GetUser("CO"));
        var vjtToken = await _jwt.GetTokenAsync(_config.GetUser("Vjestak"));

        _amClient  = new WorkflowApiClient(_config.ApiUrl, amToken);
        _caClient  = new WorkflowApiClient(_config.ApiUrl, caToken);
        _coClient  = new WorkflowApiClient(_config.ApiUrl, coToken);
        _vjtClient = new WorkflowApiClient(_config.ApiUrl, vjtToken);

        // Browser context za AM (za UI verifikaciju)
        _amBrowserCtx = await _fixture.NewAuthenticatedContextAsync("AM");
        _amPage       = await _amBrowserCtx.NewPageAsync();
        _amPage.SetDefaultTimeout(_config.Timeout);
    }

    public async Task DisposeAsync()
    {
        _amClient.Dispose();
        _caClient.Dispose();
        _coClient.Dispose();
        _vjtClient.Dispose();
        _jwt.Dispose();
        await _amBrowserCtx.DisposeAsync();
    }

    [Fact(Timeout = 90000)]
    public async Task FL_KompletnaTok_Stan_BezProvjereVristupa_ZavrsiUReadyForProcedure()
    {
        using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(80));
        var ct = cts.Token;

        // ── Korak 0: Priprema testnih podataka ─────────────────────────────

        // Dohvati ID za kolateral "Stan" (APP_STAN) iz šifarnika
        var stanCollateralId = await _caClient.GetCodebookValueIdAsync(
            "tipovi_kolaterala", "APP_STAN", ct);

        // Dohvati ID tipa dokumenta (bilo koji — za upload procjene)
        var documentTypeId = await _caClient.GetFirstCodebookValueIdAsync(
            "tipovi_dokumenata", ct);

        // Osiguraj da postoji barem jedan vještak (kreiraj ako nema)
        var appraiserId = await _caClient.GetFirstAppraiserIdAsync(ct);
        if (appraiserId is null)
        {
            appraiserId = await _caClient.CreateTestAppraiserAsync(ct);
            Assert.True(appraiserId > 0, "Nije moguće kreirati test vještaka.");
        }

        // ── Korak 1: AM kreira narudžbu (FL, Stan) ─────────────────────────

        var createRequest = new
        {
            clientName          = $"E2E FL Test Klijent {Guid.NewGuid().ToString()[..6]}",
            clientType          = "FL",
            clientIdentifier    = "0101990123456",   // JMBG format
            collateralTypeId    = stanCollateralId,
            combinedCollateralTypeId = (int?)null,
            city                = "Sarajevo",
            propertyAddress     = "Ulica test 1",
            branch              = "Sarajevo Centar",
            branchAddress       = "Titova 1, Sarajevo",
            contactName         = "E2E Kontakt",
            contactPhone        = "061000001",
            contactEmail        = (string?)null,
            internalNote        = "E2E test — može se obrisati",
            deliveryContactName = "E2E Dostava Osoba",
            amRecipientName     = "E2E AM Primalac",
            propertyCity        = "Sarajevo"
        };

        var orderId = await _amClient.CreateOrderAsync(createRequest, ct);
        Assert.True(orderId > 0, "Narudžba nije kreirana (ID = 0).");

        // ── Korak 2: AM podnosi narudžbu CA-u ──────────────────────────────

        await _amClient.SubmitOrderAsync(orderId, ct);

        var statusAfterSubmit = await _amClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("SubmittedBySales", statusAfterSubmit);

        // Provjeri vidljivost u UI (AM može vidjeti svoju narudžbu)
        await _amPage.GotoAsync($"/narudzbe/{orderId}");
        await _amPage.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await _amPage.WaitForTimeoutAsync(500);
        Assert.Contains("/narudzbe/", _amPage.Url);

        // ── Korak 3: CA prihvata narudžbu ──────────────────────────────────

        // POST /api/tasks/{acceptTaskId}/accept
        // → AcceptedByCA + DocumentationReviewInProgress + ReviewDocumentation task
        var acceptTaskId = await _caClient.GetActiveTaskIdAsync(orderId, "AcceptCAOrder", ct);
        await _caClient.AcceptTaskAsync(acceptTaskId, ct);

        var statusAfterAccept = await _caClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("DocumentationReviewInProgress", statusAfterAccept);

        // ── Korak 4: CA završava pregled dokumentacije ──────────────────────

        // Stan → DocumentationApproved (bez AccessCheckRequested!)
        await _caClient.CompleteDocumentReviewAsync(orderId, ct);

        var statusAfterReview = await _caClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("DocumentationApproved", statusAfterReview);

        // ── Korak 5: CA automatski odabira vještaka (FL — stan) ─────────────

        await _caClient.AutoSelectAppraiserAsync(orderId, ct);

        var statusAfterAutoSelect = await _caClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("AppraiserSelected", statusAfterAutoSelect);

        // ── Korak 6: CA šalje narudžbu vještaku ─────────────────────────────

        await _caClient.SendToAppraiserAsync(orderId, ct);

        var statusAfterSend = await _caClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("OrderSentToAppraiser", statusAfterSend);

        // ── Korak 7: Vještak prihvata narudžbu ──────────────────────────────

        await _vjtClient.AcceptByAppraiserAsync(orderId, ct);

        var statusAfterAppraiserAccept = await _vjtClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("AppraisalInProgress", statusAfterAppraiserAccept);

        // ── Korak 8: Vještak uploaduje dokument procjene ────────────────────

        await _vjtClient.UploadAppraisalDocumentAsync(orderId, documentTypeId, ct);

        // ── Korak 9: Vještak dostavlja finalnu procjenu ─────────────────────

        var visitDate = DateTime.UtcNow.Date.AddDays(-1); // obilazak juče
        await _vjtClient.SubmitAppraisalAsync(orderId, visitDate, ct);

        var statusAfterSubmitAppraisal = await _vjtClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("AppraisalReceived", statusAfterSubmitAppraisal);

        // ── Korak 10: CO odobrava finalnu procjenu ───────────────────────────

        await _coClient.ApproveFinalAppraisalAsync(orderId, appraiserRating: 4, ct);

        var finalStatus = await _coClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("ReadyForProcedure", finalStatus);

        // ── Finalna verifikacija u UI ────────────────────────────────────────

        // AM osvježi stranicu i provjeri da status badge prikazuje "Spreman za proceduru"
        await _amPage.ReloadAsync();
        await _amPage.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await _amPage.WaitForTimeoutAsync(800);

        var statusBadge = _amPage.Locator("[class*='status'], [class*='badge'], .chip, .mud-chip");
        var pageText    = await _amPage.ContentAsync();

        Assert.True(
            pageText.Contains("ReadyForProcedure") ||
            pageText.Contains("Spreman za proceduru") ||
            pageText.Contains("Ready"),
            $"Status badge na stranici ne pokazuje 'ReadyForProcedure'. " +
            $"API status je: {finalStatus}. URL: {_amPage.Url}");
    }
}
