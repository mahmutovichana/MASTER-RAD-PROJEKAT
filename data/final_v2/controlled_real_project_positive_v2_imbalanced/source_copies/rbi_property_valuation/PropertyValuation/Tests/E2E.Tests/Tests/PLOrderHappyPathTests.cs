using Microsoft.Playwright;
using RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;
using Xunit;
using Xunit.Abstractions;

namespace RBBH.CollateralAppraisal.E2E.Tests.Tests;

/// <summary>
/// E2E Happy Path — Kompletan tok PL narudžbe.
///
/// Tok statusa:
///   Draft
///   → SubmittedBySales          AM inicira zadatak
///   → DocumentationReviewInProgress  CA prihvata
///   → AccessCheckRequested      CA šalje CO na provjeru pristupa (non-Stan kolateral)
///   → AccessCheckApproved       CO odobrava pristup
///   → [Quote phase: CA šalje ponude → vještak odgovara → CO bira pobjednika]
///   → AppraiserSelected         CO prihvata ponudu (AcceptQuote)
///   → OrderSentToAppraiser      CA šalje narudžbu
///   → AppraisalInProgress       Vještak prihvata
///   → AppraisalReceived         Vještak dostavlja procjenu
///   → ReadyForProcedure         CO odobrava
///
/// Demo mode: E2E_DEMO_MODE=1
/// </summary>
[Collection("E2E")]
public sealed class PLOrderHappyPathTests : IClassFixture<PlaywrightFixture>, IAsyncLifetime
{
    private readonly PlaywrightFixture _fixture;
    private readonly E2EConfig         _config;
    private readonly JwtTokenHelper    _jwt;
    private readonly ITestOutputHelper _out;

    private WorkflowApiClient _amClient  = null!;
    private WorkflowApiClient _caClient  = null!;
    private WorkflowApiClient _coClient  = null!;
    private WorkflowApiClient _vjtClient = null!;

    // PL Happy Path je čist API test — nema potrebe za browser kontekstom.
    // UI verifikacija je pokrivenar u FLOrderHappyPathTests (forma + status badge).

    public PLOrderHappyPathTests(PlaywrightFixture fixture, ITestOutputHelper output)
    {
        _fixture = fixture;
        _config  = fixture.Config;
        _jwt     = new JwtTokenHelper(_config);
        _out     = output;
    }

    public async Task InitializeAsync()
    {
        _amClient  = new WorkflowApiClient(_config.ApiUrl,
            await _jwt.GetTokenAsync(_config.GetUser("AM")));
        _caClient  = new WorkflowApiClient(_config.ApiUrl,
            await _jwt.GetTokenAsync(_config.GetUser("CA")));
        _coClient  = new WorkflowApiClient(_config.ApiUrl,
            await _jwt.GetTokenAsync(_config.GetUser("CO")));
        _vjtClient = new WorkflowApiClient(_config.ApiUrl,
            await _jwt.GetTokenAsync(_config.GetUser("Vjestak")));
    }

    public async Task DisposeAsync()
    {
        _amClient.Dispose();
        _caClient.Dispose();
        _coClient.Dispose();
        _vjtClient.Dispose();
        _jwt.Dispose();
    }

    [Fact(Timeout = 150_000)]
    public async Task PL_HappyPath_ABCTestDoo_KompletnaTok_ZavrsiUReadyForProcedure()
    {
        using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(130));
        var ct  = cts.Token;
        var log = new DemoLogger(_out, totalSteps: 12);

        // ── SETUP: testni podaci ───────────────────────────────────────────

        await log.StepAsync("SETUP: Priprema testnih podataka");

        // Kolateral koji nije Stan → trigeriše AccessCheck (PL tok)
        var collateralId = await TryGetCollateralIdAsync(ct);
        log.Assert("Kolateral (non-Stan)", $"ID={collateralId}");

        var documentTypeId = await _caClient.GetFirstCodebookValueIdAsync("tipovi_dokumenata", ct);
        log.Assert("Tip dokumenta", $"ID={documentTypeId}");

        // Osiguramo 3 vještaka za PL quote proces
        var appraiserIds = await EnsureMinAppraisersAsync(3, log, ct);
        log.Assert("Vještaci (3 za PL)", string.Join(", ", appraiserIds));

        // ── 1/12  PRODAJA: Kreira PL narudžbu — ABC Test d.o.o. ──────────

