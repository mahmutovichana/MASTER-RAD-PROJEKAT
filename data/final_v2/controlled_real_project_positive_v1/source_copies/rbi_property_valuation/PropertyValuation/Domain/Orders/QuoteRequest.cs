using RBBH.CollateralAppraisal.Domain.Common;

namespace RBBH.CollateralAppraisal.Domain.Orders;

/// <summary>
/// Zahtjev za ponudu poslan vještaku za PL narudžbu procjene.
/// CA šalje zahtjev na više vještaka koje odredi CO; nakon prijema ponuda
/// CO bira najpovoljnijeg, a ostali primaju zahvalnicu.
/// </summary>
using System.Diagnostics.CodeAnalysis;
[ExcludeFromCodeCoverage]
public sealed class QuoteRequest : BaseEntity
{
    public int AppraisalOrderId { get; private set; }
    public int AppraiserId { get; private set; }
    public QuoteRequestStatus Status { get; private set; }
    public DateTime SentAt { get; private set; }
    public DateTime Deadline { get; private set; }
    public string? SentByUserId { get; private set; }

    public decimal? OfferedPrice { get; private set; }
    public int? OfferedDays { get; private set; }
    public DateTime? RespondedAt { get; private set; }

    public DateTime? ThankYouSentAt { get; private set; }

    private QuoteRequest() { }

    public static QuoteRequest Create(
        int orderId,
        int appraiserId,
        DateTime deadline,
        string? sentByUserId,
        DateTime? now = null)
    {
        return new QuoteRequest
        {
            AppraisalOrderId = orderId,
            AppraiserId      = appraiserId,
            Status           = QuoteRequestStatus.Sent,
            SentAt           = now ?? DateTime.UtcNow,
            Deadline         = deadline,
            SentByUserId     = sentByUserId
        };
    }

    public void RecordResponse(decimal price, int days, DateTime now)
    {
        OfferedPrice = price;
        OfferedDays  = days;
        RespondedAt  = now;
        Status       = QuoteRequestStatus.Responded;
        SetUpdatedAt(now);
    }

    public void MarkSelected(DateTime now)
    {
        Status = QuoteRequestStatus.Selected;
        SetUpdatedAt(now);
    }

    public void MarkThankYouSent(DateTime now)
    {
        Status         = QuoteRequestStatus.ThankYouSent;
        ThankYouSentAt = now;
        SetUpdatedAt(now);
    }
}

public enum QuoteRequestStatus
{
    Sent         = 0,
    Responded    = 1,
    Selected     = 2,
    ThankYouSent = 3
}
