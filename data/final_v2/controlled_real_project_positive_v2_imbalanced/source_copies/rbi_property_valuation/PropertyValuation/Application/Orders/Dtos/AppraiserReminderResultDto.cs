namespace RBBH.CollateralAppraisal.Application.Orders.Dtos;

public sealed record AppraiserReminderResultDto(
    int OrderId,
    string OrderNumber,
    int ReminderCount,
    DateTime LastReminderAt,
    bool NotificationSent,
    string Message);