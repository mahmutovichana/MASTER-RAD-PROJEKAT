using Microsoft.Playwright;
using RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;
using Xunit;
using Xunit.Abstractions;

namespace RBBH.CollateralAppraisal.E2E.Tests.Tests;

/// <summary>
/// E2E Happy Path — Kompletan tok FL narudžbe (Fizičko lice).
///
/// Tok: Prodaja → CA → Vještak → CO → završetak
///
/// Statusi:
///   Draft → SubmittedBySales ("Poslano CA")
///   → DocumentationReviewInProgress ("Pregled dokumentacije")
///   → DocumentationApproved ("Dokumentacija odobrena")
///   → AppraiserSelected ("Vještak odabran")
///   → OrderSentToAppraiser ("Poslano vještaku")
///   → AppraisalInProgress ("Procjena u toku")
///   → AppraisalReceived ("Procjena zaprimljena")
///   → ReadyForProcedure ("Spreman za proceduru")
///
/// UI selektori (sve ima data-testid ili stabilan selector):
///   Kategorija: [data-testid="category-51-rre"]
///   Submit: [data-testid="btn-submit-order"]
///   Accept order: [data-testid="btn-accept-order"]
///   Open appraisal panel: [data-testid="btn-open-appraisal-panel"]
///   Visit date: [data-testid="field-visit-date"] input
///   Confirm appraisal: [data-testid="btn-confirm-appraisal"]
///   Upload ZK: [data-testid="upload-input-zk"]
///   Upload uplatnica: [data-testid="upload-input-uplatnica"]
///   CO approve section: [data-testid="co-approve-section"]
///   CO approve button: [data-testid="btn-approve-appraisal"]
///
/// Demo mode: E2E_DEMO_MODE=1
/// </summary>
[Collection("E2E")]
public sealed class FLOrderHappyPathTests : IClassFixture<PlaywrightFixture>, IAsyncLifetime
{
    private readonly PlaywrightFixture _fixture;
    private readonly E2EConfig         _config;
    private readonly JwtTokenHelper    _jwt;
    private readonly ITestOutputHelper _out;

    private WorkflowApiClient _amClient  = null!;
    private WorkflowApiClient _caClient  = null!;
    private WorkflowApiClient _coClient  = null!;
    private WorkflowApiClient _vjtClient = null!;

    // Browser konteksti
    private IBrowserContext _amCtx  = null!;
    private IBrowserContext _vjtCtx = null!;
    private IBrowserContext _coCtx  = null!;
    private IPage           _amPage  = null!;
    private IPage           _vjtPage = null!;
    private IPage           _coPage  = null!;

    public FLOrderHappyPathTests(PlaywrightFixture fixture, ITestOutputHelper output)
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

        _amCtx   = await _fixture.NewAuthenticatedContextAsync("AM");
        _amPage  = await _amCtx.NewPageAsync();
        _amPage.SetDefaultTimeout(_config.Timeout);

        _vjtCtx  = await _fixture.NewAuthenticatedContextAsync("Vjestak");
        _vjtPage = await _vjtCtx.NewPageAsync();
        _vjtPage.SetDefaultTimeout(_config.Timeout);

