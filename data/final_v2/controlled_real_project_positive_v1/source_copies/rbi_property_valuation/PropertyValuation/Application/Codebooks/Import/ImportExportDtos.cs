using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Application.Codebooks.Import;

// â”€â”€ Import â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

public enum ImportMode
{
    AddNewOnly = 1,
    UpdateExistingOnly = 2,
    AddAndUpdate = 3,
    DeactivateMissing = 4
}

[ExcludeFromCodeCoverage]
public sealed record ImportPreviewRequest(
    string CodebookType,
    string FileName,
    Stream FileContent,
    ImportMode Mode = ImportMode.AddAndUpdate);

[ExcludeFromCodeCoverage]
public sealed record ImportPreviewResult(
    string CodebookType,
    string FileName,
    int TotalRows,
    int NewCount,
    int UpdateCount,
    int SkipCount,
    int ErrorCount,
    IReadOnlyList<ImportRowError> Errors,
    Guid PreviewToken)
{
    public bool HasErrors => ErrorCount > 0;
    public bool IsValid => ErrorCount == 0 && TotalRows > 0;
}

[ExcludeFromCodeCoverage]
public sealed record ImportRowError(
    int Row,
    string Column,
    string Message);

[ExcludeFromCodeCoverage]
public sealed record ImportConfirmRequest(
    Guid PreviewToken);

[ExcludeFromCodeCoverage]
public sealed record ImportResult(
    string CodebookType,
    int AddedCount,
    int UpdatedCount,
    int SkippedCount,
    int DeactivatedCount,
    string Message);

// â”€â”€ Export â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

public enum ExportFormat { Csv = 1, Xlsx = 2 }

[ExcludeFromCodeCoverage]
public sealed record ExportRequest(
    string CodebookType,
    ExportFormat Format = ExportFormat.Xlsx,
    bool IncludeInactive = false);

[ExcludeFromCodeCoverage]
public sealed record ExportResult(
    Stream Content,
    string ContentType,
    string FileName);

// â”€â”€ Generićki parsed row â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

[ExcludeFromCodeCoverage]
public sealed class ParsedRow
{
    public int RowNumber { get; init; }
    public Dictionary<string, string?> Values { get; init; } = new();

    public string? Get(string column) =>
        Values.TryGetValue(column, out var v) ? v?.Trim() : null;
}
