using RBBH.CollateralAppraisal.Domain.Common;

namespace RBBH.CollateralAppraisal.Domain.Orders;

/// <summary>
/// Protokolni unos za narudžbu procjene.
/// Generiše se automatski pri podnošenju narudžbe (Submit).
/// Format broja: YYYY/NNNNN — sekvencijalan po godini.
/// </summary>
public sealed class OrderProtocolEntry : BaseEntity
{
    public int    OrderId           { get; private set; }
    public AppraisalOrder? Order   { get; private set; }   // Navigation property
    public string ProtocolNumber    { get; private set; } = null!;
    public int    ProtocolYear      { get; private set; }
    public int    ProtocolSequence  { get; private set; }
    public DateTime GeneratedAt     { get; private set; }
    public string GeneratedByUserId { get; private set; } = null!;
    public ProtocolStatus Status    { get; private set; }

    private OrderProtocolEntry() { }

    public static OrderProtocolEntry Create(
        int orderId,
        int year,
        int sequence,
        string generatedByUserId,
        DateTime now)
    {
        return new OrderProtocolEntry
        {
            OrderId           = orderId,
            ProtocolNumber    = $"{year}/{sequence:D5}",
            ProtocolYear      = year,
            ProtocolSequence  = sequence,
            GeneratedAt       = now,
            GeneratedByUserId = generatedByUserId,
            Status            = ProtocolStatus.Active
        };
    }

    public void Cancel(DateTime now)
    {
        Status = ProtocolStatus.Cancelled;
        SetUpdatedAt(now);
    }
}

public enum ProtocolStatus
{
    Active    = 0,
    Cancelled = 1
}
