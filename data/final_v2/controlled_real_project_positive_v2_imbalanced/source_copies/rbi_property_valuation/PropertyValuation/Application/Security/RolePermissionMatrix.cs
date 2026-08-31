namespace RBBH.CollateralAppraisal.Application.Security;

/// <summary>
/// Centralna mapa: rola → skup permission-a.
///
/// Ovo je jedino mjesto u sistemu gdje se definiše koje permission-e ima koja rola.
/// Svaka promjena prava u sistemu ide ovdje.
///
/// Podrška za više rola:
/// Korisnik može imati više rola. Metoda <see cref="GetPermissionsForRoles"/> sabira
/// sve permission-e. Poslovna pravila (npr. zabrana samoverifikacije) provjeravaju
/// se posebno — ne mogu se zaobići dodavanjem rola.
/// </summary>
public static class RolePermissionMatrix
{
    /// <summary>
    /// Permission set zajednički za sve role segmenta Prodaja (AM, SM, UB).
    /// Definisan jednom i dijeljen kroz mapu ispod kako AM/SM/UB nikad ne mogu
    /// "iskliznuti" iz sinhronizacije (zahtjev: "sve tri role mapirati na iste
    /// Prodaja permissione").
    /// </summary>
    private static readonly string[] ProdajaSegmentPermissions =
    [
        AppPermissions.CodebooksView,
        AppPermissions.DocumentsUpload,
        AppPermissions.DocumentsView,
        AppPermissions.DocumentsDownload,
        AppPermissions.DocumentsDelete,
        AppPermissions.SharedDocumentsView,
        AppPermissions.OrdersView,
        AppPermissions.OrdersDownloadAppraisal,
        AppPermissions.OrdersConfirmOriginal,
        AppPermissions.OrdersRemindAppraiser,
        AppPermissions.OpinionsRequest,
        AppPermissions.OpinionsView,
        AppPermissions.NotificationsView,

        // ── Narudžbe procjene — inicijacija i radni tok (US-1, US-2) ──────────
        AppPermissions.OrdersCreate,
        AppPermissions.OrdersViewOwn,
        AppPermissions.OrdersViewAll,
        AppPermissions.OrdersUpdateDraft,
        AppPermissions.OrdersSubmit,
        AppPermissions.OrdersCancel,

        // ── Dopuna podataka po zahtjevu CA ─────────────────────────────────────
        AppPermissions.OrdersSubmitCorrection,

        // ── Saglasnost klijenta (PL) ───────────────────────────────────────────
        AppPermissions.OrdersSignConsent,

        // ── Faktura — vidljivost statusa plaćanja ─────────────────────────────
        AppPermissions.InvoiceView,

        // ── Imenovani permission katalog segmenta Prodaja (sales.*) ───────────
        AppPermissions.SalesDashboardView,
        AppPermissions.SalesOrderCreate,
        AppPermissions.SalesOrderView,
        AppPermissions.SalesOrderEditDraft,
        AppPermissions.SalesOrderSubmit,
        AppPermissions.SalesOrderDetailsView
    ];

