namespace RBBH.CollateralAppraisal.Application.Codebooks.Requests;

/// <summary>
/// Request tijelo za kreiranje nove vrijednosti šifarnika.
/// CodebookKey se preuzima iz URL rute, ne iz tijela zahtjeva.
/// </summary>
public sealed record CreateCodebookValueRequest(
    string  Code,
    string  Label,
    string? Description,
    int     SortOrder
);
