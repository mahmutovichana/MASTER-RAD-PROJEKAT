using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Api.Services.Scenarios;

namespace UnitTests.Scenariji;

/// <summary>
/// Unit testovi za <see cref="ScenarioVariableResolver"/>.
///
/// Pokriva AC4 (zamjena varijabli) i AC6 (upozorenja o nerazriješenim tokenima):
///   Resolve  — zamjena poznatih, čuvanje nepoznatih, whitespace, case-insensitivnost, null/prazan
///   ExtractTokens — izvlačenje svih naziva, deduplikacija
///   FindUnknownTokens — samo nerazriješene varijable
/// </summary>
public class ScenarioVariableResolverTests
{
    private static RunConfigDto Config(params (string Naziv, string Vrijednost)[] varijable) =>
        new(varijable.Select(v => new RunVariableDto(v.Naziv, v.Vrijednost)).ToList());

    private static readonly RunConfigDto DevConfig = Config(
        ("baseUrl", "https://api.dev.local"),
        ("token",   "mock-jwt-abc"),
        ("userId",  "42")
    );

    // ═══════════════════════════════════════════════════════════════════════════
    // Resolve
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public void Resolve_ZamjenjujePoznateTokene()
    {
        var result = ScenarioVariableResolver.Resolve("{{baseUrl}}/api/health", DevConfig);
        Assert.Equal("https://api.dev.local/api/health", result);
    }

    [Fact]
    public void Resolve_ZamjenjujeViseTokenaURijeci()
    {
        var result = ScenarioVariableResolver.Resolve("{{baseUrl}}/users/{{userId}}", DevConfig);
        Assert.Equal("https://api.dev.local/users/42", result);
    }

    [Fact]
    public void Resolve_NepoznatTokenOstajeDoSlovan()
    {
        var result = ScenarioVariableResolver.Resolve("{{nepostojeca}}", DevConfig);
        Assert.Equal("{{nepostojeca}}", result);
    }

    [Fact]
    public void Resolve_MjesovitoPoznatoNepoznato()
    {
        var result = ScenarioVariableResolver.Resolve("{{baseUrl}}/{{nepostojeca}}", DevConfig);
        Assert.Equal("https://api.dev.local/{{nepostojeca}}", result);
    }

    [Fact]
    public void Resolve_WhitespacUnutarZagrada()
    {
        var result = ScenarioVariableResolver.Resolve("{{ baseUrl }}/test", DevConfig);
        Assert.Equal("https://api.dev.local/test", result);
    }

    [Fact]
    public void Resolve_CaseInsensitivanNaziv()
    {
        var result = ScenarioVariableResolver.Resolve("{{BASEURL}}/test", DevConfig);
        Assert.Equal("https://api.dev.local/test", result);
    }

    [Fact]
    public void Resolve_NullTemplate_VracaPrazanString()
    {
        var result = ScenarioVariableResolver.Resolve(null, DevConfig);
        Assert.Equal(string.Empty, result);
    }

    [Fact]
    public void Resolve_PrazanTemplate_VracaPrazanString()
    {
        var result = ScenarioVariableResolver.Resolve("", DevConfig);
        Assert.Equal(string.Empty, result);
    }

    [Fact]
    public void Resolve_BezTokena_VracaOriginalanTekst()
    {
        const string tekst = "Nema varijabli ovdje.";
        var result = ScenarioVariableResolver.Resolve(tekst, DevConfig);
        Assert.Equal(tekst, result);
    }

    [Fact]
    public void Resolve_PraznaKonfiguracija_CuvaTokene()
    {
        var result = ScenarioVariableResolver.Resolve("{{token}}", Config());
        Assert.Equal("{{token}}", result);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // ExtractTokens
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public void ExtractTokens_VracaSvaImena()
    {
        var tokeni = ScenarioVariableResolver.ExtractTokens("{{baseUrl}}/users/{{userId}}");
        Assert.Contains("baseUrl", tokeni);
        Assert.Contains("userId",  tokeni);
        Assert.Equal(2, tokeni.Count);
    }

    [Fact]
    public void ExtractTokens_DedupliciraDuplikate()
    {
        var tokeni = ScenarioVariableResolver.ExtractTokens("{{token}} i {{token}}");
        Assert.Single(tokeni);
        Assert.Equal("token", tokeni[0]);
    }

    [Fact]
    public void ExtractTokens_BezTokena_VracaPraznoList()
    {
        var tokeni = ScenarioVariableResolver.ExtractTokens("Nema tokena.");
        Assert.Empty(tokeni);
    }

    [Fact]
    public void ExtractTokens_NullTemplate_VracaPraznoList()
    {
        var tokeni = ScenarioVariableResolver.ExtractTokens(null);
        Assert.Empty(tokeni);
    }

    [Fact]
    public void ExtractTokens_WhitespacUnutarZagrada_TrimujeIme()
    {
        var tokeni = ScenarioVariableResolver.ExtractTokens("{{ baseUrl }}");
        Assert.Single(tokeni);
        Assert.Equal("baseUrl", tokeni[0]);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // FindUnknownTokens
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public void FindUnknownTokens_VracaSamoNerazrijesen()
    {
        var nepoznati = ScenarioVariableResolver.FindUnknownTokens(
            "{{baseUrl}}/{{nepostoji}}", DevConfig);

        Assert.Single(nepoznati);
        Assert.Equal("nepostoji", nepoznati[0]);
    }

    [Fact]
    public void FindUnknownTokens_SviPoznati_VracaPraznoList()
    {
        var nepoznati = ScenarioVariableResolver.FindUnknownTokens(
            "{{baseUrl}}/{{token}}", DevConfig);

        Assert.Empty(nepoznati);
    }

    [Fact]
    public void FindUnknownTokens_NullTemplate_VracaPraznoList()
    {
        var nepoznati = ScenarioVariableResolver.FindUnknownTokens(null, DevConfig);
        Assert.Empty(nepoznati);
    }

    [Fact]
    public void FindUnknownTokens_PraznaKonfiguracija_VracaSveTokene()
    {
        var nepoznati = ScenarioVariableResolver.FindUnknownTokens("{{baseUrl}}/{{token}}", Config());
        Assert.Equal(2, nepoznati.Count);
    }
}
