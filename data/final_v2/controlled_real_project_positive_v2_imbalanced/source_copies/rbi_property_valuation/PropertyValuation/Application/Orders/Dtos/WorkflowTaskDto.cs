namespace RBBH.CollateralAppraisal.Application.Orders.Dtos;

public sealed record WorkflowTaskDto(
    int       Id,
    int       OrderId,
    string    OrderNumber,
    string?   OrderTitle,
    string    TaskType,
    int       TaskTypeCode,
    string    Title,
    string?   Description,
    string?   AssignedRole,
    string?   AssignedUserId,
    string    Status,
    int       StatusCode,
    bool      IsLocked,
    DateTime? DueDate,
    DateTime? AcceptedAt,
    string?   AcceptedByUserId,
    DateTime? CompletedAt,
    string?   CompletedByUserId,
    string?   Comment,
    DateTime  CreatedAt
);
