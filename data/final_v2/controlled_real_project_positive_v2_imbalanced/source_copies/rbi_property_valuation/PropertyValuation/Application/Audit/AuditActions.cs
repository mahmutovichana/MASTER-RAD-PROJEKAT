namespace RBBH.CollateralAppraisal.Application.Audit;

/// <summary>
/// Poslovne akcije koje se bilježe u audit log.
/// Pokriveni user story-ji: US1 Login, US2 Role Management, US3 Validacije, US4 Sifarnici.
/// Format: VELIKA_SLOVA_SA_UNDERSCOREOM — jedinstven identifier akcije.
/// </summary>
public static class AuditActions
{
    // ── Korisnici (US1, US2) ──────────────────────────────────────────────────
    public const string UserSuspended              = "USER_SUSPENDED";
    public const string UserReactivated            = "USER_REACTIVATED";
    public const string UserRoleAssigned           = "USER_ROLE_ASSIGNED";
    public const string UserRoleRemoved            = "USER_ROLE_REMOVED";
    public const string UserLoggedIn               = "USER_LOGGED_IN";
    public const string UserLoggedOut              = "USER_LOGGED_OUT";
    public const string UserLoginFailed            = "USER_LOGIN_FAILED";

    // ── Upravljanje rolama (US2) ───────────────────────────────────────────────
    public const string RoleCreated                = "ROLE_CREATED";
    public const string RoleUpdated                = "ROLE_UPDATED";
    public const string RoleDeactivated            = "ROLE_DEACTIVATED";
    public const string RoleReactivated            = "ROLE_REACTIVATED";
    public const string RoleSoftDeleted            = "ROLE_SOFT_DELETED";
    public const string RoleDeleteBlockedInUse     = "ROLE_DELETE_BLOCKED_IN_USE";
    public const string RolePermissionAdded        = "ROLE_PERMISSION_ADDED";
    public const string RolePermissionRemoved      = "ROLE_PERMISSION_REMOVED";

    // ── Role context (aktivna uloga) ──────────────────────────────────────────
    public const string ActiveRoleSelected          = "ACTIVE_ROLE_SELECTED";
    public const string InvalidActiveRoleSelection  = "INVALID_ACTIVE_ROLE_SELECTION";

    // ── Sigurnost (US1, US2, US3) ─────────────────────────────────────────────
    public const string PermissionDenied                    = "PERMISSION_DENIED";
    public const string TokenRefreshed                      = "TOKEN_REFRESHED";
    public const string AdminRoleTransferred                = "ADMIN_ROLE_TRANSFERRED";
    public const string MinimumAdminCountBlocked            = "MINIMUM_ADMIN_COUNT_BLOCKED";
    public const string UnknownRoleDetected                 = "UNKNOWN_ROLE_DETECTED";
    public const string KeycloakRoleSyncFailed              = "KEYCLOAK_ROLE_SYNC_FAILED";

    // ── Sifarnici — Codebook container (US4) ─────────────────────────────────
    public const string CodebookCreated                             = "CODEBOOK_CREATED";
    public const string CodebookUpdated                             = "CODEBOOK_UPDATED";
    public const string CodebookDeactivated                         = "CODEBOOK_DEACTIVATED";
    public const string CodebookActivated                           = "CODEBOOK_ACTIVATED";
    public const string CodebookDeleted                             = "CODEBOOK_DELETED";
    public const string CodebookDeleteBlockedInUse                  = "CODEBOOK_DELETE_BLOCKED_IN_USE";

    // ── Sifarnici — Vrijednosti (US4) ─────────────────────────────────────────
    public const string CodebookEntryCreated                        = "CODEBOOK_ENTRY_CREATED";
    public const string CodebookEntryUpdated                        = "CODEBOOK_ENTRY_UPDATED";
    public const string CodebookEntryDeactivated                    = "CODEBOOK_ENTRY_DEACTIVATED";
    public const string CodebookValueActivated                      = "CODEBOOK_VALUE_ACTIVATED";
    public const string CodebookValueDeleted                        = "CODEBOOK_VALUE_DELETED";
    public const string CodebookValueDeleteBlockedInUse             = "CODEBOOK_VALUE_DELETE_BLOCKED_IN_USE";
    public const string CodebookValueDeleteBlockedUsageCheckFailed  = "CODEBOOK_VALUE_DELETE_BLOCKED_USAGE_CHECK_FAILED";
    public const string CodebookValueSystemDeleteBlocked            = "CODEBOOK_VALUE_SYSTEM_DELETE_BLOCKED";
    public const string CodebookValueCriticalDeactivationBlocked    = "CODEBOOK_VALUE_CRITICAL_DEACTIVATION_BLOCKED";
    public const string CodebookValueCriticalDeleteBlocked          = "CODEBOOK_VALUE_CRITICAL_DELETE_BLOCKED";

