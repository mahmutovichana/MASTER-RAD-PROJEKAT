using RBBH.CollateralAppraisal.Domain.Common;

namespace RBBH.CollateralAppraisal.Domain.Codebooks;

/// <summary>
/// Definicija šifarnika — container koji grupiše skup referentnih vrijednosti.
///
/// Svaki šifarnik ima jedinstveni Code koji odgovara CodebookKey u CodebookValue tablici.
/// Ovo omogućava CRUD nad šifarnikom kao cjelinom, a ne samo nad pojedinim vrijednostima.
///
/// IsSystem = true → šifarnik ne može biti fizički obrisan ni Code ne može biti promijenjen.
/// IsActive = false → šifarnik nije dostupan za nove unose; vrijednosti ostaju za historiju.
/// DeletedAt != null → soft delete; šifarnik je arhiviran.
/// </summary>
public sealed class Codebook : BaseEntity
{
    /// <summary>
    /// Tehnički ključ šifarnika. Mora odgovarati CodebookKey u CodebookValue.
    /// Jedinstven, nepromjenjiv nakon kreiranja (osim za non-system šifarnike).
    /// Primjeri: "tipovi_nekretnina", "vrste_limita", "gradovi"
    /// </summary>
    public string Code { get; private set; } = null!;

    /// <summary>Naziv šifarnika koji se prikazuje u UI.</summary>
    public string Name { get; private set; } = null!;

    /// <summary>Opcijski opis namjene šifarnika.</summary>
    public string? Description { get; private set; }

    /// <summary>
    /// Kategorija šifarnika za grupiranje u UI.
    /// Primjeri: "Nekretnine", "Narudžbe", "Lokacije", "Limiti"
    /// </summary>
    public string? Category { get; private set; }

    // ── Status ────────────────────────────────────────────────────────────────

    /// <summary>Aktivan šifarnik je dostupan za nove unose.</summary>
    public bool IsActive { get; private set; }

    /// <summary>
    /// Sistemski šifarnik ne može biti obrisan, a Code se ne smije mijenjati.
    /// Primjeri: tipovi_nekretnina, statusi_zahtjeva.
    /// </summary>
    public bool IsSystem { get; private set; }

    // ── Audit trail ───────────────────────────────────────────────────────────
    public string? CreatedByUserId { get; private set; }
    public string? UpdatedByUserId { get; private set; }

    // ── Soft delete / arhiviranje ─────────────────────────────────────────────
    public DateTime? DeletedAt { get; private set; }
    public string? DeletedByUserId { get; private set; }

    private Codebook() { }

    public static Codebook CreateSystem(
        string code, string name, string? description, string? category)
        => new()
        {
            Code        = code,
            Name        = name,
            Description = description,
            Category    = category,
            IsActive    = true,
            IsSystem    = true
        };

    public static Codebook CreateCustom(
        string code, string name, string? description, string? category,
        string? createdByUserId)
        => new()
        {
            Code             = code,
            Name             = name,
            Description      = description,
            Category         = category,
            IsActive         = true,
            IsSystem         = false,
            CreatedByUserId  = createdByUserId
        };

    public void Update(string name, string? description, string? category,
        string? userId, DateTime now)
    {
        Name            = name;
        Description     = description;
        Category        = category;
        UpdatedByUserId = userId;
        SetUpdatedAt(now);
    }

    public void Deactivate(string? userId, DateTime now)
    {
        IsActive        = false;
        UpdatedByUserId = userId;
        SetUpdatedAt(now);
    }

    public void Activate(string? userId, DateTime now)
    {
        IsActive        = true;
        UpdatedByUserId = userId;
        SetUpdatedAt(now);
    }

    public void SoftDelete(string? userId, DateTime now)
    {
        DeletedAt       = now;
        DeletedByUserId = userId;
        UpdatedByUserId = userId;
        SetUpdatedAt(now);
    }
}
