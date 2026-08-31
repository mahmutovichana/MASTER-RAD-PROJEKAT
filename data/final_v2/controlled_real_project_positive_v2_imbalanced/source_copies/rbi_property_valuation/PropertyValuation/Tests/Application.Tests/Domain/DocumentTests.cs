using RBBH.CollateralAppraisal.Domain.Documents;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Domain;

public sealed class DocumentTests
{
    private static Document MakeDocument(int orderId = 1, int? documentTypeId = 2) =>
        Document.Create(
            orderId:          orderId,
            documentTypeId:   documentTypeId,
            fileName:         "stored-name.pdf",
            originalFileName: "procjena.pdf",
            contentType:      "application/pdf",
            fileSize:         1024,
            storagePath:      "/storage/1/stored-name.pdf",
            uploadedByUserId: "user-1");

    // ── Create ───────────────────────────────────────────────────────────────

    [Fact]
    public void Create_SetsVersionToOneAndUploadedAt()
    {
        var before = DateTime.UtcNow;

        var document = MakeDocument();

        var after = DateTime.UtcNow;

        Assert.Equal(1, document.Version);
        Assert.InRange(document.UploadedAt, before, after);
        Assert.Equal(1,                          document.AppraisalOrderId);
        Assert.Equal(2,                          document.DocumentTypeId);
        Assert.Equal("stored-name.pdf",          document.FileName);
        Assert.Equal("procjena.pdf",             document.OriginalFileName);
        Assert.Equal("application/pdf",          document.ContentType);
        Assert.Equal(1024,                       document.FileSize);
        Assert.Equal("/storage/1/stored-name.pdf", document.StoragePath);
        Assert.Equal("user-1",                   document.UploadedByUserId);
        Assert.False(document.IsDeleted);
    }

    [Fact]
    public void Create_IsActiveByDefault()
    {
        var document = MakeDocument();

        Assert.True(document.IsActive);
        Assert.Null(document.DeactivatedAt);
        Assert.Null(document.DeactivatedByUserId);
        Assert.Null(document.DeactivationReason);
    }

    [Fact]
    public void Create_NullDocumentTypeId_IsAllowed()
    {
        var document = MakeDocument(documentTypeId: null);

        Assert.Null(document.DocumentTypeId);
    }

    [Fact]
    public void Create_NoPreviousVersion()
    {
        var document = MakeDocument();

        Assert.Null(document.PreviousVersionId);
        Assert.Null(document.ChangeReason);
    }

    [Fact]
    public void Create_NullContentType_IsAllowed()
    {
        var document = Document.Create(
            orderId: 1, documentTypeId: 2,
            fileName: "f.pdf", originalFileName: "o.pdf",
            contentType: null, fileSize: 512,
            storagePath: "/s/f.pdf", uploadedByUserId: "u1");

        Assert.Null(document.ContentType);
    }

    [Fact]
    public void Create_NullUploadedByUserId_IsAllowed()
    {
        var document = Document.Create(
            orderId: 1, documentTypeId: 2,
            fileName: "f.pdf", originalFileName: "o.pdf",
            contentType: "application/pdf", fileSize: 512,
            storagePath: "/s/f.pdf", uploadedByUserId: null);

        Assert.Null(document.UploadedByUserId);
    }

    // ── SoftDelete ───────────────────────────────────────────────────────────

    [Fact]
    public void SoftDelete_SetsIsDeletedAndDeletedFields()
    {
        var document = MakeDocument();
        var now      = DateTime.UtcNow;

        document.SoftDelete("user-2", now);

        Assert.True(document.IsDeleted);
        Assert.Equal(now,      document.DeletedAt);
        Assert.Equal("user-2", document.DeletedByUserId);
        Assert.Equal(now,      document.UpdatedAt);
    }

    // ── CreateNewVersion ─────────────────────────────────────────────────────