    // ── Narudžbe procjene (US-1, US-2) ───────────────────────────────────────
    public const string OrderCreated               = "ORDER_CREATED";
    public const string OrderDraftCreated          = "ORDER_DRAFT_CREATED";
    public const string OrderDraftUpdated          = "ORDER_DRAFT_UPDATED";
    public const string OrderDraftAutosaved        = "ORDER_DRAFT_AUTOSAVED";
    public const string OrderViewed                = "ORDER_VIEWED";
    public const string OrderSubmitted             = "ORDER_SUBMITTED";
    public const string OrderCancelled             = "ORDER_CANCELLED";
    public const string OrderAcceptedByCA          = "ORDER_ACCEPTED_BY_CA";
    public const string TaskCreated                = "TASK_CREATED";
    public const string NotificationCreated        = "NOTIFICATION_CREATED";
    public const string EmailFailed                = "EMAIL_FAILED";
    public const string ProtocolGenerated          = "PROTOCOL_GENERATED";
    public const string UnauthorizedOrderAccess    = "UNAUTHORIZED_ORDER_ACCESS";
    public const string CaTaskCreationFailed        = "CA_TASK_CREATION_FAILED";
    public const string ProtocolEntryCreationFailed = "PROTOCOL_ENTRY_CREATION_FAILED";
    public const string CaEmailNotificationSent     = "CA_EMAIL_NOTIFICATION_SENT";
    public const string CaEmailNotificationFailed   = "CA_EMAIL_NOTIFICATION_FAILED";

    // ── CA pregled dokumentacije — "Dopuna podataka" / "Završi pregled" ───────
    public const string OrderReturnedForCorrection = "ORDER_RETURNED_FOR_CORRECTION";
    public const string OrderCorrectionSubmitted   = "ORDER_CORRECTION_SUBMITTED";
    public const string OrderReviewCompleted       = "ORDER_REVIEW_COMPLETED";

    // ── CO provjera pristupa prije narudžbe ───────────────────────────────────
    public const string OrderAccessCheckRequested  = "ORDER_ACCESS_CHECK_REQUESTED";
    public const string OrderAccessCheckApproved   = "ORDER_ACCESS_CHECK_APPROVED";
    public const string OrderAccessCheckRejected   = "ORDER_ACCESS_CHECK_REJECTED";

    // ── Vještaci — master-data i odabir (Faza C) ──────────────────────────────
    public const string AppraiserCreated           = "APPRAISER_CREATED";
    public const string AppraiserUpdated           = "APPRAISER_UPDATED";
    public const string AppraiserSelected          = "APPRAISER_SELECTED";

    // ── Slanje narudžbe vještaku (Faza D) ─────────────────────────────────────
    public const string OrderSentToAppraiser       = "ORDER_SENT_TO_APPRAISER";

    // ── Doplata ──────────────────────────────────────────────────────────────
    public const string AdditionalPaymentRequested = "ADDITIONAL_PAYMENT_REQUESTED";
    public const string AdditionalPaymentCompleted = "ADDITIONAL_PAYMENT_COMPLETED";

    // ── Odbijanje narudžbe (vještak) ────────────────────────────────────────
    public const string OrderRejectedByAppraiser  = "ORDER_REJECTED_BY_APPRAISER";
    public const string OrderReassignedAppraiser  = "ORDER_REASSIGNED_APPRAISER";

    // ── Dorada procjene (CO vraća) ───────────────────────────────────────
    public const string AppraisalReturnedForRework = "APPRAISAL_RETURNED_FOR_REWORK";
    public const string AppraisalReworkSubmitted    = "APPRAISAL_REWORK_SUBMITTED";

    // ── Faktura workflow (US-F1/F2/F3) ──────────────────────────────────────
    public const string InvoiceUploaded           = "INVOICE_UPLOADED";
    public const string InvoiceSentForPayment     = "INVOICE_SENT_FOR_PAYMENT";
    public const string InvoicePaymentConfirmed   = "INVOICE_PAYMENT_CONFIRMED";

    // ── Taskovi (workflow koraci) ────────────────────────────────────────────
    public const string TaskAccepted               = "TASK_ACCEPTED";
    public const string TaskCompleted              = "TASK_COMPLETED";

    // ── Izvještaji ──────────────────────────────────────────────────────────
    public const string ReportDownloaded           = "REPORT_DOWNLOADED";

    // ── Dokumenti — pristup i upravljanje (audit download/preview mehanizam) ──
    public const string DocumentPreviewed           = "DOCUMENT_PREVIEWED";
    public const string DocumentUploaded           = "DOCUMENT_UPLOADED";
    public const string DocumentDownloaded          = "DOCUMENT_DOWNLOADED";
    public const string DocumentDownloadFailed      = "DOCUMENT_DOWNLOAD_FAILED";
    public const string DocumentDeleted             = "DOCUMENT_DELETED";
    public const string DocumentVersionCreated      = "DOCUMENT_VERSION_CREATED";
    public const string DocumentDeactivated         = "DOCUMENT_DEACTIVATED";
    public const string DocumentReactivated         = "DOCUMENT_REACTIVATED";

    // ── Zahtjevi za ponudu (PL workflow) ──────────────────────────────────────
    public const string QuoteRequestsSent        = "QUOTE_REQUESTS_SENT";
    public const string QuoteAccepted            = "QUOTE_ACCEPTED";
    public const string QuoteThankYouSent        = "QUOTE_THANK_YOU_SENT";

    // ── Dijeljeni dokumenti ───────────────────────────────────────────────────
    public const string SharedDocumentUploaded   = "SHARED_DOCUMENT_UPLOADED";
    public const string SharedDocumentDownloaded = "SHARED_DOCUMENT_DOWNLOADED";
    public const string SharedDocumentDeleted    = "SHARED_DOCUMENT_DELETED";
}
