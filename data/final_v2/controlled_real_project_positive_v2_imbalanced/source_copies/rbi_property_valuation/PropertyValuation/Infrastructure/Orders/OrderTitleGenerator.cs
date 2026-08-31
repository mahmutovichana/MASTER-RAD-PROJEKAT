using RBBH.CollateralAppraisal.Application.Orders.Interfaces;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

public sealed class OrderTitleGenerator : IOrderTitleGenerator
{
    public string Generate(
        string  collateralTypeLabel,
        string? combinedTypeLabel,
        string  clientName,
        string  city)
    {
        var collateralPart = combinedTypeLabel ?? collateralTypeLabel;
        return $"Narudžba procjene za {collateralPart} za klijenta {clientName} grad {city}";
    }
}
