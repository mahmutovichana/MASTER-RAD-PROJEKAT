namespace RBBH.CollateralAppraisal.Application.Orders.Dtos;

public sealed record OriginalReceivedResultDto(
    int OrderId,
    string OrderNumber,
    string Status,
    DateTime OriginalReceivedAt,
    string OriginalReceivedByUserId,
    bool NotificationsSent,
    string Message);

public sealed record DeliverOriginalResultDto(
    int OrderId,
    string OrderNumber,
    DateTime DeliveredAt,
    string DeliveredByUserId,
    string Message);