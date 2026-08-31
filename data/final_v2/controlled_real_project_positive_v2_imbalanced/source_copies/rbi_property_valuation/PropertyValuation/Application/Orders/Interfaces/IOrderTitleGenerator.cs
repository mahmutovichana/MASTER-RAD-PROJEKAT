namespace RBBH.CollateralAppraisal.Application.Orders.Interfaces;

public interface IOrderTitleGenerator
{
    /// <summary>
    /// Generiše naslov narudžbe prema poslovnom pravilu:
    /// "Narudžba procjene za {kolateral} za klijenta {klijent} grad {grad}"
    /// Ako postoji kombinovani tip, koristi se kao kolateral — inače osnovni tip.
    /// </summary>
    string Generate(
        string  collateralTypeLabel,
        string? combinedTypeLabel,
        string  clientName,
        string  city);
}
