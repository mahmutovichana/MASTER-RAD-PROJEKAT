﻿using ClosedXML.Excel;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Application.Reports;
using RBBH.CollateralAppraisal.Application.Reports.Dtos;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Reports;

[ExcludeFromCodeCoverage]
public sealed class OrdersTimeReportService : IOrdersTimeReportService
{
    private readonly IProtocolService _protocol;

    public OrdersTimeReportService(IProtocolService protocol)
    {
        _protocol = protocol;
    }

    public async Task<List<OrdersTimeReportRowDto>> GetReportAsync(DateTime? endDate = null, CancellationToken ct = default)
    {
        // Ućitaj sve zapise (velika stranica); filtriranje u memoriji po endDate
        var page = await _protocol.GetProtocolListAsync(1, 10_000, ct);
        var rows = page.Items.AsEnumerable();

        if (endDate.HasValue)
        {
            var cutoff = endDate.Value.Date.AddDays(1); // ukljući cijeli endDate dan
            rows = rows.Where(e => e.RequestReceivedAt == null || e.RequestReceivedAt.Value < cutoff);
        }

        return rows.Select(MapRow).ToList();
    }

    public async Task<(Stream Stream, string ContentType, string FileName)> GetReportXlsxAsync(
        DateTime? endDate = null, CancellationToken ct = default)
    {
        var rows = await GetReportAsync(endDate, ct);
        var ms = BuildXlsx(rows);
        var fileName = $"pregled-narudzbi-{DateTime.UtcNow:yyyyMMdd}.xlsx";
        return (ms, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", fileName);
    }

    // â”€â”€ Mapiranje â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    public static OrdersTimeReportRowDto MapRow(ProtocolEntryDto e) => new(
        OrderId:                    e.OrderId,
        OrderNumber:                e.OrderNumber,
        ProtocolNumber:             e.ProtocolNumber,
        ProtocolYear:               e.ProtocolYear,
        ProtocolSequence:           e.ProtocolSequence,
        OrderTitle:                 e.OrderTitle,
        ClientName:                 e.ClientName,
        ClientType:                 e.ClientType,
        ClientIdentifier:           e.ClientIdentifier,
        City:                       e.City,
        Branch:                     e.Branch,
        BranchAddress:              e.BranchAddress,
        PropertyAddress:            e.PropertyAddress,
        ContactName:                e.ContactName,
        ContactPhone:               e.ContactPhone,
        CreatedByName:              e.CreatedByName,
        CreatedByRole:              e.CreatedByRole,
        AmRecipientName:            e.AmRecipientName,
        DeliveryContactName:        e.DeliveryContactName,
        OrderStatus:                e.OrderStatus,
        OrderStatusCode:            e.OrderStatusCode,
        CollateralTypeLabel:        e.CollateralTypeLabel,
        CombinedCollateralTypeLabel: e.CombinedCollateralTypeLabel,
        DocumentationReviewStatus:  e.DocumentationReviewStatus,
        PaymentConsentStatus:       e.PaymentConsentStatus,
        AppraiserName:              e.AppraiserName,
        AppraiserRating:            e.AppraiserRating,
        EsgCertificate:             e.EsgCertificate,
        AppraisalFee:               e.AppraisalFee,
        CollateralStatus:           e.CollateralStatus,
        CoApprovalComment:          e.CoApprovalComment,
        AcceptedByCAName:           e.AcceptedByCAName,
        CoApprovedByUserId:         e.CoApprovedByUserId,
        RequestReceivedAt:          e.RequestReceivedAt,
        RequestSentAt:              e.RequestSentAt,
        SubmittedAt:                e.SubmittedAt,
        OrderSentToAppraiserAt:     e.OrderSentToAppraiserAt,
        AppraiserVisitDate:         e.AppraiserVisitDate,
        SignedDocumentsReceivedAt:  e.SignedDocumentsReceivedAt,
        DocumentationSupplementAt:  e.DocumentationSupplementAt,
        AppraisalDeliveredToCoAt:   e.AppraisalDeliveredToCoAt,
        CorrectionRequestedAt:      e.CorrectionRequestedAt,
        CorrectedAppraisalReceivedAt: e.CorrectedAppraisalReceivedAt,
        CoApprovedAt:               e.CoApprovedAt,
        ReadyForProcedureAt:        e.ReadyForProcedureAt,
        OriginalReceivedAt:         e.OriginalReceivedAt,
        InvoiceSentDate:            e.InvoiceSentDate,
        InvoiceReceivedDate:        e.InvoiceReceivedDate,
        GeneratedAt:                e.GeneratedAt,

        // 7 vremenskih kolona
        DaneProdajaCA:          DaysBetween(e.RequestReceivedAt, e.SubmittedAt),
        DaneCAVjestak:          DaysBetween(e.SubmittedAt, e.OrderSentToAppraiserAt),
        DaneVjestavCO:          DaysBetween(e.OrderSentToAppraiserAt, e.AppraisalDeliveredToCoAt),
        DaneCOFinalna:          DaysBetween(e.AppraisalDeliveredToCoAt, e.ReadyForProcedureAt),
        DaneFinalnaOriginal:    DaysBetween(e.ReadyForProcedureAt, e.OriginalReceivedAt),
        DaneGrandTotal:         DaysBetween(e.RequestReceivedAt, e.ReadyForProcedureAt),
        DaneGrandTotalProdaja:  DaysBetween(e.SubmittedAt, e.ReadyForProcedureAt)
    );

