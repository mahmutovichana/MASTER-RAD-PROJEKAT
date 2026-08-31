using RBBH.CollateralAppraisal.Domain.Common;

namespace RBBH.CollateralAppraisal.Domain.Orders;

/// <summary>
/// Mišljenje (CO ili Pravna služba) za narudžbu procjene — US 94.
/// Za svaku narudžbu kojoj je zatraženo mišljenje postoji po jedan red za CO i jedan za Pravnu.
/// "Oba gotova" = oba reda imaju status <see cref="OpinionStatus.Imported"/>
/// (vidi <see cref="AppraisalOrder.MarkOpinionsCompleted"/>).
/// </summary>
public sealed class Opinion : BaseEntity
{
    public int AppraisalOrderId { get; private set; }
    public OpinionType OpinionType { get; private set; }
    public OpinionStatus Status { get; private set; }

    // ── Import ─────────────────────────────────────────────────────────────
    public int? DocumentId { get; private set; }
    public string? ImportedByUserId { get; private set; }
    public DateTime? ImportedAt { get; private set; }
    public string? Comment { get; private set; }

    private Opinion() { }

    /// <summary>Kreira mišljenje u stanju "zatraženo" (poziva se kad AM/SM/UB klikne "Molim mišljenje...").</summary>
    public static Opinion CreateRequested(int appraisalOrderId, OpinionType opinionType)
    {
        return new Opinion
        {
            AppraisalOrderId = appraisalOrderId,
            OpinionType      = opinionType,
            Status           = OpinionStatus.Requested
        };
    }

    /// <summary>CO ili Pravna importuju svoje mišljenje (upload PDF + komentar).</summary>
    public void Import(int documentId, string userId, string? comment, DateTime now)
    {
        DocumentId       = documentId;
        ImportedByUserId = userId;
        ImportedAt       = now;
        Comment          = comment;
        Status           = OpinionStatus.Imported;
        SetUpdatedAt(now);
    }
}

/// <summary>Tip mišljenja — koja kućica ga daje.</summary>
public enum OpinionType
{
    CO     = 0,
    Pravna = 1
}

/// <summary>Status pojedinačnog mišljenja.</summary>
public enum OpinionStatus
{
    Requested = 0,
    Imported  = 1
}
