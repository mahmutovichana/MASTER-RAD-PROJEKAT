using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging.Abstractions;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Documents;
using RBBH.CollateralAppraisal.Application.Documents.Dtos;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Opinions.Dtos;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Application.Users.Models;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Opinions;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Opinions;

public class OpinionServiceTests
{
    private readonly ApplicationDbContext    _db;
    private readonly INotificationService   _notificationService;
    private readonly IDocumentService       _documentService;
    private readonly IUserRoleProvider      _userRoleProvider;
    private readonly IAuditService          _auditService;
    private readonly OpinionService         _service;

    public OpinionServiceTests()
    {
        // In-memory baza za testove
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;

        _db                  = new ApplicationDbContext(options);
        _notificationService = Substitute.For<INotificationService>();
        _documentService     = Substitute.For<IDocumentService>();
        _userRoleProvider    = Substitute.For<IUserRoleProvider>();
        _auditService        = Substitute.For<IAuditService>();

        // Šifarnik tipova dokumenata — potreban za klasifikaciju mišljenja prilikom importa
        _db.CodebookValues.AddRange(
            CodebookValue.Create("tipovi_dokumenata", "MISLJENJE_CO", "Mišljenje CO", null, 1, null, isSystem: true),
            CodebookValue.Create("tipovi_dokumenata", "MISLJENJE_PRAVNA", "Mišljenje Pravne službe", null, 2, null, isSystem: true));
        _db.SaveChanges();

        // UserRoleProvider uvijek vraća praznu listu (testovi ne testuju notifikacije)
        _userRoleProvider
            .GetUsersWithRolesAsync(Arg.Any<UserRoleListRequest>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromResult(new PagedResult<UserRoleSourceItem> { Items = [], TotalCount = 0, Page = 1, PageSize = 100 }));

        _service = new OpinionService(
            _db,
            _notificationService,
            _documentService,
            _userRoleProvider,
            _auditService,
            NullLogger<OpinionService>.Instance);
    }

    // ── RequestOpinions ───────────────────────────────────────────────────────

    [Fact]
    public async Task RequestOpinionsAsync_KreiraOpinionRedoveZaCoIPravnu()
    {
        // Arrange
        var order = CreateTestOrder();
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        // Act
        await _service.RequestOpinionsAsync(order.Id);

        // Assert
        var opinions = _db.Opinions.Where(o => o.AppraisalOrderId == order.Id).ToList();
        Assert.Equal(2, opinions.Count);
        Assert.Contains(opinions, o => o.OpinionType == OpinionType.CO);
        Assert.Contains(opinions, o => o.OpinionType == OpinionType.Pravna);
        Assert.All(opinions, o => Assert.Equal(OpinionStatus.Requested, o.Status));
    }

    [Fact]
    public async Task RequestOpinionsAsync_KreiraTaskItemoveZaCoIPravnu()
    {
        // Arrange
        var order = CreateTestOrder();
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        // Act
        await _service.RequestOpinionsAsync(order.Id);

        // Assert
        var tasks = _db.TaskItems.Where(t => t.AppraisalOrderId == order.Id).ToList();
        Assert.Equal(2, tasks.Count);
        Assert.Contains(tasks, t => t.AssignedRole == AppRoles.KolateralOficir);
        Assert.Contains(tasks, t => t.AssignedRole == AppRoles.PravnaSluzba);
        Assert.All(tasks, t => Assert.Equal(TaskItemType.RequestOpinion, t.TaskType));
    }

    [Fact]
    public async Task RequestOpinionsAsync_BacaExceptionAkoNarudzbaNePostoji()
    {
        // Act & Assert
        await Assert.ThrowsAsync<InvalidOperationException>(
            () => _service.RequestOpinionsAsync(999));
    }

    // ── SubmitOpinion ─────────────────────────────────────────────────────────

    [Fact]
    public async Task SubmitOpinionAsync_SetiraStatusNaImported()
    {
        // Arrange
        var order = CreateTestOrder();
        _db.AppraisalOrders.Add(order);
        _db.Opinions.Add(Opinion.CreateRequested(order.Id, OpinionType.CO));
        await _db.SaveChangesAsync();

        SetupDocumentServiceSubstitute();

        // Act
        await _service.SubmitOpinionAsync(
            order.Id, OpinionType.CO,
            Stream.Null, "misljenje.pdf", "application/pdf",
            "Komentar CO", "user-co-id");

        // Assert
        var opinion = _db.Opinions.First(o => o.OpinionType == OpinionType.CO);
        Assert.Equal(OpinionStatus.Imported, opinion.Status);
        Assert.Equal("Komentar CO", opinion.Comment);
        Assert.Equal("user-co-id", opinion.ImportedByUserId);
    }

