using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Tests.Helpers;
using RBBH.CollateralAppraisal.Domain.Appraisers;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

// ═══════════════════════════════════════════════════════════════
// TEST MATRIX — PlAppraiserSelectionService
//
// GetCandidatesForOrderAsync
// ─────────────────────────────────────────────────────────────
// Scenario                           | Expected              | Type
// PL narudžba, 5 aktivnih            | Max 3 kandidata       | BVA (PL limit = 3)
// PL narudžba, 2 aktivna             | 2 kandidata           | BVA (ispod limita)
// PL narudžba, 4 aktivnih            | Max 3 kandidata       | Decision table
// Neaktivan vještak                  | Isključen             | Filter
// Blacklisted vještak                | Isključen             | Filter
// Na godišnjem odmoru                | Isključen             | Filter (ADR-005 fix)
// City filter — svi u Sarajevu       | Sarjevo kandidati     | Geolocation
// City filter — nijedan u gradu      | Svi kandidati         | City fallback
// Sortirani po aktivnim narudžbama   | Rastuće              | Ordering
// Nema aktivnih vještaka             | Prazna lista          | Edge case
//
// ManualSelectAppraiserAsync
// ─────────────────────────────────────────────────────────────
// Vještak već odabran                | ConflictException     | State transition
// Nema aktivnog SelectAppraiser taska| ConflictException     | State
// Vještak ne postoji                 | NotFoundException     | Negative
// Vještak neaktivan                  | ConflictException     | Business rule
// Vještak blacklisted                | ConflictException     | Business rule
// Vještak na godišnjem              | ConflictException     | Business rule (ADR-005 fix)
// Scope mismatch (FL na PL)          | ConflictException     | Scope rule
// Validan odabir PL                  | Returns result        | Happy path
// ═══════════════════════════════════════════════════════════════

public sealed class PlAppraiserSelectionServiceTests : IDisposable
{
    private readonly ApplicationDbContext   _db;
    private readonly ICurrentUserService    _user;
    private readonly INotificationProvider  _notify;
    private readonly IAuditService          _audit;
    private readonly IProtocolService       _protocol;
    private readonly PlAppraiserSelectionService _sut;

