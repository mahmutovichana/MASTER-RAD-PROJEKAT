using NSubstitute;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Infrastructure.Reports;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Reports;

public sealed class OrdersTimeReportTests
{
    // ── DaysBetween unit testovi ──────────────────────────────────────────────

    [Fact]
    public void DaysBetween_ObaDatetimePopunjena_VracaTacneBrojDana()
    {
        var from = new DateTime(2025, 1, 1);
        var to   = new DateTime(2025, 1, 11);
        Assert.Equal(10, OrdersTimeReportService.DaysBetween(from, to));
    }

    [Fact]
    public void DaysBetween_IstiDan_VracaNula()
    {
        var d = new DateTime(2025, 3, 15);
        Assert.Equal(0, OrdersTimeReportService.DaysBetween(d, d));
    }

    [Fact]
    public void DaysBetween_FromNull_VracaNull()
    {
        Assert.Null(OrdersTimeReportService.DaysBetween(null, new DateTime(2025, 1, 10)));
    }

    [Fact]
    public void DaysBetween_ToNull_VracaNull()
    {
        Assert.Null(OrdersTimeReportService.DaysBetween(new DateTime(2025, 1, 1), null));
    }

    [Fact]
    public void DaysBetween_ObaNull_VracaNull()
    {
        Assert.Null(OrdersTimeReportService.DaysBetween(null, null));
    }

    [Fact]
    public void DaysBetween_ToManjeOdFrom_VracaNull()
    {
        // Negativan interval → prazna kolona (ne prikazujemo negativno)
        var from = new DateTime(2025, 5, 10);
        var to   = new DateTime(2025, 5, 1);
        Assert.Null(OrdersTimeReportService.DaysBetween(from, to));
    }

    // ── MapRow: 7 vremenskih kolona ──────────────────────────────────────────

    [Fact]
    public void MapRow_GrandTotal_IspravnoRacuna()
    {
        var entry = BuildEntry(
            requestReceivedAt:   new DateTime(2025, 1, 1),
            readyForProcedureAt: new DateTime(2025, 1, 21));

        var row = OrdersTimeReportService.MapRow(entry);

        Assert.Equal(20, row.DaneGrandTotal);
    }

    [Fact]
    public void MapRow_ProdajaCA_IspravnoRacuna()
    {
        var entry = BuildEntry(
            requestReceivedAt: new DateTime(2025, 2, 1),
            submittedAt:       new DateTime(2025, 2, 6));

        var row = OrdersTimeReportService.MapRow(entry);

        Assert.Equal(5, row.DaneProdajaCA);
    }

    [Fact]
    public void MapRow_NullDatumZnacaziNullKolona()
    {
        var entry = BuildEntry(requestReceivedAt: null, submittedAt: new DateTime(2025, 2, 6));

        var row = OrdersTimeReportService.MapRow(entry);

        Assert.Null(row.DaneProdajaCA);
        Assert.Null(row.DaneGrandTotal);
    }

    [Fact]
    public void MapRow_GrandTotalProdaja_IspravnoRacuna()
    {
        var entry = BuildEntry(
            submittedAt:         new DateTime(2025, 3, 1),
            readyForProcedureAt: new DateTime(2025, 3, 16));

        var row = OrdersTimeReportService.MapRow(entry);

        Assert.Equal(15, row.DaneGrandTotalProdaja);
    }

    [Fact]
    public void MapRow_CAVjestak_IspravnoRacuna()
    {
        var entry = BuildEntry(
            submittedAt:            new DateTime(2025, 4, 1),
            orderSentToAppraiserAt: new DateTime(2025, 4, 4));

        var row = OrdersTimeReportService.MapRow(entry);

        Assert.Equal(3, row.DaneCAVjestak);
    }

    [Fact]
    public void MapRow_SviDatumiNull_SveVremenskeKoloneNull()
    {
        var entry = BuildEntry();
        var row = OrdersTimeReportService.MapRow(entry);

        Assert.Null(row.DaneProdajaCA);
        Assert.Null(row.DaneCAVjestak);
        Assert.Null(row.DaneVjestavCO);
        Assert.Null(row.DaneCOFinalna);
        Assert.Null(row.DaneFinalnaOriginal);
        Assert.Null(row.DaneGrandTotal);
        Assert.Null(row.DaneGrandTotalProdaja);
    }

    // ── GetReportAsync: endDate filter ───────────────────────────────────────

