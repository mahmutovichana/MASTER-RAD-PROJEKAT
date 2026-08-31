using System.IO.Compression;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Xml.Linq;
using RBBH.TestAutomation.Api.DTO;

namespace RBBH.TestAutomation.Api.Services.Run;

/// <summary>Ishod jednog E2E scenarija izvršenog na GitHub Actions runneru.</summary>
public sealed record E2EScenarioResult(
    Guid ScenarioId,
    string MethodName,
    bool Passed,
    long DurationMs,
    string? Detail);

/// <summary>
/// Izvještaj jednog <c>workflow_dispatch</c> E2E pokretanja.
/// <see cref="Triggered"/> = dispatch prihvaćen; <see cref="Completed"/> = run završio (nije timeout).
/// </summary>
public sealed record E2ERunReport(
    bool Triggered,
    bool Completed,
    string Conclusion,
    int Passed,
    int Failed,
    long DurationMs,
    IReadOnlyList<E2EScenarioResult> Scenarios,
    string? RunUrl,
    string RawOutput);

public interface IGitHubActionsE2eRunner
{
    Task<E2ERunReport> RunAsync(
        IReadOnlyList<ScenarioDto> uiScenarios,
        IProgress<string>? progress = null,
        CancellationToken ct = default);
}

/// <summary>
/// Okida Playwright E2E na GitHub Actions preko <c>workflow_dispatch</c>: sastavi test iz UI scenarija,
/// pošalji ga kao base64 input, poll-uj Actions API dok run ne završi, skini TRX artefakt i parsiraj.
/// Konfiguracija je u sekciji <c>GitHubE2E</c> (Owner/Repo/WorkflowFile/Ref/BaseUrl) + token
/// (<c>GitHubE2E:Token</c> ili env <c>GITHUB_E2E_TOKEN</c>). Izvršavanje je 100% na GitHubu — VPS
/// ne pokreće browser.
/// </summary>
public sealed class GitHubActionsE2eRunner(
    IHttpClientFactory httpFactory,
    IConfiguration config,
    ILogger<GitHubActionsE2eRunner> logger) : IGitHubActionsE2eRunner
{
    // Korelacija run-a: workflow postavlja run-name "E2E scenariji · {run_tag}", pa run tražimo po run_tag-u u nazivu.
    private static readonly TimeSpan PollInterval   = TimeSpan.FromSeconds(6);
    private static readonly TimeSpan RunFindTimeout = TimeSpan.FromMinutes(2);   // koliko čekamo da se run pojavi
    private static readonly TimeSpan RunDoneTimeout = TimeSpan.FromMinutes(12);  // koliko čekamo da run završi

    public async Task<E2ERunReport> RunAsync(
        IReadOnlyList<ScenarioDto> uiScenarios,
        IProgress<string>? progress = null,
        CancellationToken ct = default)
    {
        var ui = uiScenarios.Where(s => s.Ui is not null).ToList();
        if (ui.Count == 0)
            return Fail("Nema UI scenarija za E2E pokretanje.");

        var owner  = config["GitHubE2E:Owner"];
        var repo   = config["GitHubE2E:Repo"];
        var wf     = config["GitHubE2E:WorkflowFile"] ?? "e2e-scenario.yml";
        var gitRef = config["GitHubE2E:Ref"] ?? "dev";
        var baseUrl = config["GitHubE2E:BaseUrl"] ?? "";
        var token  = config["GitHubE2E:Token"] ?? Environment.GetEnvironmentVariable("GITHUB_E2E_TOKEN");

        if (string.IsNullOrWhiteSpace(owner) || string.IsNullOrWhiteSpace(repo) || string.IsNullOrWhiteSpace(token))
            return Fail("GitHub E2E nije konfigurisan. Postavite GitHubE2E:Owner, :Repo i token (GitHubE2E:Token ili env GITHUB_E2E_TOKEN).");

        var built  = UiScenarioPlaywrightBuilder.Build(ui);
        var runTag = $"tag-{Guid.NewGuid():N}";
        var testB64 = Convert.ToBase64String(Encoding.UTF8.GetBytes(built.TestFileContent));

        using var http = CreateClient(token);

        try
        {
            // ── 1. workflow_dispatch ───────────────────────────────────────────
            progress?.Report($"Šaljem {ui.Count} scenarij(a) na GitHub Actions…");
            var since = DateTime.UtcNow.AddSeconds(-30); // buffer za clock skew pri filtriranju run-ova

            var dispatchBody = new
            {
                @ref = gitRef,
                inputs = new { test_b64 = testB64, run_tag = runTag, base_url = baseUrl },
            };
            var dispatch = await http.PostAsJsonAsync(
                $"repos/{owner}/{repo}/actions/workflows/{wf}/dispatches", dispatchBody, ct);

            if (!dispatch.IsSuccessStatusCode)
            {
                var err  = await dispatch.Content.ReadAsStringAsync(ct);
                var code = (int)dispatch.StatusCode;
                var hint = code switch
                {
                    404 => $" — workflow '{wf}' nije nađen. GitHub dispatch po imenu fajla radi SAMO ako workflow postoji na DEFAULT grani repoa (i na grani '{gitRef}').",
                    403 => " — token nema dozvolu (treba scope 'workflow' / Actions: Read and write).",
                    422 => $" — grana '{gitRef}' ne postoji ili nema ovaj workflow. Provjeri GitHubE2E:Ref.",
                    _   => "",
                };
                return Fail($"workflow_dispatch odbijen ({code}){hint} {Trim(err)}");
            }

            // ── 2. Pronađi pokrenuti run (po run_tag-u u nazivu) ───────────────
            progress?.Report("Workflow okinut, čekam da se run pojavi…");
            var run = await FindRunAsync(http, owner, repo, wf, runTag, since, ct);
            if (run is null)
                return Fail("Run se nije pojavio u očekivanom vremenu (provjeri da workflow postoji na grani i da token ima actions:write).");

            // ── 3. Čekaj završetak ─────────────────────────────────────────────
            progress?.Report($"Run #{run.Value.Id} pokrenut, izvršavam testove na GitHubu…");
            var final = await WaitForCompletionAsync(http, owner, repo, run.Value.Id, progress, ct);
            if (final is null)
                return new E2ERunReport(true, false, "timeout", 0, 0, 0, [], run.Value.HtmlUrl,
                    "Run nije završio u dozvoljenom vremenu.");

            var (conclusion, htmlUrl) = final.Value;

            // ── 4. Skini + parsiraj TRX ────────────────────────────────────────
            progress?.Report("Run završen, preuzimam rezultate…");
            var trxXml = await DownloadTrxAsync(http, owner, repo, run.Value.Id, ct);
            if (trxXml is null)
                return new E2ERunReport(true, true, conclusion, 0, 0, 0, [], htmlUrl,
                    $"Run završio ({conclusion}) ali TRX artefakt nije nađen. Vidi run na GitHubu.");

            var results = ParseTrx(trxXml, built.MethodToScenario);
            var passed  = results.Count(r => r.Passed);
            var failed  = results.Count - passed;
            var durMs   = results.Sum(r => r.DurationMs);

            return new E2ERunReport(true, true, conclusion, passed, failed, durMs, results, htmlUrl,
                $"Run #{run.Value.Id} · conclusion={conclusion}");
        }
        catch (OperationCanceledException) { throw; }
        catch (Exception ex)
        {
            logger.LogError(ex, "Greška pri GitHub E2E pokretanju");
            return Fail(ex.Message);
        }
    }

    // ─── GitHub API koraci ────────────────────────────────────────────────────

    private HttpClient CreateClient(string token)
    {
        var http = httpFactory.CreateClient("GitHubApi");
        http.BaseAddress ??= new Uri("https://api.github.com/");
        http.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
        http.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/vnd.github+json"));
        http.DefaultRequestHeaders.UserAgent.ParseAdd("TestForge-E2E-Runner");
        http.DefaultRequestHeaders.Add("X-GitHub-Api-Version", "2022-11-28");
        return http;
    }

    private async Task<(long Id, string HtmlUrl)?> FindRunAsync(
        HttpClient http, string owner, string repo, string wf, string runTag, DateTime since, CancellationToken ct)
    {
        var deadline = DateTime.UtcNow + RunFindTimeout;
        while (DateTime.UtcNow < deadline)
        {
            ct.ThrowIfCancellationRequested();

            var runs = await http.GetFromJsonAsync<WorkflowRunsResponse>(
                $"repos/{owner}/{repo}/actions/workflows/{wf}/runs?event=workflow_dispatch&per_page=30", ct);

            var match = runs?.WorkflowRuns?.FirstOrDefault(r =>
                (r.Name?.Contains(runTag, StringComparison.Ordinal) ?? false) && r.CreatedAt >= since);

            if (match is not null)
                return (match.Id, match.HtmlUrl ?? "");

            await Task.Delay(PollInterval, ct);
        }
        return null;
    }

    private async Task<(string Conclusion, string HtmlUrl)?> WaitForCompletionAsync(
        HttpClient http, string owner, string repo, long runId, IProgress<string>? progress, CancellationToken ct)
    {
        var deadline = DateTime.UtcNow + RunDoneTimeout;
        while (DateTime.UtcNow < deadline)
        {
            ct.ThrowIfCancellationRequested();

            var run = await http.GetFromJsonAsync<WorkflowRun>(
                $"repos/{owner}/{repo}/actions/runs/{runId}", ct);

            if (run is not null && string.Equals(run.Status, "completed", StringComparison.OrdinalIgnoreCase))
                return (run.Conclusion ?? "unknown", run.HtmlUrl ?? "");

            progress?.Report($"Run status: {run?.Status ?? "?"}…");
            await Task.Delay(PollInterval, ct);
        }
        return null;
    }

    private async Task<string?> DownloadTrxAsync(
        HttpClient http, string owner, string repo, long runId, CancellationToken ct)
    {
        var arts = await http.GetFromJsonAsync<ArtifactsResponse>(
            $"repos/{owner}/{repo}/actions/runs/{runId}/artifacts", ct);

        var artifact = arts?.Artifacts?.FirstOrDefault(a =>
            (a.Name?.Contains("trx", StringComparison.OrdinalIgnoreCase) ?? false) ||
            (a.Name?.Contains("e2e", StringComparison.OrdinalIgnoreCase) ?? false))
            ?? arts?.Artifacts?.FirstOrDefault();

        if (artifact is null) return null;

        // Artefakt se preuzima kao ZIP; unutra tražimo prvi *.trx.
        var zipBytes = await http.GetByteArrayAsync(
            $"repos/{owner}/{repo}/actions/artifacts/{artifact.Id}/zip", ct);

        using var ms = new MemoryStream(zipBytes);
        using var zip = new ZipArchive(ms, ZipArchiveMode.Read);
        var entry = zip.Entries.FirstOrDefault(e => e.FullName.EndsWith(".trx", StringComparison.OrdinalIgnoreCase));
        if (entry is null) return null;

        using var reader = new StreamReader(entry.Open());
        return await reader.ReadToEndAsync(ct);
    }

    // ─── TRX parsiranje (mapiranje po nazivu metode) ──────────────────────────

    private static List<E2EScenarioResult> ParseTrx(string trxXml, IReadOnlyDictionary<string, Guid> methodToScenario)
    {
        var doc = XDocument.Parse(trxXml);
        XName N(string n) => XName.Get(n, "http://microsoft.com/schemas/VisualStudio/TeamTest/2010");

        var byMethod = new Dictionary<string, (bool passed, long ms)>(StringComparer.Ordinal);
        foreach (var utr in doc.Descendants(N("UnitTestResult")))
        {
            var testName = utr.Attribute("testName")?.Value ?? "";
            var outcome  = utr.Attribute("outcome")?.Value ?? "";
            var passed   = outcome.Equals("Passed", StringComparison.OrdinalIgnoreCase);
            var ms       = ParseDurationMs(utr.Attribute("duration")?.Value);

            var method = testName.Split('.').Last();
            byMethod[method] = (passed, ms);
        }

        var results = new List<E2EScenarioResult>();
        foreach (var (method, scenarioId) in methodToScenario)
        {
            if (byMethod.TryGetValue(method, out var r))
                results.Add(new E2EScenarioResult(scenarioId, method, r.passed, r.ms,
                    r.passed ? "E2E prošao" : "E2E pao — vidi run na GitHubu"));
            else
                results.Add(new E2EScenarioResult(scenarioId, method, false, 0, "Nije izvršen"));
        }
        return results;
    }

    private static long ParseDurationMs(string? d)
        => TimeSpan.TryParse(d, out var ts) ? (long)ts.TotalMilliseconds : 0;

    // ─── Util ─────────────────────────────────────────────────────────────────

    private static E2ERunReport Fail(string msg) => new(false, false, "n/a", 0, 0, 0, [], null, msg);

    private static string Trim(string s) => s.Length > 4000 ? s[..4000] : s;

    // ─── GitHub API DTO-ovi ───────────────────────────────────────────────────

    private sealed record WorkflowRunsResponse(
        [property: System.Text.Json.Serialization.JsonPropertyName("workflow_runs")] List<WorkflowRun>? WorkflowRuns);

    private sealed record WorkflowRun(
        [property: System.Text.Json.Serialization.JsonPropertyName("id")] long Id,
        [property: System.Text.Json.Serialization.JsonPropertyName("name")] string? Name,
        [property: System.Text.Json.Serialization.JsonPropertyName("status")] string? Status,
        [property: System.Text.Json.Serialization.JsonPropertyName("conclusion")] string? Conclusion,
        [property: System.Text.Json.Serialization.JsonPropertyName("html_url")] string? HtmlUrl,
        [property: System.Text.Json.Serialization.JsonPropertyName("created_at")] DateTime CreatedAt);

    private sealed record ArtifactsResponse(
        [property: System.Text.Json.Serialization.JsonPropertyName("artifacts")] List<Artifact>? Artifacts);

    private sealed record Artifact(
        [property: System.Text.Json.Serialization.JsonPropertyName("id")] long Id,
        [property: System.Text.Json.Serialization.JsonPropertyName("name")] string? Name);
}
