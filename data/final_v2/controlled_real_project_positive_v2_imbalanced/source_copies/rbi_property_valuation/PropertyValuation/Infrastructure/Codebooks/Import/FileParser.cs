using ClosedXML.Excel;
using RBBH.CollateralAppraisal.Application.Codebooks.Import;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Codebooks.Import;

/// <summary>
/// Parsira CSV/XLSX/XLS fajlove u generićke ParsedRow objekte.
/// Validira format, MIME type, praznoću, kolone.
/// </summary>
[ExcludeFromCodeCoverage]
public static class FileParser
{
    private static readonly HashSet<string> AllowedExtensions = [".csv", ".xlsx", ".xls"];
    private const long MaxFileSize = 10 * 1024 * 1024; // 10 MB

    public static (IReadOnlyList<ParsedRow> Rows, IReadOnlyList<ImportRowError> Errors) Parse(
        Stream content, string fileName, IReadOnlyList<ColumnDef> expectedColumns)
    {
        var ext = Path.GetExtension(fileName).ToLowerInvariant();
        var errors = new List<ImportRowError>();

        if (!AllowedExtensions.Contains(ext))
        {
            errors.Add(new(0, "Fajl", $"Nepodržan format '{ext}'. Dozvoljeni: CSV, XLSX, XLS."));
            return ([], errors);
        }

        if (content.Length == 0)
        {
            errors.Add(new(0, "Fajl", "Fajl je prazan."));
            return ([], errors);
        }

        if (content.Length > MaxFileSize)
        {
            errors.Add(new(0, "Fajl", $"Fajl je prevelik ({content.Length / 1024 / 1024} MB). Maksimum: 10 MB."));
            return ([], errors);
        }

        content.Position = 0;

        return ext == ".csv"
            ? ParseCsv(content, expectedColumns)
            : ParseExcel(content, expectedColumns);
    }

    private static (IReadOnlyList<ParsedRow>, IReadOnlyList<ImportRowError>) ParseCsv(
        Stream content, IReadOnlyList<ColumnDef> expectedColumns)
    {
        var errors = new List<ImportRowError>();
        var rows = new List<ParsedRow>();

        using var reader = new StreamReader(content, leaveOpen: true);
        var headerLine = reader.ReadLine();
        if (string.IsNullOrWhiteSpace(headerLine))
        {
            errors.Add(new(1, "Header", "Fajl nema zaglavlje."));
            return (rows, errors);
        }

        var headers = headerLine.Split(';', ',')
            .Select(h => h.Trim().Trim('"'))
            .ToList();

        var columnErrors = ValidateColumns(headers, expectedColumns);
        if (columnErrors.Count > 0)
            return (rows, columnErrors);

        var rowNum = 1;
        while (reader.ReadLine() is { } line)
        {
            rowNum++;
            if (string.IsNullOrWhiteSpace(line)) continue;

            var values = line.Split(';', ',')
                .Select(v => v.Trim().Trim('"'))
                .ToList();

            var dict = new Dictionary<string, string?>(StringComparer.OrdinalIgnoreCase);
            for (var i = 0; i < headers.Count; i++)
                dict[headers[i]] = i < values.Count ? (string.IsNullOrWhiteSpace(values[i]) ? null : values[i]) : null;

            rows.Add(new ParsedRow { RowNumber = rowNum, Values = dict });
        }

        return (rows, errors);
    }

    private static (IReadOnlyList<ParsedRow>, IReadOnlyList<ImportRowError>) ParseExcel(
        Stream content, IReadOnlyList<ColumnDef> expectedColumns)
    {
        var errors = new List<ImportRowError>();
        var rows = new List<ParsedRow>();

        XLWorkbook workbook;
        try
        {
            workbook = new XLWorkbook(content);
        }
        catch (Exception ex)
        {
            // Čest uzrok: korisnik je odabrao ~$NazivFajla.xlsx (Excel privremeni lock fajl
            // koji Windows kreira dok je originalni fajl otvoren). Taj fajl nije validan XLSX.
            var hint = content.Length < 1000
                ? " Provjeri da li si slučajno odabrao/la privremeni fajl koji počinje sa '~$'. Zatvori Excel i pokušaj ponovo."
                : "";
            errors.Add(new(0, "Fajl", $"Excel fajl nije validan ili je oštećen.{hint} Greška: {ex.Message.Split('\n')[0]}"));
            return (rows, errors);
        }

        using var _ = workbook;
        var sheet = workbook.Worksheets.FirstOrDefault();
        if (sheet is null)
        {
            errors.Add(new(0, "Sheet", "Excel fajl nema nijedan sheet."));
            return (rows, errors);
        }

        var lastRow = sheet.LastRowUsed()?.RowNumber() ?? 0;
        if (lastRow < 2)
        {
            errors.Add(new(1, "Podaci", "Sheet nema podataka (samo zaglavlje ili prazan)."));
            return (rows, errors);
        }

        var headerRow = sheet.Row(1);
        var lastCol = sheet.LastColumnUsed()?.ColumnNumber() ?? 0;
        var headers = new List<string>();
        for (var c = 1; c <= lastCol; c++)
            headers.Add(headerRow.Cell(c).GetString().Trim());

        var columnErrors = ValidateColumns(headers, expectedColumns);
        if (columnErrors.Count > 0)
            return (rows, columnErrors);

        for (var r = 2; r <= lastRow; r++)
        {
            var row = sheet.Row(r);
            var allEmpty = true;
            var dict = new Dictionary<string, string?>(StringComparer.OrdinalIgnoreCase);

            for (var c = 0; c < headers.Count; c++)
            {
                var val = row.Cell(c + 1).GetString().Trim();
                if (!string.IsNullOrEmpty(val)) allEmpty = false;
                dict[headers[c]] = string.IsNullOrWhiteSpace(val) ? null : val;
            }

            if (allEmpty) continue;
            rows.Add(new ParsedRow { RowNumber = r, Values = dict });
        }

        return (rows, errors);
    }

    private static List<ImportRowError> ValidateColumns(
        List<string> actual, IReadOnlyList<ColumnDef> expected)
    {
        var errors = new List<ImportRowError>();
        var actualSet = new HashSet<string>(actual, StringComparer.OrdinalIgnoreCase);

        foreach (var col in expected.Where(c => c.Required))
        {
            if (!actualSet.Contains(col.Name) && !actualSet.Contains(col.Label))
                errors.Add(new(1, col.Name, $"Obavezna kolona '{col.Label}' (ili '{col.Name}') nije pronaÄ‘ena u fajlu."));
        }

        return errors;
    }

    /// <summary>
    /// Pronalazi vrijednost kolone po Name ili Label (fallback).
    /// Omogućava da Excel koristi bilo koji od dva naziva.
    /// </summary>
    public static string? GetFlexible(this ParsedRow row, ColumnDef col)
        => row.Get(col.Name) ?? row.Get(col.Label);
}
