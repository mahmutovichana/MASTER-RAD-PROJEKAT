namespace RBBH.CollateralAppraisal.Domain.Orders;

/// <summary>
/// Centralna definicija lanca odgovornosti narudžbe procjene po <see cref="WorkflowType"/>.
/// Daje "ko je trenutno vlasnik" i "ko je sljedeći odgovoran" na osnovu statusa —
/// koristi se za vidljivost workflow-a (timeline, dashboard, audit).
///
/// FL (Slika 4):   Prodaja → CA → Vještak → CO
/// PL (Slika 4.1): Prodaja → CA → CO → CA → Prodaja → CA → Vještak → CO
///
/// Role su poslovni segmenti (ne nužno tačan Keycloak naziv): "Prodaja" = AM/SM/UB.
/// </summary>
public static class OrderWorkflowRouting
{
    public const string Prodaja = "Prodaja";
    public const string CA      = "Kolateral administrator";
    public const string CO      = "Kolateral oficir";
    public const string Vjestak = "Vještak";

    /// <summary>Rola koja je trenutno odgovorna za narudžbu (kod koga je "lopta").</summary>
    public static string CurrentOwnerRole(WorkflowType? type, AppraisalOrderStatus status) => status switch
    {
        AppraisalOrderStatus.Draft                          => Prodaja,
        AppraisalOrderStatus.SubmittedBySales               => CA,
        AppraisalOrderStatus.AcceptedByCA                   => CA,
        AppraisalOrderStatus.DocumentationReviewInProgress  => CA,
        AppraisalOrderStatus.ReturnedForCorrection          => Prodaja,
        AppraisalOrderStatus.CorrectionSubmitted            => CA,
        AppraisalOrderStatus.DocumentationApproved          => CA,
        AppraisalOrderStatus.AccessCheckRequested           => CO,
        AppraisalOrderStatus.AccessCheckApproved            => CA,
        AppraisalOrderStatus.AccessCheckRejected            => CA,
        AppraisalOrderStatus.ProtocolCreated                => CA,
        AppraisalOrderStatus.AppraiserSelected              => CA,
        AppraisalOrderStatus.DocumentsGenerated             => CA,
        AppraisalOrderStatus.OrderSentToAppraiser           => Vjestak,
        AppraisalOrderStatus.AdditionalPaymentRequested     => CA,
        AppraisalOrderStatus.AdditionalPaymentCompleted     => Vjestak,
        AppraisalOrderStatus.AppraisalInProgress            => Vjestak,
        AppraisalOrderStatus.AppraisalReceived              => CO,
        AppraisalOrderStatus.COApproved                     => CO,
        AppraisalOrderStatus.ReadyForProcedure              => Prodaja,
        AppraisalOrderStatus.Completed                      => "—",
        AppraisalOrderStatus.Cancelled                      => "—",
        _                                                   => "—"
    };

    /// <summary>Rola koja je sljedeća na potezu nakon trenutnog koraka.</summary>
    public static string NextResponsibleRole(WorkflowType? type, AppraisalOrderStatus status) => status switch
    {
        AppraisalOrderStatus.Draft                          => CA,
        AppraisalOrderStatus.SubmittedBySales               => CA,
        AppraisalOrderStatus.AcceptedByCA                   => CA,
        // PL: nakon pregleda dokumentacije ide na CO (provjera pristupa); FL: direktno na vještaka.
        AppraisalOrderStatus.DocumentationReviewInProgress  => type == WorkflowType.PravnaLica ? CO : Vjestak,
        AppraisalOrderStatus.ReturnedForCorrection          => Prodaja,
        AppraisalOrderStatus.CorrectionSubmitted            => CA,
        AppraisalOrderStatus.DocumentationApproved          => type == WorkflowType.PravnaLica ? CO : Vjestak,
        AppraisalOrderStatus.AccessCheckRequested           => CO,
        AppraisalOrderStatus.AccessCheckApproved            => Vjestak,
        AppraisalOrderStatus.AccessCheckRejected            => Prodaja,
        AppraisalOrderStatus.ProtocolCreated                => Vjestak,
        AppraisalOrderStatus.AppraiserSelected              => Vjestak,
        AppraisalOrderStatus.DocumentsGenerated             => Vjestak,
        AppraisalOrderStatus.OrderSentToAppraiser           => CO,
        AppraisalOrderStatus.AdditionalPaymentRequested     => Vjestak,
        AppraisalOrderStatus.AdditionalPaymentCompleted     => CO,
        AppraisalOrderStatus.AppraisalInProgress            => CO,
        AppraisalOrderStatus.AppraisalReceived              => CO,
        AppraisalOrderStatus.COApproved                     => Prodaja,
        AppraisalOrderStatus.ReadyForProcedure              => Prodaja,
        AppraisalOrderStatus.Completed                      => "—",
        AppraisalOrderStatus.Cancelled                      => "—",
        _                                                   => "—"
    };
}
