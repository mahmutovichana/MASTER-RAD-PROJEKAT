#pragma warning disable CS0618 // ChangeStatus je [Obsolete] — seeder smije koristiti direktne prelaze
using System.Text;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Application.Users.Models;
using RBBH.CollateralAppraisal.Domain.Documents;
using RBBH.CollateralAppraisal.Domain.Notifications;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Seed;

/// <summary>
/// Idempotentno popunjava narudžbe procjene testnim podacima:
///  - PN-2026-001/002 (US 92/93/94 — upload dokumentacije, traženje/import mišljenja,
///    odobrenje finalne procjene, preuzimanje originala),
///  - demo skup narudžbi za Prodaju i Kolateral administratora (Početna — KPI kartice,
///    Pregled narudžbi, CA dashboard).
///
/// Idempotentnost: PN-2026-* se provjerava po <c>OrderNumber</c>, demo skup po
/// <c>InternalNote</c> markeru.
/// </summary>
public static class AppraisalOrderSeeder
{
    private const string TipoviNekretninaKey            = "tipovi_nekretnina";
    private const string TipoviDokumentaKey             = "tipovi_dokumenata";
    private const string TipoviKolateralaKey            = "tipovi_kolaterala";
    private const string KombiniraniTipoviKolateralaKey = "kombinovani_tipovi_kolaterala";
    private const string StanCode                       = "STAN";
    private const string KucaCode                       = "KUCA";
    private const string FinalAppraisalCode             = "FINALNA_PROCJENA";

    private const string FallbackProdajaUserId = "seed-am-user";
    private const string FallbackCAUserId      = "seed-ca-user";

    private const string DemoSeedMarker      = "Demo podaci za testiranje (seed).";
    private const string DemoDraftSeedMarker = "Demo nacrt za demonstraciju (seed).";

    public static async Task SeedAsync(
        ApplicationDbContext db,
        IFileStorageProvider fileStorage,
        IUserRoleProvider userRoleProvider,
        ILogger? logger = null,
        CancellationToken ct = default)
    {
        var existingOrderNumbers = await db.AppraisalOrders
            .IgnoreQueryFilters()
            .Select(x => x.OrderNumber)
            .ToListAsync(ct);

        var existing = new HashSet<string>(existingOrderNumbers, StringComparer.OrdinalIgnoreCase);

        var demoAlreadySeeded = await db.AppraisalOrders
            .IgnoreQueryFilters()
            .AnyAsync(x => x.InternalNote == DemoSeedMarker, ct);

        var demoDraftsSeeded = await db.AppraisalOrders
            .IgnoreQueryFilters()
            .AnyAsync(x => x.InternalNote == DemoDraftSeedMarker, ct);

        var pnOrdersSeeded = existing.Contains("PN-2026-001") && existing.Contains("PN-2026-002");
        if (pnOrdersSeeded && demoAlreadySeeded && demoDraftsSeeded)
        {
            logger?.LogInformation("AppraisalOrderSeeder: testne narudžbe već postoje, preskačem.");
            var now2 = DateTime.UtcNow;
            await SeedMissingCaTasksAsync(db, now2, logger, ct);
            var adminUserId = await ResolveUserIdAsync(
                userRoleProvider, AppRoles.Administrator, "admin.test", logger, ct);
            await SeedSupportingDemoDataAsync(db, adminUserId, now2, logger, ct);
            return;
        }

        var now = DateTime.UtcNow;

        var stanTypeId = await GetCodebookValueIdAsync(db, TipoviNekretninaKey, StanCode, ct);
        var kucaTypeId = await GetCodebookValueIdAsync(db, TipoviNekretninaKey, KucaCode, ct);
        var finalAppraisalTypeId = await GetCodebookValueIdAsync(db, TipoviDokumentaKey, FinalAppraisalCode, ct);

        var prodajaUserId = await ResolveUserIdAsync(userRoleProvider, AppRoles.AM, FallbackProdajaUserId, logger, ct);
        var caUserId      = await ResolveUserIdAsync(userRoleProvider, AppRoles.KolateralAdministrator, FallbackCAUserId, logger, ct);

        if (!existing.Contains("PN-2026-001"))
            await SeedOrderWithFinalAppraisalAsync(db, fileStorage, prodajaUserId, caUserId, stanTypeId, finalAppraisalTypeId, now, logger, ct);

        if (!existing.Contains("PN-2026-002"))
            await SeedAcceptedOrderAsync(db, prodajaUserId, caUserId, kucaTypeId, now, logger, ct);

        if (!demoAlreadySeeded)
            await SeedDemoOrdersAsync(db, prodajaUserId, caUserId, now, logger, ct);

        if (!demoDraftsSeeded)
            await SeedDemoDraftsAsync(db, prodajaUserId, now, logger, ct);

        await SeedMissingCaTasksAsync(db, now, logger, ct);
        var resolvedAdminUserId = await ResolveUserIdAsync(
            userRoleProvider, AppRoles.Administrator, "admin.test", logger, ct);
        await SeedSupportingDemoDataAsync(db, resolvedAdminUserId, now, logger, ct);
    }

