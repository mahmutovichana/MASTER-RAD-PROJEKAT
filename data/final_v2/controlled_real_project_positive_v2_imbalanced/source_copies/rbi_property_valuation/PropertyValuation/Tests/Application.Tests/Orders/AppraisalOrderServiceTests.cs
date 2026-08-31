// CS0618: AppraisalOrder.ChangeStatus() is marked [Obsolete] in production code.
// In tests, deliberately using this method to bypass the state machine and set up
// arbitrary order states for test scenarios â€” this is intentional and acceptable.
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Common.Validation;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Application.Orders.Requests;
using RBBH.CollateralAppraisal.Application.Tests.Helpers;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Domain.Orders;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

public sealed class AppraisalOrderServiceTests : IDisposable
{
    private readonly ApplicationDbContext  _db;
    private readonly ICurrentUserService   _user;
    private readonly IAuditService         _audit;
    private readonly INotificationProvider _notify;
    private readonly AppraisalOrderService _sut;
    private OrderQueryService QuerySvc => new(_db, _user, Substitute.For<IUserRoleProvider>());
    private const string CaInboxEmail = "narudzbe.procjena@rbibh.local";

    // Seeded codebook value IDs
    private int _collateralTypeId;
    private int _combinedTypeId;
    private int _garazaTypeId;

    public AppraisalOrderServiceTests()
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
        _user.Role.Returns("AM");
        _user.Roles.Returns(["AM"]);
        _user.IsAuthenticated.Returns(true);

        _sut = BuildSut(new OrderNotificationsOptions { CaInboxEmail = CaInboxEmail });