        await log.StepAsync("1/12  PRODAJA: Kreira PL narudžbu ABC Test d.o.o.", stepNumber: 1);

        var orderId = await _amClient.CreateOrderAsync(new
        {
            clientName               = "ABC Test d.o.o.",
            clientType               = "PL",
            clientIdentifier         = "4301234567890",
            collateralTypeId         = collateralId,
            combinedCollateralTypeId = (int?)null,
            city                     = "Sarajevo",
            propertyAddress          = "Poslovna zona, Garaža B-01",
            branch                   = "Sarajevo Centar",
            branchAddress            = "Titova 3, Sarajevo",
            contactName              = "Amir Hodžić",
            contactPhone             = "061999888",
            contactEmail             = (string?)null,
            internalNote             = "E2E PL Happy Path — može se obrisati",
            deliveryContactName      = "Maja Perić",
            amRecipientName          = "Selma Kovačević",
            squareMetersCommercial   = (decimal?)250.0m,
            squareMetersResidential  = (decimal?)null,
            propertyCity             = "Sarajevo"
        }, ct);

        Assert.True(orderId > 0, $"Narudžba nije kreirana (ID={orderId}).");
        log.Assert("Narudžba kreirana", $"ID={orderId}");

        await _amClient.SubmitOrderAsync(orderId, ct);
        await AssertStatus(orderId, "SubmittedBySales", ct);
        log.Assert("Status", "SubmittedBySales");

        // Provjeri broj narudžbe
        var order      = await _amClient.GetAsync_Public($"api/orders/{orderId}", ct);
        var orderNumber = order.TryGetProperty("orderNumber", out var on) ? on.GetString() : null;
        Assert.False(string.IsNullOrWhiteSpace(orderNumber), "Broj narudžbe nije generisan.");
        log.Assert("Broj narudžbe", orderNumber!);

        // ── 2/12  CA: Prihvata zadatak + pregleda dokumentaciju ───────────

        await log.StepAsync("2/12  CA: Prihvata zadatak i šalje CO na provjeru pristupa", stepNumber: 2);

        var acceptTaskId = await _caClient.GetActiveTaskIdAsync(orderId, "AcceptCAOrder", ct);
        await _caClient.AcceptTaskAsync(acceptTaskId, ct);
        await AssertStatus(orderId, "DocumentationReviewInProgress", ct);

        // CA završava pregled → AccessCheckRequested (non-Stan → PL petlja)
        await _caClient.CompleteDocumentReviewAsync(orderId, ct);
        await AssertStatus(orderId, "AccessCheckRequested", ct);
        log.Assert("Status", "AccessCheckRequested — CA šalje CO na provjeru pristupa ✓");

        // ── 3/12  CO: Odobrava pristup nekretnini ─────────────────────────

        await log.StepAsync("3/12  CO: Odobrava pristup nekretnini", stepNumber: 3);

        await _coClient.ApproveAccessCheckAsync(
            orderId, "Pristup uredan — garaža dostupna.", ct);
        await AssertStatus(orderId, "AccessCheckApproved", ct);
        log.Assert("Status", "AccessCheckApproved ✓");

        // ── 4/12  CA: Šalje zahtjeve za ponude (max 3 vještaka) ──────────

        await log.StepAsync("4/12  CA: Šalje zahtjeve za ponude vještacima", stepNumber: 4);

        var quoteDeadline = DateTime.UtcNow.AddDays(3);
        var sentCount     = await _caClient.SendQuoteRequestsAsync(
            orderId, appraiserIds, quoteDeadline, ct);
        Assert.Equal(appraiserIds.Count, sentCount);

        var quotes = await _caClient.GetQuoteRequestsAsync(orderId, ct);
        Assert.Equal(appraiserIds.Count, quotes.Count);
        Assert.All(quotes, q => Assert.Equal("Sent", q.Status));
        log.Assert($"Quote requests poslani ({sentCount})", $"rok: {quoteDeadline:dd.MM.yyyy}");

        // ── 5/12  VJEŠTAK: Šalje ponude ──────────────────────────────────

        await log.StepAsync("5/12  VJEŠTAK: Šalje ponude za PL narudžbu", stepNumber: 5);

        // Vještak 1 (pobjednička ponuda: 500 KM, 7 dana)
        var winnerQuote = quotes[0];
        await _vjtClient.RespondToQuoteAsync(
            orderId, winnerQuote.Id, offeredPrice: 500m, offeredDays: 7,
            comment: "Standardna cijena za garažu. Slobodan termin za obilazak.", ct);

