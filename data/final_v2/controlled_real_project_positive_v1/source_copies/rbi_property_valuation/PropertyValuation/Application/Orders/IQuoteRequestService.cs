using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Application.Orders;

/// <summary>
/// PL proces: slanje zahtjeva za ponudu na više vještaka, praćenje ponuda,
/// izbor najpovoljnijeg i slanje zahvalnice ostalima.
/// </summary>
public interface IQuoteRequestService
{
    /// <summary>CA šalje zahtjev za ponudu na odabrane vještake (PL).</summary>
    Task<SendQuoteRequestsResult> SendQuoteRequestsAsync(
        int orderId, SendQuoteRequestsInput command, CancellationToken ct = default);

    /// <summary>Lista zahtjeva za ponudu za narudžbu.</summary>
    Task<IReadOnlyList<QuoteRequestDto>> GetByOrderAsync(int orderId, CancellationToken ct = default);

    /// <summary>Vještak odgovara na zahtjev za ponudu — šalje iznos i rok izrade (AC 5).</summary>
    Task<RespondToQuoteResult> RespondToQuoteAsync(
        int orderId, int quoteRequestId, RespondToQuoteCommand command, CancellationToken ct = default);

    /// <summary>CO/CA prihvata ponudu odabranog vještaka — dodijeljuje se narudžbi (PL).</summary>
    Task<AcceptQuoteResult> AcceptQuoteAsync(int orderId, int quoteRequestId, CancellationToken ct = default);

    /// <summary>CA šalje zahvalnicu vještacima koji nisu odabrani.</summary>
    Task<SendThankYouResult> SendThankYouAsync(int orderId, CancellationToken ct = default);
}

[ExcludeFromCodeCoverage]
public sealed record AcceptQuoteResult(
    int    OrderId,
    string OrderNumber,
    int    SelectedAppraiserId,
    string SelectedAppraiserName,
    string Message);

public sealed record SendQuoteRequestsInput(
    IReadOnlyList<int> AppraiserIds,
    DateTime           Deadline);

[ExcludeFromCodeCoverage]
public sealed record SendQuoteRequestsResult(
    int    OrderId,
    string OrderNumber,
    int    SentCount,
    bool   NotificationSent,
    string Message);

public sealed record RespondToQuoteCommand(
    decimal OfferedPrice,
    int     OfferedDays);

[ExcludeFromCodeCoverage]
public sealed record RespondToQuoteResult(
    int     OrderId,
    string  OrderNumber,
    int     QuoteRequestId,
    decimal OfferedPrice,
    int     OfferedDays,
    string  Message);

[ExcludeFromCodeCoverage]
public sealed record QuoteRequestDto(
    int       Id,
    int       OrderId,
    int       AppraiserId,
    string    AppraiserName,
    string?   AppraiserCity,
    string?   AppraiserEmail,
    string    Status,
    DateTime  SentAt,
    DateTime  Deadline,
    decimal?  OfferedPrice,
    int?      OfferedDays,
    DateTime? RespondedAt,
    DateTime? ThankYouSentAt);

[ExcludeFromCodeCoverage]
public sealed record SendThankYouResult(
    int    OrderId,
    string OrderNumber,
    int    SentCount,
    string Message);