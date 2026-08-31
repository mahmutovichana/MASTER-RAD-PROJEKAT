using RBBH.CollateralAppraisal.Domain.Common;

namespace RBBH.CollateralAppraisal.Domain.Documents;

/// <summary>
/// Dijeljeni (app-level) dokument — nije vezan za narudžbu.
/// Koristi se za cjenovnik procjena, listu dokumentacije po tipu kolaterala i sl.
/// Upload/brisanje: samo CA. Pregled/download: sve role.
/// </summary>
public sealed class SharedDocument : BaseEntity
{
    public string Title          { get; private set; } = null!;
    public string Category       { get; private set; } = null!;
    public string FileName       { get; private set; } = null!;
    public string OriginalFileName { get; private set; } = null!;
    public string? ContentType   { get; private set; }
    public long   FileSize       { get; private set; }
    public string StoragePath    { get; private set; } = null!;

    public string?   UploadedByUserId { get; private set; }
    public DateTime  UploadedAt       { get; private set; }

    public bool     IsActive              { get; private set; } = true;
    public DateTime? DeactivatedAt        { get; private set; }
    public string?   DeactivatedByUserId  { get; private set; }

    private SharedDocument() { }

    public static SharedDocument Create(
        string title,
        string category,
        string fileName,
        string originalFileName,
        string? contentType,
        long fileSize,
        string storagePath,
        string? uploadedByUserId)
    {
        return new SharedDocument
        {
            Title            = title,
            Category         = category,
            FileName         = fileName,
            OriginalFileName = originalFileName,
            ContentType      = contentType,
            FileSize         = fileSize,
            StoragePath      = storagePath,
            UploadedByUserId = uploadedByUserId,
            UploadedAt       = DateTime.UtcNow,
            IsActive         = true
        };
    }

    public void Deactivate(string userId, DateTime now)
    {
        IsActive             = false;
        DeactivatedAt        = now;
        DeactivatedByUserId  = userId;
        SetUpdatedAt(now);
    }
}
