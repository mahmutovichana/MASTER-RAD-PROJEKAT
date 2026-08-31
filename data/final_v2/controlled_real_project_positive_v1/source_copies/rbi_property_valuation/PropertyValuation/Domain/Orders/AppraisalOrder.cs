using RBBH.CollateralAppraisal.Domain.Common;

namespace RBBH.CollateralAppraisal.Domain.Orders;

/// <summary>
/// Centralni entitet koji predstavlja narudžbu procjene nekretnine.
/// Povezuje prodaju, CA, CO, Pravnu službu, dokumente, taskove, protokol, vještaka.
///
/// NAPOMENA: Konačni workflow (statusi, prijelazi, validacije) zahtijeva potvrdu poslovnog korisnika.
/// Pogledati docs/adr/ADR-workflow-rules.md.
/// </summary>
public sealed class AppraisalOrder : BaseEntity, IConcurrencyAware
{
    public uint RowVersion { get; private set; }

    // ── Identifikacija ─────────────────────────────────────────────────────
    public string OrderNumber { get; private set; } = null!;
    public string Title { get; private set; } = null!;
    public AppraisalOrderStatus Status { get; private set; }

    /// <summary>
    /// Tip workflow-a (Fizička/Pravna lica) — odabran na ulaznom ekranu, određuje
    /// cijeli tok narudžbe (routing, statusi, lanac rola). Nullable za stare nacrte.
    /// </summary>
    public WorkflowType? WorkflowType { get; private set; }

    // ── Klijent ────────────────────────────────────────────────────────────
    public string ClientName { get; private set; } = null!;
    public string? ClientType { get; private set; }          // FL, PL, itd.
    public string? ClientIdentifier { get; private set; }    // JMBG / Matični broj

    // ── Kontakt ────────────────────────────────────────────────────────────
    public string? ContactName { get; private set; }
    public string? ContactPhone { get; private set; }
    public string? ContactEmail { get; private set; }

    // ── Poslovnica ─────────────────────────────────────────────────────────
    public string? Branch { get; private set; }
    public string? BranchAddress { get; private set; }
    public string? City { get; private set; }

    // ── FK reference na normalizirane tabele (P1.1 — referencijalni integritet) ──
    public int? CityId { get; private set; }
    public int? BranchId { get; private set; }

    // ── Kolateral ──────────────────────────────────────────────────────────
    public int? CollateralTypeId { get; private set; }
    public int? CombinedCollateralTypeId { get; private set; }
    public string? PropertyAddress { get; private set; }
    public string? PropertyCity { get; private set; }

    // ── Kreator ────────────────────────────────────────────────────────────
    public string? CreatedByUserId { get; private set; }
    public string? CreatedByRole { get; private set; }
    public string? CreatedByName { get; private set; }
    public string? CreatedByEmail { get; private set; }

    // ── Dostava / AM za slanje procjene ───────────────────────────────────
    public string? DeliveryContactName { get; private set; }
    public string? AmRecipientName { get; private set; }

    // ── Preuzimanje CA ─────────────────────────────────────────────────────
    public string? AcceptedByCAUserId { get; private set; }
    public string? AcceptedByCAName { get; private set; }
    public DateTime? AcceptedAt { get; private set; }
    public DateTime? SubmittedAt { get; private set; }
    public DocumentationReviewStatus? DocumentationReviewStatus { get; private set; }

    // ── Vještak ────────────────────────────────────────────────────────────
    public int? AppraiserId { get; private set; }

    // ── Soft delete ────────────────────────────────────────────────────────
    public bool IsDeleted { get; private set; }
    public DateTime? DeletedAt { get; private set; }
    public string? DeletedByUserId { get; private set; }

    // ── PL-specifična polja (Pravna lica) ─────────────────────────────────
    public decimal? SquareMetersCommercial  { get; private set; }  // Broj m² poslovnog dijela
    public decimal? SquareMetersResidential { get; private set; }  // Broj m² stambenog dijela

