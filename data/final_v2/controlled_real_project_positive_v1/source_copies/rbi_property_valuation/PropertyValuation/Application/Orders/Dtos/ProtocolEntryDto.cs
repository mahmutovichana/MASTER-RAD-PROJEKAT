namespace RBBH.CollateralAppraisal.Application.Orders.Dtos;

public sealed record ProtocolEntryDto(
    int      Id,
    int      OrderId,
    string   OrderNumber,
    string   OrderTitle,
    string   ProtocolNumber,
    int      ProtocolYear,
    int      ProtocolSequence,
    string   Status,
    DateTime GeneratedAt,
    string   GeneratedByUserId,

    // Podaci preslikani iz narudžbe (AppraisalOrder)
    string   ClientName,
    string?  City,
    string?  Branch,
    string   OrderStatus,
    int      OrderStatusCode,
    string?  CollateralTypeLabel,
    string?  CombinedCollateralTypeLabel,

    // Dodatna polja iz kućice "Prodaja" (US1 AC: svi unešeni podaci preslikani u protokol)
    string?  ClientType,
    string?  ClientIdentifier,
    string?  ContactName,
    string?  ContactPhone,
    string?  PropertyAddress,
    string?  BranchAddress,
    string?  CreatedByName,

    /// <summary>Aktivna rola inicijatora narudžbe — AM, SM ili UB (segment Prodaja).</summary>
    string?  CreatedByRole,
    string?  DeliveryContactName,
    string?  AmRecipientName,
    DateTime? RequestReceivedAt = null,
    DateTime? RequestSentAt     = null,
    DateTime? InvoiceSentDate   = null,
    DateTime? InvoiceReceivedDate = null,

    // CA polja
    string? PaymentConsentStatus = null,

    // Polja preslikana iz kućica Vještak / CO
    string? CoApprovalComment   = null,
    string? AppraiserName       = null,
    int? AppraiserRating        = null,
    string? EsgCertificate      = null,
    DateTime? AppraiserVisitDate = null,

    // Spec DIO_2 str. 66-68: dodatna protokol polja
    decimal? AppraisalFee                  = null,
    string?  CollateralStatus              = null,
    DateTime? SubmittedAt                  = null,
    DateTime? OrderSentToAppraiserAt       = null,
    DateTime? SignedDocumentsReceivedAt     = null,
    DateTime? DocumentationSupplementAt    = null,
    DateTime? CoApprovedAt                 = null,
    DateTime? AppraisalDeliveredToCoAt      = null,
    DateTime? CorrectionRequestedAt        = null,
    DateTime? CorrectedAppraisalReceivedAt = null,
    DateTime? ReadyForProcedureAt          = null,
    DateTime? OriginalReceivedAt           = null,
    string?  CoApprovedByUserId            = null,
    string?  AcceptedByCAName              = null,
    string?  DocumentationReviewStatus     = null
);
