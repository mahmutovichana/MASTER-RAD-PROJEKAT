namespace RBBH.CollateralAppraisal.Application.Orders.Interfaces;

public interface IOrderNumberGenerator
{
    /// <summary>
    /// Generiše jedinstveni broj narudžbe u formatu PN-YYYY-NNNNNN.
    /// Implementacija mora garantovati jedinstvenost.
    /// </summary>
    Task<string> GenerateAsync(CancellationToken ct = default);
}