    // ── Napomene ───────────────────────────────────────────────────────────
    public string? InternalNote { get; private set; }

    // ── CA polja ──────────────────────────────────────────────────────────
    public string? PaymentConsentStatus { get; private set; }

    // ── Finalna procjena / odobrenje CO (US 93) ───────────────────────────
    public int? FinalAppraisalDocumentId { get; private set; }
    public DateTime? CoApprovedAt { get; private set; }
    public string? CoApprovedByUserId { get; private set; }
    public DateTime? ReadyForProcedureAt { get; private set; }

    // ── Original procjene u poslovnici (US 93) ────────────────────────────
    public DateTime? OriginalReceivedAt { get; private set; }
    public string? OriginalReceivedByUserId { get; private set; }
    public int CorrectionCount { get; private set; }
    public int AppraiserReminderCount { get; private set; }
    public DateTime? AppraiserReminderLastSentAt { get; private set; }

    // ── Mišljenja CO i Pravne službe (US 94) ──────────────────────────────
    public DateTime? OpinionsCompletedAt { get; private set; }

    // ── Datum prijema / slanja zahtjeva (kućica Prodaja) ──────────────────
    public DateTime? RequestReceivedAt { get; private set; }
    public DateTime? RequestSentAt     { get; private set; }

    // ── Faktura (kućica CA) ───────────────────────────────────────────────
    public DateTime? InvoiceSentDate     { get; private set; }
    public DateTime? InvoiceReceivedDate { get; private set; }

    // ── Faktura workflow (US-F1/F2/F3) ───────────────────────────────────
    public InvoiceWorkflowStatus InvoiceStatus { get; private set; }
    public int?      InvoiceDocumentId           { get; private set; }
    public string?   InvoiceUploadedByUserId     { get; private set; }
    public string?   InvoiceUploadedByName       { get; private set; }
    public DateTime? InvoiceUploadedAt            { get; private set; }
    public string?   InvoiceSentForPaymentByUserId { get; private set; }
    public string?   InvoiceSentForPaymentByName   { get; private set; }
    public DateTime? InvoiceSentForPaymentAt        { get; private set; }
    public string?   InvoicePaidByUserId           { get; private set; }
    public string?   InvoicePaidByName             { get; private set; }
    public DateTime? InvoicePaidAt                  { get; private set; }

    // ── Procjena / vještak ────────────────────────────────────────────────
    public DateTime? AppraiserVisitDate { get; private set; }
    public int? AppraiserRating         { get; private set; }
    public string? EsgCertificate       { get; private set; }

    // ── CO pregled dokumentacije (DIO_1: Slika 15.7 — datumi CO workflow-a) ─
    public DateTime? CoDocumentationReviewStartedAt { get; private set; }
    public DateTime? CoOpinionSentToAmAt            { get; private set; }

    // ── Spec DIO_2 str. 66-68: protokol polja ────────────────────────────
    public decimal? AppraisalFee                  { get; private set; }
    public string?  CollateralStatus              { get; private set; }
    public DateTime? OrderSentToAppraiserAt        { get; private set; }
    public DateTime? SignedDocumentsReceivedAt      { get; private set; }
    public DateTime? DocumentationSupplementAt     { get; private set; }
    public DateTime? AppraisalDeliveredToCoAt       { get; private set; }
    public DateTime? CorrectionRequestedAt         { get; private set; }
    public DateTime? CorrectedAppraisalReceivedAt  { get; private set; }

    // ── Saglasnost klijenta — PL-specifičan korak (kućica Prodaja) ────────
    public bool      SalesConsentSigned       { get; private set; }
    public DateTime? SalesConsentSignedAt     { get; private set; }
    public string?   SalesConsentSignedByName { get; private set; }

    private AppraisalOrder() { }

