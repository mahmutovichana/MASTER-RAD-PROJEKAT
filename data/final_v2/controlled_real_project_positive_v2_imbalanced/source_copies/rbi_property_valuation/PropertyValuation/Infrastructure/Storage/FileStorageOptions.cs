namespace RBBH.CollateralAppraisal.Infrastructure.Storage;

/// <summary>
/// Konfiguracija lokalnog skladišta fajlova.
/// Popuniti putem appsettings.json (sekcija "FileStorage") ili environment varijable
/// "FileStorage__RootPath".
/// </summary>
[System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage]
public sealed class FileStorageOptions
{
    public const string SectionName = "FileStorage";

    /// <summary>
    /// Korijenski direktorij na disku u koji se snimaju svi fajlovi.
    /// Relativne putanje se rješavaju u odnosu na radni direktorij aplikacije.
    /// </summary>
    public string RootPath { get; init; } = "storage";

    /// <summary>
    /// Maksimalna dozvoljena veličina fajla u bajtovima. Default: 50 MB.
    /// Postaviti na 0 da se onemogući provjera (nije preporučeno).
    /// </summary>
    public long MaxFileSizeBytes { get; init; } = 50 * 1024 * 1024;
}
