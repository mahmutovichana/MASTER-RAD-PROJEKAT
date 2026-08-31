using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Tests.Helpers;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Application.Orders.Requests;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Domain.Orders;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

/// <summary>
/// 20 testova za Prodaja segment (FL/PL) prema specifikaciji.
/// </summary>
public sealed class SalesProdajaTests : IDisposable
{
    private readonly ApplicationDbContext  _db;
    private readonly ICurrentUserService   _user;
    private readonly IAuditService         _audit;
    private readonly INotificationProvider _notify;
    private readonly AppraisalOrderService _sut;

    private int _collateralTypeId;
    private int _combinedTypeId;

    public SalesProdajaTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;

        _db     = new ApplicationDbContext(options);
        _user   = Substitute.For<ICurrentUserService>();
        _audit  = Substitute.For<IAuditService>();
        _notify = Substitute.For<INotificationProvider>();

        _user.UserId.Returns("user-am-1");
        _user.Role.Returns(AppRoles.AM);
        _user.Roles.Returns([AppRoles.AM]);
        _user.IsAuthenticated.Returns(true);

        var createSvc = new OrderCreateService(
            _db, _user, new OrderTitleGenerator(), new FakeOrderNumberGenerator(), _audit, new FakeClock());
        var submitSvc = new OrderSubmitService(
            _db, _user, _notify, _audit,
            Substitute.For<ILogger<OrderSubmitService>>(),
            Options.Create(new OrderNotificationsOptions { CaInboxEmail = "narudzbe@test.ba" }),
            Options.Create(new WorkflowSlaOptions()),
            new FakeClock());
        _sut = new AppraisalOrderService(_db, _user, _audit, createSvc, submitSvc);

