namespace RBBH.CollateralAppraisal.Application.Codebooks.Requests;

public sealed record CreateCodebookRequest(
    string  Code,
    string  Name,
    string? Description,
    string? Category);

public sealed record UpdateCodebookRequest(
    string  Name,
    string? Description,
    string? Category);

public sealed record DeactivateCodebookRequest(string? Reason = null);

public sealed record CodebookQueryRequest(
    string? Search     = null,
    bool?   IsActive   = null,
    bool?   IsSystem   = null,
    string? Category   = null,
    string? SortBy     = null,
    bool    SortAsc    = true,
    int     Page       = 1,
    int     PageSize   = 50);
