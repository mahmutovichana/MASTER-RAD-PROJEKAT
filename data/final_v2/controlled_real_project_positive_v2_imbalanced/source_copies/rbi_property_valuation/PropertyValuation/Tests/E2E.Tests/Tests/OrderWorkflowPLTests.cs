using Microsoft.Playwright;
using RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;
using Xunit;

namespace RBBH.CollateralAppraisal.E2E.Tests.Tests;

/// <summary>
/// E2E test koji pokriva KOMPLETAN tok narudžbe za PRAVNA LICA (PL).
///
/// Scenario: Garaža (GARAZA) — sa provjerom pristupa CO-a (PL petlja).
///
/// Tok statusa:
///   Draft → SubmittedBySales → AcceptedByCA → DocumentationReviewInProgress
///   → DocumentationApproved → AccessCheckRequested → AccessCheckApproved
///   → AppraiserSelected → OrderSentToAppraiser → AppraisalInProgress
///   → AppraisalReceived → ReadyForProcedure
///
/// Ključna razlika od FL:
///   - Kolateral nije Stan → CompleteReview trigeriše AccessCheckRequested
///   - CO odobrava pristup nekretnini PRIJE odabira vještaka
///   - CA manuelno odabira vještaka (PL — nema automatskog algoritma)
///
/// Učesnici: AM (inicira), CA (pregled, odabir vještaka),
///           CO (provjera pristupa + finalno odobrenje), Vještak (procjena).
/// </summary>
[Collection("E2E")]
public sealed class OrderWorkflowPLTests : IClassFixture<PlaywrightFixture>, IAsyncLifetime
{
    private readonly PlaywrightFixture _fixture;
    private readonly E2EConfig         _config;
    private readonly JwtTokenHelper    _jwt;

    private WorkflowApiClient _amClient  = null!;
    private WorkflowApiClient _caClient  = null!;
    private WorkflowApiClient _coClient  = null!;
    private WorkflowApiClient _vjtClient = null!;

    // Browser context za CA — za vizuelnu verifikaciju access check koraka
    private IBrowserContext _caBrowserCtx = null!;
    private IPage           _caPage       = null!;

    public OrderWorkflowPLTests(PlaywrightFixture fixture)
    {
        _fixture = fixture;
        _config  = fixture.Config;
        _jwt     = new JwtTokenHelper(_config);
    }

    public async Task InitializeAsync()
    {
        var amToken  = await _jwt.GetTokenAsync(_config.GetUser("AM"));
        var caToken  = await _jwt.GetTokenAsync(_config.GetUser("CA"));
        var coToken  = await _jwt.GetTokenAsync(_config.GetUser("CO"));
        var vjtToken = await _jwt.GetTokenAsync(_config.GetUser("Vjestak"));

        _amClient  = new WorkflowApiClient(_config.ApiUrl, amToken);
        _caClient  = new WorkflowApiClient(_config.ApiUrl, caToken);
        _coClient  = new WorkflowApiClient(_config.ApiUrl, coToken);
        _vjtClient = new WorkflowApiClient(_config.ApiUrl, vjtToken);

        _caBrowserCtx = await _fixture.NewAuthenticatedContextAsync("CA");
        _caPage       = await _caBrowserCtx.NewPageAsync();
        _caPage.SetDefaultTimeout(_config.Timeout);
    }

    public async Task DisposeAsync()
    {
        _amClient.Dispose();
        _caClient.Dispose();
        _coClient.Dispose();
        _vjtClient.Dispose();
        _jwt.Dispose();
        await _caBrowserCtx.DisposeAsync();
    }

    [Fact(Timeout = 90000)]
    public async Task PL_KompletnaTok_Garaza_SaProvjeromPristupa_ZavrsiUReadyForProcedure()
    {
        using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(80));
        var ct = cts.Token;

        // ── Korak 0: Priprema testnih podataka ─────────────────────────────

        // Kolateral "Garaža" — nije Stan → trigeriše AccessCheckRequested (PL petlja)
        int garazaCollateralId;
        try
        {
            garazaCollateralId = await _caClient.GetCodebookValueIdAsync(
                "tipovi_kolaterala", "GARAZA", ct);
        }
        catch
        {
            // Fallback: uzmi bilo koji kolateral koji nije APP ili APP_STAN
            garazaCollateralId = await _caClient.GetCodebookValueIdAsync(
                "tipovi_kolaterala", "OSTAVA", ct);
        }

