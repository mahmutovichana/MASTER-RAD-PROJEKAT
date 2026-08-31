using System.Text;
using RBBH.TestAutomation.Api.DTO;

namespace RBBH.TestAutomation.Api.Services.Run;

/// <summary>
/// Sastavlja <b>jedan</b> samostalan Playwright (.NET + xUnit) test fajl iz UI scenarija.
/// Svaki scenarij → jedna <c>[Fact]</c> metoda; koraci (<see cref="UiKorakDto"/>) se mapiraju
/// na Playwright akcije. Fajl se šalje kao base64 input na GitHub Actions (workflow_dispatch),
/// gdje se kompajlira i pokrene protiv živog deploya (BASE_URL env).
/// </summary>
public static class UiScenarioPlaywrightBuilder
{
    /// <summary>Rezultat sastavljanja: sadržaj .cs fajla + mapa naziva metode → scenarioId (za TRX korelaciju).</summary>
    public sealed record Built(string TestFileContent, IReadOnlyDictionary<string, Guid> MethodToScenario);

    /// <summary>
    /// Generiše test klasu iz UI scenarija. <c>{{baseUrl}}</c> token u URL-u stranice se
    /// razrješava u runtime-u iz <c>BASE_URL</c> env varijable (postavlja je workflow).
    /// </summary>
    public static Built Build(IReadOnlyList<ScenarioDto> uiScenarios)
    {
        var methodToScenario = new Dictionary<string, Guid>(StringComparer.Ordinal);
        var usedNames = new HashSet<string>(StringComparer.Ordinal);

        var body = new StringBuilder();

        foreach (var s in uiScenarios)
        {
            if (s.Ui is null) continue;

            var method = UniqueName($"Scenario_{ToPascalCase(s.Naziv)}", usedNames);
            methodToScenario[method] = s.Id;

            body.AppendLine("    [Fact]");
            body.AppendLine($"    public async Task {method}()");
            body.AppendLine("    {");
            body.AppendLine("        var (browser, page) = await NewPageAsync();");
            body.AppendLine("        try");
            body.AppendLine("        {");
            // NE koristi WaitForLoadStateAsync(NetworkIdle): Blazor Server drži trajni SignalR
            // WebSocket pa mreža nikad nije idle → 30s timeout. GotoAsync po defaultu čeka 'load',
            // a locator akcije (Klik/Expect) same auto-čekaju da se element pojavi (circuit render).
            body.AppendLine($"            await page.GotoAsync({UrlExpr(s.Ui.UrlStranice)});");

            foreach (var k in s.Ui.Koraci)
                body.AppendLine("            " + StepToPlaywright(k));

            body.AppendLine("        }");
            body.AppendLine("        finally");
            body.AppendLine("        {");
            body.AppendLine("            await browser.DisposeAsync();");
            body.AppendLine("        }");
            body.AppendLine("    }");
            body.AppendLine();
        }

        var sb = new StringBuilder();
        sb.AppendLine("using Microsoft.Playwright;");
        sb.AppendLine("using Xunit;");
        sb.AppendLine();
        sb.AppendLine("namespace GeneratedE2E;");
        sb.AppendLine();
        sb.AppendLine("public class ScenarioE2eTests");
        sb.AppendLine("{");
        sb.AppendLine("    // BASE_URL postavlja GitHub workflow (npr. https://tag.rbbh-test-automation.local).");
        sb.AppendLine("    private static string BaseUrl =>");
        sb.AppendLine("        (Environment.GetEnvironmentVariable(\"BASE_URL\") ?? \"http://localhost:5000\").TrimEnd('/');");
        sb.AppendLine();
        sb.AppendLine("    private static async Task<(IBrowser browser, IPage page)> NewPageAsync()");
        sb.AppendLine("    {");
        sb.AppendLine("        var pw = await Playwright.CreateAsync();");
        sb.AppendLine("        var browser = await pw.Chromium.LaunchAsync(new BrowserTypeLaunchOptions { Headless = true });");
        sb.AppendLine("        // IgnoreHTTPSErrors: interni/staging hostovi (npr. nip.io) često imaju cert koji ne");
        sb.AppendLine("        // matcha hostname — funkcionalni E2E ne smije padati zbog toga (ERR_CERT_COMMON_NAME_INVALID).");
        sb.AppendLine("        var page = await browser.NewPageAsync(new BrowserNewPageOptions { IgnoreHTTPSErrors = true });");
        sb.AppendLine("        return (browser, page);");
        sb.AppendLine("    }");
        sb.AppendLine();
        sb.Append(body);
        sb.AppendLine("}");

        return new Built(sb.ToString(), methodToScenario);
    }

