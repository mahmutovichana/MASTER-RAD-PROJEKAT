using RBBH.CollateralAppraisal.Application.Documents.Dtos;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Dtos;

public sealed class DocumentsDtosTests
{
    [Fact]
    public void DocumentDto_AllFieldsPopulated_StoresCorrectValues()
    {
        var uploaded = new DateTime(2026, 6, 5, 14, 30, 0, DateTimeKind.Utc);

        var dto = new DocumentDto(
            Id: 100,
            OrderId: 50,
            DocumentTypeId: 3,
            FileName: "procjena_final_v2.pdf",
            OriginalFileName: "Procjena Final V2.pdf",
            ContentType: "application/pdf",
            FileSize: 5242880,
            UploadedAt: uploaded,
            UploadedByUserId: "ca-user-5",
            DownloadUrl: "/api/orders/50/documents/100",
            Version: 2,
            PreviousVersionId: 99,
            IsActive: true);

        Assert.Equal(100, dto.Id);
        Assert.Equal(50, dto.OrderId);
        Assert.Equal(3, dto.DocumentTypeId);
        Assert.Equal("procjena_final_v2.pdf", dto.FileName);
        Assert.Equal("Procjena Final V2.pdf", dto.OriginalFileName);
        Assert.Equal("application/pdf", dto.ContentType);
        Assert.Equal(5242880, dto.FileSize);
        Assert.Equal(uploaded, dto.UploadedAt);
        Assert.Equal("ca-user-5", dto.UploadedByUserId);
        Assert.Equal("/api/orders/50/documents/100", dto.DownloadUrl);
        Assert.Equal(2, dto.Version);
        Assert.Equal(99, dto.PreviousVersionId);
        Assert.True(dto.IsActive);
    }

    [Fact]
    public void DocumentDto_NullOptionalFields_StoresNull()
    {
        var dto = new DocumentDto(
            Id: 1,
            OrderId: 1,
            DocumentTypeId: null,
            FileName: "file.bin",
            OriginalFileName: null,
            ContentType: null,
            FileSize: 0,
            UploadedAt: DateTime.UtcNow,
            UploadedByUserId: null,
            DownloadUrl: "/api/orders/1/documents/1",
            Version: 1,
            PreviousVersionId: null,
            IsActive: true);

        Assert.Null(dto.DocumentTypeId);
        Assert.Null(dto.OriginalFileName);
        Assert.Null(dto.ContentType);
        Assert.Null(dto.UploadedByUserId);
        Assert.Null(dto.PreviousVersionId);
        Assert.Equal(0, dto.FileSize);
        Assert.Equal(1, dto.Version);
    }

    [Fact]
    public void DocumentDto_InactiveDocument_StoresFalse()
    {
        var dto = new DocumentDto(
            Id: 50,
            OrderId: 10,
            DocumentTypeId: 1,
            FileName: "old_version.pdf",
            OriginalFileName: "Old Version.pdf",
            ContentType: "application/pdf",
            FileSize: 1024,
            UploadedAt: DateTime.UtcNow,
            UploadedByUserId: "user-1",
            DownloadUrl: "/api/orders/10/documents/50",
            Version: 1,
            PreviousVersionId: null,
            IsActive: false);

        Assert.False(dto.IsActive);
        Assert.Equal(1, dto.Version);
        Assert.Null(dto.PreviousVersionId);
    }

    [Fact]
    public void DocumentDto_VersionChain_StoresPreviousVersionId()
    {
        var v1 = new DocumentDto(
            Id: 10, OrderId: 5, DocumentTypeId: 1,
            FileName: "v1.pdf", OriginalFileName: "V1.pdf",
            ContentType: "application/pdf", FileSize: 1000,
            UploadedAt: DateTime.UtcNow, UploadedByUserId: "user-1",
            DownloadUrl: "/api/orders/5/documents/10",
            Version: 1, PreviousVersionId: null, IsActive: false);

        var v2 = new DocumentDto(
            Id: 11, OrderId: 5, DocumentTypeId: 1,
            FileName: "v2.pdf", OriginalFileName: "V2.pdf",
            ContentType: "application/pdf", FileSize: 2000,
            UploadedAt: DateTime.UtcNow, UploadedByUserId: "user-1",
            DownloadUrl: "/api/orders/5/documents/11",
            Version: 2, PreviousVersionId: 10, IsActive: true);

        Assert.Null(v1.PreviousVersionId);
        Assert.Equal(10, v2.PreviousVersionId);
        Assert.Equal(1, v1.Version);
        Assert.Equal(2, v2.Version);
        Assert.False(v1.IsActive);
        Assert.True(v2.IsActive);
    }

    [Fact]
    public void DocumentDto_LargeFileSize_StoresCorrectly()
    {
        var dto = new DocumentDto(
            Id: 1, OrderId: 1, DocumentTypeId: null,
            FileName: "large_file.zip", OriginalFileName: null,
            ContentType: "application/zip", FileSize: 10737418240,
            UploadedAt: DateTime.UtcNow, UploadedByUserId: null,
            DownloadUrl: "/api/orders/1/documents/1",
            Version: 1, PreviousVersionId: null, IsActive: true);

        Assert.Equal(10737418240, dto.FileSize);
    }

    [Theory]
    [InlineData("application/pdf")]
    [InlineData("image/jpeg")]
    [InlineData("image/png")]
    [InlineData("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")]
    public void DocumentDto_ContentType_AcceptsVariousTypes(string contentType)
    {
        var dto = new DocumentDto(
            Id: 1, OrderId: 1, DocumentTypeId: null,
            FileName: "file", OriginalFileName: null,
            ContentType: contentType, FileSize: 100,
            UploadedAt: DateTime.UtcNow, UploadedByUserId: null,
            DownloadUrl: "/download",
            Version: 1, PreviousVersionId: null, IsActive: true);

        Assert.Equal(contentType, dto.ContentType);
    }
}