    [Fact]
    public void CreateNewVersion_IncrementsVersion()
    {
        var v1 = MakeDocument();

        var v2 = Document.CreateNewVersion(
            previous: v1,
            fileName: "v2.pdf",
            originalFileName: "procjena-v2.pdf",
            contentType: "application/pdf",
            fileSize: 2048,
            storagePath: "/storage/1/v2.pdf",
            uploadedByUserId: "user-2",
            changeReason: "Updated appraisal");

        Assert.Equal(2, v2.Version);
        Assert.Equal(v1.Id, v2.PreviousVersionId);
    }

    [Fact]
    public void CreateNewVersion_InheritsOrderIdAndDocumentTypeId()
    {
        var v1 = MakeDocument(orderId: 42, documentTypeId: 7);

        var v2 = Document.CreateNewVersion(
            previous: v1,
            fileName: "v2.pdf",
            originalFileName: "o-v2.pdf",
            contentType: "application/pdf",
            fileSize: 512,
            storagePath: "/s/v2.pdf",
            uploadedByUserId: "user-2");

        Assert.Equal(42, v2.AppraisalOrderId);
        Assert.Equal(7, v2.DocumentTypeId);
    }

    [Fact]
    public void CreateNewVersion_SetsNewFileProperties()
    {
        var v1 = MakeDocument();

        var v2 = Document.CreateNewVersion(
            previous: v1,
            fileName: "new-file.docx",
            originalFileName: "updated.docx",
            contentType: "application/vnd.openxmlformats",
            fileSize: 4096,
            storagePath: "/storage/new-file.docx",
            uploadedByUserId: "user-3");

        Assert.Equal("new-file.docx", v2.FileName);
        Assert.Equal("updated.docx", v2.OriginalFileName);
        Assert.Equal("application/vnd.openxmlformats", v2.ContentType);
        Assert.Equal(4096, v2.FileSize);
        Assert.Equal("/storage/new-file.docx", v2.StoragePath);
        Assert.Equal("user-3", v2.UploadedByUserId);
    }

    [Fact]
    public void CreateNewVersion_WithChangeReason_StoresReason()
    {
        var v1 = MakeDocument();

        var v2 = Document.CreateNewVersion(v1, "v2.pdf", "o.pdf", null, 100, "/s/v2.pdf", "u2",
            changeReason: "Korekcija procjene");

        Assert.Equal("Korekcija procjene", v2.ChangeReason);
    }

    [Fact]
    public void CreateNewVersion_NullChangeReason_DefaultsToMessage()
    {
        var v1 = MakeDocument();

        var v2 = Document.CreateNewVersion(v1, "v2.pdf", "o.pdf", null, 100, "/s/v2.pdf", "u2",
            changeReason: null);

        Assert.Equal("Zamijenjen novom verzijom", v2.ChangeReason);
    }

    [Fact]
    public void CreateNewVersion_IsActiveByDefault()
    {
        var v1 = MakeDocument();
        var v2 = Document.CreateNewVersion(v1, "v2.pdf", "o.pdf", null, 100, "/s/v2.pdf", "u2");

        Assert.True(v2.IsActive);
    }

    [Fact]
    public void CreateNewVersion_SetsUploadedAt()
    {
        var v1 = MakeDocument();
        var before = DateTime.UtcNow;

        var v2 = Document.CreateNewVersion(v1, "v2.pdf", "o.pdf", null, 100, "/s/v2.pdf", "u2");

        var after = DateTime.UtcNow;
        Assert.InRange(v2.UploadedAt, before, after);
    }

    [Fact]
    public void CreateNewVersion_ChainedVersions_VersionIncrementsCorrectly()
    {
        var v1 = MakeDocument();
        var v2 = Document.CreateNewVersion(v1, "v2.pdf", "o.pdf", null, 100, "/s/v2.pdf", "u2");
        var v3 = Document.CreateNewVersion(v2, "v3.pdf", "o.pdf", null, 200, "/s/v3.pdf", "u3");

        Assert.Equal(1, v1.Version);
        Assert.Equal(2, v2.Version);
        Assert.Equal(3, v3.Version);
        Assert.Equal(v1.Id, v2.PreviousVersionId);
        Assert.Equal(v2.Id, v3.PreviousVersionId);
    }