    // ── Workflow type helpers ─────────────────────────────────────────────────
    // WorkflowType je kanonski diskriminator; ClientType ("FL"/"PL") je legacy
    // string koji se čuva radi kompatibilnosti. Za sve operativne provjere
    // koristiti IsFL() / IsPL() — nikad direktno order.ClientType == "FL".

    /// <summary>
    /// Razrješava WorkflowType za narudžbu, uključujući stare nacrte bez postavljenog
    /// WorkflowType-a (koristi ClientType kao fallback).
    /// </summary>
    public WorkflowType EffectiveWorkflowType =>
        WorkflowType ?? WorkflowTypes.FromClientType(ClientType);

    /// <summary>True za narudžbe fizičkih lica (FL workflow).</summary>
    public bool IsFL() => EffectiveWorkflowType == WorkflowTypes.FromClientType("FL");

    /// <summary>True za narudžbe pravnih lica (PL workflow).</summary>
    public bool IsPL() => EffectiveWorkflowType == WorkflowTypes.FromClientType("PL");

    public static AppraisalOrder Create(
        string orderNumber,
        string title,
        string clientName,
        string? clientType,
        string? clientIdentifier,
        string? contactName,
        string? contactPhone,
        string? contactEmail,
        string? city,
        string? branch,
        string? branchAddress,
        string? propertyAddress,
        int? collateralTypeId,
        int? combinedCollateralTypeId,
        string createdByUserId,
        string createdByRole,
        string? createdByName,
        string? deliveryContactName,
        string? amRecipientName,
        WorkflowType? workflowType = null,
        DateTime? requestReceivedAt = null,
        DateTime? requestSentAt = null,
        decimal? squareMetersCommercial = null,
        decimal? squareMetersResidential = null,
        string? propertyCity = null,
        string? createdByEmail = null,
        int? cityId = null,
        int? branchId = null)
    {
        return new AppraisalOrder
        {
            OrderNumber               = orderNumber,
            Title                     = title,
            WorkflowType              = workflowType,
            ClientName                = clientName,
            ClientType                = clientType ?? (workflowType is { } wt ? WorkflowTypes.ToClientType(wt) : null),
            ClientIdentifier          = clientIdentifier,
            ContactName               = contactName,
            ContactPhone              = contactPhone,
            ContactEmail              = contactEmail,
            City                      = city,
            Branch                    = branch,
            BranchAddress             = branchAddress,
            PropertyAddress           = propertyAddress,
            PropertyCity              = propertyCity,
            CollateralTypeId          = collateralTypeId,
            CombinedCollateralTypeId  = combinedCollateralTypeId,
            CreatedByUserId           = createdByUserId,
            CreatedByRole             = createdByRole,
            CreatedByName             = createdByName,
            CreatedByEmail            = createdByEmail,
            DeliveryContactName       = deliveryContactName,
            AmRecipientName           = amRecipientName,
            RequestReceivedAt         = requestReceivedAt,
            RequestSentAt             = requestSentAt,
            SquareMetersCommercial    = squareMetersCommercial,
            SquareMetersResidential   = squareMetersResidential,
            CityId                    = cityId,
            BranchId                  = branchId,
            Status                    = AppraisalOrderStatus.Draft
        };
    }

    public void SetCityReference(int? cityId, DateTime now)
    {
        CityId = cityId;
        SetUpdatedAt(now);
    }

    public void SetBranchReference(int? branchId, DateTime now)
    {
        BranchId = branchId;
        SetUpdatedAt(now);
    }

    public void UpdateTitle(string title, DateTime now)
    {
        Title = title;
        SetUpdatedAt(now);
    }

    /// <summary>
    /// Postavlja tip workflow-a (Fizička/Pravna lica) i automatski usklađuje ClientType.
    /// Koristi se kad se nacrt kreira sa ulaznog ekrana ili kad se mijenja tip prije slanja.
    /// </summary>
    public void SetWorkflowType(WorkflowType type, DateTime now)
    {
        WorkflowType = type;
        ClientType   = WorkflowTypes.ToClientType(type);
        SetUpdatedAt(now);
    }

