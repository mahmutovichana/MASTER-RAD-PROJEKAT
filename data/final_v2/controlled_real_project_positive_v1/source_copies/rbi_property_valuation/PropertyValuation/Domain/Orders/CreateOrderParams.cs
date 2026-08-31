namespace RBBH.CollateralAppraisal.Domain.Orders;

public sealed record CreateOrderParams
{
    public required string OrderNumber { get; init; }
    public required string Title { get; init; }
    public required string ClientName { get; init; }
    public string? ClientType { get; init; }
    public string? ClientIdentifier { get; init; }
    public string? ContactName { get; init; }
    public string? ContactPhone { get; init; }
    public string? ContactEmail { get; init; }
    public string? City { get; init; }
    public string? Branch { get; init; }
    public string? BranchAddress { get; init; }
    public string? PropertyAddress { get; init; }
    public string? PropertyCity { get; init; }
    public int? CollateralTypeId { get; init; }
    public int? CombinedCollateralTypeId { get; init; }
    public required string CreatedByUserId { get; init; }
    public required string CreatedByRole { get; init; }
    public string? CreatedByName { get; init; }
    public string? CreatedByEmail { get; init; }
    public string? DeliveryContactName { get; init; }
    public string? AmRecipientName { get; init; }
    public WorkflowType? WorkflowType { get; init; }
    public DateTime? RequestReceivedAt { get; init; }
    public DateTime? RequestSentAt { get; init; }
    public decimal? SquareMetersCommercial { get; init; }
    public decimal? SquareMetersResidential { get; init; }
    public int? CityId { get; init; }
    public int? BranchId { get; init; }
}
