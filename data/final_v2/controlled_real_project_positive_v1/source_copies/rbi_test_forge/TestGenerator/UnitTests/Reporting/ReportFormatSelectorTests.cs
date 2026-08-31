using RBBH.TestAutomation.Api.Services.Ci;
using RBBH.TestAutomation.Core.Reporting;
using Xunit;

namespace UnitTests.Reporting;

/// <summary>
/// Testovi za <see cref="ReportFormatSelector"/> — parsiranje formata iz rute i izbor
/// formattera. Ključno: numeričke/nedefinirane vrijednosti se ODBIJAJU (inače bi endpoint
/// pao na HTTP 500 umjesto da vrati 400).
/// </summary>
public class ReportFormatSelectorTests
{
    private static readonly IRunReportFormatter[] AllFormatters =
    [
        new JUnitReportFormatter(),
        new TrxReportFormatter(),
        new HtmlReportFormatter(),
        new JsonReportFormatter(),
    ];

    [Theory]
    [InlineData("junit", RunReportFormat.Junit)]
    [InlineData("JUNIT", RunReportFormat.Junit)]   // case-insensitive
    [InlineData("trx", RunReportFormat.Trx)]
    [InlineData("html", RunReportFormat.Html)]
    [InlineData("json", RunReportFormat.Json)]
    public void TryResolve_ValidanFormat_VracaTrueITacanFormatter(string format, RunReportFormat expected)
    {
        var ok = ReportFormatSelector.TryResolve(format, AllFormatters, out var fmt, out var formatter);

        Assert.True(ok);
        Assert.Equal(expected, fmt);
        Assert.NotNull(formatter);
        Assert.Equal(expected, formatter.Format);
    }

    [Theory]
    [InlineData("99")]     // numerička vrijednost — Enum.TryParse je inače prihvata!
    [InlineData("5")]
    [InlineData("-1")]
    [InlineData("xml")]    // nepostojeći format
    [InlineData("")]
    [InlineData(null)]
    public void TryResolve_NevalidanIliNumerickiFormat_VracaFalse(string? format)
    {
        var ok = ReportFormatSelector.TryResolve(format, AllFormatters, out _, out var formatter);

        Assert.False(ok);
        Assert.Null(formatter);
    }

    [Fact]
    public void TryResolve_FormatterNijeRegistrovan_VracaFalse()
    {
        // Validan format, ali odgovarajući formatter nije u kolekciji (npr. DI greška) → false, ne izuzetak.
        IRunReportFormatter[] samoJson = [new JsonReportFormatter()];

        var ok = ReportFormatSelector.TryResolve("junit", samoJson, out _, out var formatter);

        Assert.False(ok);
        Assert.Null(formatter);
    }
}
