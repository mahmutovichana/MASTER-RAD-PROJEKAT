namespace RBBH.CollateralAppraisal.Application.Orders;

/// <summary>
/// Faktura workflow: Protokol uploaduje → CA šalje na plaćanje → Likvidatura potvrđuje plaćanje.
/// Tri user story-ja: US-F1 (upload), US-F2 (plaćanje), US-F3 (evidentiranje).
/// </summary>
public interface IInvoiceWorkflowService
{
    /// <summary>US-F1: Protokol uploaduje fakturu vještaka — bilježi ime/datum, notifikacija CA.</summary>
    Task<InvoiceWorkflowResultDto> UploadInvoiceAsync(
        int orderId, int documentId, CancellationToken ct = default);

    /// <summary>US-F2: CA šalje fakturu na plaćanje — status → 'u obradi', notifikacije prema FL/PL pravilima.</summary>
    Task<InvoiceWorkflowResultDto> SendForPaymentAsync(
        int orderId, CancellationToken ct = default);

    /// <summary>US-F3: Likvidatura potvrđuje plaćanje — status → 'plaćeno'.</summary>
    Task<InvoiceWorkflowResultDto> ConfirmPaidAsync(
        int orderId, CancellationToken ct = default);

    /// <summary>Vraća trenutni status fakture za narudžbu (evidencija tko/kad).</summary>
    Task<InvoiceStatusDto> GetStatusAsync(
        int orderId, CancellationToken ct = default);
}

public sealed record InvoiceWorkflowResultDto(
    int OrderId,
    string OrderNumber,
    string InvoiceStatus,
    bool NotificationSent,
    string Message);

public sealed record InvoiceStatusDto(
    int OrderId,
    string OrderNumber,
    string Status,
    string? UploadedByName,
    DateTime? UploadedAt,
    string? SentForPaymentByName,
    DateTime? SentForPaymentAt,
    string? PaidByName,
    DateTime? PaidAt,
    int? InvoiceDocumentId);
