using System.Diagnostics;
using System.Xml.Linq;
using RBBH.TestAutomation.Api.DTO;

namespace RBBH.TestAutomation.Api.Services.Run;

/// <summary>Ishod jednog scenarija izvršenog kao kompajlirani xUnit test.</summary>
public sealed record XUnitScenarioResult(
    Guid ScenarioId,
    string ClassName,
    bool Passed,
    long DurationMs,
    string? Detail);

/// <summary>
/// Izvještaj jednog <c>dotnet test</c> pokretanja generisanog xUnit projekta.
/// <see cref="Compiled"/> = da li se projekt uopće kompajlirao (build prošao).
/// </summary>
public sealed record XUnitRunReport(
    bool Compiled,
    int Passed,
    int Failed,
    long DurationMs,
    IReadOnlyList<XUnitScenarioResult> Scenarios,
    string RawOutput);

/// <summary>
/// Pravi runner opcije A: od REST scenarija sastavi <b>samostalan</b> xUnit projekt koji preko
/// <c>HttpClient</c> gađa živi API (base URL = <c>ApiUrl</c>), pokrene <c>dotnet test</c> kao
/// zaseban proces i parsira TRX. Ne treba izvorni kod API-ja — samo .NET SDK na mašini.
/// Generisani kod se stvarno kompajlira i izvršava kao xUnit (nije simulacija).
/// </summary>
public interface IXUnitTestRunner
{
    Task<XUnitRunReport> RunAsync(IReadOnlyList<ScenarioDto> scenarios, CancellationToken ct = default);
}

