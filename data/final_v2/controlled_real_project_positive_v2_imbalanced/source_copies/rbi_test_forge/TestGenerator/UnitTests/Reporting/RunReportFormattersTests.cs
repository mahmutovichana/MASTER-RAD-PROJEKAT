using System.Globalization;
using System.Text.Json;
using System.Xml.Linq;
using RBBH.TestAutomation.Core.Reporting;
using Xunit;

namespace UnitTests.Reporting;

/// <summary>
/// Testovi za formattere izvještaja run-a. Dokazuju da svaki format sadrži
/// nazive testova, trajanje, status i poruke grešaka (Acceptance Criteria).
/// </summary>
public class RunReportFormattersTests
{
    private static RunReport Sample() => new(
        JobId: Guid.Parse("11111111-1111-1111-1111-111111111111"),
        RunName: "TestForge CI Run",
        StartedAt: new DateTime(2026, 6, 28, 10, 0, 0, DateTimeKind.Utc),
        CompletedAt: new DateTime(2026, 6, 28, 10, 1, 0, DateTimeKind.Utc),
        Tests:
        [
            new RunReportTest("GET /api/users", "Smoke", RunReportStatus.Passed, 0.123, null, null),
            new RunReportTest("POST /api/users", "Smoke", RunReportStatus.Failed, 0.450,
                "Očekivani status: 201, dobijeni: 500", "Response: Internal Server Error"),
            new RunReportTest("UI Login", "Regression", RunReportStatus.Skipped, 0, null, null),
        ]);

    // ─── JUnit ────────────────────────────────────────────────────────────────

    [Fact]
    public void JUnit_ProducesValidXmlWithCountsNamesAndFailure()
    {
        var content = new JUnitReportFormatter().Render(Sample());
        var doc = XDocument.Parse(content); // ne smije baciti

        Assert.Equal("testsuites", doc.Root!.Name.LocalName);
        Assert.Equal("3", doc.Root.Attribute("tests")!.Value);
        Assert.Equal("1", doc.Root.Attribute("failures")!.Value);
        Assert.Equal("1", doc.Root.Attribute("skipped")!.Value);

        var cases = doc.Descendants("testcase").ToList();
        Assert.Contains(cases, c => c.Attribute("name")!.Value == "GET /api/users");
        Assert.Contains(cases, c => c.Attribute("name")!.Value == "POST /api/users");

        var failure = doc.Descendants("failure").Single();
        Assert.Contains("500", failure.Attribute("message")!.Value);
        Assert.Single(doc.Descendants("skipped"));
    }

    [Fact]
    public void JUnit_GroupsTestsBySuite()
    {
        var content = new JUnitReportFormatter().Render(Sample());
        var doc = XDocument.Parse(content);

        var suites = doc.Descendants("testsuite").Select(s => s.Attribute("name")!.Value).ToList();
        Assert.Contains("Smoke", suites);
        Assert.Contains("Regression", suites);
    }

    [Fact]
    public void JUnit_IncludesErrorsAndTimestampAttributes()
    {
        var content = new JUnitReportFormatter().Render(Sample());
        var doc = XDocument.Parse(content);

        // errors atribut na korijenu i na svakom testsuite-u (JUnit šema / GitLab parser).
        Assert.Equal("0", doc.Root!.Attribute("errors")!.Value);
        Assert.All(doc.Descendants("testsuite"), s => Assert.Equal("0", s.Attribute("errors")!.Value));

        // timestamp na svakom testsuite-u u ISO-8601 formatu (početak run-a).
        Assert.All(doc.Descendants("testsuite"),
            s => Assert.Equal("2026-06-28T10:00:00", s.Attribute("timestamp")!.Value));
    }

    // ─── TRX ──────────────────────────────────────────────────────────────────

    [Fact]
    public void Trx_ProducesValidXmlWithLinkedIdsAndOutcomes()
    {
        var content = new TrxReportFormatter().Render(Sample());
        XNamespace ns = "http://microsoft.com/schemas/VisualStudio/TeamTest/2010";
        var doc = XDocument.Parse(content);

        Assert.Equal("TestRun", doc.Root!.Name.LocalName);

        var counters = doc.Descendants(ns + "Counters").Single();
        Assert.Equal("3", counters.Attribute("total")!.Value);
        Assert.Equal("1", counters.Attribute("passed")!.Value);
        Assert.Equal("1", counters.Attribute("failed")!.Value);
        Assert.Equal("1", counters.Attribute("notExecuted")!.Value);

        var outcomes = doc.Descendants(ns + "UnitTestResult")
            .Select(r => r.Attribute("outcome")!.Value).ToList();
        Assert.Contains("Passed", outcomes);
        Assert.Contains("Failed", outcomes);
        Assert.Contains("NotExecuted", outcomes);

        // testId iz UnitTestResult mora postojati u TestDefinitions/UnitTest (konzistentne veze).
        var defIds = doc.Descendants(ns + "UnitTest").Select(u => u.Attribute("id")!.Value).ToHashSet();
        foreach (var resultId in doc.Descendants(ns + "UnitTestResult").Select(r => r.Attribute("testId")!.Value))
            Assert.Contains(resultId, defIds);
    }

    [Fact]
    public void Trx_FailedResult_ContainsErrorMessage()
    {
        var content = new TrxReportFormatter().Render(Sample());
        XNamespace ns = "http://microsoft.com/schemas/VisualStudio/TeamTest/2010";
        var doc = XDocument.Parse(content);

        var message = doc.Descendants(ns + "Message").Single().Value;
        Assert.Contains("500", message);
    }

    // ─── HTML ─────────────────────────────────────────────────────────────────

