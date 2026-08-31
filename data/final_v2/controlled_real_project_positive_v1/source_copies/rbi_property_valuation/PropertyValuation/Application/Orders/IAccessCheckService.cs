using RBBH.CollateralAppraisal.Application.Orders.Dtos;

namespace RBBH.CollateralAppraisal.Application.Orders;

/// <summary>
/// CO provjera pristupa prije narudžbe (US-93) — "Uredan pristup" / "Dopuna".
/// </summary>
public interface IAccessCheckService
{
    /// <summary>CO potvrđuje uredan pristup nekretnini — narudžba ide CA na odabir vještaka.</summary>
    Task<CaDocumentReviewResultDto> ApproveAccessAsync(
        int orderId, string? comment, CancellationToken ct = default);

    /// <summary>CO traži dopunu prije odobrenja pristupa — narudžba se vraća CA na ponovni pregled.</summary>
    Task<CaDocumentReviewResultDto> RejectAccessAsync(
        int orderId, string comment, CancellationToken ct = default);
}
