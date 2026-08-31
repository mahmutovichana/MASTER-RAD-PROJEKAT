using System.Collections.Generic;
using System.IO;
using System.Linq;
using ClosedXML.Excel;
using RBBH.CollateralAppraisal.Application.Reports;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Reports;

/// <summary>
/// xlsx generator zasnovan na ClosedXML (već referenciran u projektu).
/// Prvi red = podebljani naslovi; ostali redovi = podaci s pravim Excel tipovima.
/// </summary>
[ExcludeFromCodeCoverage]
public sealed class ClosedXmlReportBuilder : IExcelReportBuilder
{
    public byte[] BuildSingleSheet(
        string sheetName,
        IReadOnlyList<string> headers,
        IEnumerable<IReadOnlyList<object?>> rows)
    {
        using var workbook = new XLWorkbook();
        var ws = workbook.AddWorksheet(SanitizeSheetName(sheetName));

        for (var c = 0; c < headers.Count; c++)
        {
            var cell = ws.Cell(1, c + 1);
            cell.Value = headers[c];
            cell.Style.Font.Bold = true;
        }

        var r = 2;
        foreach (var row in rows)
        {
            for (var c = 0; c < row.Count; c++)
                SetCell(ws.Cell(r, c + 1), row[c]);
            r++;
        }

        ws.Columns().AdjustToContents();

        using var ms = new MemoryStream();
        workbook.SaveAs(ms);
        return ms.ToArray();
    }

    private static void SetCell(IXLCell cell, object? value)
    {
        switch (value)
        {
            case null:        break; // prazna ćelija
            case string s:    cell.Value = s;  break;
            case bool b:      cell.Value = b;  break;
            case int i:       cell.Value = i;  break;
            case long l:      cell.Value = l;  break;
            case double d:    cell.Value = d;  break;
            case decimal m:   cell.Value = m;  break;
            case DateTime dt: cell.Value = dt; break;
            default:          cell.Value = value.ToString() ?? string.Empty; break;
        }
    }

    /// <summary>Excel naziv lista: max 31 znak, bez : \ / ? * [ ].</summary>
    private static string SanitizeSheetName(string name)
    {
        var cleaned = new string(name
            .Where(ch => ch is not (':' or '\\' or '/' or '?' or '*' or '[' or ']'))
            .ToArray());

        if (string.IsNullOrWhiteSpace(cleaned))
            cleaned = "Izvjestaj";

        return cleaned.Length > 31 ? cleaned[..31] : cleaned;
    }
}
