using RBBH.CollateralAppraisal.Application.Documents.Dtos;

namespace RBBH.CollateralAppraisal.Application.Documents;

public interface IDocumentService
{
    Task<IReadOnlyList<DocumentDto>> UploadAsync(
        int orderId,
        int documentTypeId,
        IReadOnlyList<DocumentUploadFile> files,
        CancellationToken ct = default);

    Task<IReadOnlyList<DocumentDto>> GetByOrderAsync(
        int orderId,
        CancellationToken ct = default);

    Task<DocumentDownloadDto> OpenDownloadAsync(
        int documentId,
        CancellationToken ct = default);

    Task DeleteAsync(
        int documentId,
        CancellationToken ct = default);

    /// <summary>
    /// Zamjenjuje dokument novom verzijom (Version = staraVerzija + 1). Stara verzija se
    /// deaktivira (IsActive=false, DeactivationReason="Zamijenjen novom verzijom"), ostaje
    /// dostupna za audit/historijski pregled.
    /// </summary>
    Task<DocumentDto> ReplaceAsync(
        int documentId,
        DocumentUploadFile file,
        CancellationToken ct = default);

    /// <summary>Deaktivira dokument bez brisanja — ostaje vidljiv u historiji/auditu.</summary>
    Task<DocumentDto> DeactivateAsync(
        int documentId,
        string? reason,
        CancellationToken ct = default);

    /// <summary>Ponovo aktivira prethodno deaktiviran dokument.</summary>
    Task<DocumentDto> ReactivateAsync(
        int documentId,
        CancellationToken ct = default);
}