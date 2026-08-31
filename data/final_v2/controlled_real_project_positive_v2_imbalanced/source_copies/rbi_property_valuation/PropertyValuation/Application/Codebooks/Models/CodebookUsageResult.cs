namespace RBBH.CollateralAppraisal.Application.Codebooks.Models;

/// <summary>
/// Rezultat provjere da li je vrijednost šifarnika u upotrebi.
/// Vraća se iz GET /values/{id}/usage endpointa i koristi se interno u DELETE akciji.
///
/// Fail-safe princip: ako IsReliable=false, delete se ne smije dozvoliti —
/// bolje je blokirati brisanje nego obrisati vrijednost koja je možda u upotrebi.
/// </summary>
public sealed class CodebookUsageResult
{
    /// <summary>Da li je vrijednost referencirana u nekom poslovnom zapisu.</summary>
    public bool IsInUse { get; init; }

    /// <summary>Ukupan broj zapisa koji koriste ovu vrijednost (suma svih lokacija).</summary>
    public int UsageCount { get; init; }

    /// <summary>Lista modula i entiteta koji koriste ovu vrijednost.</summary>
    public IReadOnlyList<CodebookUsageLocation> Locations { get; init; } = [];

    /// <summary>
    /// Da li je provjera bila pouzdana. False ako je neki usage checker pao s greškom.
    /// Ako IsReliable=false, <see cref="CanDelete"/> je automatski false (fail-safe).
    /// </summary>
    public bool IsReliable { get; init; } = true;

    /// <summary>
    /// Brisanje je dozvoljeno samo ako je provjera pouzdana I vrijednost nije u upotrebi.
    /// DELETE endpoint uvijek ponavlja usage check neposredno prije brisanja.
    /// </summary>
    public bool CanDelete => IsReliable && !IsInUse;

    /// <summary>Deaktivacija je uvijek dozvoljena (osim za kritične sistemske vrijednosti).</summary>
    public bool CanDeactivate => true;

    /// <summary>Preporučena akcija: "Deactivate" ako je u upotrebi, "Delete" ako nije.</summary>
    public string RecommendedAction => IsInUse ? "Deactivate" : "Delete";
}
