namespace RBBH.CollateralAppraisal.Application.Orders.Dtos;

public sealed record ApproveFinalAppraisalResultDto(
    int OrderId,
    string OrderNumber,
    string Status,
    DateTime CoApprovedAt,
    string CoApprovedByUserId,
    DateTime ReadyForProcedureAt,
    int FinalAppraisalDocumentId,
    string DownloadUrl,
    bool NotificationSent,
    string Message);
