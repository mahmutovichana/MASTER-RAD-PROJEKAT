namespace RBBH.CollateralAppraisal.Application.Documents.Dtos;

public sealed record SharedDocumentDto(
    int      Id,
    string   Title,
    string   Category,
    string   FileName,
    string   OriginalFileName,
    string?  ContentType,
    long     FileSize,
    DateTime UploadedAt,
    string?  UploadedByUserId,
    string   DownloadUrl,
    bool     IsActive);
