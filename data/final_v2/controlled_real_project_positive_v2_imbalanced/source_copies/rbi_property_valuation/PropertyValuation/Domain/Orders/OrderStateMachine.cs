namespace RBBH.CollateralAppraisal.Domain.Orders;

/// <summary>
/// Centralna definicija dozvoljenih prelaza statusa narudžbe procjene.
/// Svaka transition metoda na <see cref="AppraisalOrder"/> poziva
/// <see cref="EnsureValidTransition"/> prije promjene statusa.
/// </summary>
public static class OrderStateMachine
{
    private static readonly Dictionary<AppraisalOrderStatus, HashSet<AppraisalOrderStatus>> ValidTransitions = new()
    {
        [AppraisalOrderStatus.Draft] = [
            AppraisalOrderStatus.SubmittedBySales,
            AppraisalOrderStatus.Cancelled
        ],
        [AppraisalOrderStatus.SubmittedBySales] = [
            AppraisalOrderStatus.AcceptedByCA,
            AppraisalOrderStatus.Cancelled
        ],
        [AppraisalOrderStatus.AcceptedByCA] = [
            AppraisalOrderStatus.DocumentationReviewInProgress
        ],
        [AppraisalOrderStatus.DocumentationReviewInProgress] = [
            AppraisalOrderStatus.ReturnedForCorrection,
            AppraisalOrderStatus.DocumentationApproved,
            AppraisalOrderStatus.AccessCheckRequested
        ],
        [AppraisalOrderStatus.ReturnedForCorrection] = [
            AppraisalOrderStatus.CorrectionSubmitted,
            AppraisalOrderStatus.Cancelled
        ],
        [AppraisalOrderStatus.CorrectionSubmitted] = [
            AppraisalOrderStatus.DocumentationReviewInProgress,
            AppraisalOrderStatus.AcceptedByCA,
            AppraisalOrderStatus.ReturnedForCorrection
        ],
        [AppraisalOrderStatus.DocumentationApproved] = [
            AppraisalOrderStatus.AccessCheckRequested,
            AppraisalOrderStatus.ProtocolCreated,
            AppraisalOrderStatus.AppraiserSelected
        ],
        [AppraisalOrderStatus.AccessCheckRequested] = [
            AppraisalOrderStatus.AccessCheckApproved,
            AppraisalOrderStatus.AccessCheckRejected
        ],
        [AppraisalOrderStatus.AccessCheckApproved] = [
            AppraisalOrderStatus.ProtocolCreated,
            AppraisalOrderStatus.AppraiserSelected
        ],
        [AppraisalOrderStatus.AccessCheckRejected] = [
            AppraisalOrderStatus.DocumentationReviewInProgress,
            AppraisalOrderStatus.ReturnedForCorrection
        ],
        [AppraisalOrderStatus.ProtocolCreated] = [
            AppraisalOrderStatus.AppraiserSelected
        ],
        [AppraisalOrderStatus.AppraiserSelected] = [
            AppraisalOrderStatus.DocumentsGenerated,
            AppraisalOrderStatus.OrderSentToAppraiser
        ],
        [AppraisalOrderStatus.DocumentsGenerated] = [
            AppraisalOrderStatus.OrderSentToAppraiser
        ],
        [AppraisalOrderStatus.OrderSentToAppraiser] = [
            AppraisalOrderStatus.AppraisalInProgress,
            AppraisalOrderStatus.AppraiserRejected,
            AppraisalOrderStatus.AdditionalPaymentRequested,
            // Vještak može direktno submitovati procjenu bez prethodnog Accept koraka
            AppraisalOrderStatus.AppraisalReceived
        ],
        [AppraisalOrderStatus.AppraiserRejected] = [
            AppraisalOrderStatus.AppraiserSelected,
            AppraisalOrderStatus.AccessCheckApproved,
            AppraisalOrderStatus.DocumentationApproved
        ],
        [AppraisalOrderStatus.AdditionalPaymentRequested] = [
            AppraisalOrderStatus.AdditionalPaymentCompleted
        ],
        [AppraisalOrderStatus.AdditionalPaymentCompleted] = [
            AppraisalOrderStatus.AppraisalInProgress,
            AppraisalOrderStatus.OrderSentToAppraiser,
            // Vještak može submitovati direktno nakon potvrđene doplate
            AppraisalOrderStatus.AppraisalReceived
        ],
        [AppraisalOrderStatus.AppraisalInProgress] = [
            AppraisalOrderStatus.AppraisalReceived,
            AppraisalOrderStatus.AdditionalPaymentRequested,
            // CA/CO administrativno odbijanje dok je vještak u izradi (RejectOrderAsync)
            AppraisalOrderStatus.AppraiserRejected
        ],
        [AppraisalOrderStatus.AppraisalReturnedForRework] = [
            AppraisalOrderStatus.AppraisalReceived
        ],
        [AppraisalOrderStatus.AppraisalReceived] = [
            AppraisalOrderStatus.ReadyForProcedure,
            AppraisalOrderStatus.AppraisalReturnedForRework,
            AppraisalOrderStatus.COApproved
        ],
        [AppraisalOrderStatus.COApproved] = [
            AppraisalOrderStatus.ReadyForProcedure
        ],
        [AppraisalOrderStatus.ReadyForProcedure] = [
            AppraisalOrderStatus.Completed
        ],
        [AppraisalOrderStatus.Completed] = [],
        [AppraisalOrderStatus.Cancelled] = []
    };

    public static bool CanTransition(AppraisalOrderStatus from, AppraisalOrderStatus to)
        => ValidTransitions.TryGetValue(from, out var allowed) && allowed.Contains(to);

    public static void EnsureValidTransition(AppraisalOrderStatus from, AppraisalOrderStatus to)
    {
        if (!CanTransition(from, to))
            throw new InvalidStateTransitionException(from, to);
    }
}