    /// <summary>Razlika u danima (cijeli broj, â‰¥0). Null ako je bilo koji datum null.</summary>
    public static int? DaysBetween(DateTime? from, DateTime? to)
    {
        if (from is null || to is null) return null;
        var days = (int)(to.Value.Date - from.Value.Date).TotalDays;
        return days < 0 ? null : days;
    }

    // â”€â”€ Excel builder â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    private static MemoryStream BuildXlsx(List<OrdersTimeReportRowDto> rows)
    {
        var ms = new MemoryStream();
        using (var wb = new XLWorkbook())
        {
            var ws = wb.AddWorksheet("Pregled narudžbi");

            // Zaglavlje
            var headers = new[]
            {
                "ID narudžbe", "Broj narudžbe", "Broj protokola", "Godina", "Sekvenca",
                "Naziv", "Klijent", "Tip klijenta", "ID klijenta", "Grad", "Poslovnica",
                "Adresa poslovnice", "Adresa imovine", "Kontakt", "Telefon",
                "Kreirao", "Rola", "AM primalac", "Kontakt dostave",
                "Status", "Kod statusa", "Tip kolaterala", "Kombinirani tip kolaterala",
                "Status pregleda dok.", "Status saglasnosti",
                "Vještak", "Ocjena vještaka", "ESG certifikat", "Naknada (KM)", "Status kolaterala",
                "Komentar CO", "Prihvatio CA", "Odobrio CO (ID)",
                "Prijem od Prodaje (K)", "Zahtjev poslan (RequestSentAt)", "Prijem od Prodaje/CA (P)",
                "Narudžba vještaku (V)", "Datum obilaska", "Potpisi primljeni",
                "Dopuna dokumentacije", "Dostava CO (Y)", "Zatražena dorada",
                "Primljena korigovana", "Odobreno za print (AB)", "Generisano",
                "Original primljen (AC)", "Faktura poslana", "Faktura primljena",
                // 7 vremenskih
                "1. Prodajaâ†’CA (dani)", "2. CAâ†’Vještak (dani)", "3. Vještakâ†’CO (dani)",
                "4. COâ†’Finalna (dani)", "5. Finalnaâ†’Original (dani)",
                "6. Grand total (dani)", "7. Grand total Prodaja (dani)"
            };

            for (var c = 0; c < headers.Length; c++)
            {
                var cell = ws.Cell(1, c + 1);
                cell.Value = headers[c];
                cell.Style.Font.Bold = true;
                cell.Style.Fill.BackgroundColor = XLColor.LightBlue;
            }

            // Redovi
            for (var r = 0; r < rows.Count; r++)
            {
                var row = rows[r];
                var rowIdx = r + 2;
                var col = 1;

                ws.Cell(rowIdx, col++).Value = row.OrderId;
                ws.Cell(rowIdx, col++).Value = row.OrderNumber;
                ws.Cell(rowIdx, col++).Value = row.ProtocolNumber;
                ws.Cell(rowIdx, col++).Value = row.ProtocolYear;
                ws.Cell(rowIdx, col++).Value = row.ProtocolSequence;
                ws.Cell(rowIdx, col++).Value = row.OrderTitle;
                ws.Cell(rowIdx, col++).Value = row.ClientName;
                ws.Cell(rowIdx, col++).Value = row.ClientType ?? "";
                ws.Cell(rowIdx, col++).Value = row.ClientIdentifier ?? "";
                ws.Cell(rowIdx, col++).Value = row.City ?? "";
                ws.Cell(rowIdx, col++).Value = row.Branch ?? "";
                ws.Cell(rowIdx, col++).Value = row.BranchAddress ?? "";
                ws.Cell(rowIdx, col++).Value = row.PropertyAddress ?? "";
                ws.Cell(rowIdx, col++).Value = row.ContactName ?? "";
                ws.Cell(rowIdx, col++).Value = row.ContactPhone ?? "";
                ws.Cell(rowIdx, col++).Value = row.CreatedByName ?? "";
                ws.Cell(rowIdx, col++).Value = row.CreatedByRole ?? "";
                ws.Cell(rowIdx, col++).Value = row.AmRecipientName ?? "";
                ws.Cell(rowIdx, col++).Value = row.DeliveryContactName ?? "";
                ws.Cell(rowIdx, col++).Value = row.OrderStatus;
                ws.Cell(rowIdx, col++).Value = row.OrderStatusCode;
                ws.Cell(rowIdx, col++).Value = row.CollateralTypeLabel ?? "";
                ws.Cell(rowIdx, col++).Value = row.CombinedCollateralTypeLabel ?? "";
                ws.Cell(rowIdx, col++).Value = row.DocumentationReviewStatus ?? "";
                ws.Cell(rowIdx, col++).Value = row.PaymentConsentStatus ?? "";
                ws.Cell(rowIdx, col++).Value = row.AppraiserName ?? "";
                SetNullableInt(ws.Cell(rowIdx, col++), row.AppraiserRating);
                ws.Cell(rowIdx, col++).Value = row.EsgCertificate ?? "";
                SetNullableDecimal(ws.Cell(rowIdx, col++), row.AppraisalFee);
                ws.Cell(rowIdx, col++).Value = row.CollateralStatus ?? "";
                ws.Cell(rowIdx, col++).Value = row.CoApprovalComment ?? "";
                ws.Cell(rowIdx, col++).Value = row.AcceptedByCAName ?? "";
                ws.Cell(rowIdx, col++).Value = row.CoApprovedByUserId ?? "";
                SetNullableDate(ws.Cell(rowIdx, col++), row.RequestReceivedAt);
                SetNullableDate(ws.Cell(rowIdx, col++), row.RequestSentAt);
                SetNullableDate(ws.Cell(rowIdx, col++), row.SubmittedAt);
                SetNullableDate(ws.Cell(rowIdx, col++), row.OrderSentToAppraiserAt);
                SetNullableDate(ws.Cell(rowIdx, col++), row.AppraiserVisitDate);
                SetNullableDate(ws.Cell(rowIdx, col++), row.SignedDocumentsReceivedAt);
                SetNullableDate(ws.Cell(rowIdx, col++), row.DocumentationSupplementAt);
                SetNullableDate(ws.Cell(rowIdx, col++), row.AppraisalDeliveredToCoAt);
                SetNullableDate(ws.Cell(rowIdx, col++), row.CorrectionRequestedAt);
                SetNullableDate(ws.Cell(rowIdx, col++), row.CorrectedAppraisalReceivedAt);
                SetNullableDate(ws.Cell(rowIdx, col++), row.CoApprovedAt);
                SetNullableDate(ws.Cell(rowIdx, col++), row.ReadyForProcedureAt);
                SetNullableDate(ws.Cell(rowIdx, col++), row.GeneratedAt);
                SetNullableDate(ws.Cell(rowIdx, col++), row.OriginalReceivedAt);
                SetNullableDate(ws.Cell(rowIdx, col++), row.InvoiceSentDate);
                SetNullableDate(ws.Cell(rowIdx, col++), row.InvoiceReceivedDate);

                // 7 vremenskih kolona — žuta pozadina
                SetTimeDays(ws.Cell(rowIdx, col++), row.DaneProdajaCA);
                SetTimeDays(ws.Cell(rowIdx, col++), row.DaneCAVjestak);
                SetTimeDays(ws.Cell(rowIdx, col++), row.DaneVjestavCO);
                SetTimeDays(ws.Cell(rowIdx, col++), row.DaneCOFinalna);
                SetTimeDays(ws.Cell(rowIdx, col++), row.DaneFinalnaOriginal);
                SetTimeDays(ws.Cell(rowIdx, col++), row.DaneGrandTotal);
                SetTimeDays(ws.Cell(rowIdx, col++), row.DaneGrandTotalProdaja);
            }

            ws.Columns().AdjustToContents();
            wb.SaveAs(ms);
        }

        ms.Position = 0;
        return ms;
    }

    private static void SetNullableDate(IXLCell cell, DateTime? value)
    {
        if (value.HasValue)
            cell.Value = value.Value.ToString("dd.MM.yyyy");
    }

    private static void SetNullableInt(IXLCell cell, int? value)
    {
        if (value.HasValue) cell.Value = value.Value;
    }

    private static void SetNullableDecimal(IXLCell cell, decimal? value)
    {
        if (value.HasValue) cell.Value = (double)value.Value;
    }

    private static void SetTimeDays(IXLCell cell, int? days)
    {
        if (days.HasValue)
        {
            cell.Value = days.Value;
            cell.Style.Fill.BackgroundColor = XLColor.LightYellow;
        }
    }
}
