namespace RBBH.CollateralAppraisal.Application.Reports;

/// <summary>
/// Zajednički generator Excel (xlsx) izvještaja. Uvodi ga T1 (reporting foundation);
/// koriste ga svi izvještaji (koncentracija vještaka, pregled narudžbi s vremenima, …).
/// Implementacija je u Infrastructure sloju (ClosedXML).
/// </summary>
public interface IExcelReportBuilder
{
    /// <summary>
    /// Gradi xlsx s jednim radnim listom: prvi red su podebljani naslovi kolona,
    /// zatim redovi podataka. Vrijednosti se upisuju kao pravi Excel tipovi
    /// (broj, datum, tekst) gdje je moguće. Null vrijednost ostaje prazna ćelija.
    /// </summary>
    byte[] BuildSingleSheet(
        string sheetName,
        IReadOnlyList<string> headers,
        IEnumerable<IReadOnlyList<object?>> rows);
}
