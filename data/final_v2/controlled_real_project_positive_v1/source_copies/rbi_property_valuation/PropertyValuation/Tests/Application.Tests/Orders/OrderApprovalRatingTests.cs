using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Tests.Helpers;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

public sealed class OrderApprovalRatingTests : IDisposable
{
    private readonly ApplicationDbContext    _db;
    private readonly ICurrentUserService     _user;
    private readonly INotificationService    _notifService;
    private readonly INotificationProvider   _notifProvider;
    private readonly IAuditService           _audit;
    private readonly IUserRoleProvider       _userRoleProvider;
    private readonly OrderApprovalService    _sut;

    public OrderApprovalRatingTests()
    {
        var opts = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w =>
                w.Ignore(Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;

        _db               = new ApplicationDbContext(opts);
        _user             = Substitute.For<ICurrentUserService>();
        _notifService     = Substitute.For<INotificationService>();
        _notifProvider    = Substitute.For<INotificationProvider>();
        _audit            = Substitute.For<IAuditService>();
        _userRoleProvider = Substitute.For<IUserRoleProvider>();

        _user.UserId.Returns("user-co-1");
        _user.IsAuthenticated.Returns(true);
        _user.Roles.Returns([AppRoles.KolateralOficir]);

        _sut = new OrderApprovalService(
            _db, _user, _notifService, _notifProvider, _audit,
            _userRoleProvider,
            Substitute.For<ILogger<OrderApprovalService>>(),
            Options.Create(new WorkflowSlaOptions()),
            new FakeClock());
    }

    public void Dispose() => _db.Dispose();

    private async Task<(AppraisalOrder order, RBBH.CollateralAppraisal.Domain.Documents.Document doc)> SeedOrderWithFinalDocAsync()
    {
        var order = AppraisalOrder.Create(
            "PN-APPR-001", "Odobrenje test", "Klijent", "FL", "0101985100129",
            "Kontakt", "061000000", null,
            "Sarajevo", "POS_SARAJEVO_CENTAR", "Adresa", "Obala 1",
            1, null, "user-am-1", AppRoles.AM, "Amar", "Dostava", "AM",
            workflowType: RBBH.CollateralAppraisal.Domain.Orders.WorkflowType.FizickaLica);
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        var doc = RBBH.CollateralAppraisal.Domain.Documents.Document.Create(
            order.Id, null, "procjena.pdf", "procjena.pdf", "application/pdf",
            1024, "/storage/procjena.pdf", "user-vjestak-1", DateTime.UtcNow);
        _db.Documents.Add(doc);
        await _db.SaveChangesAsync();

        // Postavi FinalAppraisalDocumentId direktno
        _db.Entry(order).Property("FinalAppraisalDocumentId").CurrentValue = doc.Id;
        await _db.SaveChangesAsync();

        return (order, doc);
    }

    // ── ApproveFinalAppraisalAsync — rating validacija ─────────────────────────

    [Fact]
    public async Task ApproveFinal_WhenOrderNotFound_ShouldThrowNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.ApproveFinalAppraisalAsync(99999, 5));
    }

    [Fact]
    public async Task ApproveFinal_WhenRatingNull_ShouldThrowConflict()
    {
        var (order, _) = await SeedOrderWithFinalDocAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ApproveFinalAppraisalAsync(order.Id, null));

        ex.ErrorCode.Should().Be("APPRAISER_RATING_REQUIRED");
    }

    [Theory]
    [InlineData(0)]
    [InlineData(6)]
    [InlineData(-1)]
    [InlineData(100)]
    public async Task ApproveFinal_WhenRatingOutOfRange_ShouldThrowConflict(int rating)
    {
        // BVA: valjani opseg je 1-5
        var (order, _) = await SeedOrderWithFinalDocAsync();

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ApproveFinalAppraisalAsync(order.Id, rating));

        ex.ErrorCode.Should().Be("APPRAISER_RATING_OUT_OF_RANGE");
    }

    [Theory]
    [InlineData(1)]
    [InlineData(3)]
    [InlineData(5)]
    public async Task ApproveFinal_WhenValidRating_ShouldSucceed(int rating)
    {
        // BVA: 1, 3 (srednji), 5 su validni
        var (order, _) = await SeedOrderWithFinalDocAsync();

        var result = await _sut.ApproveFinalAppraisalAsync(order.Id, rating);

        result.Should().NotBeNull();
        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        updated.AppraiserRating.Should().Be(rating);
    }

    [Fact]
    public async Task ApproveFinal_WhenWrongStatus_ShouldThrowConflict()
    {
        // Metoda provjerava dokument PRIJE statusa — seedujemo oba da dođemo do provjere statusa.
        // Order je u Draft statusu, koji nije AppraisalReceived/COApproved → ConflictException.
        var order = AppraisalOrder.Create(
            "PN-APPR-002", "Test", "Klijent", "FL", "0101985100129",
            "Kontakt", "061000000", null,
            "Sarajevo", "POS_SARAJEVO_CENTAR", "Adresa", "Obala 1",
            1, null, "user-am-1", AppRoles.AM, "Amar", "Dostava", "AM",
            workflowType: RBBH.CollateralAppraisal.Domain.Orders.WorkflowType.FizickaLica);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        var doc = RBBH.CollateralAppraisal.Domain.Documents.Document.Create(
            order.Id, null, "procjena.pdf", "procjena.pdf", "application/pdf",
            1024, "/storage/procjena.pdf", "user-vjestak-1", DateTime.UtcNow);
        _db.Documents.Add(doc);
        await _db.SaveChangesAsync();

        // Postavljamo FinalAppraisalDocumentId direktno da bypass-ujemo codebook lookup
        _db.Entry(order).Property("FinalAppraisalDocumentId").CurrentValue = doc.Id;
        await _db.SaveChangesAsync();

        // Order je u Draft statusu → EnsureCanApprove baca ConflictException
        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ApproveFinalAppraisalAsync(order.Id, 4));

        ex.ErrorCode.Should().Be("FINAL_APPRAISAL_INVALID_STATUS");
    }

    // ── ReturnForReworkAsync ───────────────────────────────────────────────────

    [Fact]
    public async Task ReturnForRework_WhenNotFound_ShouldThrowNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.ReturnForReworkAsync(99999, "Greška", "Komentar"));
    }

    [Fact]
    public async Task ReturnForRework_WhenWrongStatus_ShouldThrowConflict()
    {
        var order = AppraisalOrder.Create(
            "PN-RW-001", "Rework Test", "Klijent", "FL", "0101985100129",
            "Kontakt", "061000000", null,
            "Sarajevo", "POS_SARAJEVO_CENTAR", "Adresa", "Obala 1",
            1, null, "user-am-1", AppRoles.AM, "Amar", "Dostava", "AM",
            workflowType: RBBH.CollateralAppraisal.Domain.Orders.WorkflowType.FizickaLica);
        order.ChangeStatus(AppraisalOrderStatus.Draft, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ReturnForReworkAsync(order.Id, "Greška", "Komentar"));
    }
}