        SeedCodebooks();
    }

    private void SeedCodebooks()
    {
        var collateral = CodebookValue.Create("tipovi_kolaterala", "APP_STAN", "Stan", null, 10, "seed");
        var combined   = CodebookValue.Create("kombinovani_tipovi_kolaterala", "APP_STAN_I_GARAZA", "APP-stan i garaža", null, 10, "seed");
        _db.CodebookValues.AddRange(collateral, combined);
        _db.SaveChanges();
        _collateralTypeId = collateral.Id;
        _combinedTypeId   = combined.Id;
    }

    private static readonly DateTime DefaultReceivedAt =
        new(2026, 6, 1, 9, 0, 0, DateTimeKind.Utc);

    private CreateOrderRequest FlRequest(string city = "Sarajevo") =>
        new(ClientName:               "Petar Petrović",
            ClientType:               "FL",
            ClientIdentifier:         "0101990000019",
            CollateralTypeId:         _collateralTypeId,
            CombinedCollateralTypeId: null,
            City:                     city,
            PropertyAddress:          "Ul. Mira 1",
            Branch:                   "POS_SARAJEVO_CENTAR",
            BranchAddress:            "Titova 1",
            ContactName:              "Petar Petrović",
            ContactPhone:             "061-111-222",
            ContactEmail:             "petar@test.ba",
            InternalNote:             null,
            DeliveryContactName:      "Amina Dostava",
            AmRecipientName:          "Amar Primalac",
            RequestReceivedAt:        DefaultReceivedAt);

    private CreateOrderRequest PlRequest(
        decimal? sqmCommercial  = null,
        decimal? sqmResidential = null) =>
        new(ClientName:               "Firma d.o.o.",
            ClientType:               "PL",
            ClientIdentifier:         "1506985440012",
            CollateralTypeId:         _collateralTypeId,
            CombinedCollateralTypeId: null,
            City:                     "Banja Luka",
            PropertyAddress:          "Poslovni put 10",
            Branch:                   "POS_BANJA_LUKA",
            BranchAddress:            "Veselina Masleše 6",
            ContactName:              "Amer Kontakt",
            ContactPhone:             "065-777-888",
            ContactEmail:             "amer@firma.ba",
            InternalNote:             null,
            DeliveryContactName:      "Jasna Dostava",
            AmRecipientName:          "Jasna Primalac",
            RequestReceivedAt:        DefaultReceivedAt,
            SquareMetersCommercial:   sqmCommercial,
            SquareMetersResidential:  sqmResidential);

    // ── Test 1: AM može kreirati FL narudžbu ──────────────────────────────────

    [Fact]
    public async Task T01_AM_CanCreate_FL_Order()
    {
        _user.Role.Returns(AppRoles.AM);

        var dto = await _sut.CreateAsync(FlRequest());

        Assert.NotNull(dto);
        Assert.Equal("FL",    dto.ClientType);
        Assert.Equal("Draft", dto.Status);
    }

    // ── Test 2: SM može kreirati FL narudžbu ─────────────────────────────────

    [Fact]
    public async Task T02_SM_CanCreate_FL_Order()
    {
        _user.Role.Returns(AppRoles.SM);
        _user.Roles.Returns([AppRoles.SM]);

        var dto = await _sut.CreateAsync(FlRequest());

        Assert.Equal("Draft", dto.Status);
        Assert.Equal("FL",    dto.ClientType);
    }

    // ── Test 3: Prodaja može kreirati PL narudžbu ─────────────────────────────

    [Fact]
    public async Task T03_SalesRole_CanCreate_PL_Order()
    {
        var dto = await _sut.CreateAsync(PlRequest());

        Assert.NotNull(dto);
        Assert.Equal("PL",    dto.ClientType);
        Assert.Equal("Draft", dto.Status);
    }

    // ── Test 4: PL narudžba čuva kvadrate poslovnog dijela ───────────────────

    [Fact]
    public async Task T04_PL_SquareMetersCommercial_IsPersisted()
    {
        var dto = await _sut.CreateAsync(PlRequest(sqmCommercial: 350.5m));

        Assert.Equal(350.5m, dto.SquareMetersCommercial);
        Assert.Null(dto.SquareMetersResidential);
    }

    // ── Test 5: PL narudžba čuva kvadrate stambenog dijela ───────────────────

    [Fact]
    public async Task T05_PL_SquareMetersResidential_IsPersisted()
    {
        var dto = await _sut.CreateAsync(PlRequest(sqmResidential: 120.0m));

        Assert.Equal(120.0m, dto.SquareMetersResidential);
        Assert.Null(dto.SquareMetersCommercial);
    }

    // ── Test 6: PL polja mogu biti oba postavljana istovremeno ────────────────

    [Fact]
    public async Task T06_PL_BothSquareMeters_Persisted()
    {
        var dto = await _sut.CreateAsync(PlRequest(sqmCommercial: 200m, sqmResidential: 150m));

        Assert.Equal(200m, dto.SquareMetersCommercial);
        Assert.Equal(150m, dto.SquareMetersResidential);
    }

    // ── Test 7: FL narudžba ne šalje PL kvadrate (null) ─────────────────────

    [Fact]
    public async Task T07_FL_SquareMeters_AreNull()
    {
        var dto = await _sut.CreateAsync(FlRequest());

        Assert.Null(dto.SquareMetersCommercial);
        Assert.Null(dto.SquareMetersResidential);
    }

    // ── Test 8: Negativni kvadrati odbijaju se validacijom ───────────────────

    [Fact]
    public async Task T08_PL_NegativeSquareMeters_ThrowsValidation()
    {
        var req = PlRequest(sqmCommercial: -1m);

        await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(req));
    }

    // ── Test 9: Negativni stambeni kvadrati odbijaju se validacijom ───────────

    [Fact]
    public async Task T09_PL_NegativeResidential_ThrowsValidation()
    {
        var req = PlRequest(sqmResidential: -50m);

        await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(req));
    }

    // ── Test 10: FL narudžba — naslov sadrži tip nekretnine i grad ────────────

    [Fact]
    public async Task T10_FL_Title_ContainsCollateralType_And_City()
    {
        // Sarajevo branch + grad moraju biti konzistentni (BranchCityMap)
        var dto = await _sut.CreateAsync(FlRequest(city: "Sarajevo"));

        Assert.Contains("Stan",     dto.Title);
        Assert.Contains("Sarajevo", dto.Title);
    }

    // ── Test 11: PL narudžba — naslov sadrži tip nekretnine i grad ───────────

    [Fact]
    public async Task T11_PL_Title_ContainsCollateralType_And_City()
    {
        var dto = await _sut.CreateAsync(PlRequest());

        Assert.Contains("Stan",      dto.Title);
        Assert.Contains("Banja Luka", dto.Title);
    }

    // ── Test 12: CreatedByRole se čuva za Prodaja rolu ───────────────────────

    [Fact]
    public async Task T12_CreatedByRole_IsAM()
    {
        _user.Role.Returns(AppRoles.AM);

        var dto = await _sut.CreateAsync(FlRequest());

        Assert.Equal(AppRoles.AM, dto.CreatedByRole);
    }

    // ── Test 13: Ažuriranje PL kvadrata kroz UpdateAsync ─────────────────────

    [Fact]
    public async Task T13_UpdateAsync_PL_SquareMeters_AreUpdated()
    {
        var created = await _sut.CreateAsync(PlRequest(sqmCommercial: 100m));

        var updated = await _sut.UpdateDraftAsync(created.Id, new UpdateOrderRequest(
            ClientName:               created.ClientName,
            ClientType:               "PL",
            ClientIdentifier:         created.ClientIdentifier,
            CollateralTypeId:         created.CollateralTypeId,
            CombinedCollateralTypeId: null,
            City:                     created.City,
            PropertyAddress:          created.PropertyAddress,
            Branch:                   created.Branch,
            BranchAddress:            created.BranchAddress,
            ContactName:              created.ContactName,
            ContactPhone:             created.ContactPhone,
            ContactEmail:             created.ContactEmail,
            InternalNote:             null,
            SquareMetersCommercial:   500m,
            SquareMetersResidential:  250m));

        Assert.Equal(500m, updated.SquareMetersCommercial);
        Assert.Equal(250m, updated.SquareMetersResidential);
    }

    // ── Test 14: UpdateAsync s negativnim kvadratima baca ValidationException ─

    [Fact]
    public async Task T14_UpdateAsync_NegativeSqm_ThrowsValidation()
    {
        var created = await _sut.CreateAsync(PlRequest());

        await Assert.ThrowsAsync<ValidationException>(() =>
            _sut.UpdateDraftAsync(created.Id, new UpdateOrderRequest(
                ClientName:               created.ClientName,
                ClientType:               "PL",
                ClientIdentifier:         created.ClientIdentifier,
                CollateralTypeId:         created.CollateralTypeId,
                CombinedCollateralTypeId: null,
                City:                     created.City,
                PropertyAddress:          created.PropertyAddress,
                Branch:                   created.Branch,
                BranchAddress:            created.BranchAddress,
                ContactName:              created.ContactName,
                ContactPhone:             created.ContactPhone,
                ContactEmail:             created.ContactEmail,
                InternalNote:             null,
                SquareMetersCommercial:   -10m)));
    }

    // ── Test 15: GetByIdAsync vraća CanEdit=false za narudžbu drugog vlasnika ──

    [Fact]
    public async Task T15_NonOwner_GetById_Capabilities_CanEdit_IsFalse()
    {
        // Kreator je "user-am-1" (default)
        var created = await _sut.CreateAsync(FlRequest());

        // Prepostavimo CA usera koji ima hasAllAccess ali nije vlasnik
        _user.UserId.Returns("user-ca-1");
        _user.Role.Returns(AppRoles.KolateralAdministrator);
        _user.Roles.Returns([AppRoles.KolateralAdministrator]);

        // CA može čitati narudžbu, ali ne može je editovati (nije vlasnik)
        var dto = await _sut.GetByIdAsync(created.Id);
        Assert.False(dto.Capabilities.CanEdit);
    }

    // ── Test 16: Vještak ne može pristupiti tuđoj Prodaja narudžbi ───────────

    [Fact]
    public async Task T16_Vjestak_CannotUpdate_AnotherUsersOrder()
    {
        // AM kreira narudžbu
        var created = await _sut.CreateAsync(FlRequest());

        // Vještak pokuša ažurirati istu narudžbu
        _user.UserId.Returns("user-vjestak-1");
        _user.Role.Returns(AppRoles.Vjestak);
        _user.Roles.Returns([AppRoles.Vjestak]);

        await Assert.ThrowsAsync<ForbiddenException>(() =>
            _sut.UpdateDraftAsync(created.Id, new UpdateOrderRequest(
                ClientName:               "Promijenjen",
                ClientType:               "FL",
                ClientIdentifier:         "0101990000019",
                CollateralTypeId:         created.CollateralTypeId,
                CombinedCollateralTypeId: null,
                City:                     "Sarajevo",
                PropertyAddress:          "Nova adresa",
                Branch:                   "POS_SARAJEVO_CENTAR",
                BranchAddress:            "Titova 1",
                ContactName:              "Kontakt",
                ContactPhone:             "061-111-222",
                ContactEmail:             "test@test.ba",
                InternalNote:             null)));
    }

    // ── Test 17: FL klijent — identifikator je valjani JMBG ─────────────────

    [Fact]
    public async Task T17_FL_ClientIdentifier_ValidJmbg_IsPersisted()
    {
        var dto = await _sut.CreateAsync(FlRequest());
        Assert.Equal("0101990000019", dto.ClientIdentifier);
    }

    // ── Test 18: PL klijent — identifikator je valjani JMBG ─────────────────

    [Fact]
    public async Task T18_PL_ClientIdentifier_ValidJmbg_IsPersisted()
    {
        var dto = await _sut.CreateAsync(PlRequest());
        Assert.Equal("1506985440012", dto.ClientIdentifier);
        Assert.Equal("PL", dto.ClientType);
    }

    // ── Test 19: FL narudžba — broj narudžbi se povećava sekvencijalno ────────

    [Fact]
    public async Task T19_FL_MultipleOrders_HaveUniqueOrderNumbers()
    {
        var dto1 = await _sut.CreateAsync(FlRequest());
        var dto2 = await _sut.CreateAsync(FlRequest());

        Assert.NotEqual(dto1.OrderNumber, dto2.OrderNumber);
        Assert.NotEqual(dto1.Id, dto2.Id);
    }

    // ── Test 20: PL i FL narudžbe — obje se čuvaju u bazi ────────────────────

    [Fact]
    public async Task T20_FL_And_PL_Orders_PersistedInDb()
    {
        await _sut.CreateAsync(FlRequest());
        await _sut.CreateAsync(PlRequest());

        var count = await _db.AppraisalOrders.CountAsync();
        Assert.Equal(2, count);

        var fl = await _db.AppraisalOrders.FirstAsync(o => o.ClientType == "FL");
        var pl = await _db.AppraisalOrders.FirstAsync(o => o.ClientType == "PL");

        Assert.Equal("FL", fl.ClientType);
        Assert.Equal("PL", pl.ClientType);
    }

    public void Dispose() => _db.Dispose();
}
