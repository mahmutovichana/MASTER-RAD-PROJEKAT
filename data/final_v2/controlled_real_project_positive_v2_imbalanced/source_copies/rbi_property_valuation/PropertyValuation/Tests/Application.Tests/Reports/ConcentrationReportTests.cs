#pragma warning disable CS0618
using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Reports;
using RBBH.CollateralAppraisal.Domain.Appraisers;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using RBBH.CollateralAppraisal.Infrastructure.Reports;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Reports;

public sealed class ConcentrationReportTests : IDisposable
{
    private readonly ApplicationDbContext _db;
    private readonly CapturingExcelReportBuilder _excel = new();
    private readonly ReportService _sut;

    public ConcentrationReportTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;

        _db = new ApplicationDbContext(options);
        _sut = new ReportService(_db, _excel);
    }

    [Fact]
    public async Task GenerateConcentrationAsync_Option3_KoristiKombinovaniTipKadPostoji()
    {
        var stan = CodebookValue.Create("tipovi_kolaterala", "STAN", "Stan", null, 1, "test");
        var poslovni = CodebookValue.Create("tipovi_kolaterala", "POSLOVNI", "Poslovni prostor", null, 2, "test");
        _db.CodebookValues.AddRange(stan, poslovni);
        await _db.SaveChangesAsync();

        var combinedOrder = CreateOrder("Sarajevo", collateralTypeId: stan.Id, combinedCollateralTypeId: poslovni.Id);
        MarkReadyForProcedure(combinedOrder, new DateTime(2026, 6, 10));

        var baseTypeOrder = CreateOrder("Sarajevo", collateralTypeId: stan.Id, combinedCollateralTypeId: null);
        MarkReadyForProcedure(baseTypeOrder, new DateTime(2026, 6, 11));

        _db.AppraisalOrders.AddRange(combinedOrder, baseTypeOrder);
        await _db.SaveChangesAsync();

        await _sut.GenerateConcentrationAsync(3, new DateTime(2026, 6, 30));

        Assert.Equal("Tip kolaterala", _excel.SheetName);
        Assert.Contains(_excel.Rows, r => (string?)r[0] == "Poslovni prostor" && (int)r[1]! == 1);
        Assert.Contains(_excel.Rows, r => (string?)r[0] == "Stan" && (int)r[1]! == 1);
    }

    [Fact]
    public async Task GenerateConcentrationAsync_Option5_UzimaSamoZadnjihMjesecDana()
    {
        var appraiser = Appraiser.Create(
            "Procjenitelj A",
            "Sarajevo",
            AppraiserLegalForm.Individual,
            "procjenitelj@test.ba",
            null,
            null);
        _db.Appraisers.Add(appraiser);
        await _db.SaveChangesAsync();

        var included = CreateOrder("Sarajevo", appraiser.Id);
        MarkReadyForProcedure(included, new DateTime(2026, 6, 10));

        var tooOld = CreateOrder("Sarajevo", appraiser.Id);
        MarkReadyForProcedure(tooOld, new DateTime(2026, 5, 20));

        _db.AppraisalOrders.AddRange(included, tooOld);
        await _db.SaveChangesAsync();

        await _sut.GenerateConcentrationAsync(5, new DateTime(2026, 6, 27));

        var row = Assert.Single(_excel.Rows);
        Assert.Equal("Sarajevo", row[0]);
        Assert.Equal("Procjenitelj A", row[1]);
        Assert.Equal(1, row[2]);
    }

    [Fact]
    public async Task GenerateConcentrationAsync_NevazecaOpcija_BacaValidacijskuGresku()
    {
        await Assert.ThrowsAsync<ValidationException>(
            () => _sut.GenerateConcentrationAsync(9, new DateTime(2026, 6, 30)));
    }

    private static AppraisalOrder CreateOrder(
        string city,
        int? appraiserId = null,
        int? collateralTypeId = null,
        int? combinedCollateralTypeId = null)
    {
        var order = AppraisalOrder.Create(
            orderNumber: $"PN-{Guid.NewGuid():N}"[..12],
            title: "Procjena nekretnine",
            clientName: "Test Klijent",
            clientType: "FL",
            clientIdentifier: "0101990170000",
            contactName: "Test Klijent",
            contactPhone: "061123456",
            contactEmail: "test@example.ba",
            city: city,
            branch: "Sarajevo",
            branchAddress: "Adresa 1",
            propertyAddress: "Nekretnina 1",
            collateralTypeId: collateralTypeId,
            combinedCollateralTypeId: combinedCollateralTypeId,
            createdByUserId: "user-am",
            createdByRole: "AM",
            createdByName: "AM Test",
            deliveryContactName: null,
            amRecipientName: null,
            propertyCity: city);

        if (appraiserId.HasValue)
        {
            // State machine: Draft → ... → DocumentationApproved → AppraiserSelected
            // ChangeStatus zaobilazi state machine (test helper — samo postavlja status)
            order.ChangeStatus(AppraisalOrderStatus.DocumentationApproved, DateTime.UtcNow);
            order.SelectAppraiser(appraiserId.Value, DateTime.UtcNow);
        }

        return order;
    }

    private static void MarkReadyForProcedure(AppraisalOrder order, DateTime completedAt)
    {
        order.ChangeStatus(AppraisalOrderStatus.ReadyForProcedure, completedAt);
        SetProperty(order, nameof(AppraisalOrder.ReadyForProcedureAt), completedAt);
    }

    private static void SetProperty<T>(object target, string propertyName, T value)
    {
        var property = target.GetType().GetProperty(propertyName)
            ?? throw new InvalidOperationException($"Property {propertyName} nije pronađen.");
        property.SetValue(target, value);
    }

    public void Dispose() => _db.Dispose();

    private sealed class CapturingExcelReportBuilder : IExcelReportBuilder
    {
        public string? SheetName { get; private set; }
        public IReadOnlyList<string> Headers { get; private set; } = [];
        public List<IReadOnlyList<object?>> Rows { get; } = [];

        public byte[] BuildSingleSheet(
            string sheetName,
            IReadOnlyList<string> headers,
            IEnumerable<IReadOnlyList<object?>> rows)
        {
            SheetName = sheetName;
            Headers = headers;
            Rows.Clear();
            Rows.AddRange(rows.Select(r => r.ToArray()));
            return [1, 2, 3];
        }
    }
}