    [Fact]
    public void Html_IsStandaloneAndContainsTestData()
    {
        var content = new HtmlReportFormatter().Render(Sample());

        Assert.StartsWith("<!DOCTYPE html>", content.TrimStart());
        Assert.Contains("GET /api/users", content);
        Assert.Contains("POST /api/users", content);
        Assert.Contains("Failed", content);
        Assert.Contains("500", content); // poruka greške
        Assert.DoesNotContain("<link", content); // bez vanjskih resursa
    }

    // ─── JSON ─────────────────────────────────────────────────────────────────

    [Fact]
    public void Json_RoundTripsSummaryAndTests()
    {
        var content = new JsonReportFormatter().Render(Sample());
        using var doc = JsonDocument.Parse(content);
        var root = doc.RootElement;

        var summary = root.GetProperty("summary");
        Assert.Equal(3, summary.GetProperty("total").GetInt32());
        Assert.Equal(1, summary.GetProperty("passed").GetInt32());
        Assert.Equal(1, summary.GetProperty("failed").GetInt32());
        Assert.Equal(1, summary.GetProperty("skipped").GetInt32());

        var tests = root.GetProperty("tests");
        Assert.Equal(3, tests.GetArrayLength());

        var failed = tests.EnumerateArray().Single(t => t.GetProperty("status").GetString() == "Failed");
        Assert.Equal("POST /api/users", failed.GetProperty("name").GetString());
        Assert.Contains("500", failed.GetProperty("errorMessage").GetString()!);
    }

    // ─── Metapodaci ─────────────────────────────────────────────────────────

    [Theory]
    [InlineData(typeof(JUnitReportFormatter), RunReportFormat.Junit)]
    [InlineData(typeof(TrxReportFormatter), RunReportFormat.Trx)]
    [InlineData(typeof(HtmlReportFormatter), RunReportFormat.Html)]
    [InlineData(typeof(JsonReportFormatter), RunReportFormat.Json)]
    public void Formatter_ExposesCorrectFormatAndFileName(Type type, RunReportFormat expected)
    {
        var formatter = (IRunReportFormatter)Activator.CreateInstance(type)!;

        Assert.Equal(expected, formatter.Format);
        Assert.False(string.IsNullOrWhiteSpace(formatter.ContentType));
        Assert.Contains(Sample().JobId.ToString("N"), formatter.FileName(Sample().JobId));
    }

    // ─── Rubni slučajevi ──────────────────────────────────────────────────────

    private static RunReport Empty() => new(
        JobId: Guid.Parse("22222222-2222-2222-2222-222222222222"),
        RunName: "Prazan run",
        StartedAt: new DateTime(2026, 6, 28, 10, 0, 0, DateTimeKind.Utc),
        CompletedAt: new DateTime(2026, 6, 28, 10, 0, 0, DateTimeKind.Utc),
        Tests: []);

    public static IEnumerable<object[]> AllFormatters() =>
    [
        [new JUnitReportFormatter()],
        [new TrxReportFormatter()],
        [new HtmlReportFormatter()],
        [new JsonReportFormatter()],
    ];

    [Theory]
    [MemberData(nameof(AllFormatters))]
    public void Formatter_HandlesEmptyReport_WithoutError(IRunReportFormatter formatter)
    {
        // 0 testova ne smije baciti (npr. dijeljenje nulom u pass rate) i mora dati validan sadržaj.
        var content = formatter.Render(Empty());
        Assert.False(string.IsNullOrWhiteSpace(content));

        // XML formati (JUnit/TRX) moraju ostati parsabilni i s praznim skupom testova.
        if (formatter is JUnitReportFormatter or TrxReportFormatter)
            _ = XDocument.Parse(content); // ne smije baciti
    }

    [Theory]
    [MemberData(nameof(AllFormatters))]
    public void Formatter_EscapesSpecialCharacters(IRunReportFormatter formatter)
    {
        // Naziv/greška sa XML/HTML meta-znakovima ne smije proizvesti nevalidan output.
        var report = new RunReport(
            Guid.NewGuid(), "Run <\"&\">",
            new DateTime(2026, 6, 28, 10, 0, 0, DateTimeKind.Utc), null,
            [
                new RunReportTest("GET /a?x=1&y=2 <script>", "Suite & <b>", RunReportStatus.Failed,
                    0.1, "poruka \"<greška>\" & kraj", "detalji <tag> & \"navodnici\""),
            ]);

        var content = formatter.Render(report);

        // XML mora ostati validan (auto-escaping kroz XElement).
        if (formatter is JUnitReportFormatter or TrxReportFormatter)
            _ = XDocument.Parse(content);

        // HTML ne smije sadržavati sirov <script> — mora biti HTML-enkodiran.
        if (formatter is HtmlReportFormatter)
            Assert.DoesNotContain("<script>", content);

        // JSON mora ostati parsabilan.
        if (formatter is JsonReportFormatter)
        {
            using var json = JsonDocument.Parse(content);
        }
    }

    [Theory]
    [MemberData(nameof(AllFormatters))]
    public void Formatter_IsCultureInvariant(IRunReportFormatter formatter)
    {
        // Server može raditi na kulturi s decimalnim zarezom (bs-BA, de-DE). Trajanja u
        // izvještajima MORAJU koristiti decimalnu tačku (invariant), inače Jenkins/GitLab
        // pogrešno parsiraju "0,573" kao vrijeme.
        var original = CultureInfo.CurrentCulture;
        try
        {
            CultureInfo.CurrentCulture = new CultureInfo("de-DE");
            var content = formatter.Render(Sample());

            Assert.DoesNotContain("0,123", content); // zarez se ne smije pojaviti u trajanju
            Assert.Contains("0.123", content);        // tačka mora
        }
        finally
        {
            CultureInfo.CurrentCulture = original;
        }
    }
}
