using System.Globalization;
using System.Xml.Linq;

namespace RBBH.TestAutomation.Core.Reporting;

/// <summary>
/// JUnit XML formatter — kompatibilan sa Jenkins (JUnit plugin) i GitLab CI
/// (<c>artifacts:reports:junit</c>). Testovi se grupišu po <c>Suite</c> u
/// <c>&lt;testsuite&gt;</c> elemente unutar korijenskog <c>&lt;testsuites&gt;</c>.
/// </summary>
public sealed class JUnitReportFormatter : IRunReportFormatter
{
    public RunReportFormat Format => RunReportFormat.Junit;
    public string ContentType => "application/xml";
    public string FileName(Guid jobId) => $"junit-{jobId:N}.xml";

    public string Render(RunReport report)
    {
        // Timestamp početka run-a (UTC, ISO-8601 bez offseta) — JUnit ga očekuje na svakom testsuite-u.
        var timestamp = report.StartedAt.ToUniversalTime()
            .ToString("yyyy-MM-ddTHH:mm:ss", CultureInfo.InvariantCulture);

        var suites = report.Tests
            .GroupBy(t => t.Suite)
            .Select(g => BuildSuite(g, timestamp));

        // errors="0": mi razlikujemo samo failure/skipped (nemamo infra-error kategoriju),
        // ali atribut je dio JUnit šeme i stroži parseri (GitLab) ga očekuju.
        var root = new XElement("testsuites",
            new XAttribute("name", report.RunName),
            new XAttribute("tests", report.Total),
            new XAttribute("failures", report.Failed),
            new XAttribute("errors", 0),
            new XAttribute("skipped", report.Skipped),
            new XAttribute("time", Seconds(report.DurationSeconds)),
            suites);

        return XmlReportUtil.ToXmlString(new XDocument(new XDeclaration("1.0", "utf-8", null), root));
    }

    private static XElement BuildSuite(IGrouping<string, RunReportTest> group, string timestamp)
    {
        var cases = group.Select(BuildCase);

        return new XElement("testsuite",
            new XAttribute("name", group.Key),
            new XAttribute("tests", group.Count()),
            new XAttribute("failures", group.Count(t => t.Status == RunReportStatus.Failed)),
            new XAttribute("errors", 0),
            new XAttribute("skipped", group.Count(t => t.Status == RunReportStatus.Skipped)),
            new XAttribute("time", Seconds(group.Sum(t => t.DurationSeconds))),
            new XAttribute("timestamp", timestamp),
            cases);
    }

    private static XElement BuildCase(RunReportTest test)
    {
        var element = new XElement("testcase",
            new XAttribute("name", test.Name),
            new XAttribute("classname", test.Suite),
            new XAttribute("time", Seconds(test.DurationSeconds)));

        switch (test.Status)
        {
            case RunReportStatus.Failed:
                element.Add(new XElement("failure",
                    new XAttribute("message", test.ErrorMessage ?? "Test je pao."),
                    test.ErrorDetails ?? string.Empty));
                break;

            case RunReportStatus.Skipped:
                element.Add(new XElement("skipped"));
                break;
        }

        return element;
    }

    private static string Seconds(double value) =>
        Math.Round(value, 3).ToString(CultureInfo.InvariantCulture);
}
