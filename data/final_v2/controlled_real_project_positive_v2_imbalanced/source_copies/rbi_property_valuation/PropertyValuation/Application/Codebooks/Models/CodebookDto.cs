namespace RBBH.CollateralAppraisal.Application.Codebooks.Models;

/// <summary>
/// Puni DTO za prikaz šifarnika u admin pregledu.
/// </summary>
public sealed record CodebookDto(
    int      Id,
    string   Code,
    string   Name,
    string?  Description,
    string?  Category,
    bool     IsActive,
    bool     IsSystem,
    int      ValueCount,
    DateTime CreatedAt,
    string?  CreatedByUserId,
    DateTime? UpdatedAt,
    string?  UpdatedByUserId);

/// <summary>
/// Lagani DTO za pregled šifarnika u admin tabeli.
/// </summary>
public sealed record CodebookListItemDto(
    int      Id,
    string   Code,
    string   Name,
    string?  Description,
    string?  Category,
    bool     IsActive,
    bool     IsSystem,
    int      ValueCount,
    int      ActiveValueCount,
    DateTime CreatedAt,
    DateTime? UpdatedAt,
    string?  UpdatedByUserId);
