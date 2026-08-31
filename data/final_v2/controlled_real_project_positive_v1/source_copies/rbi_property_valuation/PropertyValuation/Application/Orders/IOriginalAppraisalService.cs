using RBBH.CollateralAppraisal.Application.Orders.Dtos;

namespace RBBH.CollateralAppraisal.Application.Orders;

public interface IOriginalAppraisalService
{
    /// <summary>
    /// Prodaja (AM/SM/UB) potvrđuje da je fizički original procjene preuzet u poslovnici.
    /// Dozvoljeno tek kada je CO odobrio procjenu (status ReadyForProcedure).
    /// </summary>
    Task<OriginalReceivedResultDto> ConfirmOriginalReceivedAsync(
        int orderId,
        CancellationToken ct = default);

    /// <summary>
    /// Šalje podsjetnik vještaku za dostavu originala procjene.
    /// Dozvoljeno samo dok original nije preuzet.
    /// </summary>
    Task<AppraiserReminderResultDto> SendAppraiserReminderAsync(
        int orderId,
        CancellationToken ct = default);

    Task<DeliverOriginalResultDto> DeliverOriginalToOfficeAsync(
        int orderId, CancellationToken ct = default);

    /// <summary>
    /// Prodaja (AM/SM/UB) potvrđuje da je saglasnost klijenta potpisana.
    /// Dostupno isključivo za PL narudžbe.
    /// </summary>
    Task<SignConsentResultDto> SignSalesConsentAsync(
        int orderId, CancellationToken ct = default);
}
