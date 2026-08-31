namespace RBBH.CollateralAppraisal.Application.Codebooks.Models;

/// <summary>
/// Jedna lokacija gdje se vrijednost šifarnika koristi.
/// Vraća se kao dio <see cref="CodebookUsageResult"/> pri usage checku.
/// </summary>
public sealed class CodebookUsageLocation
{
    /// <summary>Modul aplikacije (npr. "Limits", "Clients", "Requests").</summary>
    public required string Module { get; init; }

    /// <summary>Naziv entiteta koji referencira vrijednost (npr. "LimitRequest", "Client").</summary>
    public required string EntityName { get; init; }

    /// <summary>Broj zapisa koji koriste ovu vrijednost u datom entitetu.</summary>
    public int Count { get; init; }
}