    public void UpdateDraft(
        string title,
        string clientName,
        string? clientType,
        string? clientIdentifier,
        string? contactName,
        string? contactPhone,
        string? contactEmail,
        string? city,
        string? branch,
        string? branchAddress,
        string? propertyAddress,
        int? collateralTypeId,
        int? combinedCollateralTypeId,
        string? deliveryContactName,
        string? amRecipientName,
        DateTime now,
        DateTime? requestReceivedAt = null,
        DateTime? requestSentAt = null,
        decimal? squareMetersCommercial = null,
        decimal? squareMetersResidential = null,
        string? propertyCity = null)
    {
        Title                     = title;
        ClientName                = clientName;
        ClientType                = clientType;
        ClientIdentifier          = clientIdentifier;
        ContactName               = contactName;
        ContactPhone              = contactPhone;
        ContactEmail              = contactEmail;
        City                      = city;
        Branch                    = branch;
        BranchAddress             = branchAddress;
        PropertyAddress           = propertyAddress;
        PropertyCity              = propertyCity;
        CollateralTypeId          = collateralTypeId;
        CombinedCollateralTypeId  = combinedCollateralTypeId;
        DeliveryContactName       = deliveryContactName;
        AmRecipientName           = amRecipientName;
        RequestReceivedAt         = requestReceivedAt;
        RequestSentAt             = requestSentAt;
        SquareMetersCommercial    = squareMetersCommercial;
        SquareMetersResidential   = squareMetersResidential;
        SetUpdatedAt(now);
    }

