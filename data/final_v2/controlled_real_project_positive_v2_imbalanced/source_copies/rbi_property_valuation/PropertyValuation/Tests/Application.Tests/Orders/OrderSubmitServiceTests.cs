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
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

public sealed class OrderSubmitServiceTests : IDisposable
{
    private readonly ApplicationDbContext   _db;
    private readonly ICurrentUserService    _user;
    private readonly INotificationProvider  _notify;
    private readonly IAuditService          _audit;
    private readonly OrderSubmitService     _sut;

    public OrderSubmitServiceTests()
    {
        var opts = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w =>
                w.Ignore(Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;

        _db     = new ApplicationDbContext(opts);
        _user   = Substitute.For<ICurrentUserService>();
        _notify = Substitute.For<INotificationProvider>();
        _audit  = Substitute.For<IAuditService>();

        _user.UserId.Returns("user-am-1");
        _user.IsAuthenticated.Returns(true);
        _user.Roles.Returns([AppRoles.AM]);

        _sut = new OrderSubmitService(
            _db, _user, _notify, _audit,
            Substitute.For<ILogger<OrderSubmitService>>(),
            Options.Create(new OrderNotificationsOptions { CaInboxEmail = "ca@test.ba" }),
            Options.Create(new WorkflowSlaOptions()),
            new FakeClock());
    }

    public void Dispose() => _db.Dispose();

    // ── Helper ────────────────────────────────────────────────────────────────

    private async Task<AppraisalOrder> SeedDraftOrderAsync(string? userId = "user-am-1")
    {
        var order = AppraisalOrder.Create(
            "PN-2026-000001", "Test", "Klijent Test", "FL", "0101985100129",
            "Kontakt", "061123456", null,
            "Sarajevo", "POS_SARAJEVO_CENTAR", "Adresa 1", "Obala 1",
            1, null,
            userId ?? "user-am-1", AppRoles.AM, "Amar",
            "Dostava", "AM Primalac",
            workflowType: RBBH.CollateralAppraisal.Domain.Orders.WorkflowType.FizickaLica,
            requestReceivedAt: new DateTime(2026, 1, 10, 10, 0, 0, DateTimeKind.Utc));

        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();
        return order;
    }

    // ══════════════════════════════════════════════════════════════════
    // CancelAsync
    // ══════════════════════════════════════════════════════════════════

    [Fact]
    public async Task CancelAsync_WhenOrderNotFound_ShouldThrowNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.CancelAsync(99999));
    }

    [Fact]
    public async Task CancelAsync_WhenDifferentUser_ShouldThrowForbidden()
    {
        var order = await SeedDraftOrderAsync("some-other-user");
        _user.UserId.Returns("user-am-1"); // different from creator

        await Assert.ThrowsAsync<ForbiddenException>(
            () => _sut.CancelAsync(order.Id));
    }

    [Fact]
    public async Task CancelAsync_WhenNotDraft_ShouldThrowValidation()
    {
        var order = await SeedDraftOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.SubmittedBySales, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await Assert.ThrowsAsync<ValidationException>(
            () => _sut.CancelAsync(order.Id));
    }

    [Fact]
    public async Task CancelAsync_WhenDraftAndOwner_ShouldSoftDeleteAndAudit()
    {
        var order = await SeedDraftOrderAsync();

        await _sut.CancelAsync(order.Id);

        var cancelled = await _db.AppraisalOrders
            .IgnoreQueryFilters()
            .FirstAsync(o => o.Id == order.Id);
        cancelled.IsDeleted.Should().BeTrue();

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.OrderCancelled),
            Arg.Any<CancellationToken>());
    }

    // ══════════════════════════════════════════════════════════════════
    // SubmitAsync — error paths
    // ══════════════════════════════════════════════════════════════════

    [Fact]
    public async Task SubmitAsync_WhenOrderNotFound_ShouldThrowNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.SubmitAsync(99999));
    }

    [Fact]
    public async Task SubmitAsync_WhenNotDraft_ShouldThrowValidation()
    {
        var order = await SeedDraftOrderAsync();
        order.ChangeStatus(AppraisalOrderStatus.SubmittedBySales, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        await Assert.ThrowsAsync<ValidationException>(
            () => _sut.SubmitAsync(order.Id));
    }

    [Fact]
    public async Task SubmitAsync_WhenMissingClientName_ShouldFailValidation()
    {
        // Narudžba u Draft-u ali bez clientName
        var order = AppraisalOrder.Create(
            "PN-2026-000002", "Test", "", "FL", "0101985100129",
            "Kontakt", "061123456", null,
            "Sarajevo", "POS_SARAJEVO_CENTAR", "Adresa", "Obala 1",
            1, null, "user-am-1", AppRoles.AM, "Amar",
            "Dostava", "AM Primalac",
            workflowType: RBBH.CollateralAppraisal.Domain.Orders.WorkflowType.FizickaLica,
            requestReceivedAt: new DateTime(2026, 1, 10, 10, 0, 0, DateTimeKind.Utc));
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ValidationException>(
            () => _sut.SubmitAsync(order.Id));

        ex.FieldErrors.Should().Contain(e => e.Field == "clientName");
    }

    [Fact]
    public async Task SubmitAsync_WhenMissingRequestReceivedAt_ShouldFailValidation()
    {
        var order = AppraisalOrder.Create(
            "PN-2026-000003", "Test", "Klijent", "FL", "0101985100129",
            "Kontakt", "061123456", null,
            "Sarajevo", "POS_SARAJEVO_CENTAR", "Adresa", "Obala 1",
            1, null, "user-am-1", AppRoles.AM, "Amar",
            "Dostava", "AM", workflowType: RBBH.CollateralAppraisal.Domain.Orders.WorkflowType.FizickaLica,
            requestReceivedAt: null); // nedostaje
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ValidationException>(
            () => _sut.SubmitAsync(order.Id));

        ex.FieldErrors.Should().Contain(e => e.Field == "requestReceivedAt");
    }

    [Fact]
    public async Task SubmitAsync_WhenNoCollateral_ShouldFailValidation()
    {
        // collateralTypeId = null, combinedCollateralTypeId = null
        var order = AppraisalOrder.Create(
            "PN-2026-000004", "Test", "Klijent", "FL", "0101985100129",
            "Kontakt", "061123456", null,
            "Sarajevo", "POS_SARAJEVO_CENTAR", "Adresa", "Obala 1",
            null, null, // oba null — greška
            "user-am-1", AppRoles.AM, "Amar", "Dostava", "AM",
            workflowType: RBBH.CollateralAppraisal.Domain.Orders.WorkflowType.FizickaLica,
            requestReceivedAt: new DateTime(2026, 1, 10, 10, 0, 0, DateTimeKind.Utc));
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ValidationException>(
            () => _sut.SubmitAsync(order.Id));

        ex.FieldErrors.Should().Contain(e => e.Field == "collateralTypeId");
    }

    [Fact]
    public async Task SubmitAsync_WhenZkDocumentMissing_ShouldFailValidation()
    {
        // Validna narudžba ali bez ZK izvadka u DocumentTypes
        var order = await SeedDraftOrderAsync();

        // Seed codebook values for DocumentTypes
        _db.CodebookValues.Add(RBBH.CollateralAppraisal.Domain.Codebooks.CodebookValue.Create(
            RBBH.CollateralAppraisal.Application.Common.Constants.CodebookKeys.DocumentTypes,
            RBBH.CollateralAppraisal.Application.Common.Constants.DocumentTypeCodes.ZkExtract,
            "ZK Izvadak", null, 1, "system"));
        await _db.SaveChangesAsync();

        var ex = await Assert.ThrowsAsync<ValidationException>(
            () => _sut.SubmitAsync(order.Id));

        ex.FieldErrors.Should().Contain(e => e.Field == "documents.zk");
    }

    [Fact]
    public async Task SubmitAsync_WhenCaInboxEmailEmpty_ShouldNotSendEmail()
    {
        // Narudžba koja prolazi validaciju ali bez CA inbox email-a
        // Testiramo NotifyCAByEmailAsync early return
        var sut = new OrderSubmitService(
            _db, _user, _notify, _audit,
            Substitute.For<ILogger<OrderSubmitService>>(),
            Options.Create(new OrderNotificationsOptions { CaInboxEmail = null }), // prazno
            Options.Create(new WorkflowSlaOptions()),
            new FakeClock());

        var order = await SeedDraftOrderAsync();

        await sut.SubmitAsync(order.Id);

        // Samo in-app notifikacija, bez emaila (2 audit poziva post-commit)
        await _notify.Received(1).SendAsync(
            Arg.Is<NotificationRequest>(n => n.Channel == NotificationChannel.InApp),
            Arg.Any<CancellationToken>());
        await _notify.DidNotReceive().SendAsync(
            Arg.Is<NotificationRequest>(n => n.Channel == NotificationChannel.Email),
            Arg.Any<CancellationToken>());
    }
}
