using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Roles.Interfaces;
using RBBH.CollateralAppraisal.Domain.Roles;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Seed;

/// <summary>
/// Idempotentno puni RoleDefinition, PermissionDefinition i RolePermission tabele.
/// Pokušava sinhronizovati sistemske role s Keycloak-om.
///
/// Idempotentnost:
/// - Ako RoleDefinition već postoji → preskoči
/// - Ako PermissionDefinition već postoji → preskoči
/// - Ako RolePermission veza već postoji → preskoči
/// - Keycloak CreateRole: 409 Conflict se ignoriše (rola već postoji)
/// </summary>
public static class RolePermissionSeeder
{
    private const string SeedUserId = "system-seed";

    // ── Permission katalog sa svim meta-podacima ──────────────────────────────

    private static readonly (string Code, string DisplayName, string Description, string Module)[] PermissionCatalog =
    [
        (AppPermissions.UsersView,           "Pregled korisnika",          "Pregled liste korisnika i njihovih rola.",                     "Users"),
        (AppPermissions.UsersSuspend,        "Suspenzija korisnika",        "Suspenzija i reaktivacija korisničkih naloga.",               "Users"),
        (AppPermissions.RolesView,           "Pregled rola",               "Pregled kataloga rola i njihovih permissiona.",                "Roles"),
        (AppPermissions.RolesAssign,         "Dodjela rola",               "Dodjela role korisniku.",                                      "Roles"),
        (AppPermissions.RolesRemove,         "Uklanjanje rola",            "Uklanjanje role od korisnika.",                               "Roles"),
        (AppPermissions.RolesTransferAdmin,  "Prenos admin role",          "Sigurni prenos administratorske role na drugog korisnika.",    "Roles"),
        (AppPermissions.RolesManage,         "Upravljanje rolama",         "Kreiranje, uređivanje, deaktivacija i brisanje custom rola.",  "Roles"),
        (AppPermissions.RecordsCreate,       "Kreiranje zapisa",           "Kreiranje novih narudžbi procjene nekretnina.",               "Records"),
        (AppPermissions.RecordsViewOwn,      "Pregled vlastitih zapisa",   "Pregled vlastitih narudžbi i dokumenata.",                    "Records"),
        (AppPermissions.RecordsUpdateOwnDraft,"Izmjena nacrta",            "Uređivanje vlastitih zapisa u statusu Nacrt.",                "Records"),
        (AppPermissions.RecordsSubmitForVerification, "Slanje na verifikaciju", "Slanje narudžbe na verifikaciju.",                      "Records"),
        (AppPermissions.RecordsViewPendingVerification,"Pregled čekajućih verifikacija","Pregled narudžbi koje čekaju verifikaciju.",     "Records"),
        (AppPermissions.RecordsApprove,      "Odobravanje zapisa",         "Verifikacija i odobravanje narudžbi.",                        "Records"),
        (AppPermissions.RecordsReject,       "Odbijanje zapisa",           "Odbijanje narudžbi s razlogom.",                              "Records"),
        (AppPermissions.RecordsViewHistory,  "Historija zapisa",           "Pregled historije svih narudžbi i promjena.",                 "Records"),
        (AppPermissions.CodebooksView,       "Pregled šifarnika",          "Čitanje vrijednosti iz referentnih šifarnika.",               "Codebooks"),
        (AppPermissions.CodebooksManage,     "Upravljanje šifarnicima",    "Kreiranje, uređivanje i deaktivacija šifarnika i vrijednosti.", "Codebooks"),
        (AppPermissions.AuditViewSecurity,   "Pregled audit loga",         "Pregled sigurnosnog audit loga i događaja.",                  "Audit"),
        (AppPermissions.AdminAccess,         "Administrativni pristup",    "Pristup administrativnom panelu i svim admin funkcijama.",    "Admin"),

        // ── Dokumenti narudžbe (US 92) ────────────────────────────────────────
        (AppPermissions.DocumentsUpload,     "Upload dokumenata",          "Upload dokumentacije uz narudžbu procjene.",                  "Documents"),
        (AppPermissions.DocumentsView,       "Pregled dokumenata",         "Pregled liste dokumenata uz narudžbu procjene.",              "Documents"),
        (AppPermissions.DocumentsDownload,   "Preuzimanje dokumenata",     "Preuzimanje (download) dokumenata uz narudžbu procjene.",     "Documents"),
        (AppPermissions.DocumentsDelete,     "Brisanje dokumenata",        "Brisanje (soft-delete) dokumenata uz narudžbu procjene.",     "Documents"),

        // ── Narudžba / workflow procjene (US 93) ──────────────────────────────
        (AppPermissions.OrdersView,              "Pregled narudžbi",            "Pregled narudžbi procjene i njihovog statusa.",                       "Orders"),
        (AppPermissions.OrdersApproveFinal,      "Odobrenje finalne procjene",  "Odobravanje finalne procjene — \"može dalje u proceduru\".",          "Orders"),
        (AppPermissions.OrdersDownloadAppraisal, "Preuzimanje procjene",        "Preuzimanje finalnog dokumenta procjene.",                            "Orders"),
        (AppPermissions.OrdersConfirmOriginal,   "Potvrda originala",           "Potvrda preuzimanja originala procjene u poslovnici.",                "Orders"),
        (AppPermissions.OrdersRemindAppraiser,   "Reminder vještaku",           "Slanje podsjetnika vještaku za dostavu originala procjene.",          "Orders"),

        // ── Mišljenja CO i Pravne službe (US 94) ──────────────────────────────
        (AppPermissions.OpinionsRequest,     "Traženje mišljenja",         "Traženje mišljenja CO i Pravne službe za narudžbu.",          "Opinions"),
        (AppPermissions.OpinionsSubmitCo,    "Unos mišljenja CO",          "Import mišljenja Kolateral oficira (CO).",                    "Opinions"),
        (AppPermissions.OpinionsSubmitLegal, "Unos mišljenja Pravne",      "Import mišljenja Pravne službe.",                             "Opinions"),
        (AppPermissions.OpinionsView,        "Pregled mišljenja",          "Pregled statusa i sadržaja mišljenja CO i Pravne službe.",    "Opinions"),

        // ── Notifikacije ───────────────────────────────────────────────────────
        (AppPermissions.NotificationsView,   "Pregled notifikacija",       "Pregled vlastitog inboxa in-app notifikacija.",               "Notifications"),

        // ── Narudžbe procjene — inicijacija i radni tok (US-1, US-2) ──────────
        (AppPermissions.OrdersCreate,       "Kreiranje narudžbe",         "Iniciranje nove narudžbe procjene nekretnine.",               "Orders"),
        (AppPermissions.OrdersViewOwn,      "Pregled vlastitih narudžbi", "Pregled narudžbi koje je kreirao trenutni korisnik.",         "Orders"),
        (AppPermissions.OrdersViewAll,      "Pregled svih narudžbi",      "Pregled svih narudžbi u sistemu (Kolateral administrator, Administrator).", "Orders"),
        (AppPermissions.OrdersUpdateDraft,  "Izmjena nacrta narudžbe",    "Izmjena narudžbe u statusu Draft.",                          "Orders"),
        (AppPermissions.OrdersSubmit,       "Podnošenje narudžbe",        "Podnošenje narudžbe Kolateral administratoru na obradu.",     "Orders"),
        (AppPermissions.OrdersCancel,       "Otkazivanje narudžbe",       "Otkazivanje narudžbe u statusu Draft.",                      "Orders"),
        (AppPermissions.OrdersAccept,       "Prihvatanje narudžbe",       "Prihvatanje i obrada narudžbe (Kolateral administrator).",   "Orders"),
        (AppPermissions.ProtocolView,       "Pregled protokola",          "Pregled protokolnih unosa narudžbi.",                        "Orders"),

        // ── CA pregled dokumentacije — "Dopuna podataka" / "Završi pregled" (US-91/92) ──
        (AppPermissions.OrdersRequestCorrection, "Vraćanje na dopunu",       "CA vraća narudžbu Prodaji na dopunu podataka.",            "Orders"),
        (AppPermissions.OrdersCompleteReview,    "Završetak pregleda",       "CA završava pregled dokumentacije.",                       "Orders"),
        (AppPermissions.OrdersSubmitCorrection,  "Dostava dopune",           "Prodaja potvrđuje da je dopuna podataka dostavljena.",     "Orders"),

        // ── CO provjera pristupa prije narudžbe (US-93) ───────────────────────
        (AppPermissions.OrdersAccessCheck,       "Provjera pristupa",        "CO potvrđuje/odbija uredan pristup nekretnini prije narudžbe.", "Orders"),

        // ── Odabir vještaka + master-data vještaka (Faza C) ───────────────────
        (AppPermissions.OrdersSelectAppraiser,   "Odabir vještaka",          "Odabir vještaka za narudžbu (automatski FL / ručni PL).",  "Orders"),
        (AppPermissions.AppraisersManage,        "Upravljanje vještacima",   "Kreiranje, uređivanje, GO/blacklist i deaktivacija vještaka.", "Appraisers"),
        (AppPermissions.AppraisersView,          "Pregled vještaka",         "Pregled liste vještaka i njihove dostupnosti.",            "Appraisers"),
        (AppPermissions.OrdersAdditionalPayment, "Doplata",                  "Zahtjev i obrada doplate za narudžbu procjene.",           "Orders"),
        (AppPermissions.CodebooksImport,         "Import šifarnika",         "Import podataka u šifarnike iz CSV/Excel fajlova.",        "Codebooks"),
        (AppPermissions.CodebooksExport,         "Export šifarnika",         "Export šifarnika u CSV/Excel format.",                      "Codebooks"),
        (AppPermissions.AppraisersImport,        "Import vještaka",          "Masovni import vještaka iz CSV/Excel fajlova.",            "Appraisers"),
        (AppPermissions.AppraisersExport,        "Export vještaka",          "Export šifarnika vještaka u CSV/Excel format.",             "Appraisers"),

        // ── Dijeljeni dokumenti (cjenovnik, lista dokumentacije po tipu) ────────
        (AppPermissions.SharedDocumentsView,   "Pregled dijeljenih dokumenata",   "Pregled i download cjenovnika i liste dokumentacije.",          "SharedDocuments"),
        (AppPermissions.SharedDocumentsManage, "Upravljanje dijeljenim dokumentima", "Upload i brisanje dijeljenih dokumenata (CA).",              "SharedDocuments"),

        // ── Segment Prodaja (AM/SM/UB) — imenovan permission katalog ──────────
        (AppPermissions.SalesDashboardView,    "Prodaja: pristup dashboardu",  "Pristup početnom dashboardu segmenta Prodaja.",            "Prodaja"),
        (AppPermissions.SalesOrderCreate,      "Prodaja: kreiranje narudžbe",  "Kreiranje nove narudžbe procjene u segmentu Prodaja.",      "Prodaja"),
        (AppPermissions.SalesOrderView,        "Prodaja: pregled narudžbi",    "Pregled narudžbi koje pripadaju segmentu Prodaja.",         "Prodaja"),
        (AppPermissions.SalesOrderEditDraft,   "Prodaja: izmjena nacrta",      "Čuvanje i izmjena nacrta narudžbe u segmentu Prodaja.",     "Prodaja"),
        (AppPermissions.SalesOrderSubmit,      "Prodaja: završetak unosa",     "Završetak unosa i slanje narudžbe prema CA.",               "Prodaja"),
        (AppPermissions.SalesOrderDetailsView, "Prodaja: pregled detalja",     "Pregled detalja narudžbe u segmentu Prodaja.",              "Prodaja"),
    ];

