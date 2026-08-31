using System.Globalization;
using System.Net;
using System.Text;

namespace RBBH.TestAutomation.Core.Reporting;

/// <summary>
/// Samostalni HTML formatter — jedna stranica s inline CSS-om (bez vanjskih resursa),
/// pogodna za dijeljenje. Sadrži sažetak (brojači, pass rate) i tabelu testova s
/// nazivom, suite-om, statusom, trajanjem i porukom greške.
/// </summary>
public sealed class HtmlReportFormatter : IRunReportFormatter
{
    public RunReportFormat Format => RunReportFormat.Html;
    public string ContentType => "text/html; charset=utf-8";
    public string FileName(Guid jobId) => $"run-{jobId:N}.html";

    public string Render(RunReport report)
    {
        var sb = new StringBuilder();

        sb.AppendLine("<!DOCTYPE html>");
        sb.AppendLine("<html lang=\"bs\"><head><meta charset=\"utf-8\">");
        sb.AppendLine($"<title>{E(report.RunName)}</title>");
        sb.AppendLine("<style>");
        sb.AppendLine(Css);
        sb.AppendLine("</style></head><body>");

        sb.AppendLine("<div class=\"wrap\">");
        sb.AppendLine($"<h1>{E(report.RunName)}</h1>");
        sb.AppendLine($"<p class=\"meta\">Job: {report.JobId} &middot; Početak: {report.StartedAt:yyyy-MM-dd HH:mm:ss} UTC" +
                      (report.CompletedAt is { } c ? $" &middot; Kraj: {c:yyyy-MM-dd HH:mm:ss} UTC" : "") + "</p>");

        // Sažetak
        sb.AppendLine("<div class=\"cards\">");
        sb.AppendLine(Card("Ukupno", report.Total, "total"));
        sb.AppendLine(Card("Prošlo", report.Passed, "passed"));
        sb.AppendLine(Card("Palo", report.Failed, "failed"));
        sb.AppendLine(Card("Preskočeno", report.Skipped, "skipped"));
        sb.AppendLine(Card("Pass rate", $"{report.PassRate.ToString(CultureInfo.InvariantCulture)}%", "rate"));
        sb.AppendLine($"<div class=\"card\"><div class=\"num\">{Secs(report.DurationSeconds)}s</div><div class=\"lbl\">Trajanje</div></div>");
        sb.AppendLine("</div>");

        // Tabela
        sb.AppendLine("<table><thead><tr>" +
                      "<th>Test</th><th>Suite</th><th>Status</th><th class=\"r\">Trajanje (s)</th><th>Greška</th>" +
                      "</tr></thead><tbody>");

        foreach (var t in report.Tests)
        {
            var badge = t.Status switch
            {
                RunReportStatus.Passed => "<span class=\"b pass\">Passed</span>",
                RunReportStatus.Failed => "<span class=\"b fail\">Failed</span>",
                _ => "<span class=\"b skip\">Skipped</span>",
            };

            var error = t.Status == RunReportStatus.Failed
                ? $"<div class=\"err\">{E(t.ErrorMessage)}</div>" +
                  (string.IsNullOrWhiteSpace(t.ErrorDetails) ? "" : $"<pre>{E(t.ErrorDetails)}</pre>")
                : "—";

            sb.AppendLine("<tr>" +
                          $"<td>{E(t.Name)}</td>" +
                          $"<td>{E(t.Suite)}</td>" +
                          $"<td>{badge}</td>" +
                          $"<td class=\"r\">{Secs(t.DurationSeconds)}</td>" +
                          $"<td>{error}</td>" +
                          "</tr>");
        }

        sb.AppendLine("</tbody></table>");
        sb.AppendLine("<p class=\"foot\">Generisano u RBBH Test Automation aplikaciji.</p>");
        sb.AppendLine("</div></body></html>");

        return sb.ToString();
    }

    private static string Card(string label, object value, string cls) =>
        $"<div class=\"card {cls}\"><div class=\"num\">{value}</div><div class=\"lbl\">{label}</div></div>";

    private static string Secs(double value) =>
        Math.Round(value, 3).ToString(CultureInfo.InvariantCulture);

    private static string E(string? value) => WebUtility.HtmlEncode(value ?? string.Empty);

    private const string Css = """
        * { box-sizing: border-box; }
        body { font-family: -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 0; background: #f5f6f8; color: #1a1a1a; }
        .wrap { max-width: 1100px; margin: 0 auto; padding: 24px; }
        h1 { font-size: 22px; margin: 0 0 4px; }
        .meta { color: #666; font-size: 13px; margin: 0 0 20px; }
        .cards { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 20px; }
        .card { background: #fff; border: 1px solid #e3e5e8; border-radius: 8px; padding: 14px 18px; min-width: 110px; }
        .card .num { font-size: 24px; font-weight: 700; }
        .card .lbl { font-size: 12px; color: #777; text-transform: uppercase; letter-spacing: .03em; }
        .card.passed .num { color: #1a7f37; }
        .card.failed .num { color: #cf222e; }
        .card.skipped .num { color: #9a6700; }
        table { width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #e3e5e8; border-radius: 8px; overflow: hidden; }
        th, td { text-align: left; padding: 10px 14px; border-bottom: 1px solid #eef0f2; vertical-align: top; font-size: 14px; }
        th { background: #fafbfc; font-size: 12px; text-transform: uppercase; letter-spacing: .03em; color: #555; }
        td.r, th.r { text-align: right; white-space: nowrap; }
        .b { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 12px; font-weight: 600; }
        .b.pass { background: #dafbe1; color: #1a7f37; }
        .b.fail { background: #ffebe9; color: #cf222e; }
        .b.skip { background: #fff8c5; color: #9a6700; }
        .err { color: #cf222e; font-weight: 600; }
        pre { margin: 6px 0 0; padding: 8px; background: #f6f8fa; border-radius: 6px; font-size: 12px; white-space: pre-wrap; word-break: break-word; }
        .foot { color: #999; font-size: 12px; margin-top: 18px; }
        """;
}