    [Fact]
    public async Task GetReportAsync_EndDateFilter_IsključujeNarudžbeNakonDatuma()
    {
        var protocol = Substitute.For<IProtocolService>();
        var entries = new List<ProtocolEntryDto>
        {
            BuildEntry(requestReceivedAt: new DateTime(2025, 1, 10)),  // treba biti uključena
            BuildEntry(requestReceivedAt: new DateTime(2025, 1, 20)),  // treba biti isključena
        };
        protocol.GetProtocolListAsync(Arg.Any<int>(), Arg.Any<int>(), Arg.Any<CancellationToken>())
            .Returns(new PagedResult<ProtocolEntryDto> { Items = entries, TotalCount = 2, Page = 1, PageSize = 10_000 });

        var sut = new OrdersTimeReportService(protocol);
        var result = await sut.GetReportAsync(endDate: new DateTime(2025, 1, 15));

        Assert.Single(result);
        Assert.Equal(new DateTime(2025, 1, 10), result[0].RequestReceivedAt);
    }

    [Fact]
    public async Task GetReportAsync_BezEndDate_VracaSveNarudzbe()
    {
        var protocol = Substitute.For<IProtocolService>();
        var entries = new List<ProtocolEntryDto>
        {
            BuildEntry(requestReceivedAt: new DateTime(2024, 6, 1)),
            BuildEntry(requestReceivedAt: new DateTime(2025, 6, 1)),
            BuildEntry(requestReceivedAt: null),
        };
        protocol.GetProtocolListAsync(Arg.Any<int>(), Arg.Any<int>(), Arg.Any<CancellationToken>())
            .Returns(new PagedResult<ProtocolEntryDto> { Items = entries, TotalCount = 3, Page = 1, PageSize = 10_000 });

        var sut = new OrdersTimeReportService(protocol);
        var result = await sut.GetReportAsync();

        Assert.Equal(3, result.Count);
    }

    // ── Helper ────────────────────────────────────────────────────────────────

    private static ProtocolEntryDto BuildEntry(
        DateTime? requestReceivedAt       = null,
        DateTime? submittedAt             = null,
        DateTime? orderSentToAppraiserAt  = null,
        DateTime? appraisalDeliveredToCoAt = null,
        DateTime? readyForProcedureAt     = null,
        DateTime? originalReceivedAt      = null)
        => new(
            Id:                    1,
            OrderId:               1,
            OrderNumber:           "NP-TEST-1",
            OrderTitle:            "Test narudžba",
            ProtocolNumber:        "PR-001",
            ProtocolYear:          2025,
            ProtocolSequence:      1,
            Status:                "Active",
            GeneratedAt:           DateTime.UtcNow,
            GeneratedByUserId:     "user-1",
            ClientName:            "Test Klijent",
            City:                  "Sarajevo",
            Branch:                null,
            OrderStatus:           "Aktivna",
            OrderStatusCode:       100,
            CollateralTypeLabel:   null,
            CombinedCollateralTypeLabel: null,
            ClientType:            null,
            ClientIdentifier:      null,
            ContactName:           null,
            ContactPhone:          null,
            PropertyAddress:       null,
            BranchAddress:         null,
            CreatedByName:         null,
            CreatedByRole:         null,
            DeliveryContactName:   null,
            AmRecipientName:       null,
            RequestReceivedAt:     requestReceivedAt,
            RequestSentAt:         null,
            InvoiceSentDate:       null,
            InvoiceReceivedDate:   null,
            PaymentConsentStatus:  null,
            CoApprovalComment:     null,
            AppraiserName:         null,
            AppraiserRating:       null,
            EsgCertificate:        null,
            AppraiserVisitDate:    null,
            AppraisalFee:          null,
            CollateralStatus:      null,
            SubmittedAt:           submittedAt,
            OrderSentToAppraiserAt: orderSentToAppraiserAt,
            SignedDocumentsReceivedAt: null,
            DocumentationSupplementAt: null,
            CoApprovedAt:          null,
            AppraisalDeliveredToCoAt: appraisalDeliveredToCoAt,
            CorrectionRequestedAt: null,
            CorrectedAppraisalReceivedAt: null,
            ReadyForProcedureAt:   readyForProcedureAt,
            OriginalReceivedAt:    originalReceivedAt,
            CoApprovedByUserId:    null,
            AcceptedByCAName:      null,
            DocumentationReviewStatus: null
        );
}