    // ── Sistemske role ────────────────────────────────────────────────────────

    private static readonly (string Name, string DisplayName, string Description)[] SystemRoles =
    [
        (AppRoles.Administrator, "Administrator",       "Potpuni pristup svim modulima i administracijskim funkcijama."),
        (AppRoles.Verifikator,   "Verifikator",         "Pregled, provjera i verifikacija unesenih podataka o nekretninama."),
        (AppRoles.Unosnik,       "Unosnik podataka",   "Kreiranje i unos podataka o nekretninama i narudžbama."),

        // ── Segment Prodaja — AM, SM, UB (narudžbe procjene — US 92/93/94) ────
        // Tri odvojene role, identičan permission set (vidi RolePermissionMatrix).
        (AppRoles.AM, "Account Manager (AM)", "Segment Prodaja — inicira narudžbu procjene, uploaduje dokumentaciju, traži mišljenja i preuzima procjenu."),
        (AppRoles.SM, "Sales Manager (SM)",   "Segment Prodaja — inicira narudžbu procjene, uploaduje dokumentaciju, traži mišljenja i preuzima procjenu."),
        (AppRoles.UB, "Universal Banker (UB)","Segment Prodaja — inicira narudžbu procjene, uploaduje dokumentaciju, traži mišljenja i preuzima procjenu."),
        (AppRoles.KolateralAdministrator, "Kolateral administrator",   "Vodi narudžbu procjene, provjerava dokumentaciju i bira vještaka."),
        (AppRoles.KolateralOficir,        "Kolateral oficir",          "Provjerava pristup, odobrava finalnu procjenu i daje mišljenje CO."),
        (AppRoles.Vjestak,                "Vještak",                   "Eksterni izvođač procjene nekretnine."),
        (AppRoles.PravnaSluzba,           "Pravna služba",             "Daje pravno mišljenje za narudžbu procjene."),
        (AppRoles.Protokol,               "Protokol",                  "Upload i obrada fakture u protokolu narudžbi."),
        (AppRoles.Likvidatura,            "Likvidatura / Računovodstvo","Evidentira plaćanje fakture vještaka (US-F3)."),
        (AppRoles.SpecijalniRacuni,       "Specijalni računi",         "Prima notifikaciju o fakturi za PL klijente (US-F2)."),
        (AppRoles.Racunovodstvo,          "Računovodstvo",             "Prima notifikaciju o fakturi za PL i evidentira plaćanje (US-F2/F3)."),
    ];

