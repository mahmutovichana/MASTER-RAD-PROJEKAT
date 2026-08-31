namespace RBBH.CollateralAppraisal.Application.Reports.Dtos;

/// <summary>
/// Jedan red izvještaja — sva polja iz Protokola narudžbi + 7 vremenskih kolona (u danima).
/// Null = datum nije popunjen, nije prikazano negativno ni nula ako oba datuma isti.
/// </summary>
public sealed record OrdersTimeReportRowDto(
    // ── Identifikacija ────────────────────────────────────────────────────────
    int      OrderId,
    string   OrderNumber,
    string   ProtocolNumber,
    int      ProtocolYear,
    int      ProtocolSequence,
    string   OrderTitle,

    // ── Klijent / lokacija ────────────────────────────────────────────────────
    string   ClientName,
    string?  ClientType,
    string?  ClientIdentifier,
    string?  City,
    string?  Branch,
    string?  BranchAddress,
    string?  PropertyAddress,
    string?  ContactName,
    string?  ContactPhone,

    // ── Prodaja ───────────────────────────────────────────────────────────────
    string?  CreatedByName,
    string?  CreatedByRole,
    string?  AmRecipientName,
    string?  DeliveryContactName,

    // ── Status i workflow ─────────────────────────────────────────────────────
    string   OrderStatus,
    int      OrderStatusCode,
    string?  CollateralTypeLabel,
    string?  CombinedCollateralTypeLabel,
    string?  DocumentationReviewStatus,
    string?  PaymentConsentStatus,

    // ── Vještak / procjena ────────────────────────────────────────────────────
    string?  AppraiserName,
    int?     AppraiserRating,
    string?  EsgCertificate,
    decimal? AppraisalFee,
    string?  CollateralStatus,
    string?  CoApprovalComment,
    string?  AcceptedByCAName,
    string?  CoApprovedByUserId,

    // ── Ključni datumi protokola ──────────────────────────────────────────────
    DateTime? RequestReceivedAt,
    DateTime? RequestSentAt,
    DateTime? SubmittedAt,
    DateTime? OrderSentToAppraiserAt,
    DateTime? AppraiserVisitDate,
    DateTime? SignedDocumentsReceivedAt,
    DateTime? DocumentationSupplementAt,
    DateTime? AppraisalDeliveredToCoAt,
    DateTime? CorrectionRequestedAt,
    DateTime? CorrectedAppraisalReceivedAt,
    DateTime? CoApprovedAt,
    DateTime? ReadyForProcedureAt,
    DateTime? OriginalReceivedAt,
    DateTime? InvoiceSentDate,
    DateTime? InvoiceReceivedDate,
    DateTime  GeneratedAt,

    // ── 7 vremenskih kolona (cijeli broj dana; null = datum nedostaje) ─────────
    /// <summary>1. Prodaja → CA: K→P (RequestReceivedAt → SubmittedAt)</summary>
    int? DaneProdajaCA,
    /// <summary>2. CA → Narudžba vještaku: P→V (SubmittedAt → OrderSentToAppraiserAt)</summary>
    int? DaneCAVjestak,
    /// <summary>3. Narudžba → dostava CO: V→Y (OrderSentToAppraiserAt → AppraisalDeliveredToCoAt)</summary>
    int? DaneVjestavCO,
    /// <summary>4. CO → Finalna procjena: Y→AB (AppraisalDeliveredToCoAt → ReadyForProcedureAt)</summary>
    int? DaneCOFinalna,
    /// <summary>5. Finalna → Original: AB→AC (ReadyForProcedureAt → OriginalReceivedAt)</summary>
    int? DaneFinalnaOriginal,
    /// <summary>6. Grand total: K→AB (RequestReceivedAt → ReadyForProcedureAt)</summary>
    int? DaneGrandTotal,
    /// <summary>7. Grand total Prodaja: P→AB (SubmittedAt → ReadyForProcedureAt)</summary>
    int? DaneGrandTotalProdaja
);
