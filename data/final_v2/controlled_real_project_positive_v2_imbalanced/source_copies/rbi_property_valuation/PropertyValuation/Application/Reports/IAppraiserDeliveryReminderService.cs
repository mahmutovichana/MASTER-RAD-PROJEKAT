using RBBH.CollateralAppraisal.Application.Reports.Dtos;

namespace RBBH.CollateralAppraisal.Application.Reports;

/// <summary>
/// Servis za praćenje i slanje podsjetnika vještacima koji nisu dostavili
/// procjenu u roku (specifikacija S3-15).
///
/// Filter: status 'u obradi' (AppraisalInProgress, OrderSentToAppraiser...) +
///         OrderSentToAppraiserAt > N radnih dana.
///
/// Notification: "U kojem je statusu izrada procjene za klijenta XY?"
/// </summary>
public interface IAppraiserDeliveryReminderService
{
    /// <summary>
    /// Vraća listu narudžbi koje su kod vještaka duže od <paramref name="minBusinessDays"/> radnih dana.
    /// Sortiranje: najduže čekanje prvo.
    /// </summary>
    Task<AppraiserReminderReportDto> GetOverdueAppraisalsAsync(
        int?  appraiserId,
        int   minBusinessDays,
        int   page,
        int   pageSize,
        CancellationToken ct = default);

    /// <summary>
    /// Šalje email podsjetnik vještaku za narudžbu:
    /// "U kojem je statusu izrada procjene za klijenta XY?"
    /// Evidentira slanje u audit log.
    /// </summary>
    Task<ReminderSentResultDto> SendAppraisalStatusReminderAsync(
        int orderId,
        CancellationToken ct = default);
}

public sealed record ReminderSentResultDto(
    int    OrderId,
    string OrderNumber,
    bool   NotificationSent,
    string Message);
