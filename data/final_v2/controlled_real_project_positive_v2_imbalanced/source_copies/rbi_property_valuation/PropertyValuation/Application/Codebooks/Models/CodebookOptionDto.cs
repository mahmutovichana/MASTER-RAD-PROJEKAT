namespace RBBH.CollateralAppraisal.Application.Codebooks.Models;

/// <summary>
/// Lagani DTO za dropdown menije. Vraća se iz GET /values/active endpointa.
/// Sadrži samo polja koja su potrebna za prikaz u padajućem meniju.
/// </summary>
public sealed record CodebookOptionDto(
    int     Id,
    string  Code,
    string  Label,
    int     SortOrder,
    string? Description = null
);
