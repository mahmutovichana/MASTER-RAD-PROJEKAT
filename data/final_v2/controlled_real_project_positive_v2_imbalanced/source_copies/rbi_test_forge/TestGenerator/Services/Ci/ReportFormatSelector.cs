using RBBH.TestAutomation.Core.Reporting;

namespace RBBH.TestAutomation.Api.Services.Ci;

/// <summary>
/// Rješava format iz rute (npr. <c>junit</c>, <c>trx</c>) u odgovarajući
/// <see cref="IRunReportFormatter"/>. Izdvojeno iz endpointa radi unit-testabilnosti.
/// </summary>
public static class ReportFormatSelector
{
    /// <summary>
    /// Parsira <paramref name="format"/> i pronalazi registrovani formatter.
    /// Odbija numeričke i nedefinirane vrijednosti — <c>Enum.TryParse</c> inače prihvata
    /// npr. "99" ili "5" kao "validan" enum, što bi kasnije oborilo pretragu formattera
    /// na neuhvaćeni izuzetak (HTTP 500). Vraća <c>false</c> ako format nije prepoznat
    /// ili formatter za njega nije registrovan.
    /// </summary>
    public static bool TryResolve(
        string? format,
        IEnumerable<IRunReportFormatter> formatters,
        out RunReportFormat fmt,
        out IRunReportFormatter formatter)
    {
        formatter = null!;

        if (!Enum.TryParse(format, ignoreCase: true, out fmt) || !Enum.IsDefined(fmt))
            return false;

        var resolved = fmt; // out parametar se ne smije hvatati u lambdi
        var match = formatters.FirstOrDefault(f => f.Format == resolved);
        if (match is null)
            return false;

        formatter = match;
        return true;
    }
}
