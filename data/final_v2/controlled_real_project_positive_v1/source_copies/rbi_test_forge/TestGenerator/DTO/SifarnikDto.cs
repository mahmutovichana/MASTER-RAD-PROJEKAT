namespace RBBH.TestAutomation.Api.DTO;

/// <summary>
/// Kategorija šifarnika (npr. "tipovi_rola", "osnov_povezanosti", "vrste_limita").
/// Mapira tabelu <c>sifarnici_kategorije</c>.
/// </summary>
public sealed record SifarnikKategorijaDto(
    Guid Id,
    string Naziv,
    string Slug,
    string? Opis,
    bool Active,
    DateTime KreiranAt
);

/// <summary>
/// Vrijednost unutar kategorije šifarnika (npr. "Unosnik", "Verifikator").
/// Mapira tabelu <c>sifarnici_vrijednosti</c>.
/// <c>KreiranOd</c>/<c>IzmjenjenOd</c> su Keycloak sub claim-ovi (UserId).
/// </summary>
public sealed record SifarnikVrijednostDto(
    Guid Id,
    Guid KategorijaId,
    string Naziv,
    string? Kod,
    int Redoslijed,
    bool Active,
    string? KreiranOd,
    DateTime KreiranAt,
    string? IzmjenjenOd,
    DateTime? IzmjenjenAt
);

/// <summary>
/// Ulaz za kreiranje nove vrijednosti šifarnika.
/// </summary>
public sealed record CreateSifarnikVrijednostRequest(
    Guid KategorijaId,
    string Naziv,
    string? Kod,
    int Redoslijed,
    bool Active
);

/// <summary>
/// Ulaz za izmjenu postojeće vrijednosti šifarnika.
/// </summary>
public sealed record UpdateSifarnikVrijednostRequest(
    string Naziv,
    string? Kod,
    int Redoslijed,
    bool Active
);

/// <summary>
/// Jedan zapis audit traga. Mapira tabelu <c>audit_log</c>.
/// <c>ChangedBy</c> je Keycloak sub claim, <c>ChangedByName</c> je puno ime za prikaz u UI.
/// </summary>
public sealed record AuditLogEntryDto(
    Guid Id,
    string EntityType,
    Guid? EntityId,
    string Action,
    string ChangedBy,
    string? ChangedByName,
    DateTime ChangedAt,
    string? OldValues,
    string? NewValues
);

/// <summary>
/// Konstante za <c>entity_type</c> kolonu audit_log tabele.
/// </summary>
public static class AuditEntityTypes
{
    public const string SifarnikVrijednost = "sifarnik_vrijednost";
    public const string SifarnikKategorija = "sifarnik_kategorija";
    public const string RoleAssignment = "role_assignment";
}

/// <summary>
/// Konstante za <c>action</c> kolonu audit_log tabele.
/// Moraju odgovarati CHECK constraint-u u init.sql.
/// </summary>
public static class AuditActions
{
    public const string Create = "CREATE";
    public const string Update = "UPDATE";
    public const string Delete = "DELETE";
}
