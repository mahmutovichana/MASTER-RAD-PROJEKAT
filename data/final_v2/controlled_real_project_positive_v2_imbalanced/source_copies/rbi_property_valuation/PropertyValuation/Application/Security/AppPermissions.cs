namespace RBBH.CollateralAppraisal.Application.Security;

/// <summary>
/// Centralne konstante za permission-e aplikacije.
///
/// Permission = konkretna dozvoljena akcija.
/// Format: "resurs.akcija" (lowercase, kebab-case).
///
/// PRAVILO: Nikad ne pisati hardkodirane permission stringove po endpointima.
/// Uvijek koristiti ove konstante.
///
/// Kako dodati novu permission:
/// 1. Dodaj konstantu ovdje i u niz <see cref="All"/>.
/// 2. Dodaj permission odgovarajućoj roli u <see cref="RolePermissionMatrix"/>.
/// 3. Policy se automatski registruje u <see cref="AppPolicies"/> i AuthorizationExtensions.
/// 4. Zaštiti endpoint sa .RequireAuthorization(AppPolicies.NovPermission).
/// </summary>
public static class AppPermissions
{
    // ── Administracija korisnika ──────────────────────────────────────────────
    public const string UsersView           = "users.view";

    // ── Upravljanje rolama ────────────────────────────────────────────────────
    public const string RolesView           = "roles.view";
    public const string RolesAssign         = "roles.assign";
    public const string RolesRemove         = "roles.remove";
    public const string RolesTransferAdmin  = "roles.transfer-admin";

    // ── Rad sa zapisima ───────────────────────────────────────────────────────
    public const string RecordsCreate                 = "records.create";
    public const string RecordsViewOwn                = "records.view-own";
    public const string RecordsUpdateOwnDraft         = "records.update-own-draft";
    public const string RecordsSubmitForVerification  = "records.submit-for-verification";
    public const string RecordsViewPendingVerification = "records.view-pending-verification";
    public const string RecordsApprove                = "records.approve";
    public const string RecordsReject                 = "records.reject";
    public const string RecordsViewHistory            = "records.view-history";

    // ── Šifarnici ─────────────────────────────────────────────────────────────
    public const string CodebooksView       = "codebooks.view";

    /// <summary>
    /// Dozvoljava upravljanje šifarnicima: deaktivacija, aktivacija, brisanje, kreiranje, uređivanje.
    /// Samo Administrator rola ima ovu permission.
    /// </summary>
    public const string CodebooksManage     = "codebooks.manage";

    // ── Upravljanje definicijama rola ─────────────────────────────────────────
    /// <summary>Kreiranje, uređivanje, deaktivacija i brisanje custom rola + dodjela permissiona roli.</summary>
    public const string RolesManage         = "roles.manage";

    // ── Suspenzija korisnika ──────────────────────────────────────────────────
    public const string UsersSuspend        = "users.suspend";

    // ── Audit / Sigurnost ─────────────────────────────────────────────────────
    public const string AuditViewSecurity   = "audit.view-security";

    // ── Administrativni pristup ───────────────────────────────────────────────
    public const string AdminAccess         = "admin.access";

    // ── Dokumenti narudžbe (US 92) ────────────────────────────────────────────
    public const string DocumentsUpload     = "documents.upload";
    public const string DocumentsView       = "documents.view";
    public const string DocumentsDownload   = "documents.download";
    public const string DocumentsDelete     = "documents.delete";

    // ── Dijeljeni dokumenti (cjenovnik, lista dokumentacije po tipu) ──────────
    public const string SharedDocumentsView   = "shared-documents.view";
    public const string SharedDocumentsManage = "shared-documents.manage";

    // ── Narudžba / workflow procjene (US 93) ──────────────────────────────────
    public const string OrdersView              = "orders.view";
    public const string OrdersApproveFinal      = "orders.approve-final";
    public const string OrdersDownloadAppraisal = "orders.download-appraisal";
    public const string OrdersConfirmOriginal   = "orders.confirm-original";
    public const string OrdersRemindAppraiser   = "orders.remind-appraiser";

    // ── Mišljenja CO i Pravne službe (US 94) ──────────────────────────────────
    public const string OpinionsRequest     = "opinions.request";
    public const string OpinionsSubmitCo    = "opinions.submit-co";
    public const string OpinionsSubmitLegal = "opinions.submit-legal";
    public const string OpinionsView        = "opinions.view";

    // ── Notifikacije ───────────────────────────────────────────────────────────
    /// <summary>Pregled vlastitog notifikacijskog inboxa (in-app notifikacije).</summary>
    public const string NotificationsView   = "notifications.view";

    // ── Narudžbe procjene — inicijacija i radni tok (US-1, US-2) ──────────────
    public const string OrdersCreate        = "orders.create";
    public const string OrdersViewOwn       = "orders.view-own";
    public const string OrdersViewAll       = "orders.view-all";
    public const string OrdersUpdateDraft   = "orders.update-draft";
    public const string OrdersSubmit        = "orders.submit";
    public const string OrdersCancel        = "orders.cancel";
    public const string OrdersAccept        = "orders.accept";
    public const string ProtocolView        = "protocol.view";

