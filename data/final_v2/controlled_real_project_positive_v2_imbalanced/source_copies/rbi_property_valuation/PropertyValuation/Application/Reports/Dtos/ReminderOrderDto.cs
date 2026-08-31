namespace RBBH.CollateralAppraisal.Application.Reports.Dtos;

public sealed record ReminderOrderDto(
    int       OrderId,
    string    OrderNumber,
    string    ClientName,
    string    City,
    string    OrderStatus,
    string    StatusLabel,
    int?      AppraiserId,
    string?   AppraiserName,
    string?   AppraiserEmail,
    DateTime? OrderSentToAppraiserAt,
    DateTime? AppraisalDeliveredToCoAt,
    int       BusinessDaysOverdue);
