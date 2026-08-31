namespace RBBH.CollateralAppraisal.Application.Orders.Dtos;

public sealed record AppraisalOrderDto(
    int      Id,
    string   OrderNumber,
    string   Title,
    string   Status,
    int      StatusCode,

    // Workflow (FizickaLica/PravnaLica) — null za stare nacrte
    string?  WorkflowType,
    string?  CurrentOwnerRole,
    string?  NextResponsibleRole,

    // Klijent
    string   ClientName,
    string?  ClientType,
    string?  ClientIdentifier,

    // Kolateral
    int?     CollateralTypeId,
    string?  CollateralTypeLabel,
    int?     CombinedCollateralTypeId,
    string?  CombinedCollateralTypeLabel,

    // Lokacija
    string?  City,
    string?  PropertyAddress,
    string?  PropertyCity,
    string?  Branch,
    string?  BranchAddress,

    // Kontakt
    string?  ContactName,
    string?  ContactPhone,
    string?  ContactEmail,

    // Dostava / AM za slanje procjene
    string?  DeliveryContactName,
    string?  AmRecipientName,

    // Meta
    string?  CreatedByUserId,
    string?  CreatedByRole,
    string?  CreatedByName,
    DateTime CreatedAt,
    DateTime? UpdatedAt,
    DateTime? SubmittedAt,
    string?   InternalNote,
    DateTime? RequestReceivedAt,
    DateTime? RequestSentAt,

    // PL polja (samo za Pravna lica)
    decimal?  SquareMetersCommercial,
    decimal?  SquareMetersResidential,

    // Spec DIO_2 str. 66-68: protokol polja
    decimal?  AppraisalFee = null,
    string?   CollateralStatus = null,

    // Protokol
    string?   ProtocolNumber = null,

    // Faktura workflow (US-F1/F2/F3)
    string?   InvoiceWorkflowStatus = null,
    string?   InvoiceUploadedByName = null,
    DateTime? InvoiceUploadedAt = null,
    string?   InvoiceSentForPaymentByName = null,
    DateTime? InvoiceSentForPaymentAt = null,
    string?   InvoicePaidByName = null,
    DateTime? InvoicePaidAt = null,
    int?      InvoiceDocumentId = null,

    // Mogućnosti korisnika za ovu narudžbu
    OrderCapabilitiesDto Capabilities = default!,

    string?  AcceptedByCAUserId = null,
    DateTime? AcceptedAt = null
);

public sealed record AppraisalOrderListItemDto(
    int      Id,
    string   OrderNumber,
    string   Title,
    string   Status,
    int      StatusCode,
    string?  WorkflowType,
    string   ClientName,
    string?  CollateralTypeLabel,
    string?  CombinedCollateralTypeLabel,
    string?  City,
    string?  CreatedByRole,
    DateTime CreatedAt,
    DateTime? SubmittedAt,
    string?  Branch,
    DateTime? UpdatedAt
);

public sealed record OrderCapabilitiesDto(
    bool CanEdit,
    bool CanSubmit,
    bool CanCancel,
    bool CanRejectOrder = false,
    bool CanRequestAdditionalPayment = false,
    bool CanCompleteAdditionalPayment = false,
    bool CanAcceptOrder = false,
    bool CanAdminRejectOrder = false
);

public sealed record OrderSummaryDto(
    int Total,
    int Draft,
    int SubmittedBySales,
    int InProgress,
    int Completed,
    int Cancelled
);