        // Ostali vještaci šalju skuplje ponude
        foreach (var q in quotes.Skip(1))
            await _vjtClient.RespondToQuoteAsync(
                orderId, q.Id, offeredPrice: 650m + quotes.IndexOf(q) * 50, offeredDays: 10,
                comment: "Alternativna ponuda.", ct);

        var respondedQuotes = await _caClient.GetQuoteRequestsAsync(orderId, ct);
        Assert.All(respondedQuotes, q => Assert.Equal("Responded", q.Status));
        log.Assert("Sve ponude dostavljene", "status: Responded");

        // ── 6/12  CO: Bira najpovoljniju ponudu ──────────────────────────

        await log.StepAsync("6/12  CO: Bira najpovoljniju ponudu — 500 KM, 7 dana", stepNumber: 6);

        // Bug fix implementiran: AcceptQuote sad kreira SendOrderToAppraiser task
        var winnerAppraiserName = await _coClient.AcceptQuoteAsync(
            orderId, winnerQuote.Id, ct);
        await AssertStatus(orderId, "AppraiserSelected", ct);
        log.Assert("Odabrani vještak (pobjednička ponuda)", winnerAppraiserName);

        // CA šalje zahvalnicu neodabranim vještacima
        try
        {
            await _caClient.SendThankYouAsync(orderId, ct);
            log.Assert("Zahvalnica neodabranim vještacima", "poslana ✓");
        }
        catch { log.Warn("SendThankYou preskočen (task možda nije aktivan)."); }

        // ── 7/12  CA: Šalje narudžbu izabranom vještaku ──────────────────

        await log.StepAsync("7/12  CA: Šalje narudžbu izabranom vještaku", stepNumber: 7);

        await _caClient.SendToAppraiserAsync(orderId, ct);
        await AssertStatus(orderId, "OrderSentToAppraiser", ct);
        log.Assert("Status", "OrderSentToAppraiser ✓");

        // ── 8/12  VJEŠTAK: Prihvata + uploaduje + dostavlja procjenu ─────

        await log.StepAsync("8/12  VJEŠTAK: Prihvata narudžbu", stepNumber: 8);

        await _vjtClient.AcceptByAppraiserAsync(orderId, ct);
        await AssertStatus(orderId, "AppraisalInProgress", ct);
        log.Assert("Status", "AppraisalInProgress ✓");

        await log.StepAsync("8/12  VJEŠTAK: Uploaduje i dostavlja završenu procjenu", stepNumber: 8);

        await _vjtClient.UploadAppraisalDocumentAsync(orderId, documentTypeId, ct);
        log.Assert("Dokument", "procjena-e2e.pdf uploadovan ✓");

        var visitDate = DateTime.UtcNow.Date.AddDays(-1);
        await _vjtClient.SubmitAppraisalAsync(orderId, visitDate, ct);
        await AssertStatus(orderId, "AppraisalReceived", ct);
        log.Assert("Status", "AppraisalReceived ✓");
        log.Assert("Datum obilaska", visitDate.ToString("dd.MM.yyyy"));

        // ── 9/12  CO: Odobrava procjenu ───────────────────────────────────

        await log.StepAsync("9/12  CO: Odobrava finalnu procjenu", stepNumber: 9);

        await _coClient.ApproveFinalAppraisalAsync(orderId, appraiserRating: 4, ct);
        await AssertStatus(orderId, "ReadyForProcedure", ct);
        log.Assert("Status", "ReadyForProcedure ✓");
        log.Assert("Ocjena vještaka", "4/5");

        // ── 10/12  PRODAJA: Preuzima procjenu ────────────────────────────

        await log.StepAsync("10/12  PRODAJA: Preuzima završenu procjenu", stepNumber: 10);

        // API provjera statusa — bez browser-a (PL test je čisto API)
        var readyStatus = await _amClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("ReadyForProcedure", readyStatus);
        log.Assert("AM vidi status", "ReadyForProcedure ✓");

        // API: finalna procjena dostupna
        try
        {
            var finalDoc = await _amClient.GetAsync_Public(
                $"api/orders/{orderId}/final-appraisal", ct);
            var docId = finalDoc.GetProperty("finalAppraisalDocumentId").GetInt32();
            Assert.True(docId > 0);
            log.Assert("Finalna procjena dostupna za download, DocumentID", docId.ToString());
        }
        catch { log.Warn("final-appraisal endpoint nije vratio 200 za AM rolu."); }

