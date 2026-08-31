using RBBH.CollateralAppraisal.Application.Orders.Dtos;

namespace RBBH.CollateralAppraisal.Application.Orders;

public interface IOrderApprovalService
{
    Task<ApproveFinalAppraisalResultDto> ApproveFinalAppraisalAsync(
        int orderId,
        int? appraiserRating = null,
        CancellationToken ct = default);

    Task<FinalAppraisalDto> GetFinalAppraisalAsync(
        int orderId,
        CancellationToken ct = default);

    /// <summary>CO vraća procjenu na doradu — vještak prima email s komentarom, neograničen broj vraćanja.</summary>
    Task<ReturnForReworkResultDto> ReturnForReworkAsync(
        int orderId,
        string internalCategory,
        string comment,
        CancellationToken ct = default);
}

public sealed record ReturnForReworkResultDto(
    int OrderId,
    string OrderNumber,
    string Status,
    bool NotificationSent,
    string Message);
