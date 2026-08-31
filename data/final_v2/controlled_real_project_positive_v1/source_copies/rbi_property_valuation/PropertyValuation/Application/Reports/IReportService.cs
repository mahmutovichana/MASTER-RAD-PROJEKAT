using RBBH.CollateralAppraisal.Application.Reports.Dtos;

namespace RBBH.CollateralAppraisal.Application.Reports;

/// <summary>
/// Generisanje izvještaja u kućici "Izvještaji":
///  • koncentracija vještaka (5 opcija) — US 9
///  • pregled svih narudžbi + 7 vremenskih kolona — US 10
/// Oba se generišu na klik, na zadati datum, u Excel formatu.
/// </summary>
public interface IReportService
{
    /// <summary>
    /// Izvještaj koncentracije vještaka (samo završene procjene), grupisan po jednoj od 5 opcija.
    /// </summary>
    /// <param name="option">1=Grad, 2=Procjenitelj, 3=Tip kolaterala, 4=Grad+Procjenitelj, 5=Grad+Procjenitelj (zadnji mjesec).</param>
    /// <param name="asOfDate">Datum na koji se generiše izvještaj (null = danas).</param>
    Task<ReportFile> GenerateConcentrationAsync(int option, DateTime? asOfDate, CancellationToken ct = default);

    /// <summary>
    /// Pregled svih narudžbi sa svim ključnim poljima iz Protokola narudžbi + 7 vremenskih kolona.
    /// </summary>
    /// <param name="endDate">Krajnji datum za filtriranje narudžbi (null = sve).</param>
    Task<ReportFile> GenerateOrdersTimeReportAsync(DateTime? endDate, CancellationToken ct = default);

    /// <summary>
    /// JSON lista narudžbi sa statusom vještaka — za reminder sekciju (DPNPN-141).
    /// </summary>
    Task<IReadOnlyList<ReminderOrderDto>> GetReminderOrdersAsync(CancellationToken ct = default);
}
