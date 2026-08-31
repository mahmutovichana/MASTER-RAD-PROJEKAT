using System.Globalization;
using System.Xml.Linq;

namespace RBBH.TestAutomation.Core.Reporting;

/// <summary>
/// TRX (Visual Studio Test Results) formatter — kompatibilan sa Azure DevOps
/// <c>PublishTestResults@2</c> (format <c>VSTest</c>). Generiše konzistentne GUID veze
/// između <c>UnitTest</c> (definicija), <c>Execution</c>, <c>TestEntry</c> i <c>UnitTestResult</c>.
/// </summary>
public sealed class TrxReportFormatter : IRunReportFormatter
{
    private static readonly XNamespace Ns = "http://microsoft.com/schemas/VisualStudio/TeamTest/2010";

    // Fiksni GUID-ovi iz VSTest TRX šeme.
    private const string UnitTestType = "13cdc9d9-ddb5-4fa4-a97d-d965ccfc6d4b";
    private const string DefaultTestListId = "8c84fa94-04c1-424b-9868-57a2d4851a1d"; // "Results Not in a List"
    private const string AllLoadedListId = "19431567-8539-422a-85d7-44ee4e166bda";   // "All Loaded Results"

    public RunReportFormat Format => RunReportFormat.Trx;
    public string ContentType => "application/xml";
    public string FileName(Guid jobId) => $"run-{jobId:N}.trx";

    public string Render(RunReport report)
    {
        var start = report.StartedAt;
        var finish = report.CompletedAt ?? DateTime.UtcNow;

        var results = new List<XElement>();
        var definitions = new List<XElement>();
        var entries = new List<XElement>();

        foreach (var test in report.Tests)
        {
            var testId = Guid.NewGuid();
            var executionId = Guid.NewGuid();
            var duration = TimeSpan.FromSeconds(Math.Max(0, test.DurationSeconds));

            definitions.Add(new XElement(Ns + "UnitTest",
                new XAttribute("name", test.Name),
                new XAttribute("storage", "testforge"),
                new XAttribute("id", testId),
                new XElement(Ns + "Execution", new XAttribute("id", executionId)),
                new XElement(Ns + "TestMethod",
                    new XAttribute("codeBase", "TestForge"),
                    new XAttribute("className", test.Suite),
                    new XAttribute("name", test.Name))));

            entries.Add(new XElement(Ns + "TestEntry",
                new XAttribute("testId", testId),
                new XAttribute("executionId", executionId),
                new XAttribute("testListId", DefaultTestListId)));

            var result = new XElement(Ns + "UnitTestResult",
                new XAttribute("executionId", executionId),
                new XAttribute("testId", testId),
                new XAttribute("testName", test.Name),
                new XAttribute("computerName", Environment.MachineName),
                new XAttribute("duration", duration.ToString(@"hh\:mm\:ss\.fffffff", CultureInfo.InvariantCulture)),
                new XAttribute("startTime", Iso(start)),
                new XAttribute("endTime", Iso(start + duration)),
                new XAttribute("testType", UnitTestType),
                new XAttribute("outcome", Outcome(test.Status)),
                new XAttribute("testListId", DefaultTestListId),
                new XAttribute("relativeResultsDirectory", executionId.ToString()));

            if (test.Status == RunReportStatus.Failed)
            {
                result.Add(new XElement(Ns + "Output",
                    new XElement(Ns + "ErrorInfo",
                        new XElement(Ns + "Message", test.ErrorMessage ?? "Test je pao."),
                        new XElement(Ns + "StackTrace", test.ErrorDetails ?? string.Empty))));
            }

            results.Add(result);
        }

        var root = new XElement(Ns + "TestRun",
            new XAttribute("id", report.JobId),
            new XAttribute("name", report.RunName),
            new XAttribute("runUser", "TestForge"),
            new XElement(Ns + "Times",
                new XAttribute("creation", Iso(start)),
                new XAttribute("queuing", Iso(start)),
                new XAttribute("start", Iso(start)),
                new XAttribute("finish", Iso(finish))),
            new XElement(Ns + "Results", results),
            new XElement(Ns + "TestDefinitions", definitions),
            new XElement(Ns + "TestEntries", entries),
            new XElement(Ns + "TestLists",
                new XElement(Ns + "TestList",
                    new XAttribute("name", "Results Not in a List"),
                    new XAttribute("id", DefaultTestListId)),
                new XElement(Ns + "TestList",
                    new XAttribute("name", "All Loaded Results"),
                    new XAttribute("id", AllLoadedListId))),
            new XElement(Ns + "ResultSummary",
                new XAttribute("outcome", report.Failed > 0 ? "Failed" : "Completed"),
                new XElement(Ns + "Counters",
                    new XAttribute("total", report.Total),
                    new XAttribute("executed", report.Executed),
                    new XAttribute("passed", report.Passed),
                    new XAttribute("failed", report.Failed),
                    new XAttribute("error", 0),
                    new XAttribute("timeout", 0),
                    new XAttribute("aborted", 0),
                    new XAttribute("inconclusive", 0),
                    new XAttribute("passedButRunAborted", 0),
                    new XAttribute("notRunnable", 0),
                    new XAttribute("notExecuted", report.Skipped),
                    new XAttribute("disconnected", 0),
                    new XAttribute("warning", 0),
                    new XAttribute("completed", 0),
                    new XAttribute("inProgress", 0),
                    new XAttribute("pending", 0))));

        return XmlReportUtil.ToXmlString(new XDocument(new XDeclaration("1.0", "utf-8", null), root));
    }

    private static string Outcome(RunReportStatus status) => status switch
    {
        RunReportStatus.Passed => "Passed",
        RunReportStatus.Failed => "Failed",
        _ => "NotExecuted",
    };

    private static string Iso(DateTime value) =>
        value.ToUniversalTime().ToString("o", CultureInfo.InvariantCulture);
}
