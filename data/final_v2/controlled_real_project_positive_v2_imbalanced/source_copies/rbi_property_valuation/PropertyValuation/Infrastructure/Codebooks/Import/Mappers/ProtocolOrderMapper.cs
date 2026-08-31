﻿using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Codebooks.Import;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Codebooks.Import.Mappers;

/// <summary>
/// Masovni import/update narudžbi iz Excel tabele (spec prilog 1 — 36 kolona, ~5700 redova).
/// Kolone odgovaraju taćnoj strukturi Excel fajla "USER STORY amela_FL_PL finalna verzija".
/// Identifikacija narudžbe po koloni "ID" (redni broj). Ažurira postojeće ili kreira nove protokolne zapise.
/// </summary>
[ExcludeFromCodeCoverage]
public sealed class ProtocolOrderMapper : ICodebookMapper
{
    public string CodebookType => "protokol_narudzbi";

    public string? DuplicateKeyColumn => null;

    /// <summary>
    /// Samo MASOVNI UPDATE kolone (prema Prorokol.xlsx prilog 4.1).
    /// BLANK kolone se ne ćitaju — popunjavaju se automatski kroz workflow.
    /// </summary>
    public IReadOnlyList<ColumnDef> Columns =>
    [
        // MASOVNI UPDATE kolone
        new("Procjenitelj",                                           "Procjenitelj (A)",                  Required: false),
        new("Ocjena procjenitelja",                                   "Ocjena procjenitelja (B)",          Required: false),
        new("Klijent",                                                "Klijent (C)",                       Required: true),
        new("Segment",                                                "Segment FL/PL (D)",                 Required: false),
        new("ESG certifikat",                                         "ESG certifikat (E)",                Required: false),
        new("Kolateral",                                              "Kolateral (F)",                     Required: false),
        new("Tip kolaterala",                                         "Tip kolaterala (G)",                Required: false),
        new("Grad",                                                   "Grad (I)",                          Required: false),
        new("Datum prijema zahtjeva od Prodaje",                      "Datum prijema od Prodaje (P)",      Required: false),
        new("Status pregleda dokumentacije za narudžbu procjene",     "Status pregleda dok. (R)",          Required: false),
        new("Datum dopune dokumentacije",                             "Datum dopune dok. (S)",             Required: false),
        new("Izjava - Saglasnost PL_Uplatnica FL",                   "Izjava/Saglasnost/Uplatnica (T)",   Required: false),
        new("Naknada za procjenu (KM)",                               "Naknada KM (U)",                   Required: false),
        new("Datum narudžbe procjene",                                "Datum narudžbe (V)",                Required: false),
        new("Datum obilaska imovine",                                 "Datum obilaska (W)",                Required: false),
        new("Datum korekcije procjene",                               "Datum korekcije (Z)",              Required: false),
        new("Datum dostavljanja finalne procjene",                    "Datum finalne procjene (AB)",       Required: false),
        new("Datum dostavljanja fakture",                             "Datum fakture (AD)",                Required: false),
        new("Status",                                                 "Status narudžbe (AF)",              Required: false),
        new("CO koji je narućio procjenu",                            "CO koji je narućio (AG)",           Required: false),
        new("Komentar",                                               "Komentar (AH)",                    Required: false),
        new("ID",                                                     "ID (AI)",                           Required: true),
    ];

    public Task<IReadOnlyList<ImportRowError>> ValidateRowAsync(ParsedRow row, ImportContext ctx, CancellationToken ct)
    {
        var errors = new List<ImportRowError>();
        if (string.IsNullOrWhiteSpace(row.Get("Klijent")))
            errors.Add(new(row.RowNumber, "Klijent", "Naziv klijenta je obavezan."));
        if (string.IsNullOrWhiteSpace(row.Get("ID")))
            errors.Add(new(row.RowNumber, "ID", "ID je obavezan za identifikaciju."));
        return Task.FromResult<IReadOnlyList<ImportRowError>>(errors);
    }