    // ── CA pregled dokumentacije — "Dopuna podataka" / "Završi pregled" (US-91/92) ──
    public const string OrdersRequestCorrection = "orders.request-correction";
    public const string OrdersCompleteReview    = "orders.complete-review";
    public const string OrdersSubmitCorrection  = "orders.submit-correction";

    // ── Saglasnost klijenta — PL-specifičan korak (kućica Prodaja) ───────────
    public const string OrdersSignConsent       = "orders.sign-consent";

    // ── CO provjera pristupa prije narudžbe (US-93) ───────────────────────────
    public const string OrdersAccessCheck       = "orders.access-check";

    // ── Odabir vještaka + master-data vještaka (US-93 Faza C) ─────────────────
    public const string OrdersSelectAppraiser   = "orders.select-appraiser";
    public const string AppraisersManage        = "appraisers.manage";
    public const string AppraisersView          = "appraisers.view";

    // ── Slanje narudžbe vještaku (US-93 Faza D) ───────────────────────────────
    public const string OrdersSendToAppraiser   = "orders.send-to-appraiser";

    // ── Doplata (vještak traži, CA obrađuje) ─────────────────────────────────
    public const string OrdersAdditionalPayment = "orders.additional-payment";

    // ── Import/Export šifarnika ───────────────────────────────────────────────
    public const string CodebooksImport  = "codebooks.import";
    public const string CodebooksExport  = "codebooks.export";
    public const string AppraisersImport = "appraisers.import";
    public const string AppraisersExport = "appraisers.export";

    // ── Izvještaji (US-R1/R2) ───────────────────────────────────────────────
    public const string ReportsGenerate = "reports.generate";

    // ── Faktura workflow (US-F1/F2/F3) ─────────────────────────────────────
    public const string InvoiceUpload         = "invoice.upload";
    public const string InvoiceSendForPayment = "invoice.send-for-payment";
    public const string InvoiceConfirmPayment = "invoice.confirm-payment";
    public const string InvoiceView           = "invoice.view";

    // ── Segment Prodaja (AM/SM/UB) — imenovan permission katalog ──────────────
    // NAPOMENA: stvarni enforcement na endpointima ide preko Orders*/Documents*
    // permission-a iznad (isti resursi, dokazana logika — vidi RolePermissionMatrix
    // gdje su AM/SM/UB mapirani i na ove i na odgovarajuće Orders* permission-e).
    // Ovi kodovi postoje da segment Prodaja ima eksplicitan, imenovan skup u
    // permission katalogu / admin UI-u za upravljanje rolama.
    public const string SalesDashboardView      = "sales.dashboard.view";
    public const string SalesOrderCreate        = "sales.order.create";
    public const string SalesOrderView          = "sales.order.view";
    public const string SalesOrderEditDraft     = "sales.order.editDraft";
    public const string SalesOrderSubmit        = "sales.order.submit";
    public const string SalesOrderDetailsView   = "sales.order.details.view";

    /// <summary>Sve permission-e sistema — koristi se za automatsku registraciju policy-ja.</summary>
    public static readonly string[] All =
    [
        UsersView,
        RolesView,
        RolesAssign,
        RolesRemove,
        RolesTransferAdmin,
        RolesManage,
        UsersSuspend,
        RecordsCreate,
        RecordsViewOwn,
        RecordsUpdateOwnDraft,
        RecordsSubmitForVerification,
        RecordsViewPendingVerification,
        RecordsApprove,
        RecordsReject,
        RecordsViewHistory,
        CodebooksView,
        CodebooksManage,
        AuditViewSecurity,
        AdminAccess,
        DocumentsUpload,
        DocumentsView,
        DocumentsDownload,
        DocumentsDelete,
        OrdersView,
        OrdersApproveFinal,
        OrdersDownloadAppraisal,
        OrdersConfirmOriginal,
        OrdersRemindAppraiser,
        OpinionsRequest,
        OpinionsSubmitCo,
        OpinionsSubmitLegal,
        OpinionsView,
        NotificationsView,
        OrdersCreate,
        OrdersViewOwn,
        OrdersViewAll,
        OrdersUpdateDraft,
        OrdersSubmit,
        OrdersCancel,
        OrdersAccept,
        ProtocolView,
        OrdersRequestCorrection,
        OrdersCompleteReview,
        OrdersSubmitCorrection,
        OrdersSignConsent,
        OrdersAccessCheck,
        OrdersSelectAppraiser,
        AppraisersManage,
        AppraisersView,
        OrdersSendToAppraiser,
        OrdersAdditionalPayment,
        CodebooksImport,
        CodebooksExport,
        AppraisersImport,
        AppraisersExport,
        SalesDashboardView,
        SalesOrderCreate,
        SalesOrderView,
        SalesOrderEditDraft,
        SalesOrderSubmit,
        SalesOrderDetailsView,
        SharedDocumentsView,
        SharedDocumentsManage,
        ReportsGenerate,
        InvoiceUpload,
        InvoiceSendForPayment,
        InvoiceConfirmPayment,
        InvoiceView
    ];
}
