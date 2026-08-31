namespace RBBH.CollateralAppraisal.Domain.Orders;

/// <summary>
/// Baca se kada domain metoda pokuša prelaz koji OrderStateMachine ne dozvoljava.
/// GlobalExceptionHandler mapira ovu iznimku na HTTP 409 Conflict.
/// </summary>
public sealed class InvalidStateTransitionException : Exception
{
    public AppraisalOrderStatus From { get; }
    public AppraisalOrderStatus To   { get; }

    public InvalidStateTransitionException(AppraisalOrderStatus from, AppraisalOrderStatus to)
        : base($"Nedozvoljen prelaz statusa narudžbe: {from} → {to}.")
    {
        From = from;
        To   = to;
    }
}