    public PlAppraiserSelectionServiceTests()
    {
        var opts = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w =>
                w.Ignore(Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;

        _db       = new ApplicationDbContext(opts);
        _user     = Substitute.For<ICurrentUserService>();
        _notify   = Substitute.For<INotificationProvider>();
        _audit    = Substitute.For<IAuditService>();
        _protocol = Substitute.For<IProtocolService>();

        _user.UserId.Returns("user-ca-1");
        _user.IsAuthenticated.Returns(true);

        _sut = new PlAppraiserSelectionService(
            _db, _user, _notify, _audit, _protocol,
            Substitute.For<ILogger<PlAppraiserSelectionService>>());
    }

    public void Dispose() => _db.Dispose();

    // ── Test Data Builders ────────────────────────────────────────────────────

    private async Task<AppraisalOrder> SeedOrderAsync(
        string  clientType = "PL",
        string? city       = "Sarajevo",
        AppraisalOrderStatus status = AppraisalOrderStatus.DocumentationApproved)
    {
        // WorkflowType mora biti eksplicitno postavljen da CanHandle() radi ispravno
        var workflowType = clientType == "PL"
            ? RBBH.CollateralAppraisal.Domain.Orders.WorkflowType.PravnaLica
            : RBBH.CollateralAppraisal.Domain.Orders.WorkflowType.FizickaLica;

        var order = AppraisalOrder.Create(
            orderNumber:     "PN-2026-000001",
            title:           "Stan PL test",
            clientName:      "Firma d.o.o.",
            clientType:      clientType,
            clientIdentifier:"0101985100129",
            contactName:     "Kontakt",
            contactPhone:    "061000000",
            contactEmail:    null,
            city:            city,
            branch:          "POS_SARAJEVO_CENTAR",
            branchAddress:   "Titova 1",
            propertyAddress: "Obala 1",
            collateralTypeId: null,
            combinedCollateralTypeId: null,
            createdByUserId: "u1",
            createdByRole:   AppRoles.AM,
            createdByName:   "Amar",
            deliveryContactName: "Dostava",
            amRecipientName:     "AM",
            workflowType:    workflowType);

        // CS0618: deliberate bypass for test state setup
        order.ChangeStatus(status, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();
        return order;
    }

    private async Task<Appraiser> SeedAppraiserAsync(
        string  name          = "Vještak Test",
        string? city          = "Sarajevo",
        bool    isActive      = true,
        bool    isBlacklisted = false,
        bool    isOnLeave     = false,
        AppraiserClientScope scope = AppraiserClientScope.Sve)
    {
        var a = Appraiser.Create(
            name, city, AppraiserLegalForm.Individual,
            $"{name.Replace(" ", ".")}@test.ba", "061-111-111",
            null, scope);

        if (!isActive)     a.Deactivate(DateTime.UtcNow);
        if (isBlacklisted) a.SetBlacklisted(true, DateTime.UtcNow);
        if (isOnLeave)     a.SetOnLeave(true, DateTime.UtcNow);

        _db.Appraisers.Add(a);
        await _db.SaveChangesAsync();
        return a;
    }

    private async Task<TaskItem> SeedTaskAsync(
        int orderId, TaskItemType type = TaskItemType.SelectAppraiser)
    {
        var task = TaskItem.Create(orderId, type, "Task", null, AppRoles.KolateralAdministrator);
        _db.TaskItems.Add(task);
        await _db.SaveChangesAsync();
        return task;
    }

    // ═══════════════════════════════════════════════════════════════
    // GetCandidatesForOrderAsync
    // ═══════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetCandidates_WhenPLOrderWith5ActiveAppraisers_ShouldReturnMax3()
    {
        // Arrange — BVA: PL limit je 3; 5 > 3
        var order = await SeedOrderAsync("PL");
        for (var i = 1; i <= 5; i++)
            await SeedAppraiserAsync($"Vještak {i}");

        // Act
        var result = await _sut.GetCandidatesForOrderAsync(order.Id);

        // Assert
        result.Should().HaveCount(3,
            "PL workflow limitira kandidate na maksimalno 3 (ADR-050, poslovni limit)");
    }

    [Fact]
    public async Task GetCandidates_WhenPLOrderWith2ActiveAppraisers_ShouldReturnBoth()
    {
        // BVA: 2 < 3, vraća sve dostupne
        var order = await SeedOrderAsync("PL");
        await SeedAppraiserAsync("Vještak A");
        await SeedAppraiserAsync("Vještak B");

        var result = await _sut.GetCandidatesForOrderAsync(order.Id);

        result.Should().HaveCount(2);
    }

    [Fact]
    public async Task GetCandidates_WhenPLOrderWith4Appraisers_ShouldStillReturnMax3()
    {
        // Decision table: 4 aktivnih → limit ostaje 3
        var order = await SeedOrderAsync("PL");
        for (var i = 1; i <= 4; i++)
            await SeedAppraiserAsync($"Vještak {i}");

        var result = await _sut.GetCandidatesForOrderAsync(order.Id);

        result.Should().HaveCount(3);
    }

    [Fact]
    public async Task GetCandidates_WhenInactiveAppraiser_ShouldExcludeInactive()
    {
        var order = await SeedOrderAsync("PL");
        await SeedAppraiserAsync("Aktivan");
        await SeedAppraiserAsync("Neaktivan", isActive: false);

        var result = await _sut.GetCandidatesForOrderAsync(order.Id);

        result.Should().HaveCount(1)
            .And.OnlyContain(a => a.Name == "Aktivan");
    }

    [Fact]
    public async Task GetCandidates_WhenBlacklistedAppraiser_ShouldExcludeBlacklisted()
    {
        var order = await SeedOrderAsync("PL");
        await SeedAppraiserAsync("Normalan");
        await SeedAppraiserAsync("Crna lista", isBlacklisted: true);

        var result = await _sut.GetCandidatesForOrderAsync(order.Id);

        result.Should().HaveCount(1)
            .And.OnlyContain(a => a.Name == "Normalan");
    }

    [Fact]
    public async Task GetCandidates_WhenAppraiserOnLeave_ShouldExcludeOnLeave()
    {
        // Regresijski test za ADR-005 fix: IsOnLeave guard dodan u ManualSelect
        var order = await SeedOrderAsync("PL");
        await SeedAppraiserAsync("Prisutan");
        await SeedAppraiserAsync("Na odmoru", isOnLeave: true);

        var result = await _sut.GetCandidatesForOrderAsync(order.Id);

        result.Should().HaveCount(1)
            .And.OnlyContain(a => a.Name == "Prisutan");
    }

    [Fact]
    public async Task GetCandidates_WhenAppraisersInOrderCity_ShouldPreferCityAppraisers()
    {
        // City filter: vještaci iz Sarajeva imaju prednost nad ostalima
        var order = await SeedOrderAsync("PL", city: "Sarajevo");
        await SeedAppraiserAsync("Sarajevlija", city: "Sarajevo");
        await SeedAppraiserAsync("Mostarac",    city: "Mostar");

        var result = await _sut.GetCandidatesForOrderAsync(order.Id);

        result.Should().HaveCount(1)
            .And.OnlyContain(a => a.Name == "Sarajevlija");
    }

    [Fact]
    public async Task GetCandidates_WhenNoAppraisersInOrderCity_ShouldReturnAllAppraisers()
    {
        // City filter fallback: ako nema vještaka u gradu, vrati sve
        var order = await SeedOrderAsync("PL", city: "Zenica");
        await SeedAppraiserAsync("Mostarac",  city: "Mostar");
        await SeedAppraiserAsync("Tuzlak",    city: "Tuzla");

        var result = await _sut.GetCandidatesForOrderAsync(order.Id);

        result.Should().HaveCount(2, "fallback vraća sve kad nema vještaka u gradu narudžbe");
    }

    [Fact]
    public async Task GetCandidates_WhenNoActiveAppraisers_ShouldReturnEmpty()
    {
        // Edge case: nema aktivnih → prazna lista, ne iznimka
        var order = await SeedOrderAsync("PL");
        await SeedAppraiserAsync("Neaktivan", isActive: false);

        var result = await _sut.GetCandidatesForOrderAsync(order.Id);

        result.Should().BeEmpty();
    }

    [Fact]
    public async Task GetCandidates_ShouldReturnSortedByActiveCountAscending()
    {
        // Ordering: vještak s manje aktivnih narudžbi dolazi prvi
        var order = await SeedOrderAsync("PL");
        var a1 = await SeedAppraiserAsync("Zauzet");
        var a2 = await SeedAppraiserAsync("Slobodan");

        // a1 ima 1 aktivnu narudžbu
        var existingOrder = await SeedOrderAsync("PL");
        existingOrder.SelectAppraiser(a1.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var result = await _sut.GetCandidatesForOrderAsync(order.Id);

        result.First().Name.Should().Be("Slobodan",
            "vještak bez aktivnih narudžbi dolazi na vrh liste");
    }

    [Fact]
    public async Task GetCandidates_WhenOrderNotFound_ShouldThrowNotFound()
    {
        // Negative: narudžba ne postoji
        await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.GetCandidatesForOrderAsync(99999));
    }

    // ═══════════════════════════════════════════════════════════════
    // ManualSelectAppraiserAsync
    // ═══════════════════════════════════════════════════════════════

    [Fact]
    public async Task ManualSelect_WithValidInput_ShouldReturnResultWithAppraiserInfo()
    {
        // Happy path
        var order    = await SeedOrderAsync("PL");
        var appraiser = await SeedAppraiserAsync("Odabrani Vještak");
        await SeedTaskAsync(order.Id, TaskItemType.SelectAppraiser);

        var result = await _sut.ManualSelectAppraiserAsync(order.Id, appraiser.Id);

        result.Should().NotBeNull();
        result.AppraiserId.Should().Be(appraiser.Id);
        result.AppraiserName.Should().Be("Odabrani Vještak");
    }

    [Fact]
    public async Task ManualSelect_WhenAppraiserAlreadySelected_ShouldThrowConflict()
    {
        // State transition: vještak je već odabran
        var order     = await SeedOrderAsync("PL");
        var appraiser = await SeedAppraiserAsync();
        await SeedTaskAsync(order.Id, TaskItemType.SelectAppraiser);

        order.SelectAppraiser(appraiser.Id, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ManualSelectAppraiserAsync(order.Id, appraiser.Id));

        ex.ErrorCode.Should().Be("APPRAISER_ALREADY_SELECTED");
    }

    [Fact]
    public async Task ManualSelect_WhenNoSelectTask_ShouldThrowConflict()
    {
        // State: nema aktivnog zadatka za odabir
        var order     = await SeedOrderAsync("PL");
        var appraiser = await SeedAppraiserAsync();
        // namjerno ne kreiramo SelectAppraiser task

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ManualSelectAppraiserAsync(order.Id, appraiser.Id));

        ex.ErrorCode.Should().Be("SELECT_APPRAISER_TASK_NOT_FOUND");
    }

    [Fact]
    public async Task ManualSelect_WhenAppraiserNotFound_ShouldThrowNotFound()
    {
        var order = await SeedOrderAsync("PL");
        await SeedTaskAsync(order.Id, TaskItemType.SelectAppraiser);

        await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.ManualSelectAppraiserAsync(order.Id, 99999));
    }

