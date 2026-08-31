#pragma warning disable CS0618
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Domain.Documents;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

public sealed class InvoiceWorkflowServiceTests : IDisposable
{
    private readonly ApplicationDbContext _db;
    private readonly ICurrentUserService _user;
    private readonly InvoiceWorkflowService _sut;

    public InvoiceWorkflowServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db = new ApplicationDbContext(options);
        _user = Substitute.For<ICurrentUserService>();
        _user.UserId.Returns("protokol-user");
        _user.FullName.Returns("Protokol User");
        _user.Role.Returns("Protokol");
        _user.Roles.Returns(["Protokol"]);
        _user.IsAuthenticated.Returns(true);

        _sut = new InvoiceWorkflowService(
            _db, _user,
            Substitute.For<INotificationProvider>(),
            Substitute.For<IAuditService>(),
            Substitute.For<IUserRoleProvider>(),
            Substitute.For<ILogger<InvoiceWorkflowService>>());
    }

    private async Task<(AppraisalOrder Order, Document Doc)> SeedAsync()
    {
        var order = AppraisalOrder.Create("NP-INV-1", "Test", "Klijent", "FL",
            null, null, null, null, "Sarajevo", null, null, null,
            null, null, "sales-user", "AM", null, null, null);
        order.ChangeStatus(AppraisalOrderStatus.ReadyForProcedure, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        var doc = Document.Create(order.Id, null, "faktura.pdf", "Faktura.pdf",
            "application/pdf", 1234, "/storage/faktura.pdf", "protokol-user");
        _db.Documents.Add(doc);
        await _db.SaveChangesAsync();
        return (order, doc);
    }

    [Fact]
    public async Task UploadInvoiceAsync_ValidOrder_SetsUploadedStatus()
    {
        var (order, doc) = await SeedAsync();
        var result = await _sut.UploadInvoiceAsync(order.Id, doc.Id);
        Assert.Equal("Uploaded", result.InvoiceStatus);
    }

    [Fact]
    public async Task UploadInvoiceAsync_NotFound_ThrowsNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.UploadInvoiceAsync(99999, 1));
    }

    [Fact]
    public async Task UploadInvoiceAsync_AlreadyUploaded_ThrowsConflict()
    {
        var (order, doc) = await SeedAsync();
        await _sut.UploadInvoiceAsync(order.Id, doc.Id);
        await Assert.ThrowsAsync<ConflictException>(() => _sut.UploadInvoiceAsync(order.Id, doc.Id));
    }

    [Fact]
    public async Task SendForPaymentAsync_AfterUpload_SetsSentStatus()
    {
        var (order, doc) = await SeedAsync();
        await _sut.UploadInvoiceAsync(order.Id, doc.Id);
        _user.UserId.Returns("ca-user");
        _user.FullName.Returns("CA User");
        var result = await _sut.SendForPaymentAsync(order.Id);
        Assert.Equal("SentForPayment", result.InvoiceStatus);
    }

    [Fact]
    public async Task ConfirmPaidAsync_AfterSent_SetsPaidStatus()
    {
        var (order, doc) = await SeedAsync();
        await _sut.UploadInvoiceAsync(order.Id, doc.Id);
        _user.UserId.Returns("ca-user");
        _user.FullName.Returns("CA");
        await _sut.SendForPaymentAsync(order.Id);
        _user.UserId.Returns("likv-user");
        _user.FullName.Returns("Likvidatura");
        var result = await _sut.ConfirmPaidAsync(order.Id);
        Assert.Equal("Paid", result.InvoiceStatus);
    }

    [Fact]
    public async Task GetStatusAsync_ReturnsCurrentStatus()
    {
        var (order, _) = await SeedAsync();
        var result = await _sut.GetStatusAsync(order.Id);
        Assert.Equal("None", result.Status);
    }

    // ── Sad path: SendForPaymentAsync ────────────────────────────────────────

    [Fact]
    public async Task SendForPaymentAsync_NotUploaded_ThrowsConflict()
    {
        var (order, _) = await SeedAsync();
        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.SendForPaymentAsync(order.Id));
        Assert.Equal("INVOICE_NOT_UPLOADED", ex.ErrorCode);
    }

    [Fact]
    public async Task SendForPaymentAsync_NotFound_ThrowsNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.SendForPaymentAsync(99999));
    }

    // ── Sad path: ConfirmPaidAsync ───────────────────────────────────────────

    [Fact]
    public async Task ConfirmPaidAsync_NotInPaymentStatus_ThrowsConflict()
    {
        var (order, _) = await SeedAsync();
        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ConfirmPaidAsync(order.Id));
        Assert.Equal("INVOICE_NOT_IN_PAYMENT", ex.ErrorCode);
    }

    [Fact]
    public async Task ConfirmPaidAsync_NotFound_ThrowsNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.ConfirmPaidAsync(99999));
    }

    [Fact]
    public async Task ConfirmPaidAsync_AfterUploadButNotSent_ThrowsConflict()
    {
        var (order, doc) = await SeedAsync();
        await _sut.UploadInvoiceAsync(order.Id, doc.Id);

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ConfirmPaidAsync(order.Id));
        Assert.Equal("INVOICE_NOT_IN_PAYMENT", ex.ErrorCode);
    }

    // ── Auth ─────────────────────────────────────────────────────────────────

    [Fact]
    public async Task UploadInvoiceAsync_NotAuthenticated_ThrowsForbidden()
    {
        _user.IsAuthenticated.Returns(false);
        _user.UserId.Returns((string?)null);

        var (order, doc) = await SeedAsync();
        await Assert.ThrowsAsync<ForbiddenException>(() => _sut.UploadInvoiceAsync(order.Id, doc.Id));
    }

    [Fact]
    public async Task SendForPaymentAsync_NotAuthenticated_ThrowsForbidden()
    {
        _user.IsAuthenticated.Returns(false);
        _user.UserId.Returns((string?)null);

        await Assert.ThrowsAsync<ForbiddenException>(() => _sut.SendForPaymentAsync(1));
    }

    [Fact]
    public async Task ConfirmPaidAsync_NotAuthenticated_ThrowsForbidden()
    {
        _user.IsAuthenticated.Returns(false);
        _user.UserId.Returns((string?)null);

        await Assert.ThrowsAsync<ForbiddenException>(() => _sut.ConfirmPaidAsync(1));
    }

    // ── UploadInvoiceAsync edge cases ────────────────────────────────────────

    [Fact]
    public async Task UploadInvoiceAsync_DocumentNotFound_ThrowsNotFound()
    {
        var (order, _) = await SeedAsync();
        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.UploadInvoiceAsync(order.Id, 99999));
        Assert.Equal("DOCUMENT_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task UploadInvoiceAsync_CreatesTask()
    {
        var (order, doc) = await SeedAsync();
        await _sut.UploadInvoiceAsync(order.Id, doc.Id);

        var task = await _db.TaskItems
            .FirstOrDefaultAsync(t => t.AppraisalOrderId == order.Id && t.TaskType == TaskItemType.SendInvoiceForPayment);
        Assert.NotNull(task);
        Assert.Contains("Pošalji fakturu na plaćanje", task!.Title);
    }

    [Fact]
    public async Task UploadInvoiceAsync_SetsInvoiceDocumentId()
    {
        var (order, doc) = await SeedAsync();
        await _sut.UploadInvoiceAsync(order.Id, doc.Id);

        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        Assert.Equal(doc.Id, updated.InvoiceDocumentId);
    }

    // ── SendForPaymentAsync edge cases ───────────────────────────────────────

    [Fact]
    public async Task SendForPaymentAsync_CompletesPaymentTask()
    {
        var (order, doc) = await SeedAsync();
        await _sut.UploadInvoiceAsync(order.Id, doc.Id);

        var payTask = await _db.TaskItems
            .FirstAsync(t => t.AppraisalOrderId == order.Id && t.TaskType == TaskItemType.SendInvoiceForPayment);

        _user.UserId.Returns("ca-user");
        _user.FullName.Returns("CA User");
        await _sut.SendForPaymentAsync(order.Id);

        var updatedTask = await _db.TaskItems.FirstAsync(t => t.Id == payTask.Id);
        Assert.Equal(TaskItemStatus.Completed, updatedTask.Status);
    }

    [Fact]
    public async Task SendForPaymentAsync_CreatesConfirmPaidTask()
    {
        var (order, doc) = await SeedAsync();
        await _sut.UploadInvoiceAsync(order.Id, doc.Id);

        _user.UserId.Returns("ca-user");
        _user.FullName.Returns("CA User");
        await _sut.SendForPaymentAsync(order.Id);

        var confirmTask = await _db.TaskItems
            .FirstOrDefaultAsync(t => t.AppraisalOrderId == order.Id && t.TaskType == TaskItemType.ConfirmInvoicePaid);
        Assert.NotNull(confirmTask);
        Assert.Contains("Potvrdi plaćanje fakture", confirmTask!.Title);
    }

    [Fact]
    public async Task SendForPaymentAsync_PLWorkflow_NotifiesSalesRoles()
    {
        var order = AppraisalOrder.Create("NP-INV-PL", "Test PL", "Firma d.o.o.", "PL",
            null, null, null, null, "Sarajevo", null, null, null,
            null, null, "sales-user", "AM", null, null, null,
            workflowType: WorkflowType.PravnaLica);
        order.ChangeStatus(AppraisalOrderStatus.ReadyForProcedure, DateTime.UtcNow);
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        var doc = Document.Create(order.Id, null, "faktura.pdf", "Faktura.pdf",
            "application/pdf", 1234, "/storage/faktura.pdf", "protokol-user");
        _db.Documents.Add(doc);
        await _db.SaveChangesAsync();

        await _sut.UploadInvoiceAsync(order.Id, doc.Id);

        _user.UserId.Returns("ca-user");
        _user.FullName.Returns("CA User");
        var result = await _sut.SendForPaymentAsync(order.Id);

        Assert.Equal("SentForPayment", result.InvoiceStatus);
    }

    // ── ConfirmPaidAsync edge cases ──────────────────────────────────────────

    [Fact]
    public async Task ConfirmPaidAsync_CompletesConfirmTask()
    {
        var (order, doc) = await SeedAsync();
        await _sut.UploadInvoiceAsync(order.Id, doc.Id);
        _user.UserId.Returns("ca-user");
        _user.FullName.Returns("CA User");
        await _sut.SendForPaymentAsync(order.Id);

        var confirmTask = await _db.TaskItems
            .FirstAsync(t => t.AppraisalOrderId == order.Id && t.TaskType == TaskItemType.ConfirmInvoicePaid);

        _user.UserId.Returns("likv-user");
        _user.FullName.Returns("Likvidatura");
        await _sut.ConfirmPaidAsync(order.Id);

        var updatedTask = await _db.TaskItems.FirstAsync(t => t.Id == confirmTask.Id);
        Assert.Equal(TaskItemStatus.Completed, updatedTask.Status);
    }

    [Fact]
    public async Task ConfirmPaidAsync_SetsInvoicePaidTimestamp()
    {
        var (order, doc) = await SeedAsync();
        await _sut.UploadInvoiceAsync(order.Id, doc.Id);
        _user.UserId.Returns("ca-user");
        _user.FullName.Returns("CA User");
        await _sut.SendForPaymentAsync(order.Id);
        _user.UserId.Returns("likv-user");
        _user.FullName.Returns("Likvidatura");
        await _sut.ConfirmPaidAsync(order.Id);

        var updated = await _db.AppraisalOrders.FirstAsync(o => o.Id == order.Id);
        Assert.NotNull(updated.InvoicePaidAt);
        Assert.NotNull(updated.InvoicePaidByName);
    }

    // ── GetStatusAsync edge cases ────────────────────────────────────────────

    [Fact]
    public async Task GetStatusAsync_NotFound_ThrowsNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.GetStatusAsync(99999));
    }

    [Fact]
    public async Task GetStatusAsync_AfterUpload_ReturnsUploadedStatus()
    {
        var (order, doc) = await SeedAsync();
        await _sut.UploadInvoiceAsync(order.Id, doc.Id);

        var result = await _sut.GetStatusAsync(order.Id);

        Assert.Equal("Uploaded", result.Status);
        Assert.NotNull(result.UploadedAt);
    }

    [Fact]
    public async Task GetStatusAsync_AfterPaid_ReturnsPaidWithAllTimestamps()
    {
        var (order, doc) = await SeedAsync();
        await _sut.UploadInvoiceAsync(order.Id, doc.Id);
        _user.UserId.Returns("ca-user");
        _user.FullName.Returns("CA User");
        await _sut.SendForPaymentAsync(order.Id);
        _user.UserId.Returns("likv-user");
        _user.FullName.Returns("Likvidatura");
        await _sut.ConfirmPaidAsync(order.Id);

        var result = await _sut.GetStatusAsync(order.Id);

        Assert.Equal("Paid", result.Status);
        Assert.NotNull(result.UploadedAt);
        Assert.NotNull(result.SentForPaymentAt);
        Assert.NotNull(result.PaidAt);
        Assert.Equal(doc.Id, result.InvoiceDocumentId);
    }

    // ── Full workflow ────────────────────────────────────────────────────────

    [Fact]
    public async Task FullInvoiceWorkflow_UploadSendConfirm_AllStatusTransitionsWork()
    {
        var (order, doc) = await SeedAsync();

        var upload = await _sut.UploadInvoiceAsync(order.Id, doc.Id);
        Assert.Equal("Uploaded", upload.InvoiceStatus);

        _user.UserId.Returns("ca-user");
        _user.FullName.Returns("CA User");
        var sent = await _sut.SendForPaymentAsync(order.Id);
        Assert.Equal("SentForPayment", sent.InvoiceStatus);

        _user.UserId.Returns("likv-user");
        _user.FullName.Returns("Likvidatura");
        var paid = await _sut.ConfirmPaidAsync(order.Id);
        Assert.Equal("Paid", paid.InvoiceStatus);

        // Try double-pay should fail
        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ConfirmPaidAsync(order.Id));
        Assert.Equal("INVOICE_NOT_IN_PAYMENT", ex.ErrorCode);
    }

    public void Dispose() => _db.Dispose();
}
