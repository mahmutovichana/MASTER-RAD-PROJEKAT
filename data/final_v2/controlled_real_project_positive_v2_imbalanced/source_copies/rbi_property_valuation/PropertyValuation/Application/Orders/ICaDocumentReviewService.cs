using RBBH.CollateralAppraisal.Application.Orders.Dtos;

namespace RBBH.CollateralAppraisal.Application.Orders;

/// <summary>
/// CA pregled dokumentacije (US-91/92) — petlja "Dopuna podataka" ↔ "Podaci dopunjeni" / "Završi pregled".
/// </summary>
public interface ICaDocumentReviewService
{
    /// <summary>CA vraća narudžbu Prodaji na dopunu podataka, sa razlogom i komentarom.</summary>
    Task<CaDocumentReviewResultDto> RequestCorrectionAsync(
        int orderId, int reasonCodeId, string? comment, CancellationToken ct = default);

    /// <summary>CA završava pregled dokumentacije — dokumentacija je odobrena.</summary>
    Task<CaDocumentReviewResultDto> CompleteReviewAsync(
        int orderId, CancellationToken ct = default);

    /// <summary>Prodaja potvrđuje da je dopuna dostavljena — narudžba ide ponovo CA na pregled.</summary>
    Task<CaDocumentReviewResultDto> SubmitCorrectionAsync(
        int orderId, string? comment, CancellationToken ct = default);
}