    public void Submit(DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.SubmittedBySales);
        Status        = AppraisalOrderStatus.SubmittedBySales;
        SubmittedAt   = now;
        RequestSentAt ??= now;
        SetUpdatedAt(now);
    }

    public void AcceptByCA(string caUserId, string? caName, DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.AcceptedByCA);
        Status                    = AppraisalOrderStatus.AcceptedByCA;
        AcceptedByCAUserId        = caUserId;
        AcceptedByCAName          = caName;
        AcceptedAt                = now;
        DocumentationReviewStatus = Orders.DocumentationReviewStatus.NijePregledano;
        SetUpdatedAt(now);
    }

    /// <summary>CA počinje pregled dokumentacije (US-91/92).</summary>
    public void StartDocumentationReview(DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.DocumentationReviewInProgress);
        Status = AppraisalOrderStatus.DocumentationReviewInProgress;
        DocumentationReviewStatus = Orders.DocumentationReviewStatus.UToku;
        SetUpdatedAt(now);
    }

    /// <summary>CA vraća narudžbu Prodaji na dopunu podataka.</summary>
    public void ReturnForCorrection(DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.ReturnedForCorrection);
        Status = AppraisalOrderStatus.ReturnedForCorrection;
        DocumentationReviewStatus = Orders.DocumentationReviewStatus.Vraceno;
        CorrectionCount++;
        SetUpdatedAt(now);
    }

    /// <summary>Prodaja je dostavila dopunu — narudžba ide ponovo CA na pregled.</summary>
    public void SubmitCorrection(DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.CorrectionSubmitted);
        Status = AppraisalOrderStatus.CorrectionSubmitted;
        DocumentationSupplementAt = now;
        SetUpdatedAt(now);
    }

    /// <summary>CA je završio pregled dokumentacije — dokumentacija je odobrena.</summary>
    public void ApproveDocumentation(DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.DocumentationApproved);
        Status = AppraisalOrderStatus.DocumentationApproved;
        DocumentationReviewStatus = Orders.DocumentationReviewStatus.Odobreno;
        SetUpdatedAt(now);
    }

    /// <summary>CO potvrđuje uredan pristup nekretnini — narudžba ide na odabir vještaka.</summary>
    public void ApproveAccessCheck(DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.AccessCheckApproved);
        Status = AppraisalOrderStatus.AccessCheckApproved;
        SetUpdatedAt(now);
    }

    /// <summary>CO traži dopunu prije odobrenja pristupa — narudžba se vraća CA na ponovni pregled.</summary>
    public void RejectAccessCheck(DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.AccessCheckRejected);
        Status = AppraisalOrderStatus.AccessCheckRejected;
        SetUpdatedAt(now);
    }

    /// <summary>CA odabire vještaka za narudžbu (FL automatski ili PL ručno) — narudžba ide na slanje vještaku.</summary>
    public void SelectAppraiser(int appraiserId, DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.AppraiserSelected);
        AppraiserId = appraiserId;
        Status      = AppraisalOrderStatus.AppraiserSelected;
        SetUpdatedAt(now);
    }

    /// <summary>CA šalje narudžbu odabranom vještaku (dokumentacija + obavijest).</summary>
    public void SendToAppraiser(DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.OrderSentToAppraiser);
        Status = AppraisalOrderStatus.OrderSentToAppraiser;
        OrderSentToAppraiserAt = now;
        SetUpdatedAt(now);
    }

    /// <summary>Vještak prihvata dodijeljenu narudžbu i započinje izradu procjene.</summary>
    public void StartAppraisal(DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.AppraisalInProgress);
        Status = AppraisalOrderStatus.AppraisalInProgress;
        SetUpdatedAt(now);
    }

    /// <summary>Vještak odbija narudžbu — briše se dodijeljeni vještak, status → AppraiserRejected.</summary>
    public void RejectByAppraiser(DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.AppraiserRejected);
        AppraiserId = null;
        Status = AppraisalOrderStatus.AppraiserRejected;
        SetUpdatedAt(now);
    }

    /// <summary>CO vraća procjenu na doradu — status → AppraisalReturnedForRework.</summary>
    public void ReturnForRework(DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.AppraisalReturnedForRework);
        Status = AppraisalOrderStatus.AppraisalReturnedForRework;
        FinalAppraisalDocumentId = null;
        CorrectionRequestedAt = now;
        SetUpdatedAt(now);
    }

    /// <summary>Vještak dostavlja korigovanu procjenu nakon dorade — status → AppraisalReceived.</summary>
    public void SubmitReworkedAppraisal(int documentId, DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.AppraisalReceived);
        FinalAppraisalDocumentId = documentId;
        Status = AppraisalOrderStatus.AppraisalReceived;
        CorrectedAppraisalReceivedAt = now;
        SetUpdatedAt(now);
    }

    /// <summary>Vještak traži doplatu — narudžba ide CA-u na obradu uplate.</summary>
    public void RequestAdditionalPayment(DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.AdditionalPaymentRequested);
        Status = AppraisalOrderStatus.AdditionalPaymentRequested;
        SetUpdatedAt(now);
    }

    /// <summary>CA potvrđuje da je doplata izvršena — narudžba se vraća vještaku.</summary>
    public void CompleteAdditionalPayment(DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.AdditionalPaymentCompleted);
        Status = AppraisalOrderStatus.AdditionalPaymentCompleted;
        SetUpdatedAt(now);
    }

    /// <summary>CO inicira provjeru pristupa nekretnini (PL/FL) — status → AccessCheckRequested.</summary>
    public void RequestAccessCheck(DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.AccessCheckRequested);
        Status = AppraisalOrderStatus.AccessCheckRequested;
        SetUpdatedAt(now);
    }

    [Obsolete("Koristiti specifične transition metode (Submit, AcceptByCA, itd.). Zadržano samo za seeding/testove.")]
    public void ChangeStatus(AppraisalOrderStatus newStatus, DateTime now)
    {
        Status = newStatus;
        SetUpdatedAt(now);
    }

    public void SetInternalNote(string? note, DateTime now)
    {
        InternalNote = note;
        SetUpdatedAt(now);
    }

    public void SoftDelete(string userId, DateTime now)
    {
        IsDeleted       = true;
        DeletedAt       = now;
        DeletedByUserId = userId;
        SetUpdatedAt(now);
    }

    /// <summary>Vještak/CA evidentira finalni dokument procjene (US 93, kućica 4).</summary>
    public void SetFinalAppraisalDocument(int documentId, DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.AppraisalReceived);
        FinalAppraisalDocumentId = documentId;
        AppraisalDeliveredToCoAt = now;
        Status                   = AppraisalOrderStatus.AppraisalReceived;
        SetUpdatedAt(now);
    }

    /// <summary>CO odobrava finalnu procjenu — narudžba je uredna i ide dalje u proceduru.</summary>
    public void ApproveByCO(string coUserId, DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.ReadyForProcedure);
        CoApprovedAt        = now;
        CoApprovedByUserId  = coUserId;
        ReadyForProcedureAt = now;
        Status              = AppraisalOrderStatus.ReadyForProcedure;
        SetUpdatedAt(now);
    }

    /// <summary>
    /// Prodaja/poslovnica potvrđuje preuzimanje fizičkog originala procjene — posljednji
    /// korak procesa. Narudžba se time finalizira (status → Završeno/Completed).
    /// </summary>
    public void ConfirmOriginalReceived(string userId, DateTime now)
    {
        OrderStateMachine.EnsureValidTransition(Status, AppraisalOrderStatus.Completed);
        OriginalReceivedAt       = now;
        OriginalReceivedByUserId = userId;
        Status                   = AppraisalOrderStatus.Completed;
        SetUpdatedAt(now);
    }

    /// <summary>Evidentira slanje podsjetnika vještaku za dostavu originala procjene.</summary>
    public void RecordAppraiserReminder(DateTime now)
    {
        AppraiserReminderCount++;
        AppraiserReminderLastSentAt = now;
        SetUpdatedAt(now);
    }

    /// <summary>Označava da su mišljenja CO i Pravne službe kompletirana (US 94).</summary>
    public void MarkOpinionsCompleted(DateTime now)
    {
        OpinionsCompletedAt = now;
        SetUpdatedAt(now);
    }

    public void SetInvoiceSentDate(DateTime? date, DateTime now)
    {
        InvoiceSentDate = date;
        SetUpdatedAt(now);
    }

    public void SetInvoiceReceivedDate(DateTime? date, DateTime now)
    {
        InvoiceReceivedDate = date;
        SetUpdatedAt(now);
    }

    public void SetAppraiserVisitDate(DateTime date, DateTime now)
    {
        AppraiserVisitDate = date;
        SetUpdatedAt(now);
    }

    public void SetAppraiserRating(int rating, DateTime now)
    {
        AppraiserRating = rating;
        SetUpdatedAt(now);
    }

    public void SetEsgCertificate(string? value, DateTime now)
    {
        EsgCertificate = value;
        SetUpdatedAt(now);
    }

    public void StartCoDocumentationReview(DateTime now)
    {
        CoDocumentationReviewStartedAt = now;
        SetUpdatedAt(now);
    }

    public void RecordCoOpinionSentToAm(DateTime now)
    {
        CoOpinionSentToAmAt = now;
        SetUpdatedAt(now);
    }

    public void SetPaymentConsentStatus(string? value, DateTime now)
    {
        PaymentConsentStatus = value;
        SetUpdatedAt(now);
    }

    public void SetAppraisalFee(decimal? fee, DateTime now)
    {
        AppraisalFee = fee;
        SetUpdatedAt(now);
    }

    public void SetCollateralStatus(string? status, DateTime now)
    {
        CollateralStatus = status;
        SetUpdatedAt(now);
    }

    public void SetSignedDocumentsReceivedAt(DateTime receivedAt, DateTime now)
    {
        SignedDocumentsReceivedAt = receivedAt;
        SetUpdatedAt(now);
    }

    /// <summary>Protokol uploaduje fakturu vještaka (US-F1).</summary>
    public void UploadInvoice(int documentId, string userId, string userName, DateTime now)
    {
        InvoiceStatus           = InvoiceWorkflowStatus.Uploaded;
        InvoiceDocumentId       = documentId;
        InvoiceUploadedByUserId = userId;
        InvoiceUploadedByName   = userName;
        InvoiceUploadedAt       = now;
        SetUpdatedAt(now);
    }

    /// <summary>CA šalje fakturu na plaćanje (US-F2) — status → SentForPayment / 'u obradi'.</summary>
    public void SendInvoiceForPayment(string userId, string userName, DateTime now)
    {
        InvoiceStatus                  = InvoiceWorkflowStatus.SentForPayment;
        InvoiceSentForPaymentByUserId  = userId;
        InvoiceSentForPaymentByName    = userName;
        InvoiceSentForPaymentAt        = now;
        InvoiceSentDate                = now;
        SetUpdatedAt(now);
    }

    /// <summary>Likvidatura/Računovodstvo potvrđuje plaćanje fakture (US-F3) — status → Paid / 'plaćeno'.</summary>
    public void ConfirmInvoicePaid(string userId, string userName, DateTime now)
    {
        InvoiceStatus       = InvoiceWorkflowStatus.Paid;
        InvoicePaidByUserId = userId;
        InvoicePaidByName   = userName;
        InvoicePaidAt       = now;
        InvoiceReceivedDate = now;
        SetUpdatedAt(now);
    }

    /// <summary>
    /// Prodaja (AM/SM/UB) potvrđuje da je saglasnost klijenta potpisana — PL-specifičan korak.
    /// Može se pozvati višekratno (ispravak), svaki put ažurira timestamp i korisnika.
    /// </summary>
    public void SignSalesConsent(string signedByName, DateTime now)
    {
        SalesConsentSigned       = true;
        SalesConsentSignedAt     = now;
        SalesConsentSignedByName = signedByName;
        SetUpdatedAt(now);
    }
}