public sealed class XUnitTestRunner(
    IConfiguration config,
    ILogger<XUnitTestRunner> logger) : IXUnitTestRunner
{
    public async Task<XUnitRunReport> RunAsync(IReadOnlyList<ScenarioDto> scenarios, CancellationToken ct = default)
    {
        var rest = scenarios.Where(s => s.Rest is not null).ToList();
        if (rest.Count == 0)
            return new XUnitRunReport(false, 0, 0, 0, [], "Nema REST scenarija za izvršavanje.");

        var baseUrl = (config["ApiUrl"] ?? "http://api:5000").TrimEnd('/');
        var workDir = Path.Combine(Path.GetTempPath(), $"testforge_run_{Guid.NewGuid():N}");
        Directory.CreateDirectory(workDir);

        try
        {
            // ── 1. Generiši samostalan xUnit projekt (jedna klasa po scenariju) ──
            var classToScenario = new Dictionary<string, Guid>(StringComparer.Ordinal);
            var usedNames = new HashSet<string>(StringComparer.Ordinal);

            foreach (var s in rest)
            {
                var className = UniqueClassName(s.Naziv, usedNames);
                classToScenario[$"{className}Tests"] = s.Id;
                await File.WriteAllTextAsync(
                    Path.Combine(workDir, $"{className}Tests.cs"),
                    BuildTestClass(className, s.Rest!, baseUrl), ct);
            }

            await File.WriteAllTextAsync(Path.Combine(workDir, "GeneratedTests.csproj"), BuildCsproj(), ct);

            // ── 2. dotnet test ─────────────────────────────────────────────────
            var output = await RunDotnetTestAsync(workDir, ct);

            // ── 3. Parsiraj TRX ────────────────────────────────────────────────
            var trx = Directory.EnumerateFiles(workDir, "*.trx", SearchOption.AllDirectories).FirstOrDefault();
            if (trx is null)
                return new XUnitRunReport(false, 0, 0, 0, [], Trim(output)); // nema TRX → build pao

            var results = ParseTrx(trx, classToScenario, rest);
            var passed  = results.Count(r => r.Passed);
            var failed  = results.Count - passed;
            var durMs   = results.Sum(r => r.DurationMs);

            return new XUnitRunReport(true, passed, failed, durMs, results, Trim(output));
        }
        catch (OperationCanceledException) { throw; }
        catch (Exception ex)
        {
            logger.LogError(ex, "Greška pri izvršavanju xUnit runnera");
            return new XUnitRunReport(false, 0, 0, 0, [], ex.Message);
        }
        finally
        {
            try { Directory.Delete(workDir, recursive: true); } catch { /* best-effort cleanup */ }
        }
    }

    // ─── Generisanje koda ────────────────────────────────────────────────────

    private static string BuildTestClass(string className, RestScenarioDto rest, string baseUrl)
    {
        var method = rest.Metoda.ToString().ToUpperInvariant();
        var sb = new System.Text.StringBuilder();

        sb.Append("using System.Net;\n");
        sb.Append("using System.Text;\n");
        sb.Append("using Xunit;\n\n");
        sb.Append("namespace GeneratedTests;\n\n");
        sb.Append($"public class {className}Tests\n");
        sb.Append("{\n");
        sb.Append($"    private static readonly HttpClient _client = new() {{ BaseAddress = new Uri(\"{baseUrl}\") }};\n\n");
        sb.Append("    [Fact]\n");
        sb.Append($"    public async Task {className}_OcekivaniStatus_{rest.OcekivaniStatus}()\n");
        sb.Append("    {\n");
        sb.Append($"        using var req = new HttpRequestMessage(new HttpMethod(\"{method}\"), \"{rest.Url}\");\n");

        foreach (var h in rest.Headeri.Where(h => !string.Equals(h.Kljuc, "Content-Type", StringComparison.OrdinalIgnoreCase)))
            sb.Append($"        req.Headers.TryAddWithoutValidation({Lit(h.Kljuc)}, {Lit(h.Vrijednost)});\n");

        if (rest.RequestBody is not null)
        {
            var contentType = rest.Headeri.FirstOrDefault(h =>
                string.Equals(h.Kljuc, "Content-Type", StringComparison.OrdinalIgnoreCase))?.Vrijednost ?? "application/json";
            sb.Append($"        req.Content = new StringContent({Lit(rest.RequestBody)}, Encoding.UTF8, {Lit(contentType)});\n");
        }

        sb.Append("        var response = await _client.SendAsync(req);\n");
        sb.Append($"        Assert.Equal((HttpStatusCode){rest.OcekivaniStatus}, response.StatusCode);\n");
        sb.Append("    }\n");
        sb.Append("}\n");
        return sb.ToString();
    }

    private static string BuildCsproj() => """
        <Project Sdk="Microsoft.NET.Sdk">
          <PropertyGroup>
            <TargetFramework>net10.0</TargetFramework>
            <Nullable>enable</Nullable>
            <ImplicitUsings>enable</ImplicitUsings>
            <IsPackable>false</IsPackable>
            <IsTestProject>true</IsTestProject>
          </PropertyGroup>
          <ItemGroup>
            <PackageReference Include="Microsoft.NET.Test.Sdk"        Version="18.0.1" />
            <PackageReference Include="xunit"                          Version="2.9.3" />
            <PackageReference Include="xunit.runner.visualstudio"      Version="3.1.5">
              <PrivateAssets>all</PrivateAssets>
            </PackageReference>
          </ItemGroup>
        </Project>
        """;

    // ─── dotnet test proces ──────────────────────────────────────────────────

    private async Task<string> RunDotnetTestAsync(string workDir, CancellationToken ct)
    {
        var psi = new ProcessStartInfo("dotnet")
        {
            WorkingDirectory       = workDir,
            RedirectStandardOutput = true,
            RedirectStandardError  = true,
            UseShellExecute        = false,
        };
        psi.ArgumentList.Add("test");
        psi.ArgumentList.Add("--nologo");
        psi.ArgumentList.Add("--logger");
        psi.ArgumentList.Add("trx;LogFileName=results.trx");

        using var proc = new Process { StartInfo = psi };
        var sb = new System.Text.StringBuilder();
        proc.OutputDataReceived += (_, e) => { if (e.Data is not null) sb.AppendLine(e.Data); };
        proc.ErrorDataReceived  += (_, e) => { if (e.Data is not null) sb.AppendLine(e.Data); };

        proc.Start();
        proc.BeginOutputReadLine();
        proc.BeginErrorReadLine();
        await proc.WaitForExitAsync(ct);
        return sb.ToString();
    }

    // ─── TRX parsiranje ──────────────────────────────────────────────────────

    private static List<XUnitScenarioResult> ParseTrx(
        string trxPath,
        IReadOnlyDictionary<string, Guid> classToScenario,
        IReadOnlyList<ScenarioDto> scenarios)
    {
        var doc = XDocument.Load(trxPath);
        XName N(string n) => XName.Get(n, "http://microsoft.com/schemas/VisualStudio/TeamTest/2010");

        var byClass = new Dictionary<string, (bool passed, long ms)>(StringComparer.Ordinal);

        foreach (var utr in doc.Descendants(N("UnitTestResult")))
        {
            var testName = utr.Attribute("testName")?.Value ?? "";
            var outcome  = utr.Attribute("outcome")?.Value ?? "";
            var passed   = outcome.Equals("Passed", StringComparison.OrdinalIgnoreCase);
            var ms       = ParseDurationMs(utr.Attribute("duration")?.Value);

            var parts = testName.Split('.');
            var cls   = parts.Length >= 2 ? parts[^2] : testName;
            byClass[cls] = (passed, ms);
        }

        var results = new List<XUnitScenarioResult>();
        foreach (var (clsTests, scenarioId) in classToScenario)
        {
            if (byClass.TryGetValue(clsTests, out var r))
                results.Add(new XUnitScenarioResult(scenarioId, clsTests, r.passed, r.ms,
                    r.passed ? "Očekivani status potvrđen" : "Status se ne poklapa"));
            else
                results.Add(new XUnitScenarioResult(scenarioId, clsTests, false, 0, "Nije izvršen"));
        }
        return results;
    }

    private static long ParseDurationMs(string? d)
        => TimeSpan.TryParse(d, out var ts) ? (long)ts.TotalMilliseconds : 0;

    // ─── Util ────────────────────────────────────────────────────────────────

    private static string UniqueClassName(string scenarioName, HashSet<string> used)
    {
        var baseName = ToPascalCase(scenarioName);
        var name = baseName;
        var i = 2;
        while (!used.Add(name))
            name = $"{baseName}{i++}";
        return name;
    }

    private static string ToPascalCase(string input)
    {
        if (string.IsNullOrWhiteSpace(input)) return "Endpoint";
        var parts = input.Split([' ', '_', '-', '/'], StringSplitOptions.RemoveEmptyEntries);
        var pascal = string.Concat(parts.Select(p =>
            p.Length == 0 ? p : char.ToUpperInvariant(p[0]) + p[1..]));
        var clean = new string(pascal.Where(char.IsLetterOrDigit).ToArray());
        if (clean.Length == 0) return "Endpoint";
        return char.IsDigit(clean[0]) ? "E" + clean : clean;
    }

    /// <summary>Proizvoljan string → validan C# string literal (escape \, ", kontrolnih znakova).</summary>
    private static string Lit(string value)
    {
        var sb = new System.Text.StringBuilder(value.Length + 2);
        sb.Append('"');
        foreach (var c in value)
        {
            sb.Append(c switch
            {
                '\\' => "\\\\",
                '"'  => "\\\"",
                '\r' => "\\r",
                '\n' => "\\n",
                '\t' => "\\t",
                _    => c.ToString(),
            });
        }
        sb.Append('"');
        return sb.ToString();
    }

    private static string Trim(string s)
        => s.Length > 8000 ? s[^8000..] : s;
}
