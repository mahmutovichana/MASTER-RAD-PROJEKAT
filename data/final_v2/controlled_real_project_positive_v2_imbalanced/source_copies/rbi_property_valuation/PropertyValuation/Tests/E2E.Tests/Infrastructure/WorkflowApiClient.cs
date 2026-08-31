using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;

namespace RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;

/// <summary>
/// HTTP klijent za direktne API pozive tokom E2E workflow testova.
/// Svaka instanca je vezana za jednu rolu (jedan JWT token).
///
/// Sve metode koriste provjeren JSON property map:
///   CaDocumentReviewResultDto → "status"
///   AppraiserAssignmentResultDto → "status"
///   SendToAppraiserResultDto → "status"
///   ApproveFinalAppraisalResultDto → "status"
///   AcceptQuoteResult → "selectedAppraiserName" (nema "status")
///   SendQuoteRequestsResult → "sentCount"
/// </summary>
public sealed class WorkflowApiClient : IDisposable
{
    private readonly HttpClient _http;
    private readonly string     _baseUrl;

    // Minimalni validan PDF (koristi se za upload u testovima)
    public static readonly byte[] MinimalPdfBytes = Encoding.ASCII.GetBytes(
        "%PDF-1.0\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n" +
        "2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n" +
        "3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>endobj\n" +
        "xref\n0 4\n" +
        "0000000000 65535 f\n0000000009 00000 n\n" +
        "0000000058 00000 n\n0000000115 00000 n\n" +
        "trailer<</Size 4/Root 1 0 R>>\nstartxref\n190\n%%EOF");

    public WorkflowApiClient(string apiBaseUrl, string jwtToken)
    {
        _baseUrl = apiBaseUrl.TrimEnd('/');
        _http    = new HttpClient { BaseAddress = new Uri(_baseUrl + "/") };
        _http.DefaultRequestHeaders.Authorization =
            new AuthenticationHeaderValue("Bearer", jwtToken);
    }

    // ── Šifarnici ────────────────────────────────────────────────────────────

    public async Task<int> GetCodebookValueIdAsync(
        string codebookKey, string code, CancellationToken ct = default)
    {
        var json = await GetAsync($"api/codebooks/{codebookKey}/values/active", ct);
        foreach (var item in json.EnumerateArray())
        {
            if (item.GetProperty("code").GetString() == code)
                return item.GetProperty("id").GetInt32();
        }
        throw new InvalidOperationException(
            $"Šifarnik '{codebookKey}' ne sadrži code='{code}'. Provjeri seeder.");
    }

    public async Task<int> GetFirstCodebookValueIdAsync(
        string codebookKey, CancellationToken ct = default)
    {
        var json  = await GetAsync($"api/codebooks/{codebookKey}/values/active", ct);
        var items = json.EnumerateArray().ToList();
        if (items.Count == 0)
            throw new InvalidOperationException(
                $"Šifarnik '{codebookKey}' nema aktivnih vrijednosti.");
        return items[0].GetProperty("id").GetInt32();
    }

    // ── Vještaci ─────────────────────────────────────────────────────────────

    public async Task<int?> GetFirstAppraiserIdAsync(CancellationToken ct = default)
    {
        var json  = await GetAsync("api/appraisers?page=1&pageSize=1", ct);
        var items = json.GetProperty("items").EnumerateArray().ToList();
        return items.Count > 0 ? items[0].GetProperty("id").GetInt32() : null;
    }

    public async Task<List<int>> GetAppraisersAsync(
        string scope = "Sve", CancellationToken ct = default)
    {
        var json = await GetAsync("api/appraisers?page=1&pageSize=20", ct);
        var ids  = new List<int>();
        foreach (var item in json.GetProperty("items").EnumerateArray())
        {
            if (item.TryGetProperty("isActive", out var a) && !a.GetBoolean()) continue;
            if (item.TryGetProperty("isBlacklisted", out var b) && b.GetBoolean()) continue;
            if (item.TryGetProperty("isOnLeave", out var o) && o.GetBoolean()) continue;
            ids.Add(item.GetProperty("id").GetInt32());
        }
        return ids;
    }