        var documentTypeId = await _caClient.GetFirstCodebookValueIdAsync("tipovi_dokumenata", ct);

        // Za PL manuelni odabir vještaka — mora postojati barem jedan
        var appraiserId = await _caClient.GetFirstAppraiserIdAsync(ct);
        if (appraiserId is null)
        {
            appraiserId = await _caClient.CreateTestAppraiserAsync(ct);
            Assert.True(appraiserId > 0, "Nije moguće kreirati test vještaka za PL.");
        }

        // ── Korak 1: AM kreira PL narudžbu (Garaža) ────────────────────────

        var createRequest = new
        {
            clientName               = $"E2E PL Firma {Guid.NewGuid().ToString()[..6]} d.o.o.",
            clientType               = "PL",
            clientIdentifier         = "4201234567890",  // ID broj pravnog lica (13 cifara)
            collateralTypeId         = garazaCollateralId,
            combinedCollateralTypeId = (int?)null,
            city                     = "Sarajevo",
            propertyAddress          = "Poslovna Zona 5, Garaža B12",
            branch                   = "Sarajevo Poslovna",
            branchAddress            = "Hamdije Čemerlića 2, Sarajevo",
            contactName              = "E2E PL Kontakt",
            contactPhone             = "033111222",
            contactEmail             = (string?)null,
            internalNote             = "E2E PL test — može se obrisati",
            deliveryContactName      = "E2E PL Dostava",
            amRecipientName          = "E2E AM PL",
            squareMetersCommercial   = (decimal?)150.0m,
            squareMetersResidential  = (decimal?)null,
            propertyCity             = "Sarajevo"
        };

        var orderId = await _amClient.CreateOrderAsync(createRequest, ct);
        Assert.True(orderId > 0, "PL narudžba nije kreirana (ID = 0).");

        // ── Korak 2: AM podnosi narudžbu CA-u ──────────────────────────────

        await _amClient.SubmitOrderAsync(orderId, ct);

        var statusAfterSubmit = await _amClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("SubmittedBySales", statusAfterSubmit);

        // ── Korak 3: CA prihvata narudžbu ──────────────────────────────────

        // AcceptCAOrder task → AcceptedByCA + DocumentationReviewInProgress + ReviewDocumentation task
        var acceptTaskId = await _caClient.GetActiveTaskIdAsync(orderId, "AcceptCAOrder", ct);
        await _caClient.AcceptTaskAsync(acceptTaskId, ct);

        var statusAfterAccept = await _caClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("DocumentationReviewInProgress", statusAfterAccept);

        // ── Korak 4: CA završava pregled dokumentacije ──────────────────────

        // Garaža ≠ Stan → DocumentationApproved + AccessCheckRequested (PL petlja!)
        await _caClient.CompleteDocumentReviewAsync(orderId, ct);

        var statusAfterReview = await _caClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("AccessCheckRequested", statusAfterReview);

        // Vizuelna provjera: CA vidi narudžbu u statusu AccessCheckRequested
        await _caPage.GotoAsync($"/narudzbe/{orderId}");
        await _caPage.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await _caPage.WaitForTimeoutAsync(500);

        var pageContent = await _caPage.ContentAsync();
        Assert.True(
            pageContent.Contains("AccessCheckRequested") ||
            pageContent.Contains("Provjera pristupa") ||
            pageContent.Contains("pristup"),
            $"CA stranica ne prikazuje status provjere pristupa. URL: {_caPage.Url}");

        // ── Korak 5: CO odobrava pristup nekretnini ─────────────────────────

        // AccessCheckRequested → AccessCheckApproved + SelectAppraiser task
        await _coClient.ApproveAccessCheckAsync(orderId, "Pristup uredan — E2E test.", ct);

        var statusAfterAccessApproval = await _coClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("AccessCheckApproved", statusAfterAccessApproval);

        // ── Korak 6: CA manuelno odabira vještaka (PL — bez automatskog algoritma) ─

        await _caClient.ManualSelectAppraiserAsync(orderId, appraiserId.Value, ct);