    /// <summary>PN-2026-001 — status AppraisalReceived sa uploadovanom finalnom procjenom (testira US 93 T4/T6).</summary>
    private static async Task SeedOrderWithFinalAppraisalAsync(
        ApplicationDbContext db,
        IFileStorageProvider fileStorage,
        string prodajaUserId,
        string caUserId,
        int? collateralTypeId,
        int? finalAppraisalTypeId,
        DateTime now,
        ILogger? logger,
        CancellationToken ct)
    {
        var order = AppraisalOrder.Create(
            orderNumber: "PN-2026-001",
            title: "Narudžba procjene za Amir Hodžić",
            clientName: "Amir Hodžić",
            clientType: "FL",
            clientIdentifier: "1505990123456",
            contactName: "Amir Hodžić",
            contactPhone: null,
            contactEmail: null,
            city: "Sarajevo",
            branch: "Centar Sarajevo",
            branchAddress: null,
            propertyAddress: "Ferhadija 12, Sarajevo",
            collateralTypeId: collateralTypeId,
            combinedCollateralTypeId: null,
            createdByUserId: prodajaUserId,
            createdByRole: AppRoles.AM,
            createdByName: "Haris Hadžić",
            deliveryContactName: "Amir Hodžić",
            amRecipientName: "Haris Hadžić");

        order.Submit(now);
        order.AcceptByCA(caUserId, null, now);

        db.AppraisalOrders.Add(order);
        await db.SaveChangesAsync(ct);

        var pdfBytes = BuildDummyPdf("Finalna procjena — PN-2026-001 (seed)");
        await using var pdfStream = new MemoryStream(pdfBytes);
        var stored = await fileStorage.SaveAsync(
            pdfStream,
            "finalna-procjena-PN-2026-001.pdf",
            $"appraisal-orders/{order.Id}/documents",
            ct);

        var document = Document.Create(
            order.Id,
            finalAppraisalTypeId,
            Path.GetFileName(stored.StoragePath),
            "finalna-procjena-PN-2026-001.pdf",
            "application/pdf",
            stored.FileSize,
            stored.StoragePath,
            uploadedByUserId: caUserId);

        db.Documents.Add(document);
        await db.SaveChangesAsync(ct);

        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, now);
        order.SetFinalAppraisalDocument(document.Id, now);
        await db.SaveChangesAsync(ct);