    public async Task<int> CreateTestAppraiserAsync(CancellationToken ct = default)
    {
        var body = new
        {
            name                   = $"E2E Test Vještak {Guid.NewGuid().ToString()[..6]}",
            city                   = "Sarajevo",
            legalForm              = "Fizičko lice",
            contactEmail           = $"e2e.{Guid.NewGuid().ToString()[..6]}@test.ba",
            contactPhone           = "061111222",
            notes                  = "E2E test — može se obrisati",
            supportedPropertyTypes = "APP,APP_STAN,GARAZA,GRE,KUCA,GAR",
            supportedCities        = "Sarajevo,Mostar,Tuzla,Banja Luka,Zenica",
            clientScope            = "Sve"
        };
        var result = await PostJsonAsync("api/appraisers", body, ct);
        return result.GetProperty("id").GetInt32();
    }

    /// <summary>
    /// Kreira vještaka koji je linkovan s Keycloak test userom (vjestak.test@rbbh.ba).
    /// Link se uspostavlja po ContactEmail — isti email kao Keycloak user.
    /// Bez ovog linka, AcceptByAppraiser ne može naći Keycloak usera.
    ///
    /// City i SupportedPropertyTypes moraju se poklapati s narudžbom za FL auto-select.
    /// </summary>
    public async Task<int> CreateLinkedAppraiserAsync(
        string keycloakEmail,
        string city             = "Sarajevo",
        string propertyTypes    = "APP,APP_STAN",
        string clientScope      = "Sve",
        CancellationToken ct    = default)
    {
        // Provjeri da li vještak s tim emailom već postoji
        var existing = await GetAppraisersAsync("Sve", ct);
        // Ne možemo filtrirati po emailu ovdje, ali ćemo provjeriti u testu

        var body = new
        {
            name                   = $"E2E Linked Vještak ({city})",
            city,
            legalForm              = "Fizičko lice",  // Individual
            contactEmail           = keycloakEmail,   // Linkuje s Keycloak userom!
            contactPhone           = "062333444",
            notes                  = "E2E test, linkovan s Keycloak — može se obrisati",
            supportedPropertyTypes = propertyTypes,
            supportedCities        = $"{city},Mostar,Tuzla",
            clientScope
        };
        var result = await PostJsonAsync("api/appraisers", body, ct);
        return result.GetProperty("id").GetInt32();
    }

    /// <summary>
    /// Kreira vještaka na godišnjem odmoru (GoLive flag) — za verifikaciju algoritma.
    /// Ovaj vještak NE smije biti odabran pri auto-select.
    /// </summary>
    public async Task<int> CreateOnLeaveAppraiserAsync(
        string city = "Sarajevo", CancellationToken ct = default)
    {
        var body = new
        {
            name                   = $"E2E ON-LEAVE Vještak {Guid.NewGuid().ToString()[..4]}",
            city,
            legalForm              = "Fizičko lice",
            contactEmail           = $"onleave.{Guid.NewGuid().ToString()[..6]}@test.ba",
            contactPhone           = "063444555",
            notes                  = "E2E test ON-LEAVE — može se obrisati",
            supportedPropertyTypes = "APP,APP_STAN",
            supportedCities        = city,
            clientScope            = "Sve"
        };
        var result = await PostJsonAsync("api/appraisers", body, ct);
        var appraiserId = result.GetProperty("id").GetInt32();

        // Postavi na godišnji odmor
        await PostJsonAsync($"api/appraisers/{appraiserId}/on-leave", new { value = true }, ct);
        return appraiserId;
    }

    // ── Narudžbe ──────────────────────────────────────────────────────────────

    public async Task<int> CreateOrderAsync(object createRequest, CancellationToken ct = default)
    {
        var result = await PostJsonAsync("api/orders", createRequest, ct);
        return result.GetProperty("id").GetInt32();
    }

    public async Task SubmitOrderAsync(int orderId, CancellationToken ct = default)
        => await PostJsonAsync($"api/orders/{orderId}/submit", null, ct);

    public async Task<string> GetOrderStatusAsync(int orderId, CancellationToken ct = default)
    {
        var result = await GetAsync($"api/orders/{orderId}", ct);
        return result.GetProperty("status").GetString()!;
    }

    // ── Taskovi ───────────────────────────────────────────────────────────────