    public static readonly IReadOnlyDictionary<string, string[]> PermissionsByRole =
        new Dictionary<string, string[]>
        {
            [AppRoles.Administrator] =
            [
                AppPermissions.UsersView,
                AppPermissions.SharedDocumentsView,
                AppPermissions.SharedDocumentsManage,
                AppPermissions.UsersSuspend,
                AppPermissions.RolesView,
                AppPermissions.RolesAssign,
                AppPermissions.RolesRemove,
                AppPermissions.RolesTransferAdmin,
                AppPermissions.RolesManage,
                AppPermissions.AuditViewSecurity,
                AppPermissions.AdminAccess,
                AppPermissions.RecordsCreate,
                AppPermissions.RecordsViewOwn,
                AppPermissions.RecordsUpdateOwnDraft,
                AppPermissions.RecordsSubmitForVerification,
                AppPermissions.RecordsViewPendingVerification,
                AppPermissions.RecordsApprove,
                AppPermissions.RecordsReject,
                AppPermissions.RecordsViewHistory,
                AppPermissions.CodebooksView,
                AppPermissions.CodebooksManage,
                AppPermissions.DocumentsUpload,
                AppPermissions.DocumentsView,
                AppPermissions.DocumentsDownload,
                AppPermissions.DocumentsDelete,
                AppPermissions.OrdersView,
                // Admin = super-user: puni uvid i radni tok nad narudžbama
                AppPermissions.OrdersViewOwn,
                AppPermissions.OrdersViewAll,
                AppPermissions.OrdersAccept,
                AppPermissions.ProtocolView,
                AppPermissions.OrdersRequestCorrection,
                AppPermissions.OrdersCompleteReview,
                AppPermissions.OrdersSubmitCorrection,
                AppPermissions.OrdersAccessCheck,
                AppPermissions.OrdersSelectAppraiser,
                AppPermissions.OrdersSendToAppraiser,
                AppPermissions.AppraisersView,
                AppPermissions.AppraisersManage,
                AppPermissions.OrdersApproveFinal,
                AppPermissions.OrdersDownloadAppraisal,
                AppPermissions.OrdersConfirmOriginal,
                AppPermissions.OrdersRemindAppraiser,
                AppPermissions.OpinionsRequest,
                AppPermissions.OpinionsSubmitCo,
                AppPermissions.OpinionsSubmitLegal,
                AppPermissions.OpinionsView,
                AppPermissions.NotificationsView,
                AppPermissions.ReportsGenerate,

                // ── Import/Export šifarnika (Admin ima puni pristup) ─────────────────
                AppPermissions.CodebooksImport,
                AppPermissions.CodebooksExport,
                AppPermissions.AppraisersImport,
                AppPermissions.AppraisersExport
            ],

            // ── Unosnik / Verifikator — PLANIRANE ROLE (nije implementirano) ────────────
            // ODLUKA (Jul 2026): Unosnik i Verifikator su definirani u specifikaciji ali
            // nijedan API endpoint ne koristi Records.* permisije. Modul za Records je
            // planiran ali još nije implementiran (vidi ComingSoonDokumentacija.razor).
            //
            // AKCIJA: Role su zadržane u matrici da se Keycloak konfiguracija ne gubi.
            // Endpoint-i koji zahtijevaju ove permisije trebaju biti kreirani u zasebnom
            // sprintu kada se Records modul implementira.
            // TODO: Implementirati Records modul ili dokumentirati odlazak iz scope-a.
            [AppRoles.Unosnik] =
            [
                AppPermissions.RecordsCreate,
                AppPermissions.RecordsViewOwn,
                AppPermissions.RecordsUpdateOwnDraft,
                AppPermissions.RecordsSubmitForVerification,
                AppPermissions.CodebooksView
            ],

            [AppRoles.Verifikator] =
            [
                AppPermissions.RecordsViewPendingVerification,
                AppPermissions.RecordsApprove,
                AppPermissions.RecordsReject,
                AppPermissions.RecordsViewHistory,
                AppPermissions.CodebooksView
            ],

            // ── Segment Prodaja — AM, SM, UB ───────────────────────────────────
            // Tri odvojene Keycloak/aplikativne role koje dijele IDENTIČAN skup
            // permission-a (zahtjev: "iste osnovne ovlasti segmenta Prodaja").
            // AM/SM/UB inicira narudžbu, uploaduje dokumentaciju, preuzima
            // finalnu procjenu, potvrđuje preuzet original, šalje reminder
            // vještaku, traži mišljenja CO/Pravne. Razlika između njih je samo
            // u evidenciji "ko je inicirao narudžbu" (CreatedByRole/-Name),
            // ne u ovlaštenjima.
            [AppRoles.AM] = ProdajaSegmentPermissions,
            [AppRoles.SM] = ProdajaSegmentPermissions,
            [AppRoles.UB] = ProdajaSegmentPermissions,

            // ── Kolateral administrator (CA) ──────────────────────────────────
            // Vodi narudžbu, provjerava dokumentaciju, prosljeđuje vještaku.
            [AppRoles.KolateralAdministrator] =
            [
                AppPermissions.CodebooksView,
                AppPermissions.CodebooksManage,
                AppPermissions.DocumentsUpload,
                AppPermissions.DocumentsView,
                AppPermissions.DocumentsDownload,
                AppPermissions.DocumentsDelete,
                AppPermissions.SharedDocumentsView,
                AppPermissions.SharedDocumentsManage,
                AppPermissions.OrdersView,
                AppPermissions.OrdersDownloadAppraisal,
                AppPermissions.OpinionsView,
                AppPermissions.NotificationsView,

                // ── Narudžbe procjene — inicijacija i radni tok (US-1, US-2) ──
                AppPermissions.OrdersViewOwn,
                AppPermissions.OrdersViewAll,
                AppPermissions.OrdersAccept,
                AppPermissions.ProtocolView,

                // ── Pregled dokumentacije — "Dopuna podataka" / "Završi pregled" ──
                AppPermissions.OrdersRequestCorrection,
                AppPermissions.OrdersCompleteReview,

                // ── Odabir vještaka + master-data vještaka (Faza C) ───────────
                AppPermissions.OrdersSelectAppraiser,
                AppPermissions.AppraisersManage,
                AppPermissions.AppraisersView,

                // ── Slanje narudžbe vještaku (Faza D) ──────────────────────────
                AppPermissions.OrdersSendToAppraiser,

                // ── Reminder vještaku za dostavu procjene (DPNPN-141) ──────────
                AppPermissions.OrdersRemindAppraiser,

                // ── Doplata (CA obrađuje zahtjev vještaka za doplatu) ────────────
                AppPermissions.OrdersAdditionalPayment,

                // ── Import/Export šifarnika ───────────────────────────────────────
                AppPermissions.CodebooksImport,
                AppPermissions.CodebooksExport,
                AppPermissions.AppraisersImport,
                AppPermissions.AppraisersExport,

                // ── Faktura (CA preuzima i šalje na plaćanje — US-F2) ────────
                AppPermissions.InvoiceView,
                AppPermissions.InvoiceSendForPayment,

                // ── Izvještaji (US-R1/R2) ────────────────────────────────────
                AppPermissions.ReportsGenerate
            ],

            // ── Kolateral oficir (CO) ──────────────────────────────────────────
            // Provjera pristupa, odobrenje finalne procjene, daje mišljenje CO.
            [AppRoles.KolateralOficir] =
            [
                AppPermissions.CodebooksView,
                AppPermissions.DocumentsView,
                AppPermissions.DocumentsDownload,
                AppPermissions.SharedDocumentsView,
                AppPermissions.OrdersView,
                AppPermissions.OrdersApproveFinal,
                AppPermissions.OrdersDownloadAppraisal,
                AppPermissions.OpinionsSubmitCo,
                AppPermissions.OpinionsView,
                AppPermissions.NotificationsView,

                // ── "Moji zadaci" — pristup i PRIHVAT taskova dodijeljenih CO roli ──
                // OrdersAccept je nužan da "Prihvati task" (POST /tasks/{id}/accept) ne
                // vraća 403 — bez njega CO ne može prihvatiti zadatak provjere pristupa
                // ni odobrenja procjene.
                AppPermissions.OrdersViewOwn,
                AppPermissions.OrdersAccept,

                // ── Provjera pristupa prije narudžbe ──────────────────────────
                AppPermissions.OrdersAccessCheck,

                // ── Uvid u listu vještaka (Faza C) ─────────────────────────────
                AppPermissions.AppraisersView,

                // ── Export šifarnika (read-only) ─────────────────────────────────
                AppPermissions.CodebooksExport,
                AppPermissions.AppraisersExport,

                // ── Izvještaji (US-R1/R2) ────────────────────────────────────
                AppPermissions.ReportsGenerate
            ],

            // ── Pravna služba ──────────────────────────────────────────────────
            // Daje pravno mišljenje (US 94).
            [AppRoles.PravnaSluzba] =
            [
                AppPermissions.CodebooksView,
                AppPermissions.DocumentsView,
                AppPermissions.DocumentsDownload,
                AppPermissions.SharedDocumentsView,
                AppPermissions.OrdersView,
                AppPermissions.OrdersViewOwn,
                AppPermissions.OpinionsSubmitLegal,
                AppPermissions.OpinionsView,
                AppPermissions.NotificationsView
            ],

            // ── Vještak (eksterni) ─────────────────────────────────────────────
            // Prihvata dodijeljene procjene, radi procjenu, uploaduje dokumentaciju
            // i finalnu procjenu, obrađuje dorade. Vidi samo narudžbe gdje je
            // dodijeljen (preko taskova / OrdersViewOwn).
            [AppRoles.Vjestak] =
            [
                // CodebooksView je nužan da kartica Dokumenti učita tipove dokumenata
                // (/api/codebooks/tipovi_dokumenata/...) — bez njega ReloadAsync vraća 403.
                AppPermissions.CodebooksView,
                AppPermissions.SharedDocumentsView,
                AppPermissions.OrdersView,
                AppPermissions.OrdersViewOwn,
                AppPermissions.OrdersAccept,
                AppPermissions.DocumentsView,
                AppPermissions.DocumentsDownload,
                AppPermissions.DocumentsUpload,
                AppPermissions.OrdersDownloadAppraisal,
                AppPermissions.NotificationsView,

                // ── Doplata (vještak traži doplatu od CA) ─────────────────────
                AppPermissions.OrdersAdditionalPayment
            ],

            // ── Protokol ───────────────────────────────────────────────────────
            // Prima narudžbe na protokol, uploaduje/obrad­uje fakturu (5. kućica),
            // vodi protokol narudžbi.
            [AppRoles.Protokol] =
            [
                AppPermissions.CodebooksView,
                AppPermissions.OrdersView,
                AppPermissions.OrdersViewOwn,
                AppPermissions.ProtocolView,
                AppPermissions.DocumentsView,
                AppPermissions.DocumentsDownload,
                AppPermissions.DocumentsUpload,
                AppPermissions.NotificationsView,

                // ── Faktura upload (US-F1) — Protokol uploaduje fakturu vještaka ──
                AppPermissions.InvoiceUpload,
                AppPermissions.InvoiceView
            ],

            // ── Likvidatura / Računovodstvo (US-F3) ───────────────────────────
            // Evidentira plaćanje fakture — vidi fakturu i potvrđuje plaćanje.
            [AppRoles.Likvidatura] =
            [
                AppPermissions.CodebooksView,
                AppPermissions.OrdersView,
                AppPermissions.OrdersViewOwn,
                AppPermissions.DocumentsView,
                AppPermissions.DocumentsDownload,
                AppPermissions.NotificationsView,
                AppPermissions.InvoiceView,
                AppPermissions.InvoiceConfirmPayment
            ],

            // ── Specijalni računi (US-F2) ──────────────────────────────────────
            // Prima notifikaciju o fakturi za PL (faktura + saglasnost + narudžbenica).
            [AppRoles.SpecijalniRacuni] =
            [
                AppPermissions.OrdersView,
                AppPermissions.OrdersViewOwn,
                AppPermissions.DocumentsView,
                AppPermissions.DocumentsDownload,
                AppPermissions.NotificationsView,
                AppPermissions.InvoiceView
            ],

            // ── Računovodstvo (US-F2/F3) ───────────────────────────────────────
            // Prima notifikaciju o fakturi za PL i može potvrditi plaćanje (uz Likvidaturu).
            [AppRoles.Racunovodstvo] =
            [
                AppPermissions.OrdersView,
                AppPermissions.OrdersViewOwn,
                AppPermissions.DocumentsView,
                AppPermissions.DocumentsDownload,
                AppPermissions.NotificationsView,
                AppPermissions.InvoiceView,
                AppPermissions.InvoiceConfirmPayment
            ]
        };

    /// <summary>
    /// Vraća uniju svih permission-a za dati skup rola.
    /// Poziva se kod claims transformation-a i <see cref="IUserPermissionService"/>.
    /// </summary>
    public static IEnumerable<string> GetPermissionsForRoles(IEnumerable<string> roles) =>
        roles
            .Where(PermissionsByRole.ContainsKey)
            .SelectMany(role => PermissionsByRole[role])
            .Distinct();

    /// <summary>Vraća true ako rola ima datu permission.</summary>
    public static bool RoleHasPermission(string role, string permission) =>
        PermissionsByRole.TryGetValue(role, out var perms) && perms.Contains(permission);
}
