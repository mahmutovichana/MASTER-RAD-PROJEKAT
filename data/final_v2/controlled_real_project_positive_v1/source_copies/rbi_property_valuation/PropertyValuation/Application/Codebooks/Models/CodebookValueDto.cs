namespace RBBH.CollateralAppraisal.Application.Codebooks.Models;

/// <summary>
/// Puni DTO za admin pregled jedne vrijednosti šifarnika.
/// Sadrži sve informacije uključujući status, audit polja i deaktivacijski trag.
/// </summary>
public sealed record CodebookValueDto(
    int       Id,
    string    CodebookKey,
    string    Code,
    string    Label,
    string?   Description,
    int       SortOrder,
    bool      IsActive,
    bool      IsSystem,
    bool      IsCritical,
    DateTime  CreatedAt,
    string?   CreatedByUserId,
    DateTime? UpdatedAt,
    string?   UpdatedByUserId,
    DateTime? DeactivatedAt,
    string?   DeactivatedByUserId,
    string?   DeactivationReason
);
