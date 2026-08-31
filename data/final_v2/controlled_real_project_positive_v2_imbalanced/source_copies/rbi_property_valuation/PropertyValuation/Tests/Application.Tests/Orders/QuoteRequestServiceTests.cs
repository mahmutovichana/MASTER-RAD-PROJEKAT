using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Domain.Appraisers;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

public sealed class QuoteRequestServiceTests : IDisposable
{
    private readonly ApplicationDbContext  _db;
    private readonly ICurrentUserService   _user;
    private readonly INotificationProvider _notify;
    private readonly IAuditService         _audit;
    private readonly IProtocolService      _protocol;
    private readonly QuoteRequestService   _sut;

    public QuoteRequestServiceTests()
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

        _sut = new QuoteRequestService(
            _db, _user, _notify, _audit, _protocol,
            Substitute.For<ILogger<QuoteRequestService>>());
    }

    public void Dispose() => _db.Dispose();

    // ── Helpers ───────────────────────────────────────────────────────────────

    private async Task<AppraisalOrder> SeedPLOrderAsync(
        AppraisalOrderStatus status = AppraisalOrderStatus.DocumentationApproved)
    {
        var order = AppraisalOrder.Create(
            "PN-QR-001", "PL Test", "Firma d.o.o.", "PL", "0101985100129",
            "Kontakt", "061000000", null,
            "Sarajevo", "POS_SARAJEVO_CENTAR", "Adresa", "Obala 1",
            1, null, "user-am-1", AppRoles.AM, "Amar", "Dostava", "AM",
            workflowType: RBBH.CollateralAppraisal.Domain.Orders.WorkflowType.PravnaLica);
        order.ChangeStatus(status, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();
        return order;
    }

    private async Task<Appraiser> SeedAppraiserAsync(string name = "Vještak PL")
    {
        var a = Appraiser.Create(name, "Sarajevo", AppraiserLegalForm.Individual,
            "v@test.ba", "061111111", null, AppraiserClientScope.PravnaLica);
        _db.Appraisers.Add(a);
        await _db.SaveChangesAsync();
        return a;
    }

    // ══════════════════════════════════════════════════════════════════
    // SendQuoteRequestsAsync — error paths
    // ══════════════════════════════════════════════════════════════════

    [Fact]
    public async Task SendQuoteRequests_WhenNotFound_ShouldThrowNotFound()
    {
        var input = new SendQuoteRequestsInput([1], DateTime.UtcNow.AddDays(3));
        await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.SendQuoteRequestsAsync(99999, input));
    }

    [Fact]
    public async Task SendQuoteRequests_WhenFLOrder_ShouldThrowConflict()
    {
        var order = AppraisalOrder.Create(
            "PN-FL-001", "FL Test", "Klijent", "FL", "0101985100129",
            "Kontakt", "061000000", null,
            "Sarajevo", "POS_SARAJEVO_CENTAR", "Adresa", "Obala 1",
            1, null, "user-am-1", AppRoles.AM, "Amar", "Dostava", "AM",
            workflowType: RBBH.CollateralAppraisal.Domain.Orders.WorkflowType.FizickaLica);
        order.ChangeStatus(AppraisalOrderStatus.DocumentationApproved, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        var input = new SendQuoteRequestsInput([1], DateTime.UtcNow.AddDays(3));
        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SendQuoteRequestsAsync(order.Id, input));

        ex.ErrorCode.Should().Be("QUOTE_REQUEST_NOT_PL");
    }

    [Fact]
    public async Task SendQuoteRequests_WhenWrongStatus_ShouldThrowConflict()
    {
        var order = await SeedPLOrderAsync(AppraisalOrderStatus.Draft);

        var input = new SendQuoteRequestsInput([1], DateTime.UtcNow.AddDays(3));
        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SendQuoteRequestsAsync(order.Id, input));

        ex.ErrorCode.Should().Be("QUOTE_REQUEST_INVALID_STATUS");
    }

    [Fact]
    public async Task SendQuoteRequests_WhenEmptyAppraiserIds_ShouldThrowValidation()
    {
        var order = await SeedPLOrderAsync(AppraisalOrderStatus.DocumentationApproved);
        var input = new SendQuoteRequestsInput([], DateTime.UtcNow.AddDays(3)); // prazna lista

        await Assert.ThrowsAsync<RBBH.CollateralAppraisal.Application.Common.Exceptions.ValidationException>(
            () => _sut.SendQuoteRequestsAsync(order.Id, input));
    }

    [Fact]
    public async Task SendQuoteRequests_WhenAlreadySent_ShouldThrowConflict()
    {
        var order    = await SeedPLOrderAsync(AppraisalOrderStatus.DocumentationApproved);
        var appraiser = await SeedAppraiserAsync();

        // Kreiraj prvi quote request ručno
        _db.QuoteRequests.Add(QuoteRequest.Create(
            order.Id, appraiser.Id, DateTime.UtcNow.AddDays(3), "user-ca-1"));
        await _db.SaveChangesAsync();

        var input = new SendQuoteRequestsInput([appraiser.Id], DateTime.UtcNow.AddDays(3));
        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SendQuoteRequestsAsync(order.Id, input));

        ex.ErrorCode.Should().Be("QUOTE_REQUESTS_ALREADY_SENT");
    }

    [Fact]
    public async Task SendQuoteRequests_WhenNoActiveAppraisers_ShouldThrowConflict()
    {
        var order = await SeedPLOrderAsync(AppraisalOrderStatus.DocumentationApproved);
        // Vještak koji ne postoji u bazi
        var input = new SendQuoteRequestsInput([99999], DateTime.UtcNow.AddDays(3));

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SendQuoteRequestsAsync(order.Id, input));

        ex.ErrorCode.Should().Be("NO_AVAILABLE_APPRAISERS");
    }

    // ══════════════════════════════════════════════════════════════════
    // GetByOrderAsync
    // ══════════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetByOrder_WhenOrderDoesNotExist_ShouldReturnEmptyList()
    {
        // GetByOrderAsync ne baca exception za nepostojeći order — vraća praznu listu
        var result = await _sut.GetByOrderAsync(99999);
        result.Should().BeEmpty();
    }

    [Fact]
    public async Task GetByOrder_WhenNoQuoteRequests_ShouldReturnEmptyList()
    {
        var order = await SeedPLOrderAsync();
        var result = await _sut.GetByOrderAsync(order.Id);
        result.Should().BeEmpty();
    }

    [Fact]
    public async Task GetByOrder_WhenHasQuoteRequests_ShouldReturnList()
    {
        var order    = await SeedPLOrderAsync();
        var appraiser = await SeedAppraiserAsync();
        _db.QuoteRequests.Add(QuoteRequest.Create(
            order.Id, appraiser.Id, DateTime.UtcNow.AddDays(3), "user-ca-1"));
        await _db.SaveChangesAsync();

        var result = await _sut.GetByOrderAsync(order.Id);
        result.Should().HaveCount(1);
    }
}
