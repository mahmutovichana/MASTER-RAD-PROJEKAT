namespace RBBH.CollateralAppraisal.Application.Security;

/// <summary>
/// Centralne konstante za policy nazive.
/// Policy nazivi su identični permission konstantama kako bi se smanjila konfuzija.
///
/// Kako zaštititi endpoint:
/// <code>
/// // Minimal API
/// app.MapPost("/api/roles/assign", ...).RequireAuthorization(AppPolicies.RolesAssign);
///
/// // Controller
/// [Authorize(Policy = AppPolicies.RolesAssign)]
/// </code>
///
/// NIKAD ne pisati:
/// [Authorize(Roles = "Administrator")] // hardkodovan role string
/// .RequireAuthorization(p => p.RequireRole("Administrator")) // zaobilazi permission model
/// </summary>
public static class AppPolicies
{
    // ── Administracija korisnika ──────────────────────────────────────────────
    public const string UsersView           = AppPermissions.UsersView;

    // ── Upravljanje rolama ────────────────────────────────────────────────────
    public const string RolesView           = AppPermissions.RolesView;
    public const string RolesAssign         = AppPermissions.RolesAssign;
    public const string RolesRemove         = AppPermissions.RolesRemove;
    public const string RolesTransferAdmin  = AppPermissions.RolesTransferAdmin;

    // ── Rad sa zapisima ───────────────────────────────────────────────────────
    public const string RecordsCreate                  = AppPermissions.RecordsCreate;
    public const string RecordsViewOwn                 = AppPermissions.RecordsViewOwn;
    public const string RecordsUpdateOwnDraft          = AppPermissions.RecordsUpdateOwnDraft;
    public const string RecordsSubmitForVerification   = AppPermissions.RecordsSubmitForVerification;
    public const string RecordsViewPendingVerification = AppPermissions.RecordsViewPendingVerification;
    public const string RecordsApprove                 = AppPermissions.RecordsApprove;
    public const string RecordsReject                  = AppPermissions.RecordsReject;
    public const string RecordsViewHistory             = AppPermissions.RecordsViewHistory;

    // ── Šifarnici ─────────────────────────────────────────────────────────────
    public const string CodebooksView       = AppPermissions.CodebooksView;
    public const string CodebooksManage     = AppPermissions.CodebooksManage;

    // ── Upravljanje definicijama rola ─────────────────────────────────────────
    public const string RolesManage         = AppPermissions.RolesManage;

    // ── Suspenzija korisnika ──────────────────────────────────────────────────
    public const string UsersSuspend        = AppPermissions.UsersSuspend;

    // ── Audit / Sigurnost ─────────────────────────────────────────────────────
    public const string AuditViewSecurity   = AppPermissions.AuditViewSecurity;

    // ── Administrativni pristup ───────────────────────────────────────────────
    public const string AdminAccess         = AppPermissions.AdminAccess;

    // ── Dokumenti narudžbe (US 92) ────────────────────────────────────────────
    public const string DocumentsUpload     = AppPermissions.DocumentsUpload;
    public const string DocumentsView       = AppPermissions.DocumentsView;
    public const string DocumentsDownload   = AppPermissions.DocumentsDownload;
    public const string DocumentsDelete     = AppPermissions.DocumentsDelete;

    // ── Dijeljeni dokumenti (cjenovnik, lista dokumentacije po tipu) ──────────
    public const string SharedDocumentsView   = AppPermissions.SharedDocumentsView;
    public const string SharedDocumentsManage = AppPermissions.SharedDocumentsManage;

    // ── Narudžba / workflow procjene (US 93) ──────────────────────────────────
    public const string OrdersView              = AppPermissions.OrdersView;
    public const string OrdersApproveFinal      = AppPermissions.OrdersApproveFinal;
    public const string OrdersDownloadAppraisal = AppPermissions.OrdersDownloadAppraisal;
    public const string OrdersConfirmOriginal   = AppPermissions.OrdersConfirmOriginal;
    public const string OrdersRemindAppraiser   = AppPermissions.OrdersRemindAppraiser;