    public async Task<int> GetActiveTaskIdAsync(
        int orderId, string taskType, CancellationToken ct = default)
    {
        var json  = await GetAsync("api/tasks/my?page=1&pageSize=50", ct);
        var items = json.GetProperty("items").EnumerateArray();

        foreach (var task in items)
        {
            var taskOrderId = task.GetProperty("appraisalOrderId").GetInt32();
            var type        = task.GetProperty("taskType").GetString();
            if (taskOrderId == orderId && type == taskType)
                return task.GetProperty("id").GetInt32();
        }

        throw new InvalidOperationException(
            $"Task '{taskType}' za narudžbu {orderId} nije pronađen. " +
            $"Provjeri da je prethodni korak uspješno izvršen.");
    }

    public async Task AcceptTaskAsync(int taskId, CancellationToken ct = default)
        => await PostJsonAsync($"api/tasks/{taskId}/accept", null, ct);

    // ── CA pregled dokumentacije ──────────────────────────────────────────────

    /// <summary>
    /// CA završava pregled dokumentacije.
    /// Za Stan (APP/APP_STAN) → DocumentationApproved + SelectAppraiser task.
    /// Za non-Stan (GRE, GAR, KUCA...) → DocumentationApproved + AccessCheckRequested.
    /// DTO: CaDocumentReviewResultDto → JSON field "status"
    /// </summary>
    public async Task<string> CompleteDocumentReviewAsync(
        int orderId, CancellationToken ct = default)
    {
        var result = await PostJsonAsync($"api/orders/{orderId}/complete-review", null, ct);
        return result.GetProperty("status").GetString()!;
    }

    // ── Provjera pristupa (CO) ────────────────────────────────────────────────

    public async Task<string> ApproveAccessCheckAsync(
        int orderId, string? comment = null, CancellationToken ct = default)
    {
        var result = await PostJsonAsync($"api/orders/{orderId}/access-check/approve",
                                         new { comment = comment ?? "Pristup uredan." }, ct);
        return result.GetProperty("status").GetString()!;
    }

    // ── Odabir vještaka ───────────────────────────────────────────────────────

    /// <summary>
    /// CA automatski odabira vještaka za FL narudžbu.
    /// DTO: AppraiserAssignmentResultDto → JSON field "status"
    /// </summary>
    public async Task<string> AutoSelectAppraiserAsync(
        int orderId, CancellationToken ct = default)
    {
        var result = await PostJsonAsync(
            $"api/orders/{orderId}/select-appraiser/auto", null, ct);
        return result.GetProperty("status").GetString()!;
    }

    /// <summary>
    /// CA manuelno odabira vještaka za PL narudžbu.
    /// Zahtijeva aktivan SelectAppraiser task.
    /// DTO: AppraiserAssignmentResultDto → JSON field "status"
    /// </summary>
    public async Task<string> ManualSelectAppraiserAsync(
        int orderId, int appraiserId, CancellationToken ct = default)
    {
        var result = await PostJsonAsync(
            $"api/orders/{orderId}/select-appraiser/manual",
            new { appraiserId }, ct);
        return result.GetProperty("status").GetString()!;
    }

    /// <summary>
    /// CA šalje narudžbu odabranom vještaku.
    /// DTO: SendToAppraiserResultDto → JSON field "status"
    /// </summary>
    public async Task<string> SendToAppraiserAsync(
        int orderId, CancellationToken ct = default)
    {
        var result = await PostJsonAsync(
            $"api/orders/{orderId}/send-to-appraiser", null, ct);
        return result.GetProperty("status").GetString()!;
    }

    // ── Vještak lifecycle ─────────────────────────────────────────────────────

    public async Task AcceptByAppraiserAsync(int orderId, CancellationToken ct = default)
        => await PostJsonAsync($"api/orders/{orderId}/accept-by-appraiser", null, ct);

    public async Task UploadAppraisalDocumentAsync(
        int orderId, int documentTypeId, CancellationToken ct = default)
    {
        using var content    = new MultipartFormDataContent();
        var       pdfContent = new ByteArrayContent(MinimalPdfBytes);
        pdfContent.Headers.ContentType = new MediaTypeHeaderValue("application/pdf");
        content.Add(pdfContent, "files", "procjena-e2e.pdf");

        var url      = $"{_baseUrl}/api/orders/{orderId}/documents?documentTypeId={documentTypeId}";
        var response = await _http.PostAsync(url, content, ct);

        if (!response.IsSuccessStatusCode)
        {
            var err = await response.Content.ReadAsStringAsync(ct);
            throw new InvalidOperationException(
                $"Upload dokumenta za narudžbu {orderId} nije uspio " +
                $"({response.StatusCode}): {err}");
        }
    }

