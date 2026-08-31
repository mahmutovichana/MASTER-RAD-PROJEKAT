using System.Text;
using ClosedXML.Excel;
using RBBH.CollateralAppraisal.Application.Codebooks.Import;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Codebooks.Import;

[ExcludeFromCodeCoverage]
public static class FileExporter
{
    public static ExportResult Export(
        IReadOnlyList<ColumnDef> columns,
        IReadOnlyList<Dictionary<string, string?>> rows,
        string codebookType,
        ExportFormat format)
    {
        return format == ExportFormat.Csv
            ? ExportCsv(columns, rows, codebookType)
            : ExportXlsx(columns, rows, codebookType);
    }

    private static ExportResult ExportCsv(
        IReadOnlyList<ColumnDef> columns,
        IReadOnlyList<Dictionary<string, string?>> rows,
        string codebookType)
    {
        var sb = new StringBuilder();
        sb.AppendLine(string.Join(";", columns.Select(c => $"\"{c.Label}\"")));

        foreach (var row in rows)
        {
            var values = columns.Select(c =>
            {
                var val = row.GetValueOrDefault(c.Name) ?? "";
                return $"\"{val.Replace("\"", "\"\"")}\"";
            });
            sb.AppendLine(string.Join(";", values));
        }

        var ms = new MemoryStream(Encoding.UTF8.GetBytes(sb.ToString()));
        return new ExportResult(ms, "text/csv", $"{codebookType}_{DateTime.UtcNow:yyyyMMdd}.csv");
    }

    private static ExportResult ExportXlsx(
        IReadOnlyList<ColumnDef> columns,
        IReadOnlyList<Dictionary<string, string?>> rows,
        string codebookType)
    {
        var ms = new MemoryStream();
        using (var wb = new XLWorkbook())
        {
            var ws = wb.AddWorksheet(codebookType);

            for (var c = 0; c < columns.Count; c++)
            {
                var cell = ws.Cell(1, c + 1);
                cell.Value = columns[c].Label;
                cell.Style.Font.Bold = true;
            }

            for (var r = 0; r < rows.Count; r++)
            {
                for (var c = 0; c < columns.Count; c++)
                {
                    var val = rows[r].GetValueOrDefault(columns[c].Name) ?? "";
                    ws.Cell(r + 2, c + 1).Value = val;
                }
            }

            ws.Columns().AdjustToContents();
            wb.SaveAs(ms);
        }

        ms.Position = 0;
        return new ExportResult(ms,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            $"{codebookType}_{DateTime.UtcNow:yyyyMMdd}.xlsx");
    }
}
