using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Application.Orders;

/// <summary>
/// Post-selekcijski lifecycle vještaka: slanje, prihvatanje/odbijanje, plaćanje, dostava procjene.
/// Zajednički za FL i PL workflow. Separiran iz IAppraiserAssignmentService (I-2 refactoring).
/// </summary>
public interface IAppraiserOrderLifecycleService
{
    /// <summary>CA šalje narudžbu odabranom vještaku — obavijest + paket dokumenata.</summary>
    Task<SendToAppraiserResultDto> SendToAppraiserAsync(int orderId, CancellationToken ct = default);

    /// <summary>Lista dokumenata narudžbe za odabranog vještaka (download linkovi).</summary>
    Task<AppraiserPackageDto> GetAppraiserPackageAsync(int orderId, CancellationToken ct = default);

    /// <summary>Vještak prihvata dodijeljenu narudžbu — status → AppraisalInProgress.</summary>
    Task<SendToAppraiserResultDto> AcceptByAppraiserAsync(int orderId, CancellationToken ct = default);

    /// <summary>Vještak odbija narudžbu — notifikacija CA, automatski odabir sljedećeg.</summary>
    Task<SendToAppraiserResultDto> RejectByAppraiserAsync(
        int orderId, AppraiserDeclineReason reason, string? freeText, CancellationToken ct = default);

    /// <summary>Vještak traži doplatu — CA prima notifikaciju.</summary>
    Task<SendToAppraiserResultDto> RequestAdditionalPaymentAsync(int orderId, CancellationToken ct = default);

    /// <summary>CA potvrđuje doplatu — vještak prima notifikaciju i nastavlja.</summary>
    Task<SendToAppraiserResultDto> ConfirmAdditionalPaymentAsync(int orderId, CancellationToken ct = default);

    /// <summary>Vještak dostavlja procjenu — status → AppraisalReceived, notifikacija CO.</summary>
    Task<SendToAppraiserResultDto> SubmitAppraisalAsync(int orderId, DateTime? visitDate = null, CancellationToken ct = default);

    /// <summary>CA/CO odbija narudžbu — auto-reassign, notifikacije.</summary>
    Task<SendToAppraiserResultDto> RejectOrderAsync(
        int orderId, string rejectionReason, string? rejectionComment, CancellationToken ct = default);

    /// <summary>Vještak završava import potpisanih dokumenata — notifikacija CA.</summary>
    Task<SendToAppraiserResultDto> CompleteSignedDocumentImportAsync(int orderId, CancellationToken ct = default);
}