    public Task<RowAction> ClassifyRowAsync(ParsedRow row, ImportContext ctx, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(row.Get("Klijent")))
            return Task.FromResult(RowAction.Skip);
        return Task.FromResult(RowAction.New);
    }

    public async Task ApplyRowAsync(ParsedRow row, RowAction action, ImportContext ctx, CancellationToken ct)
    {
        if (action == RowAction.Skip) return;
        var db = (ApplicationDbContext)ctx.DbContext;

        var clientName  = row.Get("Klijent")?.Trim() ?? "";
        var clientType  = row.Get("Segment")?.Trim();
        var city        = row.Get("Grad")?.Trim();
        var address     = row.Get("Adresa kolaterala")?.Trim();
        // â”€â”€ MASOVNI UPDATE kolone (prema Prorokol.xlsx prilog 4.1) â”€â”€
        var collateral  = row.Get("Kolateral")?.Trim();                          // F: MASOVNI UPDATE
        var esg         = row.Get("ESG certifikat")?.Trim();                     // E: MASOVNI UPDATE
        var consent     = row.Get("Izjava - Saglasnost PL_Uplatnica FL")?.Trim();// T: MASOVNI UPDATE
        var comment     = row.Get("Komentar")?.Trim();                           // AH: MASOVNI UPDATE
        var idStr       = row.Get("ID")?.Trim();                                 // AI: MASOVNI UPDATE
        var coName      = row.Get("CO koji je narućio procjenu")?.Trim();        // AG: MASOVNI UPDATE

        var feeStr    = row.Get("Naknada za procjenu (KM)")?.Trim();             // U: MASOVNI UPDATE
        decimal? fee  = decimal.TryParse(feeStr, out var f) ? f : null;

        var ratingStr = row.Get("Ocjena procjenitelja")?.Trim();                 // B: MASOVNI UPDATE

        // MASOVNI UPDATE datumi
        var requestSent       = TryParseDate(row.Get("Datum prijema zahtjeva od Prodaje"));      // P
        var docSupplementDate = TryParseDate(row.Get("Datum dopune dokumentacije"));              // S
        var orderDate         = TryParseDate(row.Get("Datum narudžbe procjene"));                 // V
        var visitDate         = TryParseDate(row.Get("Datum obilaska imovine"));                  // W
        var correctionDate    = TryParseDate(row.Get("Datum korekcije procjene"));                // Z
        var finalDate         = TryParseDate(row.Get("Datum dostavljanja finalne procjene"));     // AB
        var invoiceDate       = TryParseDate(row.Get("Datum dostavljanja fakture"));              // AD

        // BLANK kolone — NE ćitamo: J, K, L, M, N, O, Q, X, Y, AA, AC, AE, AJ

        var now = DateTime.UtcNow;
        var orderNumber = $"IMP-{idStr ?? row.RowNumber.ToString()}";

        var wfType = clientType?.Equals("PL", StringComparison.OrdinalIgnoreCase) == true
            ? WorkflowType.PravnaLica
            : WorkflowType.FizickaLica;

        var order = AppraisalOrder.Create(
            orderNumber:              orderNumber,
            title:                    $"Import — {clientName}, {city}",
            clientName:               clientName,
            clientType:               clientType,
            clientIdentifier:         null,
            contactName:              null,
            contactPhone:             null,         // L: BLANK
            contactEmail:             null,
            city:                     city,
            branch:                   null,
            branchAddress:            null,         // O: BLANK
            propertyAddress:          null,         // J: BLANK
            collateralTypeId:         null,
            combinedCollateralTypeId: null,
            createdByUserId:          ctx.UserId ?? "import",
            createdByRole:            "Import",
            createdByName:            null,         // AJ: BLANK
            deliveryContactName:      null,         // M: BLANK
            amRecipientName:          null,         // N: BLANK
            workflowType:             wfType,
            requestReceivedAt:        null,         // K: BLANK
            requestSentAt:            requestSent);

        if (fee.HasValue)             order.SetAppraisalFee(fee.Value, now);
        if (esg is not null)          order.SetEsgCertificate(esg, now);
        if (consent is not null)      order.SetPaymentConsentStatus(consent, now);
        if (collateral is not null)   order.SetCollateralStatus(collateral, now);
        if (visitDate.HasValue)       order.SetAppraiserVisitDate(visitDate.Value, now);
        if (invoiceDate.HasValue)     order.SetInvoiceReceivedDate(invoiceDate, now);

        var statusText = row.Get("Status")?.Trim();
        var mappedStatus = MapExcelStatus(statusText);
        if (mappedStatus != AppraisalOrderStatus.Draft)
        {
            #pragma warning disable CS0618
            order.ChangeStatus(mappedStatus, now);
            #pragma warning restore CS0618
        }

        var ratingValue = !string.IsNullOrWhiteSpace(ratingStr) && ratingStr != "AA"
            ? (ratingStr switch { "A" => 5, "B" => 4, "C" => 3, "D" => 2, "E" => 1, _ => (int?)null })
            : null;
        if (ratingValue.HasValue) order.SetAppraiserRating(ratingValue.Value, now);

        db.AppraisalOrders.Add(order);

        // Batch: sakupljamo podatke za protokol — kreiramo nakon SaveChanges kad imamo ID
        if (!ctx.Cache.ContainsKey("_pendingProtocols"))
            ctx.Cache["_pendingProtocols"] = new List<(AppraisalOrder Order, int Seq, int Year)>();

        var seqNum = int.TryParse(idStr, out var seq) ? seq : row.RowNumber;
        var protocolYear = requestSent?.Year ?? orderDate?.Year ?? now.Year;
        ((List<(AppraisalOrder, int, int)>)ctx.Cache["_pendingProtocols"]).Add((order, seqNum, protocolYear));

        // Batch save svakih 200 redova
        var pending = (List<(AppraisalOrder Order, int Seq, int Year)>)ctx.Cache["_pendingProtocols"];
        if (pending.Count >= 200)
            await FlushBatchAsync(db, pending, ctx.UserId, now, ct);
    }

    internal static async Task FlushBatchAsync(
        ApplicationDbContext db,
        List<(AppraisalOrder Order, int Seq, int Year)> pending,
        string? userId, DateTime now, CancellationToken ct)
    {
        if (pending.Count == 0) return;
        await db.SaveChangesAsync(ct);

        foreach (var (order, seqNum, protocolYear) in pending)
        {
            var protocol = OrderProtocolEntry.Create(
                orderId:           order.Id,
                year:              protocolYear,
                sequence:          seqNum,
                generatedByUserId: userId ?? "import",
                now:               now);
            db.OrderProtocolEntries.Add(protocol);
        }
        await db.SaveChangesAsync(ct);
        pending.Clear();
    }

    private static AppraisalOrderStatus MapExcelStatus(string? status) => status switch
    {
        "Završeno"                 => AppraisalOrderStatus.Completed,
        "Klijent odustao"          => AppraisalOrderStatus.Cancelled,
        "Odustao"                  => AppraisalOrderStatus.Cancelled,
        "Stornirana"               => AppraisalOrderStatus.Cancelled,
        "Na procjeni"              => AppraisalOrderStatus.AppraisalInProgress,
        "Za slanje na AM"          => AppraisalOrderStatus.ReadyForProcedure,
        "Uredna dokumentacija"     => AppraisalOrderStatus.DocumentationApproved,
        "Zatraženo pojašnjenje"    => AppraisalOrderStatus.ReturnedForCorrection,
        "U obradi"                 => AppraisalOrderStatus.AppraisalInProgress,
        "ÄŒeka potpisanu izjavu"    => AppraisalOrderStatus.OrderSentToAppraiser,
        "ÄŒeka dopunu"              => AppraisalOrderStatus.ReturnedForCorrection,
        "ÄŒeka saglasnost"          => AppraisalOrderStatus.OrderSentToAppraiser,
        _                          => AppraisalOrderStatus.Completed
    };

    public Task<int> DeactivateMissingAsync(IReadOnlyList<ParsedRow> rows, ImportContext ctx, CancellationToken ct)
        => Task.FromResult(0);

    public async Task<IReadOnlyList<Dictionary<string, string?>>> ExportRowsAsync(
        bool includeInactive, ImportContext ctx, CancellationToken ct)
    {
        var db = (ApplicationDbContext)ctx.DbContext;
        var orders = await db.AppraisalOrders
            .AsNoTracking()
            .OrderByDescending(o => o.CreatedAt)
            .Take(10000)
            .ToListAsync(ct);

        return orders.Select(o => new Dictionary<string, string?>
        {
            ["Klijent"]                   = o.ClientName,
            ["Segment"]                   = o.ClientType,
            ["Grad"]                      = o.City,
            ["Adresa kolaterala"]         = o.PropertyAddress,
            ["Status"]                    = o.Status.ToString(),
            ["Naknada za procjenu (KM)"]  = o.AppraisalFee?.ToString("F2"),
            ["ESG certifikat"]            = o.EsgCertificate,
            ["ID"]                        = o.Id.ToString(),
        }).ToList<Dictionary<string, string?>>();
    }

    private static DateTime? TryParseDate(string? value)
    {
        if (string.IsNullOrWhiteSpace(value)) return null;
        return DateTime.TryParse(value, out var dt)
            ? DateTime.SpecifyKind(dt, DateTimeKind.Utc)
            : null;
    }
}