    /// <summary>
    /// Vještak dostavlja finalnu procjenu.
    /// DTO: SendToAppraiserResultDto → JSON field "status"
    /// visitDate je obavezan — dan obilaska imovine.
    /// </summary>
    public async Task<string> SubmitAppraisalAsync(
        int orderId, DateTime visitDate, CancellationToken ct = default)
    {
        var result = await PostJsonAsync(
            $"api/orders/{orderId}/submit-appraisal",
            new { visitDate }, ct);
        return result.GetProperty("status").GetString()!;
    }

    // ── CO finalno odobrenje ─────────────────────────────────────────────────

    /// <summary>
    /// CO odobrava finalnu procjenu.
    /// DTO: ApproveFinalAppraisalResultDto → JSON field "status"
    /// appraiserRating: 1-5
    /// </summary>
    public async Task<string> ApproveFinalAppraisalAsync(
        int orderId, int appraiserRating = 4, CancellationToken ct = default)
    {
        var result = await PostJsonAsync(
            $"api/orders/{orderId}/approve-final",
            new { appraiserRating }, ct);
        return result.GetProperty("status").GetString()!;
    }

    // ── PL Quote Request flow ─────────────────────────────────────────────────

    /// <summary>
    /// CA šalje zahtjeve za ponude max 3 vještaka (PL).
    /// DTO: SendQuoteRequestsResult → JSON field "sentCount"
    /// </summary>
    public async Task<int> SendQuoteRequestsAsync(
        int orderId, List<int> appraiserIds, DateTime deadline,
        CancellationToken ct = default)
    {
        var result = await PostJsonAsync(
            $"api/orders/{orderId}/quote-requests",
            new { appraiserIds, deadline }, ct);
        return result.GetProperty("sentCount").GetInt32();
    }

    /// <summary>
    /// Vraća listu zahtjeva za ponudu.
    /// DTO: QuoteRequestDto → JSON fields "id", "appraiserId", "status", "offeredPrice", "offeredDays"
    /// </summary>
    public async Task<List<(int Id, int AppraiserId, string Status, decimal? Price, int? Days)>>
        GetQuoteRequestsAsync(int orderId, CancellationToken ct = default)
    {
        var json   = await GetAsync($"api/orders/{orderId}/quote-requests", ct);
        var result = new List<(int, int, string, decimal?, int?)>();
        foreach (var item in json.EnumerateArray())
        {
            result.Add((
                item.GetProperty("id").GetInt32(),
                item.GetProperty("appraiserId").GetInt32(),
                item.GetProperty("status").GetString()!,
                item.TryGetProperty("offeredPrice", out var p) &&
                    p.ValueKind != JsonValueKind.Null ? p.GetDecimal() : null,
                item.TryGetProperty("offeredDays", out var d) &&
                    d.ValueKind != JsonValueKind.Null ? d.GetInt32() : null
            ));
        }
        return result;
    }

    /// <summary>
    /// Vještak šalje ponudu. DTO: RespondToQuoteResult
    /// </summary>
    public async Task RespondToQuoteAsync(
        int orderId, int quoteRequestId,
        decimal offeredPrice, int offeredDays,
        string? comment = null, CancellationToken ct = default)
    {
        await PostJsonAsync(
            $"api/orders/{orderId}/quote-requests/{quoteRequestId}/respond",
            new { offeredPrice, offeredDays, comment }, ct);
    }

