namespace RBBH.CollateralAppraisal.Application.Orders.Requests;

public sealed record UpdateOrderRequest(
    string? ClientName,
    string? ClientType,
    string? ClientIdentifier,
    int?    CollateralTypeId,
    int?    CombinedCollateralTypeId,
    string? City,
    string? PropertyAddress,
    string? Branch,
    string? BranchAddress,
    string? ContactName,
    string? ContactPhone,
    string? ContactEmail,
    string? InternalNote,
    string?   DeliveryContactName      = null,
    string?   AmRecipientName          = null,
    DateTime? RequestReceivedAt        = null,
    DateTime? RequestSentAt            = null,
    decimal?  SquareMetersCommercial   = null,
    decimal?  SquareMetersResidential  = null,
    string?   PropertyCity             = null
);
