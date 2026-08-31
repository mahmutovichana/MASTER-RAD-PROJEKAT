using RBBH.CollateralAppraisal.Application.Orders.Dtos;

namespace RBBH.CollateralAppraisal.Application.Orders.Interfaces;

/// <summary>
/// Workflow akcije na narudžbama — podnošenje i otkazivanje.
/// Sub-interfejs od IAppraisalOrderService (I-1 refactoring).
/// </summary>
public interface IOrderSubmitService
{
    /// <summary>
    /// Prodajna uloga podnosi narudžbu CA-u (Draft → SubmittedBySales).
    /// Kreira task za CA, šalje notifikaciju. Transakcijski.
    /// </summary>
    Task<AppraisalOrderDto> SubmitAsync(int id, CancellationToken ct = default);

    /// <summary>Otkazivanje narudžbe (dozvoljeno u Draft i Submitted fazama).</summary>
    Task CancelAsync(int id, CancellationToken ct = default);
}