    [Fact]
    public async Task ManualSelect_WhenInactiveAppraiser_ShouldThrowConflict()
    {
        var order     = await SeedOrderAsync("PL");
        var appraiser = await SeedAppraiserAsync(isActive: false);
        await SeedTaskAsync(order.Id, TaskItemType.SelectAppraiser);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ManualSelectAppraiserAsync(order.Id, appraiser.Id));

        ex.ErrorCode.Should().Be("APPRAISER_NOT_AVAILABLE");
    }

    [Fact]
    public async Task ManualSelect_WhenBlacklistedAppraiser_ShouldThrowConflict()
    {
        var order     = await SeedOrderAsync("PL");
        var appraiser = await SeedAppraiserAsync(isBlacklisted: true);
        await SeedTaskAsync(order.Id, TaskItemType.SelectAppraiser);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ManualSelectAppraiserAsync(order.Id, appraiser.Id));

        ex.ErrorCode.Should().Be("APPRAISER_NOT_AVAILABLE");
    }

    [Fact]
    public async Task ManualSelect_WhenAppraiserOnLeave_ShouldThrowConflict()
    {
        // Regresijski test za ADR-005 fix: IsOnLeave guard dodan u ManualSelect
        var order     = await SeedOrderAsync("PL");
        var appraiser = await SeedAppraiserAsync(isOnLeave: true);
        await SeedTaskAsync(order.Id, TaskItemType.SelectAppraiser);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ManualSelectAppraiserAsync(order.Id, appraiser.Id));

        ex.ErrorCode.Should().Be("APPRAISER_NOT_AVAILABLE",
            "vještak na godišnjem odmoru ne smije biti odabran");
    }

    [Fact]
    public async Task ManualSelect_WhenFLAppraiserOnPLOrder_ShouldThrowScopeMismatch()
    {
        // Scope mismatch: vještak radi samo FL, narudžba je PL
        var order     = await SeedOrderAsync("PL");
        var appraiser = await SeedAppraiserAsync(scope: AppraiserClientScope.FizickaLica);
        await SeedTaskAsync(order.Id, TaskItemType.SelectAppraiser);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ManualSelectAppraiserAsync(order.Id, appraiser.Id));

        ex.ErrorCode.Should().Be("APPRAISER_SCOPE_MISMATCH");
    }

    [Fact]
    public async Task ManualSelect_WhenPLAppraiserOnPLOrder_ShouldPass()
    {
        // Scope match: vještak radi PL, narudžba je PL → ok
        var order     = await SeedOrderAsync("PL");
        var appraiser = await SeedAppraiserAsync(scope: AppraiserClientScope.PravnaLica);
        await SeedTaskAsync(order.Id, TaskItemType.SelectAppraiser);

        var result = await _sut.ManualSelectAppraiserAsync(order.Id, appraiser.Id);

        result.AppraiserId.Should().Be(appraiser.Id);
    }
}