        logger?.LogInformation(
            "AppraisalOrderSeeder: kreirana narudžba PN-2026-001 (Id={OrderId}, status={Status}) sa finalnom procjenom (DocumentId={DocumentId}).",
            order.Id, order.Status, document.Id);
    }

    /// <summary>PN-2026-002 — status AcceptedByCA, bez dokumentacije (testira US 92 upload i US 94 traženje mišljenja od nule).</summary>
    private static async Task SeedAcceptedOrderAsync(
        ApplicationDbContext db,
        string prodajaUserId,
        string caUserId,
        int? collateralTypeId,
        DateTime now,
        ILogger? logger,
        CancellationToken ct)
    {
        var order = AppraisalOrder.Create(
            orderNumber: "PN-2026-002",
            title: "Narudžba procjene za Lejla Tanović",
            clientName: "Lejla Tanović",
            clientType: "FL",
            clientIdentifier: "0203985654321",
            contactName: "Lejla Tanović",
            contactPhone: null,
            contactEmail: null,
            city: "Tuzla",
            branch: "Tuzla Centar",
            branchAddress: null,
            propertyAddress: "Slatina 5, Tuzla",
            collateralTypeId: collateralTypeId,
            combinedCollateralTypeId: null,
            createdByUserId: prodajaUserId,
            createdByRole: AppRoles.AM,
            createdByName: "Haris Hadžić",
            deliveryContactName: "Lejla Tanović",
            amRecipientName: "Haris Hadžić");

        order.Submit(now);
        order.AcceptByCA(caUserId, null, now);

        db.AppraisalOrders.Add(order);
        await db.SaveChangesAsync(ct);

        logger?.LogInformation(
            "AppraisalOrderSeeder: kreirana narudžba PN-2026-002 (Id={OrderId}, status={Status}).",
            order.Id, order.Status);
    }

    private sealed record DemoOrder(
        string ClientName, string ClientType, string? ClientIdentifier,
        string City, string Branch, string BranchAddress,
        string CollateralTypeCode, string? CombinedCollateralTypeCode, string CollateralLabel,
        AppraisalOrderStatus TargetStatus, bool CancelFromDraft = false);

    private static readonly DemoOrder[] DemoOrders =
    [
        new("Amir Hodžić", "FL", "0101990123456",
            "Sarajevo", "POS_SARAJEVO_CENTAR", "Maršala Tita 5, 71000 Sarajevo",
            "APP_STAN", "APP_STAN_I_GARAZA", "APP-stan i garaža",
            AppraisalOrderStatus.SubmittedBySales),

        new("Bosna Trade d.o.o.", "PL", "4200123450001",
            "Banja Luka", "POS_BANJA_LUKA", "Veselina Masleše 6, 78000 Banja Luka",
            "GARAZA", null, "Garaža",
            AppraisalOrderStatus.AcceptedByCA),

        new("Selma Kovačević", "FL", "1503985175310",
            "Tuzla", "POS_TUZLA", "Armije BiH 1, 75000 Tuzla",
            "OSTAVA", null, "Ostava",
            AppraisalOrderStatus.Completed),

        new("Edin Mehić", "FL", "2207992180022",
            "Mostar", "POS_MOSTAR", "Kralja Tomislava 5, 88000 Mostar",
            "APP_STAN", "APP_STAN_I_OSTAVA", "APP-stan i ostava",
            AppraisalOrderStatus.Cancelled),

        new("Drina Inženjering d.o.o.", "PL", "4300987650002",
            "Sarajevo", "POS_SARAJEVO_CENTAR", "Maršala Tita 5, 71000 Sarajevo",
            "APP_STAN", "APP_STAN_GARAZA_I_OSTAVA", "APP-stan garaža i ostava",
            AppraisalOrderStatus.Draft),

        new("Jasmin Begić", "FL", "0905988160044",
            "Banja Luka", "POS_BANJA_LUKA", "Veselina Masleše 6, 78000 Banja Luka",
            "GARAZA", null, "Garaža",
            AppraisalOrderStatus.SubmittedBySales),

        new("Lejla Hadžić", "FL", "1212991195566",
            "Tuzla", "POS_TUZLA", "Armije BiH 1, 75000 Tuzla",
            "APP_STAN", "APP_STAN_I_GARAZA", "APP-stan i garaža",
            AppraisalOrderStatus.AcceptedByCA),

        new("Una Gradnja d.o.o.", "PL", "4400112230003",
            "Mostar", "POS_MOSTAR", "Kralja Tomislava 5, 88000 Mostar",
            "OSTAVA", null, "Ostava",
            AppraisalOrderStatus.Completed),

        new("Adnan Tahirović", "FL", "0311987130077",
            "Sarajevo", "POS_SARAJEVO_ILIDZA", "Bosanski trg 3, 71210 Ilidža",
            "APP_STAN", null, "APP-stan",
            AppraisalOrderStatus.Draft),

        new("Maja Petrović", "FL", "1809993205588",
            "Banja Luka", "POS_BANJA_LUKA", "Veselina Masleše 6, 78000 Banja Luka",
            "APP_STAN", "APP_STAN_I_OSTAVA", "APP-stan i ostava",
            AppraisalOrderStatus.SubmittedBySales),

        new("Vrbas Komerc d.o.o.", "PL", "4500778890004",
            "Tuzla", "POS_TUZLA", "Armije BiH 1, 75000 Tuzla",
            "GARAZA", null, "Garaža",
            AppraisalOrderStatus.AcceptedByCA),

        new("Nina Đurić", "FL", "2604994215599",
            "Mostar", "POS_MOSTAR", "Kralja Tomislava 5, 88000 Mostar",
            "OSTAVA", null, "Ostava",
            AppraisalOrderStatus.Cancelled, CancelFromDraft: true),
    ];

    /// <summary>
    /// Demo skup narudžbi (raznih statusa) za Prodaju i Kolateral administratora —
    /// daje realne podatke za "Početna" (KPI kartice), "Pregled narudžbi" i CA dashboard.
    /// </summary>
    private static async Task SeedDemoOrdersAsync(
        ApplicationDbContext db,
        string prodajaUserId,
        string caUserId,
        DateTime now,
        ILogger? logger,
        CancellationToken ct)
    {
        var collateralTypeCodes = DemoOrders.Select(d => d.CollateralTypeCode).Distinct().ToList();
        var collateralTypeIds   = new Dictionary<string, int?>(StringComparer.OrdinalIgnoreCase);
        foreach (var code in collateralTypeCodes)
            collateralTypeIds[code] = await GetCodebookValueIdAsync(db, TipoviKolateralaKey, code, ct);

        var combinedTypeCodes = DemoOrders
            .Where(d => d.CombinedCollateralTypeCode != null)
            .Select(d => d.CombinedCollateralTypeCode!)
            .Distinct()
            .ToList();
        var combinedTypeIds = new Dictionary<string, int?>(StringComparer.OrdinalIgnoreCase);
        foreach (var code in combinedTypeCodes)
            combinedTypeIds[code] = await GetCodebookValueIdAsync(db, KombiniraniTipoviKolateralaKey, code, ct);

        var orderNum = await db.AppraisalOrders
            .IgnoreQueryFilters()
            .CountAsync(x => x.CreatedAt.Year == now.Year, ct);

        foreach (var s in DemoOrders)
        {
            orderNum++;
            var orderNumber = $"PN-{now.Year}-{orderNum:D6}";
            var title       = $"Narudžba procjene za {s.CollateralLabel} za klijenta {s.ClientName} grad {s.City}";

            collateralTypeIds.TryGetValue(s.CollateralTypeCode, out var ctId);
            int? cctId = null;
            if (s.CombinedCollateralTypeCode != null
                && combinedTypeIds.TryGetValue(s.CombinedCollateralTypeCode, out var tmp))
                cctId = tmp;

            var order = AppraisalOrder.Create(
                orderNumber:              orderNumber,
                title:                    title,
                clientName:               s.ClientName,
                clientType:               s.ClientType,
                clientIdentifier:         s.ClientIdentifier,
                contactName:              s.ClientName,
                contactPhone:             "+387 61 200 100",
                contactEmail:             null,
                city:                     s.City,
                branch:                   s.Branch,
                branchAddress:            s.BranchAddress,
                propertyAddress:          null,
                collateralTypeId:         ctId,
                combinedCollateralTypeId: cctId,
                createdByUserId:          prodajaUserId,
                createdByRole:            AppRoles.AM,
                createdByName:            "Haris Hadžić",
                deliveryContactName:      s.ClientName,
                amRecipientName:          "Haris Hadžić");

            order.SetInternalNote(DemoSeedMarker, now);
            ApplyStatus(order, s.TargetStatus, s.CancelFromDraft, caUserId, now);

            db.AppraisalOrders.Add(order);
        }

        await db.SaveChangesAsync(ct);
        logger?.LogInformation("AppraisalOrderSeeder: dodano {Count} demo narudžbi.", DemoOrders.Length);

        await SeedMissingCaTasksAsync(db, now, logger, ct);
    }

    /// <summary>
    /// Dva nedovršena demo nacrta (FL i PL) koja se prikazuju putem "Nastavi nacrt" bannera.
    /// Idempotentno — marker InternalNote == DemoDraftSeedMarker.
    /// </summary>
    private static async Task SeedDemoDraftsAsync(
        ApplicationDbContext db,
        string prodajaUserId,
        DateTime now,
        ILogger? logger,
        CancellationToken ct)
    {
        var stanTypeId   = await GetCodebookValueIdAsync(db, TipoviKolateralaKey, "APP_STAN", ct);
        var poslovniId   = await GetCodebookValueIdAsync(db, TipoviKolateralaKey, "POSLOVNI_PROSTOR", ct);

        var orderCount = await db.AppraisalOrders.IgnoreQueryFilters().CountAsync(x => x.CreatedAt.Year == now.Year, ct);

        // FL nacrt — Fizičko lice, stan, Sarajevo
        var flDraft = AppraisalOrder.Create(
            orderNumber:              $"PN-{now.Year}-{orderCount + 1:D6}",
            title:                    "Narudžba procjene za APP-stan za klijenta Belma Omerović grad Sarajevo",
            clientName:               "Belma Omerović",
            clientType:               "FL",
            clientIdentifier:         "1405995175388",
            contactName:              "Belma Omerović",
            contactPhone:             "+387 61 300 200",
            contactEmail:             null,
            city:                     "Sarajevo",
            branch:                   "POS_SARAJEVO_CENTAR",
            branchAddress:            "Maršala Tita 5, 71000 Sarajevo",
            propertyAddress:          "Radićeva 22, 71000 Sarajevo",
            collateralTypeId:         stanTypeId,
            combinedCollateralTypeId: null,
            createdByUserId:          prodajaUserId,
            createdByRole:            AppRoles.AM,
            createdByName:            "Haris Hadžić",
            deliveryContactName:      "Belma Omerović",
            amRecipientName:          "Haris Hadžić");
        flDraft.SetInternalNote(DemoDraftSeedMarker, now);
        db.AppraisalOrders.Add(flDraft);

        // PL nacrt — Pravno lice, poslovni prostor, Mostar
        var plDraft = AppraisalOrder.Create(
            orderNumber:              $"PN-{now.Year}-{orderCount + 2:D6}",
            title:                    "Narudžba procjene za poslovni prostor za klijenta Gradnja Plus d.o.o. grad Mostar",
            clientName:               "Gradnja Plus d.o.o.",
            clientType:               "PL",
            clientIdentifier:         "4227890450007",
            contactName:              "Muamer Hadžić",
            contactPhone:             "+387 36 555 100",
            contactEmail:             null,
            city:                     "Mostar",
            branch:                   "POS_MOSTAR",
            branchAddress:            "Kralja Tomislava 5, 88000 Mostar",
            propertyAddress:          "Bulevar 12, 88000 Mostar",
            collateralTypeId:         poslovniId ?? stanTypeId,
            combinedCollateralTypeId: null,
            createdByUserId:          prodajaUserId,
            createdByRole:            AppRoles.AM,
            createdByName:            "Haris Hadžić",
            deliveryContactName:      "Muamer Hadžić",
            amRecipientName:          "Haris Hadžić");
        plDraft.SetInternalNote(DemoDraftSeedMarker, now);
        db.AppraisalOrders.Add(plDraft);

        await db.SaveChangesAsync(ct);
        logger?.LogInformation("AppraisalOrderSeeder: kreirana 2 demo nacrta (FL + PL) za demonstraciju.");
    }

    private static async Task SeedMissingCaTasksAsync(
        ApplicationDbContext db, DateTime now, ILogger? logger, CancellationToken ct)
    {
        var existingTaskOrderIds = await db.TaskItems
            .Where(t => t.TaskType == TaskItemType.AcceptCAOrder)
            .Select(t => t.AppraisalOrderId)
            .ToListAsync(ct);

        var submittedOrders = await db.AppraisalOrders
            .IgnoreQueryFilters()
            .Where(o => o.Status == AppraisalOrderStatus.SubmittedBySales)
            .ToListAsync(ct);

        var ordersWithoutTask = submittedOrders
            .Where(o => !existingTaskOrderIds.Contains(o.Id))
            .ToList();

        foreach (var order in ordersWithoutTask)
        {
            var task = TaskItem.Create(
                orderId:      order.Id,
                type:         TaskItemType.AcceptCAOrder,
                title:        $"Prihvatanje narudžbe {order.OrderNumber}",
                description:  $"Pregled i prihvatanje narudžbe procjene: {order.Title}",
                assignedRole: AppRoles.KolateralAdministrator,
                dueDate:      now.AddDays(3));
            db.TaskItems.Add(task);
        }

        if (ordersWithoutTask.Count > 0)
        {
            await db.SaveChangesAsync(ct);
            logger?.LogInformation("AppraisalOrderSeeder: kreiran {Count} AcceptCAOrder task(ova) za SubmittedBySales narudžbe.",
                ordersWithoutTask.Count);
        }
    }

    private static async Task SeedSupportingDemoDataAsync(
        ApplicationDbContext db, string adminUserId, DateTime now, ILogger? logger, CancellationToken ct)
    {
        var orders = await db.AppraisalOrders
            .IgnoreQueryFilters()
            .Where(order => !order.IsDeleted && order.Status != AppraisalOrderStatus.Draft)
            .OrderBy(order => order.Id)
            .ToListAsync(ct);

        var protocolOrderIds = await db.OrderProtocolEntries
            .Select(entry => entry.OrderId)
            .ToHashSetAsync(ct);
        var nextSequence = await db.OrderProtocolEntries
            .Where(entry => entry.ProtocolYear == now.Year)
            .Select(entry => (int?)entry.ProtocolSequence)
            .MaxAsync(ct) ?? 0;

        foreach (var order in orders.Where(order => !protocolOrderIds.Contains(order.Id)))
        {
            nextSequence++;
            db.OrderProtocolEntries.Add(OrderProtocolEntry.Create(
                order.Id,
                now.Year,
                nextSequence,
                order.CreatedByUserId ?? adminUserId,
                order.CreatedAt));
        }

        const string demoTaskTitle = "Provjera migriranog RBI korisničkog interfejsa";
        if (!await db.TaskItems.AnyAsync(task => task.Title == demoTaskTitle, ct))
        {
            var taskOrder = orders.FirstOrDefault();
            if (taskOrder is not null)
            {
                db.TaskItems.Add(TaskItem.Create(
                    taskOrder.Id,
                    TaskItemType.ReviewDocumentation,
                    demoTaskTitle,
                    "Otvorite narudžbu i provjerite dokumente, statuse i dostupne workflow akcije.",
                    AppRoles.Administrator,
                    now.AddDays(5),
                    adminUserId));
            }
        }

        const string demoNotificationSubject = "Tema 3 je spremna za funkcionalnu provjeru";
        if (!await db.Notifications.AnyAsync(
                notification => notification.RecipientUserId == adminUserId
                    && notification.Subject == demoNotificationSubject, ct))
        {
            db.Notifications.Add(Notification.CreateInApp(
                adminUserId,
                demoNotificationSubject,
                "Lokalna baza sadrži primjere za narudžbe, zadatke, protokol, izvještaje i administraciju.",
                "AppraisalOrder",
                orders.FirstOrDefault()?.Id.ToString()));
        }

        await db.SaveChangesAsync(ct);
        logger?.LogInformation(
            "AppraisalOrderSeeder: dopunjeni protokol, administratorski zadatak i notifikacija za React provjeru.");
    }

    private static void ApplyStatus(
        AppraisalOrder order, AppraisalOrderStatus target, bool cancelFromDraft, string caUserId, DateTime now)
    {
        if (target == AppraisalOrderStatus.Draft)
            return;

        if (target == AppraisalOrderStatus.Cancelled && cancelFromDraft)
        {
            order.ChangeStatus(AppraisalOrderStatus.Cancelled, now);
            return;
        }

        order.Submit(now);

        if (target == AppraisalOrderStatus.SubmittedBySales)
            return;

        if (target == AppraisalOrderStatus.Cancelled)
        {
            order.ChangeStatus(AppraisalOrderStatus.Cancelled, now);
            return;
        }

        order.AcceptByCA(caUserId, null, now);

        if (target != AppraisalOrderStatus.AcceptedByCA)
            order.ChangeStatus(target, now);
    }

    private static async Task<int?> GetCodebookValueIdAsync(
        ApplicationDbContext db, string codebookKey, string code, CancellationToken ct)
    {
        return await db.CodebookValues
            .AsNoTracking()
            .Where(x => x.CodebookKey == codebookKey && x.Code == code)
            .Select(x => (int?)x.Id)
            .FirstOrDefaultAsync(ct);
    }

    private static async Task<string> ResolveUserIdAsync(
        IUserRoleProvider userRoleProvider, string role, string fallbackUserId, ILogger? logger, CancellationToken ct)
    {
        try
        {
            var result = await userRoleProvider.GetUsersWithRolesAsync(
                new UserRoleListRequest { Role = role, IsActive = true, Page = 1, PageSize = 1 }, ct);

            var userId = result.Items.FirstOrDefault()?.UserId;
            if (!string.IsNullOrWhiteSpace(userId))
                return userId;
        }
        catch (Exception ex)
        {
            logger?.LogWarning(ex,
                "AppraisalOrderSeeder: nije moguće dohvatiti korisnika za rolu {Role}, koristim fallback ID.", role);
        }

        return fallbackUserId;
    }

    /// <summary>Generiše minimalan validan PDF sa zadatim naslovom (dummy sadržaj za seed/test).</summary>
    private static byte[] BuildDummyPdf(string title)
    {
        var content = $"BT /F1 18 Tf 50 700 Td ({title}) Tj ET";
        var contentBytes = Encoding.ASCII.GetBytes(content);

        var sb = new StringBuilder();
        sb.Append("%PDF-1.4\n");
        sb.Append("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n");
        sb.Append("2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n");
        sb.Append("3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n");
        sb.Append("4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n");
        sb.Append($"5 0 obj\n<< /Length {contentBytes.Length} >>\nstream\n{content}\nendstream\nendobj\n");
        sb.Append("trailer\n<< /Size 6 /Root 1 0 R >>\n%%EOF");

        return Encoding.ASCII.GetBytes(sb.ToString());
    }
}
