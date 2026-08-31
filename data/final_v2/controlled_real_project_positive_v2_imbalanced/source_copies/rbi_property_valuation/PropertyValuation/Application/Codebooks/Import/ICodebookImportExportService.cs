namespace RBBH.CollateralAppraisal.Application.Codebooks.Import;

/// <summary>
/// Generički import/export servis za sve šifarnike.
/// Isti UI, validacija, preview, audit — razlikuju se samo kolone i pravila (ICodebookMapper).
/// </summary>
public interface ICodebookImportExportService
{
    IReadOnlyList<string> SupportedCodebookTypes { get; }

    Task<ImportPreviewResult> PreviewImportAsync(ImportPreviewRequest request, CancellationToken ct = default);

    Task<ImportResult> ConfirmImportAsync(ImportConfirmRequest request, CancellationToken ct = default);

    Task<ExportResult> ExportAsync(ExportRequest request, CancellationToken ct = default);
}
