using RBBH.CollateralAppraisal.Domain.Common;

namespace RBBH.CollateralAppraisal.Domain.Documents;

/// <summary>
/// Dokument vezan za narudžbu procjene.
/// Storage provider se konfigurira kroz IFileStorageProvider — lokalni, S3, MinIO.
/// ODLUKA POTREBNA (stakeholder): specificirati obavezne dokumente po tipu kolaterala.
/// ValidateSubmitRequirementsAsync u AppraisalOrderService trenutno provjerava ZK, Uplatnicu i Saglasnost.
/// </summary>
public sealed class Document : BaseEntity
{
    public int AppraisalOrderId { get; private set; }
    public int? DocumentTypeId { get; private set; }     // Ref na šifarnik tip_dokumenta
    public string FileName { get; private set; } = null!;
    public string OriginalFileName { get; private set; } = null!;
    public string? ContentType { get; private set; }
    public long FileSize { get; private set; }
    public string StoragePath { get; private set; } = null!;

    public string? UploadedByUserId { get; private set; }
    public DateTime UploadedAt { get; private set; }

    // ── Verzionisanje ──────────────────────────────────────────────────────
    /// <summary>Redni broj verzije unutar lanca verzija (1 = originalni upload).</summary>
    public int Version { get; private set; } = 1;
    /// <summary>Id prethodne verzije ovog dokumenta — null za v1. Vidi <see cref="CreateNewVersion"/>.</summary>
    public int? PreviousVersionId { get; private set; }
    /// <summary>Razlog zamjene/kreiranja nove verzije — enterprise audit requirement.</summary>
    public string? ChangeReason { get; private set; }

    // ── Deaktivacija (lifecycle — odvojeno od brisanja) ───────────────────
    // Deaktivacija znači "ne koristi se za tekući workflow" (npr. zamijenjen
    // novom verzijom, ili ručno povučen) — dokument i dalje postoji i ostaje
    // dostupan za audit/historijski pregled. Brisanje (IsDeleted) je trajno
    // uklanjanje iz svih standardnih upita (globalni query filter).
    public bool IsActive { get; private set; } = true;
    public DateTime? DeactivatedAt { get; private set; }
    public string? DeactivatedByUserId { get; private set; }
    public string? DeactivationReason { get; private set; }

    // ── Soft delete ────────────────────────────────────────────────────────
    public bool IsDeleted { get; private set; }
    public DateTime? DeletedAt { get; private set; }
    public string? DeletedByUserId { get; private set; }

    private Document() { }

    public static Document Create(
        int orderId,
        int? documentTypeId,
        string fileName,
        string originalFileName,
        string? contentType,
        long fileSize,
        string storagePath,
        string? uploadedByUserId,
        DateTime? now = null)
    {
        return new Document
        {
            AppraisalOrderId = orderId,
            DocumentTypeId   = documentTypeId,
            FileName         = fileName,
            OriginalFileName = originalFileName,
            ContentType      = contentType,
            FileSize         = fileSize,
            StoragePath      = storagePath,
            UploadedByUserId = uploadedByUserId,
            UploadedAt       = now ?? DateTime.UtcNow,
            Version          = 1,
            IsActive         = true
        };
    }

    /// <summary>
    /// Kreira sljedeću verziju postojećeg dokumenta (zamjena/replace). Nova verzija
    /// nasljeđuje AppraisalOrderId/DocumentTypeId od prethodne, Version = previous.Version + 1,
    /// i čuva PreviousVersionId radi lanca historije. Prethodnu verziju treba deaktivirati
    /// (vidi <see cref="Deactivate"/>) — to radi pozivajući servis u istoj transakciji.
    /// </summary>
    public static Document CreateNewVersion(
        Document previous,
        string fileName,
        string originalFileName,
        string? contentType,
        long fileSize,
        string storagePath,
        string? uploadedByUserId,
        string? changeReason = null,
        DateTime? now = null)
    {
        return new Document
        {
            AppraisalOrderId  = previous.AppraisalOrderId,
            DocumentTypeId    = previous.DocumentTypeId,
            FileName          = fileName,
            OriginalFileName  = originalFileName,
            ContentType       = contentType,
            FileSize          = fileSize,
            StoragePath       = storagePath,
            UploadedByUserId  = uploadedByUserId,
            UploadedAt        = now ?? DateTime.UtcNow,
            Version           = previous.Version + 1,
            PreviousVersionId = previous.Id,
            ChangeReason      = changeReason ?? "Zamijenjen novom verzijom",
            IsActive          = true
        };
    }

    /// <summary>
    /// Deaktivira dokument (npr. zamijenjen novom verzijom, ili ručno povučen).
    /// Dokument ostaje vidljiv u historiji/auditu — za trajno uklanjanje koristiti SoftDelete.
    /// </summary>
    public void Deactivate(string? userId, DateTime now, string? reason)
    {
        IsActive            = false;
        DeactivatedAt       = now;
        DeactivatedByUserId = userId;
        DeactivationReason  = reason;
        SetUpdatedAt(now);
    }

    /// <summary>Ponovo aktivira prethodno deaktiviran dokument.</summary>
    public void Reactivate(DateTime now)
    {
        IsActive       = true;
        DeactivatedAt  = null;
        DeactivationReason = null;
        SetUpdatedAt(now);
    }

    public void SoftDelete(string userId, DateTime now)
    {
        IsDeleted       = true;
        DeletedAt       = now;
        DeletedByUserId = userId;
        SetUpdatedAt(now);
    }
}
