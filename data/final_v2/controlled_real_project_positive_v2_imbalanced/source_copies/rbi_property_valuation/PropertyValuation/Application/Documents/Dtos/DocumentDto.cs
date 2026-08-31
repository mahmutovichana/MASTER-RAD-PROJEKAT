namespace RBBH.CollateralAppraisal.Application.Documents.Dtos;

public sealed record DocumentDto(
    int Id,
    int OrderId,
    int? DocumentTypeId,
    string FileName,
    string? OriginalFileName,
    string? ContentType,
    long FileSize,
    DateTime UploadedAt,
    string? UploadedByUserId,
    string DownloadUrl,
    int Version,
    int? PreviousVersionId,
    bool IsActive);