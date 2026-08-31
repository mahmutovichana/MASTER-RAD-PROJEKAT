namespace RBBH.CollateralAppraisal.Application.Orders.Dtos;

public sealed record SignConsentResultDto(
    int       OrderId,
    string    OrderNumber,
    DateTime  SignedAt,
    string?   SignedByName,
    string    Message);