    // ─── Mapiranje koraka ────────────────────────────────────────────────────

    private static string StepToPlaywright(UiKorakDto k)
    {
        var sel = k.Selektor ?? "";
        return k.Akcija switch
        {
            UiAkcija.Klik           => $"await page.Locator({Lit(sel)}).ClickAsync();",
            UiAkcija.Upis           => $"await page.Locator({Lit(sel)}).FillAsync({Lit(k.Vrijednost ?? "")});",
            UiAkcija.OcekujTekst    => string.IsNullOrWhiteSpace(sel)
                                        ? $"await Assertions.Expect(page.GetByText({Lit(k.OcekivaniTekst ?? "")}).First).ToBeVisibleAsync();"
                                        : $"await Assertions.Expect(page.Locator({Lit(sel)})).ToContainTextAsync({Lit(k.OcekivaniTekst ?? "")});",
            UiAkcija.OcekujElement  => $"await Assertions.Expect(page.Locator({Lit(sel)})).ToBeVisibleAsync();",
            _                       => "// nepoznata akcija — preskočena",
        };
    }

    // {{baseUrl}} token → BaseUrl + putanja (runtime). Apsolutni URL bez tokena → literal.
    private static string UrlExpr(string? url)
    {
        var raw = (url ?? "").Trim();
        if (raw.Contains("{{baseUrl}}", StringComparison.OrdinalIgnoreCase))
        {
            var path = System.Text.RegularExpressions.Regex.Replace(raw, "{{baseUrl}}", "",
                System.Text.RegularExpressions.RegexOptions.IgnoreCase);
            return $"BaseUrl + {Lit(EnsureLeadingSlash(path))}";
        }
        if (raw.StartsWith("http://", StringComparison.OrdinalIgnoreCase) ||
            raw.StartsWith("https://", StringComparison.OrdinalIgnoreCase))
            return Lit(raw);
        return $"BaseUrl + {Lit(EnsureLeadingSlash(raw))}";
    }

    private static string EnsureLeadingSlash(string p)
        => string.IsNullOrEmpty(p) ? "/" : (p.StartsWith('/') ? p : "/" + p);

    // ─── Util (isti stil kao XUnitTestRunner) ────────────────────────────────

    private static string UniqueName(string baseName, HashSet<string> used)
    {
        var name = baseName;
        var i = 2;
        while (!used.Add(name))
            name = $"{baseName}{i++}";
        return name;
    }

    private static string ToPascalCase(string input)
    {
        if (string.IsNullOrWhiteSpace(input)) return "Scenarij";
        var parts = input.Split([' ', '_', '-', '/'], StringSplitOptions.RemoveEmptyEntries);
        var pascal = string.Concat(parts.Select(p =>
            p.Length == 0 ? p : char.ToUpperInvariant(p[0]) + p[1..]));
        var clean = new string(pascal.Where(char.IsLetterOrDigit).ToArray());
        if (clean.Length == 0) return "Scenarij";
        return char.IsDigit(clean[0]) ? "S" + clean : clean;
    }

    private static string Lit(string value)
    {
        var sb = new StringBuilder(value.Length + 2);
        sb.Append('"');
        foreach (var c in value)
            sb.Append(c switch
            {
                '\\' => "\\\\",
                '"'  => "\\\"",
                '\r' => "\\r",
                '\n' => "\\n",
                '\t' => "\\t",
                _    => c.ToString(),
            });
        sb.Append('"');
        return sb.ToString();
    }
}
