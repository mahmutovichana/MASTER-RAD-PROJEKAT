namespace RBBH.CollateralAppraisal.Application.Codebooks.Requests;

/// <summary>
/// Request tijelo za uređivanje vrijednosti šifarnika.
/// Code se ne može mijenjati — koristi se kao stabilan tehnički identifikator
/// koji može biti referenciran u historijskim zapisima.
/// </summary>
public sealed record UpdateCodebookValueRequest(
    string  Label,
    string? Description,
    int     SortOrder
);