    /// <summary>
    /// CO/CA prihvata pobjedničku ponudu → AppraiserSelected.
    /// DTO: AcceptQuoteResult → JSON field "selectedAppraiserName" (nema "status"!)
    ///
    /// BUG FIX (u aplikacijskom kodu): AcceptQuoteAsync u QuoteRequestService
    /// sad kreira SendOrderToAppraiser task i zatvara SelectAppraiser task.
    /// </summary>
    public async Task<string> AcceptQuoteAsync(
        int orderId, int quoteRequestId, CancellationToken ct = default)
    {
        var result = await PostJsonAsync(
            $"api/orders/{orderId}/quote-requests/{quoteRequestId}/accept",
            null, ct);
        // AcceptQuoteResult nema "status" — vraćamo appraiserName za potvrdu
        return result.TryGetProperty("selectedAppraiserName", out var n)
            ? n.GetString()! : "unknown";
    }

    /// <summary>CA šalje zahvalnicu neodabranim vještacima.</summary>
    public async Task SendThankYouAsync(int orderId, CancellationToken ct = default)
        => await PostJsonAsync(
            $"api/orders/{orderId}/quote-requests/thank-you", null, ct);

    // ── Vještak — import potpisanih dokumenata ────────────────────────────────

    public async Task CompleteSignedDocumentImportAsync(
        int orderId, CancellationToken ct = default)
        => await PostJsonAsync($"api/orders/{orderId}/complete-signed-docs", null, ct);

    // ── Opinion flow ──────────────────────────────────────────────────────────

    public async Task RequestOpinionsAsync(
        int orderId, string? comment = null, CancellationToken ct = default)
        => await PostJsonAsync($"api/orders/{orderId}/opinions/request",
                               new { comment = comment ?? "E2E test" }, ct);

    public async Task SubmitOpinionAsync(
        int orderId, string type, CancellationToken ct = default)
    {
        using var content    = new MultipartFormDataContent();
        var       pdfContent = new ByteArrayContent(MinimalPdfBytes);
        pdfContent.Headers.ContentType = new MediaTypeHeaderValue("application/pdf");
        content.Add(pdfContent, "file", $"misljenje-{type.ToLower()}.pdf");

        var url      = $"{_baseUrl}/api/orders/{orderId}/opinions/{type}";
        var response = await _http.PostAsync(url, content, ct);
        if (!response.IsSuccessStatusCode)
        {
            var err = await response.Content.ReadAsStringAsync(ct);
            throw new InvalidOperationException(
                $"SubmitOpinion({type}) za narudžbu {orderId}: {response.StatusCode} — {err}");
        }
    }

    // ── Confirm original ──────────────────────────────────────────────────────

    public async Task DeliverOriginalAsync(int orderId, CancellationToken ct = default)
        => await PostJsonAsync($"api/orders/{orderId}/deliver-original", null, ct);

    public async Task ConfirmOriginalReceivedAsync(int orderId, CancellationToken ct = default)
        => await PostJsonAsync($"api/orders/{orderId}/confirm-original", null, ct);

    // ── Javni query helperi ───────────────────────────────────────────────────

    public Task<JsonElement> GetAsync_Public(string path, CancellationToken ct = default)
        => GetAsync(path, ct);

    // ── Internals ─────────────────────────────────────────────────────────────

    private async Task<JsonElement> GetAsync(string path, CancellationToken ct = default)
    {
        var response = await _http.GetAsync(path, ct);
        if (!response.IsSuccessStatusCode)
        {
            var err = await response.Content.ReadAsStringAsync(ct);
            throw new InvalidOperationException($"GET {path} → {response.StatusCode}: {err}");
        }
        var body = await response.Content.ReadAsStringAsync(ct);
        return JsonDocument.Parse(body).RootElement.Clone();
    }

    private async Task<JsonElement> PostJsonAsync(
        string path, object? body, CancellationToken ct = default)
    {
        HttpContent content = body is not null
            ? new StringContent(
                JsonSerializer.Serialize(body,
                    new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase }),
                Encoding.UTF8, "application/json")
            : new StringContent("{}", Encoding.UTF8, "application/json");

        var response = await _http.PostAsync(path, content, ct);
        if (!response.IsSuccessStatusCode)
        {
            var err = await response.Content.ReadAsStringAsync(ct);
            throw new InvalidOperationException($"POST {path} → {response.StatusCode}: {err}");
        }
        var responseBody = await response.Content.ReadAsStringAsync(ct);
        if (string.IsNullOrWhiteSpace(responseBody)) return default;
        return JsonDocument.Parse(responseBody).RootElement.Clone();
    }

    public void Dispose() => _http.Dispose();
}