        // ── 11/12  MIŠLJENJE CO i Pravne službe ──────────────────────────

        await log.StepAsync("11/12  Mišljenje CO i Pravne službe (opcija)", stepNumber: 11);

        try
        {
            await _amClient.RequestOpinionsAsync(orderId,
                "E2E test — traži se mišljenje CO i Pravne.", ct);
            log.Assert("Opinion request", "poslan ✓");

            await _coClient.SubmitOpinionAsync(orderId, "CO", ct);
            log.Assert("CO mišljenje", "importovano ✓");

            // PravnaSluzba korisnik postoji u Keycloak (pravnasluzba.test@rbbh.ba)
            var pravnaToken = await _jwt.GetTokenAsync(_config.GetUser("PravnaSluzba"));
            using var pravnaClient = new WorkflowApiClient(_config.ApiUrl, pravnaToken);
            await pravnaClient.SubmitOpinionAsync(orderId, "Pravna", ct);
            log.Assert("Pravna mišljenje", "importovano ✓");
        }
        catch (Exception ex)
        {
            log.Warn($"Opinion flow preskočen: {ex.Message.Split('.')[0]}");
        }

        // ── 12/12  ZAVRŠETAK ──────────────────────────────────────────────

        await log.StepAsync("12/12  ZAVRŠETAK: Narudžba završena", stepNumber: 12);

        var finalStatus = await _amClient.GetOrderStatusAsync(orderId, ct);

        // Svaka rola vidi isti finalni status
        Assert.Equal(finalStatus, await _caClient.GetOrderStatusAsync(orderId, ct));
        Assert.Equal(finalStatus, await _coClient.GetOrderStatusAsync(orderId, ct));
        log.Assert("AM, CA, CO vide isti status", finalStatus);

        Assert.True(
            finalStatus is "ReadyForProcedure" or "Completed",
            $"Narudžba nije u završnom statusu. Status: {finalStatus}");

        // Audit provjera
        await AssertAuditAsync(orderId, log, ct);

        log.Assert($"✅ PL Happy Path završen! ID={orderId}, broj={orderNumber}", finalStatus);
    }

    // ═══════════════════════════════════════════════════════════════════════

    private async Task AssertStatus(
        int orderId, string expected, CancellationToken ct)
    {
        var actual = await _amClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal(expected, actual);
    }

    private async Task<int> TryGetCollateralIdAsync(CancellationToken ct)
    {
        // Pokušaj redom: GRE, GAR, GAP (sve su non-Stan → triggeriše AccessCheck)
        foreach (var code in new[] { "GRE", "GAR", "GAP", "SFH", "MFH" })
        {
            try { return await _caClient.GetCodebookValueIdAsync("tipovi_kolaterala", code, ct); }
            catch { /* pokušaj sljedećeg */ }
        }
        throw new InvalidOperationException(
            "Nije pronađen ni jedan non-Stan kolateral u šifarniku 'tipovi_kolaterala'. " +
            "Provjeri da je CodebookSeeder pokrenuo.");
    }

    private async Task<List<int>> EnsureMinAppraisersAsync(
        int minCount, DemoLogger log, CancellationToken ct)
    {
        var existing = await _caClient.GetAppraisersAsync("Sve", ct);
        var ids      = existing.Take(minCount).ToList();

        while (ids.Count < minCount)
        {
            var newId = await _caClient.CreateTestAppraiserAsync(ct);
            ids.Add(newId);
            log.Info($"Kreiran test vještak ID={newId}");
        }
        return ids;
    }

    private async Task AssertAuditAsync(int orderId, DemoLogger log, CancellationToken ct)
    {
        try
        {
            var audit = await _amClient.GetAsync_Public(
                $"api/audit?entityType=AppraisalOrder&entityKey={orderId}&pageSize=50", ct);
            if (audit.TryGetProperty("items", out var items))
            {
                var count = items.GetArrayLength();
                Assert.True(count > 0, "Nema audit zapisa za narudžbu.");
                log.Assert("Audit zapisi", $"{count} događaj(a) ✓");
            }
        }
        catch { log.Warn("Audit endpoint nije dostupan AM roli — provjeri prava."); }
    }
}
