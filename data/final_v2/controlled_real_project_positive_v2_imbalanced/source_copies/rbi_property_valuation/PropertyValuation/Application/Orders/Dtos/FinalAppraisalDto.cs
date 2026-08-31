namespace RBBH.CollateralAppraisal.Application.Orders.Dtos;

public sealed record FinalAppraisalDto(
    int OrderId,
    int DocumentId,
    string OriginalFileName,
    string? ContentType,
    long FileSize,
    DateTime UploadedAt,
    string? UploadedByUserId,
    string DownloadUrl);