        var statusAfterManualSelect = await _caClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("AppraiserSelected", statusAfterManualSelect);

        // ── Korak 7: CA šalje narudžbu vještaku ─────────────────────────────

        await _caClient.SendToAppraiserAsync(orderId, ct);

        var statusAfterSend = await _caClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("OrderSentToAppraiser", statusAfterSend);

        // ── Korak 8: Vještak prihvata narudžbu ──────────────────────────────

        await _vjtClient.AcceptByAppraiserAsync(orderId, ct);

        var statusAfterAppraiserAccept = await _vjtClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("AppraisalInProgress", statusAfterAppraiserAccept);

        // ── Korak 9: Vještak uploaduje i dostavlja procjenu ─────────────────

        await _vjtClient.UploadAppraisalDocumentAsync(orderId, documentTypeId, ct);

        var visitDate = DateTime.UtcNow.Date.AddDays(-2);
        await _vjtClient.SubmitAppraisalAsync(orderId, visitDate, ct);

        var statusAfterAppraisalSubmit = await _vjtClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("AppraisalReceived", statusAfterAppraisalSubmit);

        // ── Korak 10: CO odobrava finalnu procjenu ───────────────────────────

        await _coClient.ApproveFinalAppraisalAsync(orderId, appraiserRating: 5, ct);

        var finalStatus = await _coClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("ReadyForProcedure", finalStatus);

        // ── Finalna verifikacija na CA stranici ─────────────────────────────

        await _caPage.ReloadAsync();
        await _caPage.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await _caPage.WaitForTimeoutAsync(800);

        var finalPageContent = await _caPage.ContentAsync();
        Assert.True(
            finalPageContent.Contains("ReadyForProcedure") ||
            finalPageContent.Contains("Spreman za proceduru") ||
            finalPageContent.Contains("Ready"),
            $"Stranica ne prikazuje konačni status. " +
            $"Očekivano 'ReadyForProcedure', API status: {finalStatus}. URL: {_caPage.Url}");
    }

    [Fact(Timeout = 90000)]
    public async Task PL_CompleteReview_ZaNonStan_TrigerisujeAccessCheckRequested()
    {
        using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(60));
        var ct = cts.Token;

        // Fokusiran test samo na ključnu razliku PL vs FL:
        // CompleteReview za non-Stan kolateral MORA trigerisati AccessCheckRequested
        // (ne DocumentationApproved direktno kao za Stan)

        var garazaId = await _caClient.GetCodebookValueIdAsync("tipovi_kolaterala", "GARAZA", ct);

        var createRequest = new
        {
            clientName               = $"E2E PL AccessCheck Verif {Guid.NewGuid().ToString()[..6]}",
            clientType               = "PL",
            clientIdentifier         = "4209876543210",
            collateralTypeId         = garazaId,
            combinedCollateralTypeId = (int?)null,
            city                     = "Mostar",
            propertyAddress          = "Bulevar 99",
            branch                   = "Mostar",
            branchAddress            = "Kneza Domagoja 3, Mostar",
            contactName              = "Kontakt",
            contactPhone             = "036222333",
            contactEmail             = (string?)null,
            internalNote             = "E2E access check verifikacija",
            deliveryContactName      = "Dostava",
            amRecipientName          = "AM Primalac"
        };

        var orderId = await _amClient.CreateOrderAsync(createRequest, ct);
        await _amClient.SubmitOrderAsync(orderId, ct);

        var acceptTaskId = await _caClient.GetActiveTaskIdAsync(orderId, "AcceptCAOrder", ct);
        await _caClient.AcceptTaskAsync(acceptTaskId, ct);

        // Ključna asercija: CompleteReview za non-Stan MORA ići na AccessCheckRequested
        await _caClient.CompleteDocumentReviewAsync(orderId, ct);

        var status = await _caClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("AccessCheckRequested", status);

        // Verifikacija zadatka: CO mora imati AccessCheckCO task
        // (koristimo CO klijent da vidimo task)
        var coTaskId = await _coClient.GetActiveTaskIdAsync(orderId, "AccessCheckCO", ct);
        Assert.True(coTaskId > 0,
            "CO nema 'AccessCheckCO' task — workflow nije ispravno routovan.");
    }
}
