namespace RBBH.CollateralAppraisal.Application.Reports.Dtos;

public sealed record AppraiserReminderReportDto(
    int                   TotalOverdue,
    IReadOnlyList<ReminderOrderDto> Orders,
    DateTime              GeneratedAt,
    int                   MinBusinessDaysOverdue);