    [Fact]
    public async Task SubmitOpinionAsync_KadSuObaImportovana_SetiraOpinionsCompletedAt()
    {
        // Arrange
        var order = CreateTestOrder();
        _db.AppraisalOrders.Add(order);
        _db.Opinions.Add(Opinion.CreateRequested(order.Id, OpinionType.CO));
        _db.Opinions.Add(Opinion.CreateRequested(order.Id, OpinionType.Pravna));
        await _db.SaveChangesAsync();

        SetupDocumentServiceSubstitute();

        // Act — importuj oba
        await _service.SubmitOpinionAsync(
            order.Id, OpinionType.CO,
            Stream.Null, "co.pdf", "application/pdf", null, "user-co");

        await _service.SubmitOpinionAsync(
            order.Id, OpinionType.Pravna,
            Stream.Null, "pravna.pdf", "application/pdf", null, "user-pravna");

        // Assert
        var updatedOrder = _db.AppraisalOrders.First(o => o.Id == order.Id);
        Assert.NotNull(updatedOrder.OpinionsCompletedAt);
    }

    [Fact]
    public async Task SubmitOpinionAsync_KadJeSamoJedanImportovan_NeSaljeNotifikaciju()
    {
        // Arrange
        var order = CreateTestOrder();
        _db.AppraisalOrders.Add(order);
        _db.Opinions.Add(Opinion.CreateRequested(order.Id, OpinionType.CO));
        _db.Opinions.Add(Opinion.CreateRequested(order.Id, OpinionType.Pravna));
        await _db.SaveChangesAsync();

        SetupDocumentServiceSubstitute();

        // Act — importuj samo CO
        await _service.SubmitOpinionAsync(
            order.Id, OpinionType.CO,
            Stream.Null, "co.pdf", "application/pdf", null, "user-co");

        // Assert — notifikacija se NE šalje jer Pravna još nije importovala
        await _notificationService.DidNotReceive().NotifyUsersAsync(
            Arg.Any<IEnumerable<string>>(),
            Arg.Is<string>(s => s.Contains("Završen")),
            Arg.Any<string>(),
            Arg.Any<string?>(),
            Arg.Any<string?>(),
            Arg.Any<CancellationToken>());
    }

    // ── GetOpinions ───────────────────────────────────────────────────────────

    [Fact]
    public async Task GetOpinionsAsync_VracaOpinionDtoListe()
    {
        // Arrange
        var order = CreateTestOrder();
        _db.AppraisalOrders.Add(order);
        _db.Opinions.Add(Opinion.CreateRequested(order.Id, OpinionType.CO));
        _db.Opinions.Add(Opinion.CreateRequested(order.Id, OpinionType.Pravna));
        await _db.SaveChangesAsync();

        // Act
        var result = await _service.GetOpinionsAsync(order.Id);

        // Assert
        Assert.Equal(2, result.Count);
        Assert.Contains(result, o => o.OpinionType == OpinionType.CO);
        Assert.Contains(result, o => o.OpinionType == OpinionType.Pravna);
    }

    [Fact]
    public async Task GetOpinionsAsync_VracaPraznaListaAkoNemaOpiniona()
    {
        // Arrange
        var order = CreateTestOrder();
        _db.AppraisalOrders.Add(order);
        await _db.SaveChangesAsync();

        // Act
        var result = await _service.GetOpinionsAsync(order.Id);

        // Assert
        Assert.Empty(result);
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    private AppraisalOrder CreateTestOrder()
    {
        return AppraisalOrder.Create(
            orderNumber:              "TEST-001",
            title:                    "Test narudžba",
            clientName:               "Test Klijent",
            clientType:               "FL",
            clientIdentifier:         "1234567890123",
            contactName:              null,
            contactPhone:             null,
            contactEmail:             null,
            city:                     "Sarajevo",
            branch:                   "Sarajevo",
            branchAddress:            null,
            propertyAddress:          "Testna ulica 1",
            collateralTypeId:         null,
            combinedCollateralTypeId: null,
            createdByUserId:          "user-test",
            createdByRole:            AppRoles.AM,
            createdByName:            null,
            deliveryContactName:      null,
            amRecipientName:          null);
    }

    private void SetupDocumentServiceSubstitute()
    {
        _documentService
            .UploadAsync(
                Arg.Any<int>(),
                Arg.Any<int>(),
                Arg.Any<IReadOnlyList<DocumentUploadFile>>(),
                Arg.Any<CancellationToken>())
            .Returns(callInfo =>
            {
                // Use ArgAt to avoid AmbiguousArgumentsException when multiple int args exist
                var orderId        = callInfo.ArgAt<int>(0);
                var documentTypeId = callInfo.ArgAt<int>(1);
                var files          = callInfo.ArgAt<IReadOnlyList<DocumentUploadFile>>(2);
                IReadOnlyList<DocumentDto> result = new List<DocumentDto>
                {
                    new(1, orderId, documentTypeId, files[0].FileName, files[0].FileName,
                        files[0].ContentType, files[0].Length, DateTime.UtcNow, "user-test",
                        "/api/documents/1/download", 1, null, true)
                };
                return Task.FromResult(result);
            });
    }
}
