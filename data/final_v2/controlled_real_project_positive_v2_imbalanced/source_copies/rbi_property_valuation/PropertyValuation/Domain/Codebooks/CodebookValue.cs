using RBBH.CollateralAppraisal.Domain.Common;

namespace RBBH.CollateralAppraisal.Domain.Codebooks;

/// <summary>
/// Vrijednost šifarnika. Referentni podatak koji se koristi u padajućim menijima i poslovnim zapisima.
///
/// VAŽNO: Vrijednosti šifarnika nisu običan CRUD.
/// Ako se vrijednost fizički obriše dok je koriste postojeći zapisi, sistem gubi značenje
/// historijskih podataka — relacije mogu puknuti, a audit postaje nepouzdan.
///
/// Primarni mehanizam uklanjanja: DEAKTIVACIJA (IsActive = false).
/// Fizičko brisanje (soft delete) je dozvoljeno samo ako vrijednost nije referencirana.
/// </summary>
public sealed class CodebookValue : BaseEntity
{
    // ── Identifikacija šifarnika ──────────────────────────────────────────────
    /// <summary>Ključ šifarnika (npr. "role_types", "relation_basis", "limit_types").</summary>
    public string CodebookKey { get; private set; } = null!;

    /// <summary>Tehnički identifikator vrijednosti unutar šifarnika. Jedinstven po CodebookKey.</summary>
    public string Code { get; private set; } = null!;

    /// <summary>Naziv koji se prikazuje u UI (dropdown label).</summary>
    public string Label { get; private set; } = null!;

    /// <summary>Opcijski opis vrijednosti za admin pregled.</summary>
    public string? Description { get; private set; }

    /// <summary>Redoslijed prikaza u dropdownu. Sekundarno sortiranje po Label.</summary>
    public int SortOrder { get; private set; }

    // ── Status ────────────────────────────────────────────────────────────────
    /// <summary>
    /// Aktivna vrijednost se prikazuje u dropdownima i može se koristiti za nove unose.
    /// Deaktivirana vrijednost se ne prikazuje za nove unose, ali ostaje dostupna
    /// za prikaz postojećih zapisa gdje je ranije korištena.
    /// </summary>
    public bool IsActive { get; private set; }

    /// <summary>
    /// Sistemska vrijednost ne smije se brisati standardnom admin akcijom.
    /// Može se deaktivirati ako nije i kritična.
    /// </summary>
    public bool IsSystem { get; private set; }

    /// <summary>
    /// Kritična sistemska vrijednost ne smije se ni deaktivirati.
    /// Ove vrijednosti moraju uvijek ostati aktivne.
    /// </summary>
    public bool IsCritical { get; private set; }

    // ── Korisničko praćenje ───────────────────────────────────────────────────
    public string? CreatedByUserId { get; private set; }
    public string? UpdatedByUserId { get; private set; }

    // ── Deaktivacija ──────────────────────────────────────────────────────────
    public DateTime? DeactivatedAt { get; private set; }
    public string? DeactivatedByUserId { get; private set; }
    public string? DeactivationReason { get; private set; }

    // ── Soft delete ───────────────────────────────────────────────────────────
    /// <summary>
    /// Postavljeno kada je vrijednost logički obrisana.
    /// Globalni query filter u DbContext-u automatski isključuje ove zapise iz upita.
    /// </summary>
    public DateTime? DeletedAt { get; private set; }
    public string? DeletedByUserId { get; private set; }

    private CodebookValue() { } // EF Core

    public static CodebookValue Create(
        string codebookKey,
        string code,
        string label,
        string? description,
        int sortOrder,
        string? createdByUserId,
        bool isSystem   = false,
        bool isCritical = false)
    {
        return new CodebookValue
        {
            CodebookKey     = codebookKey,
            Code            = code,
            Label           = label,
            Description     = description,
            SortOrder       = sortOrder,
            IsActive        = true,
            IsSystem        = isSystem,
            IsCritical      = isCritical,
            CreatedByUserId = createdByUserId
        };
    }

    /// <summary>
    /// Deaktivira vrijednost. Deaktivirana vrijednost ostaje u bazi i na historijskim zapisima,
    /// ali se ne nudi za nove unose.
    /// </summary>
    public void Deactivate(DateTime now, string? userId, string? reason)
    {
        IsActive            = false;
        DeactivatedAt       = now;
        DeactivatedByUserId = userId;
        DeactivationReason  = reason;
        UpdatedByUserId     = userId;
        SetUpdatedAt(now);
    }

    /// <summary>
    /// Reaktivira prethodno deaktiviranu vrijednost.
    /// DeactivatedAt/DeactivatedByUserId ostaju kao historijski trag u entitetu.
    /// </summary>
    public void Activate(DateTime now, string? userId)
    {
        IsActive        = true;
        UpdatedByUserId = userId;
        SetUpdatedAt(now);
    }

    /// <summary>
    /// Soft delete — logičko brisanje. Fizičko brisanje se ne radi kako postojeći zapisi
    /// ne bi izgubili referencu na ovu vrijednost.
    /// Globalni query filter u DbContext-u isključuje soft-deleted zapise iz standardnih upita.
    /// </summary>
    public void SoftDelete(DateTime now, string? userId)
    {
        DeletedAt       = now;
        DeletedByUserId = userId;
        UpdatedByUserId = userId;
        SetUpdatedAt(now);
    }

    /// <summary>Ažurira Label i Description. Dozvoliti samo ako Code nije u upotrebi ili se Code ne mijenja.</summary>
    public void UpdateDetails(string label, string? description, int sortOrder, string? userId, DateTime now)
    {
        Label           = label;
        Description     = description;
        SortOrder       = sortOrder;
        UpdatedByUserId = userId;
        SetUpdatedAt(now);
    }
}