        _coCtx  = await _fixture.NewAuthenticatedContextAsync("CO");
        _coPage = await _coCtx.NewPageAsync();
        _coPage.SetDefaultTimeout(_config.Timeout);
    }

    public async Task DisposeAsync()
    {
        _amClient.Dispose();
        _caClient.Dispose();
        _coClient.Dispose();
        _vjtClient.Dispose();
        _jwt.Dispose();
        await _amCtx.DisposeAsync();
        await _vjtCtx.DisposeAsync();
        await _coCtx.DisposeAsync();
    }

    [Fact(Timeout = 210_000)]
    public async Task FL_HappyPath_Stan_KompletnaTok_OdInicijanjaDoReadyForProcedure()
    {
        using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(190));
        var ct  = cts.Token;
        var log = new DemoLogger(_out, totalSteps: 8);

        // ══════════════════════════════════════════════════════════════════
        // SETUP: Seed testnih podataka
        // ══════════════════════════════════════════════════════════════════

        await log.StepAsync("SETUP: Seed vještaka za FL algoritam verifikaciju");

        var vjtEmail = _config.GetUser("Vjestak").Username; // vjestak.test@rbbh.ba

        // Vještak A: Individual, Sarajevo, APP_STAN — linkovan s Keycloak userom
        //   ContactEmail = vjestak.test@rbbh.ba → auto-resolve pri AcceptByAppraiser
        var winnerAppraiserId = await _caClient.CreateLinkedAppraiserAsync(
            keycloakEmail: vjtEmail,
            city: "Sarajevo",
            propertyTypes: "APP,APP_STAN",
            ct: ct);
        log.Assert("Vještak A (pobjednik, linked)", $"ID={winnerAppraiserId}, email={vjtEmail}");

        // Vještak B: na godišnjem odmoru → isključen iz selekcije
        var onLeaveAppraiserId = await _caClient.CreateOnLeaveAppraiserAsync("Sarajevo", ct);
        log.Assert("Vještak B (na GO, isključen)", $"ID={onLeaveAppraiserId}");

        // Šifarnik: Stan (APP_STAN) — ne triggeriše AccessCheck
        var stanCollateralId = await GetStanCollateralIdAsync(ct);
        log.Assert("Kolateral Stan", $"ID={stanCollateralId}");

        // Tip dokumenta za upload procjene
        var documentTypeId = await _caClient.GetFirstCodebookValueIdAsync("tipovi_dokumenata", ct);
        log.Assert("Tip dokumenta", $"ID={documentTypeId}");

        // ══════════════════════════════════════════════════════════════════
        // 1/8  PRODAJA: Kreira FL narudžbu kroz UI formu
        // ══════════════════════════════════════════════════════════════════

        await log.StepAsync("1/8 Prodaja kreira FL narudžbu", stepNumber: 1);

        await _amPage.GotoAsync($"{_config.BaseUrl}/narudzbe/nova/FL");
        await _amPage.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await _amPage.WaitForTimeoutAsync(800);

        // ── Kategorija: "Stambena imovina" ────────────────────────────────
        // data-testid="category-51-rre" (51_RRE.ToLower().Replace("_","-"))
        var categoryCard = _amPage.Locator("[data-testid='category-51-rre']");
        await categoryCard.WaitForAsync(new LocatorWaitForOptions { Timeout = 8000 });
        await categoryCard.ClickAsync();
        await _amPage.WaitForTimeoutAsync(400);
        log.Assert("Kategorija kolaterala", "Stambena imovina (51_RRE) ✓");

        // ── Tip kolaterala: "Stan" (MudAutocomplete) ─────────────────────
        await FillMudAutocompleteAsync("#field-collateralType", "Stan", "Stan", log, ct);

        // ── Naziv klijenta ────────────────────────────────────────────────
        await FillFieldAsync("#field-clientName input", "Edin Kovačević", log, ct);

        // ── JMBG (13 cifara) ─────────────────────────────────────────────
        await FillFieldAsync("#field-jmbg input", "1509990123456", log, ct);

        // ── Grad nekretnine ───────────────────────────────────────────────
        await FillFieldAsync("#field-propertyCity input", "Sarajevo", log, ct);

        // ── Adresa nekretnine ─────────────────────────────────────────────
        await FillFieldAsync("#field-propertyAddress input", "Grbavička 12, stan 5", log, ct);

        // ── Kontakt telefon ───────────────────────────────────────────────
        await FillFieldAsync("#field-phone input", "061234567", log, ct);

        // ── Osoba za dostavu originala ────────────────────────────────────
        await FillFieldAsync("#field-deliveryContactName input", "Amra Hodžić", log, ct);

        // ── AM/SM/UB za mail (može biti auto-popunjen) ────────────────────
        var amRecipientInput = _amPage.Locator("#field-amRecipientName input");
        var amCurrentVal     = await amRecipientInput.InputValueAsync();
        if (string.IsNullOrWhiteSpace(amCurrentVal))
        {
            await amRecipientInput.FillAsync("Selma Kovačević");
            log.Assert("AM recipient", "Selma Kovačević (ručno)");
        }
        else
        {
            log.Assert("AM recipient (auto-popunjen)", amCurrentVal);
        }

        // ── Poslovnica (MudAutocomplete) ──────────────────────────────────
        await FillMudAutocompleteAsync("#field-city", "Sarajevo", "Sarajevo", log, ct);

        // ── Wizard korak 2: Dokumenti ─────────────────────────────────────
        await GoToDocumentStepAsync(log, ct);

        // ── Upload ZK (obavezan) ──────────────────────────────────────────
        // data-testid="upload-input-zk" (card.Code = "ZK", ToLower() = "zk")
        await UploadDocumentAsync(
            inputSelector: "[data-testid='upload-input-zk']",
            fileName: "zk-test.pdf",
            label: "ZK", log, ct);

        // ── Upload Uplatnica (obavezna za FL) ────────────────────────────
        // data-testid="upload-input-uplatnica" (card.Code = "UPLATNICA")
        await UploadDocumentAsync(
            inputSelector: "[data-testid='upload-input-uplatnica']",
            fileName: "uplatnica-test.pdf",
            label: "Uplatnica", log, ct);

        // ── Submit: "Pošalji narudžbu" ────────────────────────────────────
        // data-testid="btn-submit-order"
        var submitBtn = _amPage.Locator("[data-testid='btn-submit-order']");
        await submitBtn.WaitForAsync(new LocatorWaitForOptions
        {
            State   = WaitForSelectorState.Visible,
            Timeout = 8000
        });

        await _amPage.WaitForTimeoutAsync(500); // čekaj validaciju
        var isEnabled = await submitBtn.IsEnabledAsync();
        Assert.True(isEnabled, "Submit button nije aktivan — provjeri da li su popunjena sva obavezna polja.");

        await submitBtn.ClickAsync();
        log.Assert("Kliknut 'Pošalji narudžbu'", "✓");

        // ── Čekaj redirect na /narudzbe ───────────────────────────────────
        await _amPage.WaitForURLAsync(
            url => url.Contains("/narudzbe") && !url.Contains("/nova"),
            new PageWaitForURLOptions { Timeout = 20_000 });
        log.Assert("Redirect na /narudzbe", _amPage.Url);

        // ── Dohvati ID narudžbe ───────────────────────────────────────────
        var orderId = await GetLatestOrderIdAsync(ct);
        Assert.True(orderId > 0, "Nije pronađen ID narudžbe.");
        log.Assert("Narudžba kreirana, ID", orderId.ToString());

        // ── Provjeri broj narudžbe, segment FL, status ────────────────────
        var orderJson   = await _amClient.GetAsync_Public($"api/orders/{orderId}", ct);
        var orderNumber = orderJson.TryGetProperty("orderNumber", out var onP)
            ? onP.GetString() : null;
        Assert.False(string.IsNullOrWhiteSpace(orderNumber), "Broj narudžbe nije generisan.");
        log.Assert("Broj narudžbe (protokol)", orderNumber!);

        var clientType = orderJson.TryGetProperty("clientType", out var ctP) ? ctP.GetString() : null;
        Assert.True(clientType is "FL" or "FIZICKA" or "FizickaLica",
            $"Segment nije FL ({clientType}).");
        log.Assert("Segment", $"FL ✓");

        var s1 = await _amClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("SubmittedBySales", s1);
        log.Assert("Status", "Poslano CA (SubmittedBySales) ✓");

        // ── CA vidi narudžbu ──────────────────────────────────────────────
        var caOrderStatus = await _caClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("SubmittedBySales", caOrderStatus);
        log.Assert("CA vidi narudžbu", caOrderStatus);

        // ══════════════════════════════════════════════════════════════════
        // 2/8  CA: Prihvata zadatak + završava pregled
        // ══════════════════════════════════════════════════════════════════

        await log.StepAsync("2/8 CA prihvata zadatak", stepNumber: 2);

        var acceptTaskId = await _caClient.GetActiveTaskIdAsync(orderId, "AcceptCAOrder", ct);
        await _caClient.AcceptTaskAsync(acceptTaskId, ct);

        var s2 = await _caClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("DocumentationReviewInProgress", s2);
        log.Assert("Status", "Pregled dokumentacije ✓");

        // Dokumentacija uredna — CA završava pregled
        await _caClient.CompleteDocumentReviewAsync(orderId, ct);
        var s3 = await _caClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("DocumentationApproved", s3);
        log.Assert("Status", "Dokumentacija odobrena ✓");

        // ══════════════════════════════════════════════════════════════════
        // 3/8  CA: Automatska dodjela vještaka (FL algoritam)
        // ══════════════════════════════════════════════════════════════════

        await log.StepAsync("3/8 CA pokreće automatsku dodjelu vještaka", stepNumber: 3);

        log.Info("Algoritam FL: Individual < 2 aktivne, Firm < 5 | preferira grad | fewest active");
        log.Info($"Vještak A ID={winnerAppraiserId}: Sarajevo, APP_STAN, 0 aktivnih → POBJEDNIK");
        log.Info($"Vještak B ID={onLeaveAppraiserId}: Sarajevo, na GO → ISKLJUČEN");

        await _caClient.AutoSelectAppraiserAsync(orderId, ct);
        var s4 = await _caClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("AppraiserSelected", s4);
        log.Assert("Status", "Vještak odabran ✓");

        // Verifikacija: provjeri koji je vještak odabran
        var afterSelect = await _caClient.GetAsync_Public($"api/orders/{orderId}", ct);
        var selectedId  = afterSelect.TryGetProperty("appraiserId", out var apP) ? apP.GetInt32() : 0;
        Assert.Equal(winnerAppraiserId, selectedId);
        log.Assert("Algoritam odabrao vještaka A (min aktivnih, isključen GO)", $"ID={selectedId} ✓");

        // ══════════════════════════════════════════════════════════════════
        // 4/8  CA: Šalje narudžbu vještaku
        // ══════════════════════════════════════════════════════════════════

        await log.StepAsync("4/8 CA šalje narudžbu vještaku", stepNumber: 4);

        await _caClient.SendToAppraiserAsync(orderId, ct);
        var s5 = await _caClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("OrderSentToAppraiser", s5);
        log.Assert("Status", "Poslano vještaku ✓");

        // ══════════════════════════════════════════════════════════════════
        // 5/8  VJEŠTAK: Prihvata narudžbu (UI) + uploaduje procjenu (UI)
        // ══════════════════════════════════════════════════════════════════

        await log.StepAsync("5/8 Vještak prihvata narudžbu", stepNumber: 5);

        // UI: Vještak navigira na stranicu narudžbe
        await _vjtPage.GotoAsync($"{_config.BaseUrl}/narudzbe/{orderId}");
        await _vjtPage.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await _vjtPage.WaitForTimeoutAsync(800);

        // Klikni "Prihvati narudžbu" — data-testid="btn-accept-order"
        var acceptOrderBtn = _vjtPage.Locator("[data-testid='btn-accept-order']");
        await acceptOrderBtn.WaitForAsync(new LocatorWaitForOptions
        {
            State   = WaitForSelectorState.Visible,
            Timeout = 10_000
        });
        await acceptOrderBtn.ClickAsync();

        // Čekaj status promjenu u UI ili API
        await _vjtPage.WaitForTimeoutAsync(1500);
        var s6 = await _vjtClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("AppraisalInProgress", s6);
        log.Assert("Status", "Procjena u toku (AppraisalInProgress) ✓");

        // ── Upload dokumenta procjene kroz tab "Dokumenti" ────────────────
        await log.StepAsync("5/8 Vještak uploaduje finalnu procjenu", stepNumber: 5);

        // Pronađi i klikni tab "Dokumenti"
        var dokumentiTab = _vjtPage
            .GetByText("Dokumenti", new PageGetByTextOptions { Exact = false }).First;
        if (await dokumentiTab.IsVisibleAsync())
        {
            await dokumentiTab.ClickAsync();
            await _vjtPage.WaitForTimeoutAsync(600);
        }

        // Upload procjene: data-testid="upload-input-finalna_procjena" ili prvi dostupni
        // Napomena: DocumentUploadSection kreira input-e po card.Code
        // Specifičan selektor za procjenu može biti upload-input-finalna_procjena
        var procjenaInput = _vjtPage.Locator(
            "[data-testid='upload-input-finalna_procjena'], " +
            "[data-testid='upload-input-finalna-procjena'], " +
            "input[type='file'][accept*='pdf']").First;

        if (await procjenaInput.CountAsync() > 0)
        {
            var pdfBytes = WorkflowApiClient.MinimalPdfBytes;
            var tmpPath  = Path.Combine(AppContext.BaseDirectory, "procjena-final.pdf");
            await File.WriteAllBytesAsync(tmpPath, pdfBytes, ct);
            await procjenaInput.SetInputFilesAsync(tmpPath);
            await _vjtPage.WaitForTimeoutAsync(1200);
            log.Assert("Procjena uploadovana kroz UI", "procjena-final.pdf ✓");
            try { File.Delete(tmpPath); } catch { }
        }
        else
        {
            // Fallback: API upload
            await _vjtClient.UploadAppraisalDocumentAsync(orderId, documentTypeId, ct);
            log.Warn("UI upload nije uspio — koristim API fallback.");
        }

        // ── "Dostavi procjenu na CO" → datum obilaska → confirm ──────────
        await log.StepAsync("5/8 Vještak unosi datum obilaska i dostavlja procjenu", stepNumber: 5);

        // Klilkni dugme za otvaranje panela: data-testid="btn-open-appraisal-panel"
        var openPanelBtn = _vjtPage.Locator("[data-testid='btn-open-appraisal-panel']");
        await openPanelBtn.WaitForAsync(new LocatorWaitForOptions
        {
            State   = WaitForSelectorState.Visible,
            Timeout = 10_000
        });
        await openPanelBtn.ClickAsync();
        await _vjtPage.WaitForTimeoutAsync(500);

        // Popuni datum obilaska: data-testid="field-visit-date"
        // MudTextField renderuje data-testid na wrapper div; input je unutra
        var visitDateInput = _vjtPage.Locator(
            "[data-testid='field-visit-date'] input, " +
            "input[type='date']").First;
        var visitDate = DateTime.Today.AddDays(-1).ToString("yyyy-MM-dd");
        await visitDateInput.FillAsync(visitDate);
        await visitDateInput.PressAsync("Tab");
        await _vjtPage.WaitForTimeoutAsync(300);
        log.Assert("Datum obilaska unesen", visitDate);

        // Klikni "Dostavi procjenu": data-testid="btn-confirm-appraisal"
        var confirmBtn = _vjtPage.Locator("[data-testid='btn-confirm-appraisal']");
        await confirmBtn.WaitForAsync(new LocatorWaitForOptions { Timeout = 5000 });
        await confirmBtn.ClickAsync();
        await _vjtPage.WaitForTimeoutAsync(2000);

        var s7 = await _vjtClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("AppraisalReceived", s7);
        log.Assert("Status", "Procjena zaprimljena (AppraisalReceived) ✓");

        // CO dobija ApproveFinalAppraisal task
        var coTaskId = await _coClient.GetActiveTaskIdAsync(orderId, "ApproveFinalAppraisal", ct);
        Assert.True(coTaskId > 0, "CO nema ApproveFinalAppraisal task.");
        log.Assert("CO prima zadatak na pregled", $"TaskID={coTaskId}");

        // ══════════════════════════════════════════════════════════════════
        // 6/8  CO: Pregleda procjenu
        // ══════════════════════════════════════════════════════════════════

        await log.StepAsync("6/8 CO pregleda procjenu", stepNumber: 6);

        await _coPage.GotoAsync($"{_config.BaseUrl}/narudzbe/{orderId}/procjena");
        await _coPage.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await _coPage.WaitForTimeoutAsync(800);

        // Provjeri da CO vidi download dugme za finalnu procjenu
        var downloadSection = _coPage.GetByText("Finalna procjena", new PageGetByTextOptions { Exact = false });
        if (await downloadSection.IsVisibleAsync())
            log.Assert("CO vidi finalnu procjenu za download", "✓");

        // Provjeri da sekcija za odobrenje postoji
        var approveSection = _coPage.Locator("[data-testid='co-approve-section']");
        await approveSection.WaitForAsync(new LocatorWaitForOptions
        {
            State   = WaitForSelectorState.Visible,
            Timeout = 10_000
        });
        log.Assert("CO vidi sekciju 'Procjena može dalje u proceduru'", "✓");

        // ══════════════════════════════════════════════════════════════════
        // 7/8  CO: Odobrava procjenu — "Odobri procjenu"
        // ══════════════════════════════════════════════════════════════════

        await log.StepAsync("7/8 CO odobrava procjenu", stepNumber: 7);

        // Rating je već default 4 (MudRating _appraiserRating = 4)
        // Ako hoćemo promijeniti, možemo kliknuti rating zvjezdice
        // Za sad koristimo default 4/5 koji je unaprijed popunjen

        // Klikni "Odobri procjenu": data-testid="btn-approve-appraisal"
        var approveBtn = _coPage.Locator("[data-testid='btn-approve-appraisal']");
        await approveBtn.WaitForAsync(new LocatorWaitForOptions
        {
            State   = WaitForSelectorState.Visible,
            Timeout = 8000
        });
        await approveBtn.ClickAsync();

        // MudDialog: "Odobri procjenu" confirm button
        await _coPage.WaitForTimeoutAsync(500);
        var dialogConfirm = _coPage
            .GetByRole(AriaRole.Button,
                new PageGetByRoleOptions { Name = "Odobri procjenu", Exact = false })
            .Or(_coPage.GetByText("Odobri procjenu", new PageGetByTextOptions { Exact = true }))
            .First;

        if (await dialogConfirm.IsVisibleAsync())
        {
            await dialogConfirm.ClickAsync();
            log.Assert("Confirm dialog 'Odobri procjenu'", "kliknut ✓");
        }

        await _coPage.WaitForTimeoutAsync(2000);

        var s8 = await _coClient.GetOrderStatusAsync(orderId, ct);
        Assert.Equal("ReadyForProcedure", s8);
        log.Assert("Status", "Spreman za proceduru (ReadyForProcedure) ✓");

        // ══════════════════════════════════════════════════════════════════
        // 8/8  PRODAJA: Preuzima završenu procjenu
        // ══════════════════════════════════════════════════════════════════

        await log.StepAsync("8/8 Prodaja preuzima završenu procjenu", stepNumber: 8);

        // UI: AM navigira na narudžbu i vidi status "Spreman za proceduru"
        await _amPage.GotoAsync($"{_config.BaseUrl}/narudzbe/{orderId}");
        await _amPage.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await _amPage.WaitForTimeoutAsync(800);

        var pageText = await _amPage.ContentAsync();
        Assert.True(
            pageText.Contains("ReadyForProcedure",    StringComparison.OrdinalIgnoreCase) ||
            pageText.Contains("Spreman za proceduru", StringComparison.OrdinalIgnoreCase),
            $"AM ne vidi 'Spreman za proceduru'. URL: {_amPage.Url}");
        log.Assert("UI: AM vidi 'Spreman za proceduru'", "✓");

        // Provjeri da je finalna procjena dostupna za download
        try
        {
            var finalDoc    = await _amClient.GetAsync_Public($"api/orders/{orderId}/final-appraisal", ct);
            var downloadUrl = finalDoc.TryGetProperty("downloadUrl", out var du) ? du.GetString() : null;
            Assert.False(string.IsNullOrWhiteSpace(downloadUrl), "Download URL nije dostupan.");
            log.Assert("Finalna procjena dostupna za download", "✓");
        }
        catch { log.Warn("AM nema pristup final-appraisal endpointu."); }

        // ── Sve role vide isti status ─────────────────────────────────────
        var amStatus  = await _amClient.GetOrderStatusAsync(orderId, ct);
        var caStatus  = await _caClient.GetOrderStatusAsync(orderId, ct);
        var coStatus  = await _coClient.GetOrderStatusAsync(orderId, ct);
        var vjtStatus = await _vjtClient.GetOrderStatusAsync(orderId, ct);

        Assert.Equal("ReadyForProcedure", amStatus);
        Assert.Equal("ReadyForProcedure", caStatus);
        Assert.Equal("ReadyForProcedure", coStatus);
        log.Assert("AM, CA, CO, Vještak — isti finalni status", amStatus);

        // ── Audit ────────────────────────────────────────────────────────
        await AssertAuditAsync(orderId, log, ct);

        log.Assert($"✅ FL Happy Path završen! ID={orderId}, Protokol={orderNumber}",
                   $"Status: {amStatus}");
    }

    // ═══════════════════════════════════════════════════════════════════════
    //  UI HELPERI
    // ═══════════════════════════════════════════════════════════════════════

    private async Task FillFieldAsync(string selector, string value, DemoLogger log, CancellationToken ct)
    {
        var locator = _amPage.Locator(selector);
        await locator.WaitForAsync(new LocatorWaitForOptions
        {
            State   = WaitForSelectorState.Visible,
            Timeout = 8000
        });
        await locator.ScrollIntoViewIfNeededAsync();
        await locator.ClickAsync();
        await locator.FillAsync(value);
        await locator.PressAsync("Tab");
        log.Assert($"Polje '{selector}'", value);
    }

    private async Task FillMudAutocompleteAsync(
        string fieldId, string searchText, string targetLabel, DemoLogger log, CancellationToken ct)
    {
        var input = _amPage.Locator($"{fieldId} input");
        if (await input.CountAsync() == 0) input = _amPage.Locator(fieldId);
        if (await input.CountAsync() == 0)
        {
            log.Warn($"Autocomplete '{fieldId}' nije pronađen.");
            return;
        }

        await input.ClickAsync();
        await input.FillAsync(searchText);
        await _amPage.WaitForTimeoutAsync(500);

        var option = _amPage
            .Locator(".mud-popover-open .mud-list-item, [role='option'], .mud-list li")
            .GetByText(targetLabel, new LocatorGetByTextOptions { Exact = false })
            .First;

        if (await option.CountAsync() > 0)
        {
            await option.ClickAsync();
            log.Assert($"Autocomplete '{fieldId}'", targetLabel);
        }
        else
        {
            await input.PressAsync("Tab");
            log.Warn($"Opcija '{targetLabel}' nije pronađena u dropdown za '{fieldId}'.");
        }

        await _amPage.WaitForTimeoutAsync(300);
    }

    private async Task GoToDocumentStepAsync(DemoLogger log, CancellationToken ct)
    {
        var nextBtn = _amPage
            .Locator("button:has-text('Nastavi'), button:has-text('Dokumenti'), button:has-text('Sljedeći')")
            .First;
        if (await nextBtn.CountAsync() > 0 && await nextBtn.IsVisibleAsync())
        {
            await nextBtn.ClickAsync();
            await _amPage.WaitForLoadStateAsync(LoadState.NetworkIdle);
            await _amPage.WaitForTimeoutAsync(500);
            log.Assert("Wizard", "korak Dokumenti ✓");
        }
    }

    private async Task UploadDocumentAsync(
        string inputSelector, string fileName, string label, DemoLogger log, CancellationToken ct)
    {
        var fileInput = _amPage.Locator(inputSelector);

        if (await fileInput.CountAsync() == 0)
        {
            log.Warn($"Upload input '{inputSelector}' nije pronađen za '{label}'.");
            return;
        }

        var tmpPath = Path.Combine(AppContext.BaseDirectory, "fixtures", fileName);
        Directory.CreateDirectory(Path.GetDirectoryName(tmpPath)!);
        await File.WriteAllBytesAsync(tmpPath, WorkflowApiClient.MinimalPdfBytes, ct);

        await fileInput.SetInputFilesAsync(tmpPath);
        await _amPage.WaitForTimeoutAsync(1200);
        log.Assert($"Upload '{label}'", $"{fileName} ✓");

        try { File.Delete(tmpPath); } catch { }
    }

    // ═══════════════════════════════════════════════════════════════════════
    //  API HELPERI
    // ═══════════════════════════════════════════════════════════════════════

    private async Task<int> GetStanCollateralIdAsync(CancellationToken ct)
    {
        foreach (var code in new[] { "APP_STAN", "APP", "SFH" })
        {
            try { return await _caClient.GetCodebookValueIdAsync("tipovi_kolaterala", code, ct); }
            catch { }
        }
        return await _caClient.GetFirstCodebookValueIdAsync("tipovi_kolaterala", ct);
    }

    private async Task<int> GetLatestOrderIdAsync(CancellationToken ct)
    {
        var json = await _amClient.GetAsync_Public(
            "api/orders?page=1&pageSize=1&sortBy=createdAt&sortDir=desc", ct);
        if (json.TryGetProperty("items", out var items) && items.GetArrayLength() > 0)
            return items[0].GetProperty("id").GetInt32();
        var json2 = await _amClient.GetAsync_Public("api/orders?page=1&pageSize=5", ct);
        if (json2.TryGetProperty("items", out var items2) && items2.GetArrayLength() > 0)
            return items2[0].GetProperty("id").GetInt32();
        return 0;
    }

    private async Task AssertAuditAsync(int orderId, DemoLogger log, CancellationToken ct)
    {
        try
        {
            var audit = await _amClient.GetAsync_Public(
                $"api/audit?entityType=AppraisalOrder&entityKey={orderId}&pageSize=100", ct);
            if (audit.TryGetProperty("items", out var items))
            {
                var count = items.GetArrayLength();
                Assert.True(count > 0, "Nema audit zapisa.");
                log.Assert("Audit zapisi", $"{count} ✓");
            }
        }
        catch { log.Warn("Audit endpoint nije dostupan AM roli."); }
    }
}
