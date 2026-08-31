﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Reports;
using RBBH.CollateralAppraisal.Application.Reports.Dtos;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Reports;

/// <summary>
/// Generiše izvještaje koncentracije vještaka (US 9) i pregleda narudžbi s vremenima (US 10),
/// ćitajući podatke iz narudžbi (Protokol narudžbi). Excel se gradi preko <see cref="IExcelReportBuilder"/>.
/// </summary>
[ExcludeFromCodeCoverage]
public sealed class ReportService : IReportService
{
    private const string XlsxContentType =
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";

    private readonly ApplicationDbContext _db;
    private readonly IExcelReportBuilder _excel;

    public ReportService(ApplicationDbContext db, IExcelReportBuilder excel)
    {
        _db = db;
        _excel = excel;
    }

    // â”€â”€ US 9: Koncentracija vještaka (5 opcija) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    public async Task<ReportFile> GenerateConcentrationAsync(
        int option, DateTime? asOfDate, CancellationToken ct = default)
    {
        if (option is < 1 or > 5)
            throw new ValidationException("option", "Opcija izvještaja koncentracije mora biti vrijednost od 1 do 5.");

        var asOf      = asOfDate?.Date ?? DateTime.UtcNow.Date;
        var asOfEnd   = asOf.AddDays(1);          // ukljuć. cijeli zadati dan
        var monthFrom = asOf.AddMonths(-1);

        var raw = await _db.AppraisalOrders.AsNoTracking()
            .Where(o =>
                o.Status == AppraisalOrderStatus.COApproved ||
                o.Status == AppraisalOrderStatus.ReadyForProcedure ||
                o.Status == AppraisalOrderStatus.Completed)
            .Select(o => new
            {
                o.AppraiserId,
                City = o.PropertyCity ?? o.City,
                o.CollateralTypeId,
                o.CombinedCollateralTypeId,
                o.ReadyForProcedureAt,
                o.OriginalReceivedAt,
                o.UpdatedAt,
                o.CreatedAt
            })
            .ToListAsync(ct);

        var items = raw.Select(o => new ConcentrationItem(
                o.AppraiserId,
                string.IsNullOrWhiteSpace(o.City) ? "—" : o.City!,
                o.CombinedCollateralTypeId ?? o.CollateralTypeId,
                o.ReadyForProcedureAt ?? o.OriginalReceivedAt ?? o.UpdatedAt ?? o.CreatedAt))
            .Where(i => i.CompletedAt < asOfEnd)
            .ToList();

        var appraiserNames = await ResolveAppraiserNamesAsync(
            items.Where(i => i.AppraiserId.HasValue).Select(i => i.AppraiserId!.Value), ct);
        var collateralLabels = await ResolveCollateralLabelsAsync(
            items.Where(i => i.TypeId.HasValue).Select(i => i.TypeId!.Value), ct);

        string Appraiser(int? id) =>
            id.HasValue ? appraiserNames.GetValueOrDefault(id.Value, $"Vještak #{id}") : "—";
        string Type(int? id) =>
            id.HasValue ? collateralLabels.GetValueOrDefault(id.Value, $"Tip #{id}") : "—";

        string sheet;
        List<string> headers;
        List<IReadOnlyList<object?>> rows;

        switch (option)
        {
            case 2:
                sheet   = "Procjenitelj";
                headers = ["Procjenitelj", "Broj završenih narudžbi"];
                rows    = items
                    .GroupBy(i => Appraiser(i.AppraiserId))
                    .OrderByDescending(g => g.Count())
                    .Select(g => Row(g.Key, g.Count()))
                    .ToList();
                break;

            case 3:
                sheet   = "Tip kolaterala";
                headers = ["Tip kolaterala", "Broj završenih narudžbi"];
                rows    = items
                    .GroupBy(i => Type(i.TypeId))
                    .OrderByDescending(g => g.Count())
                    .Select(g => Row(g.Key, g.Count()))
                    .ToList();
                break;

            case 4:
                sheet   = "Grad + Procjenitelj";
                headers = ["Grad", "Procjenitelj", "Ukupan broj narudžbi"];
                rows    = items
                    .GroupBy(i => new { i.City, Appraiser = Appraiser(i.AppraiserId) })
                    .OrderBy(g => g.Key.City).ThenByDescending(g => g.Count())
                    .Select(g => Row(g.Key.City, g.Key.Appraiser, g.Count()))
                    .ToList();
                break;

            case 5:
                sheet   = "Zadnjih mjesec dana";
                headers = ["Grad", "Procjenitelj", "Broj narudžbi (zadnjih mjesec dana)"];
                rows    = items
                    .Where(i => i.CompletedAt >= monthFrom)
                    .GroupBy(i => new { i.City, Appraiser = Appraiser(i.AppraiserId) })
                    .OrderBy(g => g.Key.City).ThenByDescending(g => g.Count())
                    .Select(g => Row(g.Key.City, g.Key.Appraiser, g.Count()))
                    .ToList();
                break;

            default: // opcija 1
                sheet   = "Grad";
                headers = ["Grad", "Broj završenih narudžbi"];
                rows    = items
                    .GroupBy(i => i.City)
                    .OrderByDescending(g => g.Count())
                    .Select(g => Row(g.Key, g.Count()))
                    .ToList();
                break;
        }

        var bytes = _excel.BuildSingleSheet(sheet, headers, rows);
        return new ReportFile(bytes, $"koncentracija-vjestaka-{asOf:yyyyMMdd}.xlsx", XlsxContentType);
    }

    // â”€â”€ US 10: Pregled svih narudžbi + 7 vremenskih kolona â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    public async Task<ReportFile> GenerateOrdersTimeReportAsync(
        DateTime? endDate, CancellationToken ct = default)
    {
        var endExclusive = endDate?.Date.AddDays(1);

        var raw = await _db.AppraisalOrders.AsNoTracking()
            .OrderBy(o => o.CreatedAt)
            .Select(o => new OrderTimeRow(
                o.OrderNumber,
                o.ClientName,
                o.ClientType,
                o.CollateralTypeId,
                o.CombinedCollateralTypeId,
                o.PropertyCity ?? o.City,
                o.AppraiserId,
                o.Status,
                o.AppraisalFee,
                o.RequestReceivedAt,        // K
                o.SubmittedAt,              // P
                o.OrderSentToAppraiserAt,   // V
                o.AppraisalDeliveredToCoAt, // Y
                o.ReadyForProcedureAt,      // AB
                o.OriginalReceivedAt,       // AC
                o.CreatedAt))
            .ToListAsync(ct);

        if (endExclusive is { } end)
            raw = raw.Where(o => (o.RequestReceivedAt ?? o.CreatedAt) < end).ToList();

        var appraiserNames = await ResolveAppraiserNamesAsync(
            raw.Where(o => o.AppraiserId.HasValue).Select(o => o.AppraiserId!.Value), ct);
        var collateralLabels = await ResolveCollateralLabelsAsync(
            raw.SelectMany(o => new[] { o.CollateralTypeId, o.CombinedCollateralTypeId })
               .Where(id => id.HasValue).Select(id => id!.Value), ct);

        var headers = new List<string>
        {
            "Broj narudžbe", "Klijent", "Segment", "Tip kolaterala", "Tip kolaterala kombinovano",
            "Grad", "Procjenitelj", "Status", "Naknada (KM)",
            "Prijem od klijenta (K)", "Prijem od Prodaje (P)", "Narudžba vještaku (V)",
            "Dostava CO (Y)", "Finalna procjena (AB)", "Original u poslovnici (AC)",
            "1) Prodajaâ†’CA (dana)", "2) CAâ†’Vještak (dana)", "3) Vještakâ†’CO (dana)",
            "4) COâ†’Finalna (dana)", "5) Finalnaâ†’Original (dana)",
            "6) Grand total (dana)", "7) Grand total Prodaja (dana)"
        };

        var rows = raw.Select(o => (IReadOnlyList<object?>)new object?[]
        {
            o.OrderNumber,
            o.ClientName,
            o.ClientType,
            o.CollateralTypeId.HasValue        ? collateralLabels.GetValueOrDefault(o.CollateralTypeId.Value)        : null,
            o.CombinedCollateralTypeId.HasValue ? collateralLabels.GetValueOrDefault(o.CombinedCollateralTypeId.Value) : null,
            o.City,
            o.AppraiserId.HasValue ? appraiserNames.GetValueOrDefault(o.AppraiserId.Value) : null,
            o.Status.ToString(),
            o.AppraisalFee,
            FormatDate(o.RequestReceivedAt),
            FormatDate(o.SubmittedAt),
            FormatDate(o.OrderSentToAppraiserAt),
            FormatDate(o.AppraisalDeliveredToCoAt),
            FormatDate(o.ReadyForProcedureAt),
            FormatDate(o.OriginalReceivedAt),
            DaysBetween(o.RequestReceivedAt,        o.SubmittedAt),              // 1
            DaysBetween(o.SubmittedAt,              o.OrderSentToAppraiserAt),   // 2
            DaysBetween(o.OrderSentToAppraiserAt,   o.AppraisalDeliveredToCoAt), // 3
            DaysBetween(o.AppraisalDeliveredToCoAt, o.ReadyForProcedureAt),      // 4
            DaysBetween(o.ReadyForProcedureAt,      o.OriginalReceivedAt),       // 5
            DaysBetween(o.RequestReceivedAt,        o.ReadyForProcedureAt),      // 6
            DaysBetween(o.SubmittedAt,              o.ReadyForProcedureAt)       // 7
        }).ToList();

        var bytes = _excel.BuildSingleSheet("Pregled narudžbi", headers, rows);
        var stamp = endDate?.Date ?? DateTime.UtcNow.Date;
        return new ReportFile(bytes, $"pregled-narudzbi-{stamp:yyyyMMdd}.xlsx", XlsxContentType);
    }

    // ── Reminder narudžbe (DPNPN-141) ─────────────────────────────────────────

    public async Task<IReadOnlyList<ReminderOrderDto>> GetReminderOrdersAsync(CancellationToken ct = default)
    {
        var raw = await _db.AppraisalOrders.AsNoTracking()
            .Where(o => o.OrderSentToAppraiserAt != null)
            .OrderBy(o => o.OrderSentToAppraiserAt)
            .Select(o => new
            {
                o.Id,
                o.OrderNumber,
                o.ClientName,
                o.Status,
                o.AppraiserId,
                o.OrderSentToAppraiserAt,
                o.AppraisalDeliveredToCoAt
            })
            .ToListAsync(ct);

        var appraiserNames = await ResolveAppraiserNamesAsync(
            raw.Where(o => o.AppraiserId.HasValue).Select(o => o.AppraiserId!.Value), ct);

        var now = DateTime.UtcNow;
        return raw.Select(o => new ReminderOrderDto(
            OrderId:                  o.Id,
            OrderNumber:              o.OrderNumber,
            ClientName:               o.ClientName,
            City:                     string.Empty,
            OrderStatus:              o.Status.ToString(),
            StatusLabel:              o.Status.ToString(),
            AppraiserId:              o.AppraiserId,
            AppraiserName:            o.AppraiserId.HasValue ? appraiserNames.GetValueOrDefault(o.AppraiserId.Value) : null,
            AppraiserEmail:           null,
            OrderSentToAppraiserAt:   o.OrderSentToAppraiserAt,
            AppraisalDeliveredToCoAt: o.AppraisalDeliveredToCoAt,
            BusinessDaysOverdue:      o.OrderSentToAppraiserAt.HasValue
                ? Application.Common.BusinessDaysHelper.BusinessDaysBetween(o.OrderSentToAppraiserAt.Value, now)
                : 0))
            .ToList();
    }

    // ── Helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    private static IReadOnlyList<object?> Row(params object?[] cells) => cells;

    private static object? FormatDate(DateTime? d) => d?.ToString("dd.MM.yyyy");

    /// <summary>Broj dana izmeÄ‘u dva datuma; null ako bilo koji nedostaje; 0 ako bi rezultat bio negativan.</summary>
    private static int? DaysBetween(DateTime? from, DateTime? to)
    {
        if (from is null || to is null) return null;
        var days = (to.Value - from.Value).TotalDays;
        return days < 0 ? 0 : (int)Math.Round(days, MidpointRounding.AwayFromZero);
    }

    private async Task<Dictionary<int, string>> ResolveAppraiserNamesAsync(
        IEnumerable<int> ids, CancellationToken ct)
    {
        var idList = ids.Distinct().ToList();
        if (idList.Count == 0) return new Dictionary<int, string>();

        return await _db.Appraisers.AsNoTracking()
            .Where(a => idList.Contains(a.Id))
            .ToDictionaryAsync(a => a.Id, a => a.Name, ct);
    }

    private async Task<Dictionary<int, string>> ResolveCollateralLabelsAsync(
        IEnumerable<int> ids, CancellationToken ct)
    {
        var idList = ids.Distinct().ToList();
        if (idList.Count == 0) return new Dictionary<int, string>();

        return await _db.CodebookValues.AsNoTracking()
            .Where(v => idList.Contains(v.Id))
            .ToDictionaryAsync(v => v.Id, v => v.Label, ct);
    }

    private sealed record ConcentrationItem(int? AppraiserId, string City, int? TypeId, DateTime CompletedAt);

    private sealed record OrderTimeRow(
        string OrderNumber,
        string ClientName,
        string? ClientType,
        int? CollateralTypeId,
        int? CombinedCollateralTypeId,
        string? City,
        int? AppraiserId,
        AppraisalOrderStatus Status,
        decimal? AppraisalFee,
        DateTime? RequestReceivedAt,
        DateTime? SubmittedAt,
        DateTime? OrderSentToAppraiserAt,
        DateTime? AppraisalDeliveredToCoAt,
        DateTime? ReadyForProcedureAt,
        DateTime? OriginalReceivedAt,
        DateTime CreatedAt);
}