    [Fact]
    public void CreateNewVersion_NullDocumentTypeId_InheritsNull()
    {
        var v1 = MakeDocument(documentTypeId: null);
        var v2 = Document.CreateNewVersion(v1, "v2.pdf", "o.pdf", null, 100, "/s/v2.pdf", "u2");

        Assert.Null(v2.DocumentTypeId);
    }

    // ── Deactivate ───────────────────────────────────────────────────────────

    [Fact]
    public void Deactivate_SetsIsActiveFalseAndDeactivationFields()
    {
        var document = MakeDocument();
        var now = new DateTime(2026, 7, 1, 12, 0, 0, DateTimeKind.Utc);

        document.Deactivate("user-3", now, "Replaced by new version");

        Assert.False(document.IsActive);
        Assert.Equal(now, document.DeactivatedAt);
        Assert.Equal("user-3", document.DeactivatedByUserId);
        Assert.Equal("Replaced by new version", document.DeactivationReason);
        Assert.Equal(now, document.UpdatedAt);
    }

    [Fact]
    public void Deactivate_NullUserIdAndReason_Allowed()
    {
        var document = MakeDocument();
        var now = DateTime.UtcNow;

        document.Deactivate(null, now, null);

        Assert.False(document.IsActive);
        Assert.Null(document.DeactivatedByUserId);
        Assert.Null(document.DeactivationReason);
    }

    // ── Reactivate ───────────────────────────────────────────────────────────

    [Fact]
    public void Reactivate_SetsIsActiveTrueAndClearsDeactivationFields()
    {
        var document = MakeDocument();
        var deactivateTime = new DateTime(2026, 7, 1, 12, 0, 0, DateTimeKind.Utc);
        document.Deactivate("user-3", deactivateTime, "Replaced");

        var reactivateTime = deactivateTime.AddHours(2);
        document.Reactivate(reactivateTime);

        Assert.True(document.IsActive);
        Assert.Null(document.DeactivatedAt);
        Assert.Null(document.DeactivationReason);
        Assert.Equal(reactivateTime, document.UpdatedAt);
    }

    [Fact]
    public void Reactivate_AlreadyActive_StillSetsUpdatedAt()
    {
        var document = MakeDocument();
        var now = DateTime.UtcNow;

        document.Reactivate(now);

        Assert.True(document.IsActive);
        Assert.Equal(now, document.UpdatedAt);
    }

    // ── Deactivate then Reactivate roundtrip ─────────────────────────────────

    [Fact]
    public void Deactivate_ThenReactivate_RestoresActiveState()
    {
        var document = MakeDocument();
        var t1 = new DateTime(2026, 7, 1, 10, 0, 0, DateTimeKind.Utc);
        var t2 = new DateTime(2026, 7, 1, 14, 0, 0, DateTimeKind.Utc);

        document.Deactivate("user-1", t1, "Temp deactivation");
        Assert.False(document.IsActive);

        document.Reactivate(t2);
        Assert.True(document.IsActive);
        Assert.Null(document.DeactivatedAt);
        Assert.Null(document.DeactivationReason);
        Assert.Equal(t2, document.UpdatedAt);
    }

    // ── SoftDelete does not affect IsActive ──────────────────────────────────

    [Fact]
    public void SoftDelete_DoesNotChangeIsActive()
    {
        var document = MakeDocument();
        var now = DateTime.UtcNow;

        document.SoftDelete("user-1", now);

        Assert.True(document.IsActive);
        Assert.True(document.IsDeleted);
    }

    // ── Deactivate does not affect IsDeleted ─────────────────────────────────

    [Fact]
    public void Deactivate_DoesNotChangeIsDeleted()
    {
        var document = MakeDocument();
        var now = DateTime.UtcNow;

        document.Deactivate("user-1", now, "test");

        Assert.False(document.IsDeleted);
        Assert.False(document.IsActive);
    }
}