    // ── Mišljenja CO i Pravne službe (US 94) ──────────────────────────────────
    public const string OpinionsRequest     = AppPermissions.OpinionsRequest;
    public const string OpinionsSubmitCo    = AppPermissions.OpinionsSubmitCo;
    public const string OpinionsSubmitLegal = AppPermissions.OpinionsSubmitLegal;
    public const string OpinionsView        = AppPermissions.OpinionsView;

    // ── Notifikacije ───────────────────────────────────────────────────────────
    public const string NotificationsView   = AppPermissions.NotificationsView;

    // ── Narudžbe procjene — inicijacija i radni tok (US-1, US-2) ──────────────
    public const string OrdersCreate        = AppPermissions.OrdersCreate;
    public const string OrdersViewOwn       = AppPermissions.OrdersViewOwn;
    public const string OrdersViewAll       = AppPermissions.OrdersViewAll;
    public const string OrdersUpdateDraft   = AppPermissions.OrdersUpdateDraft;
    public const string OrdersSubmit        = AppPermissions.OrdersSubmit;
    public const string OrdersCancel        = AppPermissions.OrdersCancel;
    public const string OrdersAccept        = AppPermissions.OrdersAccept;
    public const string ProtocolView        = AppPermissions.ProtocolView;

    // ── CA pregled dokumentacije — "Dopuna podataka" / "Završi pregled" (US-91/92) ──
    public const string OrdersRequestCorrection = AppPermissions.OrdersRequestCorrection;
    public const string OrdersCompleteReview    = AppPermissions.OrdersCompleteReview;
    public const string OrdersSubmitCorrection  = AppPermissions.OrdersSubmitCorrection;

    // ── Saglasnost klijenta — PL-specifičan korak (kućica Prodaja) ───────────
    public const string OrdersSignConsent       = AppPermissions.OrdersSignConsent;

    // ── CO provjera pristupa prije narudžbe (US-93) ───────────────────────────
    public const string OrdersAccessCheck       = AppPermissions.OrdersAccessCheck;

    // ── Odabir vještaka + master-data vještaka (US-93 Faza C) ─────────────────
    public const string OrdersSelectAppraiser   = AppPermissions.OrdersSelectAppraiser;
    public const string AppraisersManage        = AppPermissions.AppraisersManage;
    public const string AppraisersView          = AppPermissions.AppraisersView;

    // ── Slanje narudžbe vještaku (US-93 Faza D) ───────────────────────────────
    public const string OrdersSendToAppraiser   = AppPermissions.OrdersSendToAppraiser;

    // ── Doplata ───────────────────────────────────────────────────────────────
    public const string OrdersAdditionalPayment = AppPermissions.OrdersAdditionalPayment;

    // ── Import/Export šifarnika ───────────────────────────────────────────────
    public const string CodebooksImport  = AppPermissions.CodebooksImport;
    public const string CodebooksExport  = AppPermissions.CodebooksExport;
    public const string AppraisersImport = AppPermissions.AppraisersImport;
    public const string AppraisersExport = AppPermissions.AppraisersExport;

    // ── Izvještaji (US-R1/R2) ───────────────────────────────────────────────
    public const string ReportsGenerate = AppPermissions.ReportsGenerate;

    // ── Faktura workflow (US-F1/F2/F3) ─────────────────────────────────────
    public const string InvoiceUpload         = AppPermissions.InvoiceUpload;
    public const string InvoiceSendForPayment = AppPermissions.InvoiceSendForPayment;
    public const string InvoiceConfirmPayment = AppPermissions.InvoiceConfirmPayment;
    public const string InvoiceView           = AppPermissions.InvoiceView;

    // ── Segment Prodaja (AM/SM/UB) ─────────────────────────────────────────────
    public const string SalesDashboardView      = AppPermissions.SalesDashboardView;
    public const string SalesOrderCreate        = AppPermissions.SalesOrderCreate;
    public const string SalesOrderView          = AppPermissions.SalesOrderView;
    public const string SalesOrderEditDraft     = AppPermissions.SalesOrderEditDraft;
    public const string SalesOrderSubmit        = AppPermissions.SalesOrderSubmit;
    public const string SalesOrderDetailsView   = AppPermissions.SalesOrderDetailsView;
}