    // ─────────────────────────────────────────────────────────────────────────

    public static async Task SeedAsync(
        ApplicationDbContext     db,
        IKeycloakRoleSyncService keycloakSync,
        ILogger?                 logger    = null,
        CancellationToken        ct        = default)
    {
        var now = DateTime.UtcNow;

        // ── 1. Seed PermissionDefinition ──────────────────────────────────────

        var existingPermCodes = await db.PermissionDefinitions
            .IgnoreQueryFilters()
            .Select(p => p.Code)
            .ToListAsync(ct);

        var existingPermSet = new HashSet<string>(existingPermCodes, StringComparer.OrdinalIgnoreCase);
        var newPermsCount = 0;

        foreach (var (code, displayName, description, module) in PermissionCatalog)
        {
            if (existingPermSet.Contains(code))
                continue;

            db.PermissionDefinitions.Add(
                PermissionDefinition.Create(code, displayName, description, module));
            newPermsCount++;
        }

        if (newPermsCount > 0)
        {
            await db.SaveChangesAsync(ct);
            logger?.LogInformation("Seed: dodano {Count} novih permissiona.", newPermsCount);
        }

        // ── 2. Seed RoleDefinition ────────────────────────────────────────────

        var existingRoleNames = await db.RoleDefinitions
            .IgnoreQueryFilters()
            .Select(r => r.Name)
            .ToListAsync(ct);

        var existingRoleSet = new HashSet<string>(existingRoleNames, StringComparer.OrdinalIgnoreCase);
        var newRolesCount = 0;

        foreach (var (name, displayName, description) in SystemRoles)
        {
            if (existingRoleSet.Contains(name))
                continue;

            db.RoleDefinitions.Add(RoleDefinition.CreateSystem(name, displayName, description));
            newRolesCount++;
        }

        if (newRolesCount > 0)
        {
            await db.SaveChangesAsync(ct);
            logger?.LogInformation("Seed: dodano {Count} novih sistemskih rola.", newRolesCount);
        }

        // ── 3. Seed Keycloak realm role (idempotentno) ────────────────────────

        foreach (var (name, displayName, description) in SystemRoles)
        {
            try
            {
                await keycloakSync.CreateRoleAsync(name, description, ct);
                logger?.LogDebug("Seed: Keycloak rola '{Role}' sinhronizovana.", name);
            }
            catch (Exception ex)
            {
                logger?.LogWarning(ex, "Seed: Keycloak sync nije uspio za rolu '{Role}'. Nastavlja se.", name);
                // Ne prekidamo seed ako Keycloak nije dostupan — lokalni DB seed je primarni
            }
        }

        // ── 4. Seed RolePermission veze ───────────────────────────────────────

        // Učitaj permissione iz baze (imaju Id koji treba za RolePermission)
        var allPerms = await db.PermissionDefinitions
            .AsNoTracking()
            .Select(p => new { p.Id, p.Code })
            .ToListAsync(ct);

        var permByCode = allPerms.ToDictionary(
            p => p.Code, p => p.Id, StringComparer.OrdinalIgnoreCase);

        // Učitaj role iz baze (samo aktivne — soft-obrisane role mogu imati
        // duplikate naziva i ne trebaju dobiti permission mape)
        var allRoles = await db.RoleDefinitions
            .Include(r => r.Permissions)
            .ToListAsync(ct);

        var roleByName = allRoles.ToDictionary(
            r => r.Name, StringComparer.OrdinalIgnoreCase);

        var newMappingsCount = 0;

        foreach (var (roleName, permCodes) in RolePermissionMatrix.PermissionsByRole)
        {
            if (!roleByName.TryGetValue(roleName, out var role))
                continue;

            var existingPermIds = role.Permissions
                .Select(rp => rp.PermissionDefinitionId)
                .ToHashSet();

            foreach (var permCode in permCodes)
            {
                if (!permByCode.TryGetValue(permCode, out var permId))
                    continue;

                if (existingPermIds.Contains(permId))
                    continue;

                db.RolePermissions.Add(RolePermission.Create(role.Id, permId, SeedUserId));
                newMappingsCount++;
            }
        }

        if (newMappingsCount > 0)
        {
            await db.SaveChangesAsync(ct);
            logger?.LogInformation("Seed: dodano {Count} novih role-permission veza.", newMappingsCount);
        }

        logger?.LogInformation(
            "RolePermissionSeeder završen: {Roles} rola, {Perms} permissiona, {Mappings} veza.",
            newRolesCount, newPermsCount, newMappingsCount);
    }
}
