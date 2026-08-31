namespace RBBH.CollateralAppraisal.Application.Orders.Dtos;

public sealed record RequestCorrectionRequest(int ReasonCodeId, string? Comment);

public sealed record SubmitCorrectionRequest(string? Comment);

public sealed record CaDocumentReviewResultDto(
    int OrderId,
    string OrderNumber,
    string Status,
    int StatusCode,
    bool NotificationSent,
    string Message);