        SeedCodebookValues();
    }

    private void SeedCodebookValues()
    {
        var collateral = CodebookValue.Create(
            "tipovi_kolaterala", "APP_STAN", "Stan", null, 10, "system-seed");
        _db.CodebookValues.Add(collateral);

        var combined = CodebookValue.Create(
            "kombinovani_tipovi_kolaterala", "APP_STAN_I_GARAZA", "APP-stan i garaža", null, 10, "system-seed");
        _db.CodebookValues.Add(combined);

        var garaza = CodebookValue.Create(
            "tipovi_kolaterala", "GARAZA", "Garaža", null, 20, "system-seed");
        _db.CodebookValues.Add(garaza);

        _db.SaveChanges();

        _collateralTypeId = collateral.Id;
        _combinedTypeId   = combined.Id;
        _garazaTypeId     = garaza.Id;
    }

    private AppraisalOrderService BuildSut(OrderNotificationsOptions? notifOptions = null)
    {
        var opts = notifOptions ?? new OrderNotificationsOptions { CaInboxEmail = CaInboxEmail };
        var createSvc = new OrderCreateService(
            _db, _user, new OrderTitleGenerator(), new FakeOrderNumberGenerator(), _audit, new FakeClock());
        var submitSvc = new OrderSubmitService(
            _db, _user, _notify, _audit,
            Substitute.For<ILogger<OrderSubmitService>>(),
            Options.Create(opts),
            Options.Create(new WorkflowSlaOptions()),
            new FakeClock());
        return new AppraisalOrderService(_db, _user, _audit, createSvc, submitSvc);
    }

    private CreateOrderRequest ValidRequest(int? combinedId = null) =>
        new CreateOrderRequest(
            ClientName:               "Petar Petrovic",
            ClientType:               "FL",
            ClientIdentifier:         "0101990000019",
            CollateralTypeId:         _collateralTypeId,
            CombinedCollateralTypeId: combinedId,
            City:                     "Sarajevo",
            PropertyAddress:          "Obala 1",
            Branch:                   "POS_SARAJEVO_CENTAR",
            BranchAddress:            "Titova 1",
            ContactName:              "Petar Petrovic",
            ContactPhone:             "061-123-456",
            ContactEmail:             "petar@test.ba",
            InternalNote:             null,
            DeliveryContactName:      "Amina Dostavljac",
            AmRecipientName:          "Amar Primalac",
            RequestReceivedAt:        new DateTime(2026, 6, 1, 9, 0, 0, DateTimeKind.Utc));

    //  Happy path: Create 

    [Fact]
    public async Task CreateAsync_ValidRequest_ReturnsDto()
    {
        var dto = await _sut.CreateAsync(ValidRequest());

        Assert.NotNull(dto);
        Assert.Equal("Petar Petrovic", dto.ClientName);
        Assert.Equal("Draft",          dto.Status);
        Assert.Contains("Stan",        dto.Title);
        Assert.Contains("Sarajevo",    dto.Title);
    }

    [Fact]
    public async Task CreateAsync_WithCombinedType_TitleUsesCombinedLabel()
    {
        var dto = await _sut.CreateAsync(ValidRequest(combinedId: _combinedTypeId));

        Assert.Contains("APP-stan i garaža", dto.Title);
    }

    [Fact]
    public async Task CreateAsync_SavesOrderToDb()
    {
        await _sut.CreateAsync(ValidRequest());

        var count = await _db.AppraisalOrders.CountAsync();
        Assert.Equal(1, count);
    }

    [Theory]
    [InlineData("AM")]
    [InlineData("SM")]
    [InlineData("UB")]
    public async Task CreateAsync_SalesRoles_Succeed(string role)
    {
        _user.Role.Returns(role);
        _user.Roles.Returns([role]);

        var dto = await _sut.CreateAsync(ValidRequest());

        Assert.NotNull(dto);
        Assert.Equal("Draft", dto.Status);
    }

    [Fact]
    public async Task CreateAsync_RecordsAuditEvent()
    {
        await _sut.CreateAsync(ValidRequest());

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.OrderCreated),
            Arg.Any<CancellationToken>());
    }

    //  Sad path: Create 

    [Fact]
    public async Task CreateAsync_MissingClientName_ThrowsValidation()
    {
        var req = ValidRequest() with { ClientName = "" };

        await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(req));
    }

    [Fact]
    public async Task CreateAsync_MissingCity_ThrowsValidation()
    {
        var req = ValidRequest() with { City = "" };

        await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(req));
    }

    [Fact]
    public async Task CreateAsync_MissingContactPhone_ThrowsValidation()
    {
        var req = ValidRequest() with { ContactPhone = "" };

        await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(req));
    }

    [Fact]
    public async Task CreateAsync_InvalidCollateralTypeId_ThrowsValidation()
    {
        var req = ValidRequest() with { CollateralTypeId = 9999 };

        await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(req));
    }

    [Fact]
    public async Task CreateAsync_MissingClientType_ThrowsValidationWithRequiredClientType()
    {
        var req = ValidRequest() with { ClientType = null };

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(req));

        Assert.Contains(ex.FieldErrors!, e => e.Code == ValidationErrorCodes.RequiredClientType);
    }

    [Fact]
    public async Task CreateAsync_CombinedCollateralWithNonAppStanBase_ThrowsInvalidCombinedCollateralBase()
    {
        var req = ValidRequest(combinedId: _combinedTypeId) with { CollateralTypeId = _garazaTypeId };

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(req));

        Assert.Contains(ex.FieldErrors!, e => e.Code == ValidationErrorCodes.InvalidCombinedCollateralBase);
    }

    [Theory]
    [InlineData("Petar123")]
    [InlineData("Petar@Petrovi")]
    public async Task CreateAsync_ClientNameWithDigitsOrSpecialChars_FL_ThrowsInvalidNameFormat(string clientName)
    {
        var req = ValidRequest() with { ClientName = clientName };

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(req));

        Assert.Contains(ex.FieldErrors!, e => e.Code == ValidationErrorCodes.InvalidNameFormat && e.Field == "clientName");
    }

    [Theory]
    [InlineData("Petar123")]
    [InlineData("Petar@Petrovi")]
    public async Task CreateAsync_ContactNameWithDigitsOrSpecialChars_ThrowsInvalidNameFormat(string contactName)
    {
        var req = ValidRequest() with { ContactName = contactName };

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(req));

        Assert.Contains(ex.FieldErrors!, e => e.Code == ValidationErrorCodes.InvalidNameFormat && e.Field == "contactName");
    }

    [Fact]
    public async Task CreateAsync_InvalidPhoneFormat_ThrowsInvalidPhoneFormat()
    {
        var req = ValidRequest() with { ContactPhone = "123" };

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(req));

        Assert.Contains(ex.FieldErrors!, e => e.Code == ValidationErrorCodes.InvalidPhoneFormat);
    }

    [Fact]
    public async Task CreateAsync_MissingClientIdentifier_FL_ThrowsRequiredJmbg()
    {
        var req = ValidRequest() with { ClientIdentifier = null };

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(req));

        Assert.Contains(ex.FieldErrors!, e => e.Code == ValidationErrorCodes.RequiredJmbg && e.Field == "clientIdentifier");
    }

    [Fact]
    public async Task CreateAsync_MissingClientIdentifier_PL_ThrowsRequiredJmbg()
    {
        var req = ValidRequest() with { ClientType = "PL", ClientIdentifier = null };

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(req));

        Assert.Contains(ex.FieldErrors!, e => e.Code == ValidationErrorCodes.RequiredJmbg && e.Field == "clientIdentifier");
    }

    [Fact]
    public async Task CreateAsync_MissingBranchAddress_ThrowsValidation()
    {
        var req = ValidRequest() with { BranchAddress = null };

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(req));

        Assert.Contains(ex.FieldErrors!, e => e.Code == ValidationErrorCodes.RequiredField && e.Field == "branchAddress");
    }

    [Fact]
    public async Task CreateAsync_MissingPropertyAddress_ThrowsValidation()
    {
        var req = ValidRequest() with { PropertyAddress = null };

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(req));

        Assert.Contains(ex.FieldErrors!, e => e.Code == ValidationErrorCodes.RequiredField && e.Field == "propertyAddress");
    }

    [Fact]
    public async Task CreateAsync_CollateralAndCombinedBothMissing_ThrowsRequiredField()
    {
        var req = ValidRequest() with { CollateralTypeId = 0, CombinedCollateralTypeId = null };

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(req));

        Assert.Contains(ex.FieldErrors!, e => e.Code == ValidationErrorCodes.RequiredField && e.Field == "collateralTypeId");
    }

    //  Update Draft 

    private static UpdateOrderRequest EmptyUpdateRequest() => new(
        ClientName:               null,
        ClientType:               null,
        ClientIdentifier:         null,
        CollateralTypeId:         null,
        CombinedCollateralTypeId: null,
        City:                     null,
        PropertyAddress:          null,
        Branch:                   null,
        BranchAddress:            null,
        ContactName:              null,
        ContactPhone:             null,
        ContactEmail:             null,
        InternalNote:             null);

    [Fact]
    public async Task UpdateDraftAsync_RecordsAuditEventWithChangedFieldsOnly()
    {
        var created = await _sut.CreateAsync(ValidRequest());

        var req = EmptyUpdateRequest() with { ClientName = "Marko Markovic", City = "Mostar", Branch = "POS_MOSTAR" };

        AuditEvent? captured = null;
        await _audit.RecordAsync(
            Arg.Do<AuditEvent>(e => { if (e.Action == AuditActions.OrderDraftUpdated) captured = e; }),
            Arg.Any<CancellationToken>());

        await _sut.UpdateDraftAsync(created.Id, req);

        Assert.NotNull(captured);
        var oldValues = Assert.IsType<Dictionary<string, object?>>(captured!.OldValues);
        var newValues = Assert.IsType<Dictionary<string, object?>>(captured!.NewValues);

        Assert.Equal("Petar Petrovic", oldValues["ClientName"]);
        Assert.Equal("Marko Markovic", newValues["ClientName"]);
        Assert.Equal("Sarajevo", oldValues["City"]);
        Assert.Equal("Mostar", newValues["City"]);

        // Nepromijenjena polja se ne pojavljuju u diff-u
        Assert.False(oldValues.ContainsKey("ContactPhone"));
        Assert.False(newValues.ContainsKey("ContactPhone"));
    }

    [Fact]
    public async Task UpdateDraftAsync_NoChanges_RecordsAuditEventWithoutDiff()
    {
        var created = await _sut.CreateAsync(ValidRequest());

        AuditEvent? captured = null;
        await _audit.RecordAsync(
            Arg.Do<AuditEvent>(e => { if (e.Action == AuditActions.OrderDraftUpdated) captured = e; }),
            Arg.Any<CancellationToken>());

        await _sut.UpdateDraftAsync(created.Id, EmptyUpdateRequest());

        Assert.NotNull(captured);
        Assert.Null(captured!.OldValues);
        Assert.Null(captured!.NewValues);
    }

    [Fact]
    public async Task UpdateDraftAsync_WithAutosaveTrue_RecordsAutosavedAuditEvent()
    {
        var created = await _sut.CreateAsync(ValidRequest());

        var req = EmptyUpdateRequest() with { ClientName = "Marko Markovic" };

        AuditEvent? captured = null;
        await _audit.RecordAsync(
            Arg.Do<AuditEvent>(e => { if (e.Action == AuditActions.OrderDraftAutosaved) captured = e; }),
            Arg.Any<CancellationToken>());

        await _sut.UpdateDraftAsync(created.Id, req, isAutosave: true);

        Assert.NotNull(captured);
        await _audit.DidNotReceive().RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.OrderDraftUpdated),
            Arg.Any<CancellationToken>());
    }

    //  Create Draft (autosave) 

    [Fact]
    public async Task CreateDraftAsync_CreatesEmptyDraftAndRecordsAudit()
    {
        AuditEvent? captured = null;
        await _audit.RecordAsync(
            Arg.Do<AuditEvent>(e => { if (e.Action == AuditActions.OrderDraftCreated) captured = e; }),
            Arg.Any<CancellationToken>());

        var dto = await _sut.CreateDraftAsync();

        Assert.Equal("Draft", dto.Status);
        Assert.Equal(string.Empty, dto.ClientName);
        Assert.Equal("Nacrt narudžbe", dto.Title);
        Assert.False(string.IsNullOrWhiteSpace(dto.OrderNumber));
        Assert.Null(dto.ClientType);
        Assert.Null(dto.CollateralTypeId);

        Assert.NotNull(captured);
        Assert.Equal(dto.Id.ToString(), captured!.EntityKey);
    }

    //  Happy path: Submit 

    [Fact]
    public async Task SubmitAsync_DraftOrder_ChangesStatusAndCreatesTask()
    {
        var created = await _sut.CreateAsync(ValidRequest());

        var submitted = await _sut.SubmitAsync(created.Id);

        Assert.Equal("SubmittedBySales", submitted.Status);
        var tasks = await _db.TaskItems.ToListAsync();
        Assert.Single(tasks);
        Assert.Equal(TaskItemType.AcceptCAOrder, tasks[0].TaskType);
    }

    [Fact]
    public async Task SubmitAsync_DoesNotCreateProtocol_ProtocolMovedToAppraiserSelection()
    {
        var created = await _sut.CreateAsync(ValidRequest());
        await _sut.SubmitAsync(created.Id);

        var protocols = await _db.OrderProtocolEntries.ToListAsync();
        Assert.Empty(protocols);
    }

    [Fact]
    public async Task SubmitAsync_SendsCANotification()
    {
        var created = await _sut.CreateAsync(ValidRequest());
        await _sut.SubmitAsync(created.Id);

        await _notify.Received(1).SendAsync(
            Arg.Is<NotificationRequest>(r => r.RecipientRole == "KolateralAdministrator" && r.Channel == NotificationChannel.InApp),
            Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task SubmitAsync_CANotification_MentionsInitiatorRole()
    {
        // _user.Role je "AM" (vidi konstruktor)  notifikacija prema CA mora
        // navesti koja AM/SM/UB rola je inicirala narudzbu (zahtjev US-1/US-2).
        var created = await _sut.CreateAsync(ValidRequest());
        await _sut.SubmitAsync(created.Id);

        await _notify.Received(1).SendAsync(
            Arg.Is<NotificationRequest>(r =>
                r.RecipientRole == "KolateralAdministrator" &&
                r.Channel        == NotificationChannel.InApp &&
                r.Message.Contains("od strane AM") &&
                r.Message.Contains("za klijenta Petar Petrovi") &&
                r.Message.Contains("grad Sarajevo")),
            Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task SubmitAsync_SendsEmailNotificationToCAInbox()
    {
        var created = await _sut.CreateAsync(ValidRequest());
        await _sut.SubmitAsync(created.Id);

        await _notify.Received(1).SendAsync(
            Arg.Is<NotificationRequest>(r =>
                r.Channel == NotificationChannel.Email &&
                r.RecipientRole == "KolateralAdministrator" &&
                r.RecipientEmail == CaInboxEmail),
            Arg.Any<CancellationToken>());

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.CaEmailNotificationSent),
            Arg.Any<CancellationToken>());
    }

    //  Sad path: Submit 

    [Fact]
    public async Task SubmitAsync_AlreadySubmitted_ThrowsValidation()
    {
        var created = await _sut.CreateAsync(ValidRequest());
        await _sut.SubmitAsync(created.Id);

        await Assert.ThrowsAsync<ValidationException>(() => _sut.SubmitAsync(created.Id));
    }

    [Fact]
    public async Task SubmitAsync_NotFound_ThrowsNotFound()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.SubmitAsync(9999));
    }

    //  Permission tests 

    [Fact]
    public async Task GetByIdAsync_DifferentOwner_ThrowsForbidden()
    {
        var created = await _sut.CreateAsync(ValidRequest());

        // Simuliramo drugog korisnika
        _user.UserId.Returns("other-user");
        _user.Roles.Returns(["AM"]);

        await Assert.ThrowsAsync<ForbiddenException>(() => _sut.GetByIdAsync(created.Id));
    }

    [Fact]
    public async Task CancelAsync_NotOwner_ThrowsForbidden()
    {
        var created = await _sut.CreateAsync(ValidRequest());

        _user.UserId.Returns("not-the-owner");
        _user.Roles.Returns(["AM"]);

        await Assert.ThrowsAsync<ForbiddenException>(() => _sut.CancelAsync(created.Id));
    }

    [Fact]
    public async Task CancelAsync_AdminCanCancelOtherUsersOrder()
    {
        var created = await _sut.CreateAsync(ValidRequest());

        _user.UserId.Returns("admin-user");
        _user.Roles.Returns(["Administrator"]);

        // Ne smije baciti izuzetak
        await _sut.CancelAsync(created.Id);

        var order = await _db.AppraisalOrders.IgnoreQueryFilters()
            .FirstAsync(o => o.Id == created.Id);
        Assert.True(order.IsDeleted);
    }

    //  Dashboard summary 

    [Fact]
    public async Task GetSummaryAsync_ReturnsCountsPerStatusBucket()
    {
        await _sut.CreateDraftAsync();                            // Draft

        var submitted = await _sut.CreateAsync(ValidRequest());
        await _sut.SubmitAsync(submitted.Id);                     // SubmittedBySales

        var inProgress = await _sut.CreateAsync(ValidRequest());
        var inProgressEntity = await _db.AppraisalOrders.FirstAsync(o => o.Id == inProgress.Id);
        inProgressEntity.ChangeStatus(AppraisalOrderStatus.AcceptedByCA, DateTime.UtcNow);

        var completed = await _sut.CreateAsync(ValidRequest());
        var completedEntity = await _db.AppraisalOrders.FirstAsync(o => o.Id == completed.Id);
        completedEntity.ChangeStatus(AppraisalOrderStatus.Completed, DateTime.UtcNow);

        var cancelled = await _sut.CreateAsync(ValidRequest());
        var cancelledEntity = await _db.AppraisalOrders.FirstAsync(o => o.Id == cancelled.Id);
        cancelledEntity.ChangeStatus(AppraisalOrderStatus.Cancelled, DateTime.UtcNow);

        await _db.SaveChangesAsync();

        var summary = await QuerySvc.GetSummaryAsync();

        Assert.Equal(5, summary.Total);
        Assert.Equal(1, summary.Draft);
        Assert.Equal(1, summary.SubmittedBySales);
        Assert.Equal(1, summary.InProgress);
        Assert.Equal(1, summary.Completed);
        Assert.Equal(1, summary.Cancelled);
    }

    [Fact]
    public async Task GetSummaryAsync_SalesRole_OnlyCountsOwnOrders()
    {
        await _sut.CreateAsync(ValidRequest());
        await _sut.CreateAsync(ValidRequest());

        _user.UserId.Returns("other-user");
        _user.Roles.Returns(["AM"]);

        var summary = await QuerySvc.GetSummaryAsync();

        Assert.Equal(0, summary.Total);
    }

    //  Filteri liste narudzbi ("Pregled narudžbi") 

    [Fact]
    public async Task GetListAsync_StatusFilter_InProgress_ReturnsOnlyInProgressBucket()
    {
        await _sut.CreateDraftAsync();                            // Draft

        var submitted = await _sut.CreateAsync(ValidRequest());
        await _sut.SubmitAsync(submitted.Id);                     // SubmittedBySales

        var inProgress = await _sut.CreateAsync(ValidRequest());
        var inProgressEntity = await _db.AppraisalOrders.FirstAsync(o => o.Id == inProgress.Id);
        inProgressEntity.ChangeStatus(AppraisalOrderStatus.AcceptedByCA, DateTime.UtcNow);
        await _db.SaveChangesAsync();

        var result = await QuerySvc.GetListAsync(new OrderListRequest(Status: "InProgress"));

        Assert.Equal(1, result.TotalCount);
        Assert.Equal(inProgress.Id, result.Items.Single().Id);
    }

    [Fact]
    public async Task GetListAsync_CityFilter_ReturnsOnlyMatchingCity()
    {
        await _sut.CreateAsync(ValidRequest());                                                 // Sarajevo
        await _sut.CreateAsync(ValidRequest() with { City = "Banja Luka", Branch = "POS_BANJA_LUKA" });

        var result = await QuerySvc.GetListAsync(new OrderListRequest(City: "Banja Luka"));

        Assert.Equal(1, result.TotalCount);
        Assert.Equal("Banja Luka", result.Items.Single().City);
    }

    [Fact]
    public async Task GetListAsync_AppraisalTypeFilter_Stan_ExcludesGarazaAndCombined()
    {
        await _sut.CreateAsync(ValidRequest());                                                 // Stan
        await _sut.CreateAsync(ValidRequest() with { CollateralTypeId = _garazaTypeId });        // Garaža
        await _sut.CreateAsync(ValidRequest(combinedId: _combinedTypeId));                       // Kombinovana

        var result = await QuerySvc.GetListAsync(new OrderListRequest(AppraisalType: "STAN"));

        Assert.Equal(1, result.TotalCount);
        Assert.Equal("Stan", result.Items.Single().CollateralTypeLabel);
    }

    [Fact]
    public async Task GetListAsync_AppraisalTypeFilter_StanIGaraza_ReturnsOnlyThatCombinedType()
    {
        await _sut.CreateAsync(ValidRequest());                            // Stan (bez kombinovanog)
        await _sut.CreateAsync(ValidRequest(combinedId: _combinedTypeId)); // Stan i garaža

        var result = await QuerySvc.GetListAsync(new OrderListRequest(AppraisalType: "STAN_I_GARAZA"));

        Assert.Equal(1, result.TotalCount);
        Assert.NotNull(result.Items.Single().CombinedCollateralTypeLabel);
    }

    [Fact]
    public async Task GetListAsync_AppraisalTypeFilter_Stan_ExcludesCombinedTypes()
    {
        await _sut.CreateAsync(ValidRequest());                            // Stan (bez kombinovanog)
        await _sut.CreateAsync(ValidRequest(combinedId: _combinedTypeId)); // Stan i garaža

        var result = await QuerySvc.GetListAsync(new OrderListRequest(AppraisalType: "STAN"));

        Assert.Equal(1, result.TotalCount);
        Assert.Null(result.Items.Single().CombinedCollateralTypeLabel);
    }

    [Fact]
    public async Task GetListAsync_CreatedToFilter_IncludesOrdersCreatedSameDay()
    {
        await _sut.CreateAsync(ValidRequest());

        // "Kreirano do" je datum (bez vremena)  mora obuhvatiti CIJELI taj dan,
        // ne samo do ponoi, jer su narudzbe kreirane sa stvarnim timestamp-om.
        var result = await QuerySvc.GetListAsync(new OrderListRequest(CreatedTo: DateTime.UtcNow.Date));

        Assert.Equal(1, result.TotalCount);
    }

    [Fact]
    public async Task GetListAsync_CreatedToFilter_ExcludesOrdersAfterRange()
    {
        await _sut.CreateAsync(ValidRequest());

        var result = await QuerySvc.GetListAsync(new OrderListRequest(CreatedTo: DateTime.UtcNow.Date.AddDays(-1)));

        Assert.Equal(0, result.TotalCount);
    }

    [Fact]
    public async Task GetListAsync_CreatedFromFilter_IncludesOrdersFromToday()
    {
        await _sut.CreateAsync(ValidRequest());

        var result = await QuerySvc.GetListAsync(new OrderListRequest(CreatedFrom: DateTime.UtcNow.Date));

        Assert.Equal(1, result.TotalCount);
    }

    [Fact]
    public async Task GetListAsync_CreatedFromFilter_ExcludesOrdersBeforeRange()
    {
        await _sut.CreateAsync(ValidRequest());

        var result = await QuerySvc.GetListAsync(new OrderListRequest(CreatedFrom: DateTime.UtcNow.Date.AddDays(1)));

        Assert.Equal(0, result.TotalCount);
    }

    [Fact]
    public async Task GetListAsync_DateRangeFilter_WithUnspecifiedKind_MatchesOrderCreatedToday()
    {
        // ASP.NET model binding parsira query-string datume ("?createdFrom=2026-06-14")
        // u DateTime sa Kind=Unspecified. AppraisalOrderService mora ovo normalizovati
        // na Utc prije poreenja sa "created_at" (timestamptz kolona)  u suprotnom
        // SQL Server provider baca "Cannot write DateTime with Kind=Unspecified to SQL Server type
        // 'timestamp with time zone'" na pravoj bazi (InMemory provider ovo ne provjerava).
        await _sut.CreateAsync(ValidRequest());

        var today = DateTime.SpecifyKind(DateTime.UtcNow.Date, DateTimeKind.Unspecified);
        var result = await QuerySvc.GetListAsync(new OrderListRequest(CreatedFrom: today, CreatedTo: today));

        Assert.Equal(1, result.TotalCount);
    }

    [Fact]
    public async Task GetListAsync_SearchFilter_MatchesClientNameCaseInsensitive()
    {
        await _sut.CreateAsync(ValidRequest());
        await _sut.CreateAsync(ValidRequest() with { ClientName = "Marko Markovic", ContactName = "Marko Markovic" });

        var result = await QuerySvc.GetListAsync(new OrderListRequest(Search: "marko"));

        Assert.Equal(1, result.TotalCount);
        Assert.Equal("Marko Markovic", result.Items.Single().ClientName);
    }

    [Fact]
    public async Task GetListAsync_SearchFilter_MatchesOrderNumber()
    {
        var created = await _sut.CreateAsync(ValidRequest());
        await _sut.CreateAsync(ValidRequest() with { ClientName = "Marko Markovic", ContactName = "Marko Markovic" });

        var result = await QuerySvc.GetListAsync(new OrderListRequest(Search: created.OrderNumber.ToLower()));

        Assert.Equal(1, result.TotalCount);
        Assert.Equal(created.Id, result.Items.Single().Id);
    }

    [Fact]
    public async Task GetListAsync_CollateralTypeIdFilter_ReturnsOnlyMatchingType()
    {
        await _sut.CreateAsync(ValidRequest());                                          // Stan
        await _sut.CreateAsync(ValidRequest() with { CollateralTypeId = _garazaTypeId }); // Garaža

        var result = await QuerySvc.GetListAsync(new OrderListRequest(CollateralTypeId: _garazaTypeId));

        Assert.Equal(1, result.TotalCount);
        Assert.Equal("Garaža", result.Items.Single().CollateralTypeLabel);
    }

    [Fact]
    public async Task GetListAsync_AppraisalTypeFilter_UnknownValue_ReturnsAllOrders()
    {
        await _sut.CreateAsync(ValidRequest());
        await _sut.CreateAsync(ValidRequest() with { CollateralTypeId = _garazaTypeId });

        var result = await QuerySvc.GetListAsync(new OrderListRequest(AppraisalType: "NEPOZNATO"));

        Assert.Equal(2, result.TotalCount);
    }

    [Fact]
    public async Task GetListAsync_AppraisalTypeFilter_OstavaWithoutCodebookEntry_ReturnsAllOrders()
    {
        await _sut.CreateAsync(ValidRequest());
        await _sut.CreateAsync(ValidRequest() with { CollateralTypeId = _garazaTypeId });

        var result = await QuerySvc.GetListAsync(new OrderListRequest(AppraisalType: "OSTAVA"));

        Assert.Equal(2, result.TotalCount);
    }

    [Fact]
    public async Task GetListAsync_SortByOrderNumberAscending_OrdersByOrderNumber()
    {
        var first  = await _sut.CreateAsync(ValidRequest());
        var second = await _sut.CreateAsync(ValidRequest());

        var result = await QuerySvc.GetListAsync(new OrderListRequest(SortBy: "OrderNumber", SortDescending: false));

        Assert.Equal(first.OrderNumber, result.Items[0].OrderNumber);
        Assert.Equal(second.OrderNumber, result.Items[1].OrderNumber);
    }

    [Fact]
    public async Task GetListAsync_SortByOrderNumberDescending_OrdersByOrderNumberDescending()
    {
        var first  = await _sut.CreateAsync(ValidRequest());
        var second = await _sut.CreateAsync(ValidRequest());

        var result = await QuerySvc.GetListAsync(new OrderListRequest(SortBy: "OrderNumber", SortDescending: true));

        Assert.Equal(second.OrderNumber, result.Items[0].OrderNumber);
        Assert.Equal(first.OrderNumber, result.Items[1].OrderNumber);
    }

    [Fact]
    public async Task GetListAsync_SortByTitleAscending_OrdersByTitle()
    {
        await _sut.CreateAsync(ValidRequest());                                          // "...Stan..."
        await _sut.CreateAsync(ValidRequest() with { CollateralTypeId = _garazaTypeId }); // "...Garaža..."

        var result = await QuerySvc.GetListAsync(new OrderListRequest(SortBy: "Title", SortDescending: false));

        Assert.Contains("Garaža", result.Items[0].Title);
        Assert.Contains("Stan",   result.Items[1].Title);
    }

    [Fact]
    public async Task GetListAsync_SortByCityDescending_OrdersByCityDescending()
    {
        await _sut.CreateAsync(ValidRequest());                                              // Sarajevo
        await _sut.CreateAsync(ValidRequest() with { City = "Tuzla", Branch = "POS_TUZLA" }); // Tuzla

        var result = await QuerySvc.GetListAsync(new OrderListRequest(SortBy: "City", SortDescending: true));

        Assert.Equal("Tuzla",    result.Items[0].City);
        Assert.Equal("Sarajevo", result.Items[1].City);
    }

    [Fact]
    public async Task GetListAsync_SortByStatusDescending_OrdersByStatusDescending()
    {
        var draft     = await _sut.CreateAsync(ValidRequest());
        var submitted = await _sut.CreateAsync(ValidRequest());
        await _sut.SubmitAsync(submitted.Id);

        var result = await QuerySvc.GetListAsync(new OrderListRequest(SortBy: "Status", SortDescending: true));

        Assert.Equal(submitted.Id, result.Items[0].Id);
        Assert.Equal(draft.Id,     result.Items[1].Id);
    }

    [Fact]
    public async Task GetListAsync_SortByUpdatedAtDescending_OrdersByUpdatedAtDescending()
    {
        var first  = await _sut.CreateAsync(ValidRequest());
        var second = await _sut.CreateAsync(ValidRequest());

        // Ažuriranje drugog drafta postavlja UpdatedAt na kasniji timestamp
        await _sut.UpdateDraftAsync(second.Id, EmptyUpdateRequest() with { ClientName = "Marko Markovic" });

        var result = await QuerySvc.GetListAsync(new OrderListRequest(SortBy: "UpdatedAt", SortDescending: true));

        Assert.Equal(second.Id, result.Items[0].Id);
        Assert.Equal(first.Id,  result.Items[1].Id);
    }

    [Fact]
    public async Task GetListAsync_DefaultSortAscending_OrdersByCreatedAtAscending()
    {
        var first  = await _sut.CreateAsync(ValidRequest());
        var second = await _sut.CreateAsync(ValidRequest());

        var result = await QuerySvc.GetListAsync(new OrderListRequest(SortDescending: false));

        Assert.Equal(first.Id,  result.Items[0].Id);
        Assert.Equal(second.Id, result.Items[1].Id);
    }

    [Fact]
    public async Task GetListAsync_AdministratorRole_SeesOtherUsersOrders()
    {
        await _sut.CreateAsync(ValidRequest());

        _user.UserId.Returns("admin-user");
        _user.Roles.Returns(["Administrator"]);

        var result = await QuerySvc.GetListAsync(new OrderListRequest());

        Assert.Equal(1, result.TotalCount);
    }

    [Fact]
    public async Task GetListAsync_KolateralAdministratorRole_SeesOtherUsersOrders()
    {
        await _sut.CreateAsync(ValidRequest());

        _user.UserId.Returns("ca-user");
        _user.Roles.Returns(["KolateralAdministrator"]);

        var result = await QuerySvc.GetListAsync(new OrderListRequest());

        Assert.Equal(1, result.TotalCount);
    }

    [Fact]
    public async Task GetListAsync_NonAdminRole_OnlySeesOwnOrders()
    {
        await _sut.CreateAsync(ValidRequest());

        _user.UserId.Returns("other-user");
        _user.Roles.Returns(["AM"]);

        var result = await QuerySvc.GetListAsync(new OrderListRequest());

        Assert.Equal(0, result.TotalCount);
    }

    //  GetByIdAsync 

    [Fact]
    public async Task GetByIdAsync_OwnOrder_ReturnsDtoAndRecordsAudit()
    {
        var created = await _sut.CreateAsync(ValidRequest());

        var dto = await _sut.GetByIdAsync(created.Id);

        Assert.Equal(created.Id, dto.Id);
        Assert.Equal("Stan", dto.CollateralTypeLabel);

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.OrderViewed && e.EntityKey == created.Id.ToString()),
            Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task GetByIdAsync_NonExistentId_ThrowsNotFoundException()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.GetByIdAsync(9999));
    }

    [Fact]
    public async Task GetByIdAsync_WithCombinedType_ResolvesCombinedLabel()
    {
        var created = await _sut.CreateAsync(ValidRequest(combinedId: _combinedTypeId));

        var dto = await _sut.GetByIdAsync(created.Id);

        Assert.Equal("APP-stan i garaža", dto.CombinedCollateralTypeLabel);
    }

    [Fact]
    public async Task GetByIdAsync_AdministratorRole_CanViewOtherUsersOrder()
    {
        var created = await _sut.CreateAsync(ValidRequest());

        _user.UserId.Returns("admin-user");
        _user.Roles.Returns(["Administrator"]);

        var dto = await _sut.GetByIdAsync(created.Id);

        Assert.Equal(created.Id, dto.Id);
    }

    [Fact]
    public async Task GetByIdAsync_KolateralAdministratorRole_CanViewOtherUsersOrder()
    {
        var created = await _sut.CreateAsync(ValidRequest());

        _user.UserId.Returns("ca-user");
        _user.Roles.Returns(["KolateralAdministrator"]);

        var dto = await _sut.GetByIdAsync(created.Id);

        Assert.Equal(created.Id, dto.Id);
    }

    [Fact]
    public async Task GetByIdAsync_DifferentOwner_RecordsUnauthorizedAccessAudit()
    {
        var created = await _sut.CreateAsync(ValidRequest());

        _user.UserId.Returns("other-user");
        _user.Roles.Returns(["AM"]);

        await Assert.ThrowsAsync<ForbiddenException>(() => _sut.GetByIdAsync(created.Id));

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.UnauthorizedOrderAccess && e.EntityKey == created.Id.ToString()),
            Arg.Any<CancellationToken>());
    }

    //  UpdateDraftAsync  sad paths 

    [Fact]
    public async Task UpdateDraftAsync_OrderNotFound_ThrowsNotFoundException()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.UpdateDraftAsync(9999, EmptyUpdateRequest()));
    }

    [Fact]
    public async Task UpdateDraftAsync_NotOwner_ThrowsForbiddenException()
    {
        var created = await _sut.CreateAsync(ValidRequest());

        _user.UserId.Returns("other-user");
        _user.Roles.Returns(["AM"]);

        await Assert.ThrowsAsync<ForbiddenException>(() => _sut.UpdateDraftAsync(created.Id, EmptyUpdateRequest()));
    }

    [Fact]
    public async Task UpdateDraftAsync_NonDraftStatus_ThrowsValidationException()
    {
        var created = await _sut.CreateAsync(ValidRequest());
        await _sut.SubmitAsync(created.Id);

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.UpdateDraftAsync(created.Id, EmptyUpdateRequest()));

        Assert.Equal("Samo narudžbe u statusu Draft se mogu mijenjati.", ex.Errors["status"][0]);
    }

    [Fact]
    public async Task UpdateDraftAsync_InvalidContactNameFormat_ThrowsValidationException()
    {
        var created = await _sut.CreateAsync(ValidRequest());

        var req = EmptyUpdateRequest() with { ContactName = "Petar123" };

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.UpdateDraftAsync(created.Id, req));

        Assert.Contains(ex.FieldErrors!, e => e.Code == ValidationErrorCodes.InvalidNameFormat && e.Field == "contactName");
    }

    [Fact]
    public async Task UpdateDraftAsync_InvalidBranchForCity_ThrowsValidationException()
    {
        var created = await _sut.CreateAsync(ValidRequest()); // City=Sarajevo, Branch=POS_SARAJEVO_CENTAR

        var req = EmptyUpdateRequest() with { Branch = "POS_MOSTAR" };

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.UpdateDraftAsync(created.Id, req));

        Assert.Contains(ex.FieldErrors!, e => e.Code == ValidationErrorCodes.InvalidBranchForCity);
    }

    [Fact]
    public async Task UpdateDraftAsync_InvalidCollateralTypeId_ThrowsValidationException()
    {
        var created = await _sut.CreateAsync(ValidRequest());

        var req = EmptyUpdateRequest() with { CollateralTypeId = 9999 };

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.UpdateDraftAsync(created.Id, req));

        Assert.Equal("Vrijednost šifarnika s ID-om 9999 ne postoji.", ex.Errors["collateralTypeId"][0]);
    }

    [Fact]
    public async Task UpdateDraftAsync_CombinedCollateralWithNonAppStanBase_ThrowsInvalidCombinedCollateralBase()
    {
        var created = await _sut.CreateAsync(ValidRequest() with { CollateralTypeId = _garazaTypeId });

        var req = EmptyUpdateRequest() with { CombinedCollateralTypeId = _combinedTypeId };

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.UpdateDraftAsync(created.Id, req));

        Assert.Contains(ex.FieldErrors!, e => e.Code == ValidationErrorCodes.InvalidCombinedCollateralBase);
    }

    [Fact]
    public async Task UpdateDraftAsync_CombinedCollateralTypeIdZero_RemovesCombinedType()
    {
        var created = await _sut.CreateAsync(ValidRequest(combinedId: _combinedTypeId));

        var req = EmptyUpdateRequest() with { CombinedCollateralTypeId = 0 };

        var dto = await _sut.UpdateDraftAsync(created.Id, req);

        Assert.Null(dto.CombinedCollateralTypeId);
        Assert.Null(dto.CombinedCollateralTypeLabel);
    }

    //  SubmitAsync  sad paths 

    [Fact]
    public async Task SubmitAsync_NotOwner_ThrowsForbiddenException()
    {
        var created = await _sut.CreateAsync(ValidRequest());

        _user.UserId.Returns("other-user");
        _user.Roles.Returns(["AM"]);

        await Assert.ThrowsAsync<ForbiddenException>(() => _sut.SubmitAsync(created.Id));
    }

    [Fact]
    public async Task SubmitAsync_EmptyDraft_ThrowsValidationWithAllMissingFieldMessages()
    {
        var draft = await _sut.CreateDraftAsync();

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.SubmitAsync(draft.Id));

        // A-3 fix: ValidateSubmitRequirementsAsync sada vraća per-field greške (FieldErrors)
        Assert.NotNull(ex.FieldErrors);
        var messages = ex.FieldErrors!.Select(e => e.Message).ToList();
        Assert.Contains(messages, m => m.Contains("Klijent je obavezan."));
        Assert.Contains(messages, m => m.Contains("JMBG je obavezan."));
        Assert.Contains(messages, m => m.Contains("Tip kolaterala je obavezan."));
        Assert.Contains(messages, m => m.Contains("Grad je obavezan."));
        Assert.Contains(messages, m => m.Contains("Kontakt ime je obavezno."));
        Assert.Contains(messages, m => m.Contains("Kontakt telefon je obavezan."));
        Assert.Contains(messages, m => m.Contains("Poslovnica je obavezna."));
        Assert.Contains(messages, m => m.Contains("Adresa poslovnice je obavezna."));
        Assert.Contains(messages, m => m.Contains("Adresa nekretnine je obavezna."));
        Assert.Contains(messages, m => m.Contains("Osoba u poslovnici za dostavu originala procjene je obavezna."));
        Assert.Contains(messages, m => m.Contains("Ime AM-a na kojeg se šalje procjena mailom je obavezno."));
    }

    //  SubmitAsync  notifikacije 

    [Fact]
    public async Task SubmitAsync_BlankCaInboxEmail_DoesNotSendEmailNotification()
    {
        var sutNoEmail = BuildSut(new OrderNotificationsOptions { CaInboxEmail = "" });

        var created = await sutNoEmail.CreateAsync(ValidRequest());
        await sutNoEmail.SubmitAsync(created.Id);

        await _notify.DidNotReceive().SendAsync(
            Arg.Is<NotificationRequest>(r => r.Channel == NotificationChannel.Email),
            Arg.Any<CancellationToken>());

        await _audit.DidNotReceive().RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.CaEmailNotificationSent),
            Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task SubmitAsync_InAppNotificationThrows_RecordsEmailFailedAuditButSubmitSucceeds()
    {
        _notify.SendAsync(
                Arg.Is<NotificationRequest>(r => r.Channel == NotificationChannel.InApp),
                Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("notify provider down")));

        var created = await _sut.CreateAsync(ValidRequest());

        var submitted = await _sut.SubmitAsync(created.Id);

        Assert.Equal("SubmittedBySales", submitted.Status);

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.EmailFailed && e.Reason == "notify provider down"),
            Arg.Any<CancellationToken>());

        await _notify.Received(1).SendAsync(
            Arg.Is<NotificationRequest>(r => r.Channel == NotificationChannel.Email),
            Arg.Any<CancellationToken>());
    }

    //  CancelAsync  sad paths 

    [Fact]
    public async Task CancelAsync_NotFound_ThrowsNotFoundException()
    {
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.CancelAsync(9999));
    }

    [Fact]
    public async Task CancelAsync_NonDraftStatus_ThrowsValidationException()
    {
        var created = await _sut.CreateAsync(ValidRequest());
        await _sut.SubmitAsync(created.Id);

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CancelAsync(created.Id));

        Assert.Equal("Samo narudžbe u statusu Draft se mogu otkazati.", ex.Errors["status"][0]);
    }

    // â”€â”€ Pagination boundary tests (Phase 3.1) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    [Fact]
    public async Task GetListAsync_Page1PageSize2_ReturnsFirstTwoOrders()
    {
        await _sut.CreateAsync(ValidRequest());
        await _sut.CreateAsync(ValidRequest());
        await _sut.CreateAsync(ValidRequest());

        var result = await QuerySvc.GetListAsync(new OrderListRequest(Page: 1, PageSize: 2));

        Assert.Equal(3, result.TotalCount);
        Assert.Equal(2, result.Items.Count);
        Assert.Equal(1, result.Page);
        Assert.Equal(2, result.PageSize);
    }

    [Fact]
    public async Task GetListAsync_Page2PageSize2_ReturnsRemainingOrder()
    {
        await _sut.CreateAsync(ValidRequest());
        await _sut.CreateAsync(ValidRequest());
        await _sut.CreateAsync(ValidRequest());

        var result = await QuerySvc.GetListAsync(new OrderListRequest(Page: 2, PageSize: 2));

        Assert.Equal(3, result.TotalCount);
        Assert.Single(result.Items);
        Assert.Equal(2, result.Page);
    }

    [Fact]
    public async Task GetListAsync_PageBeyondData_ReturnsEmptyItems()
    {
        await _sut.CreateAsync(ValidRequest());

        var result = await QuerySvc.GetListAsync(new OrderListRequest(Page: 100, PageSize: 20));

        Assert.Equal(1, result.TotalCount);
        Assert.Empty(result.Items);
    }

    [Fact]
    public async Task GetListAsync_EmptyDatabase_ReturnsEmptyResult()
    {
        var result = await QuerySvc.GetListAsync(new OrderListRequest());

        Assert.Equal(0, result.TotalCount);
        Assert.Empty(result.Items);
    }

    // â”€â”€ Soft-delete filter (Phase 3.2) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    [Fact]
    public async Task GetListAsync_AfterCancelAsync_CancelledOrderNotVisibleToSales()
    {
        // Admin creates and cancels the order as owner first
        var created = await _sut.CreateAsync(ValidRequest());
        await _sut.CancelAsync(created.Id);

        // The order's user queries the list
        var result = await QuerySvc.GetListAsync(new OrderListRequest());

        // Cancelled (soft-deleted) orders must not appear in default list view for sales
        // (CancelAsync soft-deletes: IsDeleted=true, so query filter excludes them)
        Assert.Equal(0, result.TotalCount);
    }

    [Fact]
    public async Task GetListAsync_CancelledOrder_NotReturnedByDefaultFilter()
    {
        var created1 = await _sut.CreateAsync(ValidRequest());
        var created2 = await _sut.CreateAsync(ValidRequest());

        // Cancel the first one
        await _sut.CancelAsync(created1.Id);

        var result = await QuerySvc.GetListAsync(new OrderListRequest());

        // Only the non-cancelled order should appear
        Assert.Equal(1, result.TotalCount);
        Assert.Equal(created2.Id, result.Items.Single().Id);
    }

    // â”€â”€ Concurrent OrderNumber (Phase 3.5) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    [Fact]
    public async Task CreateAsync_MultipleSequentialCreations_AllHaveUniqueOrderNumbers()
    {
        var tasks = Enumerable.Range(0, 5)
            .Select(_ => _sut.CreateAsync(ValidRequest()))
            .ToList();

        var results = await Task.WhenAll(tasks);

        var orderNumbers = results.Select(r => r.OrderNumber).ToList();
        Assert.Equal(orderNumbers.Distinct().Count(), orderNumbers.Count);
    }

    public void Dispose() => _db.Dispose();
}