/// <summary>
/// Statusi narudžbe procjene. Prijelazi su ograničeni u <see cref="OrderStateMachine"/>.
/// </summary>
public enum AppraisalOrderStatus
{
    Draft                          = 0,
    SubmittedBySales               = 10,
    AcceptedByCA                   = 20,
    DocumentationReviewInProgress  = 30,
    ReturnedForCorrection          = 40,
    CorrectionSubmitted            = 45,
    DocumentationApproved          = 50,
    AccessCheckRequested           = 60,
    AccessCheckApproved            = 65,
    AccessCheckRejected            = 70,
    ProtocolCreated                = 80,
    AppraiserSelected              = 90,
    DocumentsGenerated             = 95,
    OrderSentToAppraiser           = 100,
    AppraiserRejected              = 105,
    AdditionalPaymentRequested     = 110,
    AdditionalPaymentCompleted     = 115,
    AppraisalInProgress            = 120,
    AppraisalReturnedForRework     = 125,
    AppraisalReceived              = 130,
    COApproved                     = 140,
    ReadyForProcedure              = 150,
    // OriginalReceived = 160 uklonjen (Jul 2026): status je bio planiran ali nikada nije bio
    // dostižan — ConfirmOriginalReceived() uvijek prelazi direktno na Completed. Uklonjen.
    Completed                      = 200,
    Cancelled                      = 999
}

/// <summary>Status fakture vještaka kroz workflow: upload → plaćanje → plaćeno.</summary>
public enum InvoiceWorkflowStatus
{
    None             = 0,
    Uploaded         = 1,
    SentForPayment   = 2,
    Paid             = 3
}
