using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Codebooks;
using RBBH.CollateralAppraisal.Application.Codebooks.Requests;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Infrastructure.Codebooks;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Codebooks;

public sealed class CodebookServiceTests : IDisposable
{
    private readonly ApplicationDbContext _db;
    private readonly ICurrentUserService  _user;
    private readonly IAuditService        _audit;
    private readonly CodebookService      _sut;

    public CodebookServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db    = new ApplicationDbContext(options);
        _user  = Substitute.For<ICurrentUserService>();
        _audit = Substitute.For<IAuditService>();
        _user.UserId.Returns("user-admin-1");

        _sut = new CodebookService(_db, _user, _audit, Substitute.For<ILogger<CodebookService>>());
    }

    public void Dispose() => _db.Dispose();

    private Codebook SeedCodebook(
        string code = "tipovi_kolaterala", string name = "Tipovi kolaterala",
        bool isSystem = false, bool isActive = true, string? category = "Nekretnine",
        string? description = "Opis")
    {
        var entity = isSystem
            ? Codebook.CreateSystem(code, name, description, category)
            : Codebook.CreateCustom(code, name, description, category, "user-admin-1");

        if (!isActive)
            entity.Deactivate("user-admin-1", DateTime.UtcNow);

        _db.Codebooks.Add(entity);
        _db.SaveChanges();
        return entity;
    }

    private void SeedCodebookValue(string codebookKey, string code, bool isActive = true)
    {
        var value = CodebookValue.Create(codebookKey, code, code, null, 0, "user-admin-1");
        if (!isActive)
            value.Deactivate(DateTime.UtcNow, "user-admin-1", "test");

        _db.CodebookValues.Add(value);
        _db.SaveChanges();
    }

    // ── CreateAsync ──────────────────────────────────────────────────────────

    [Fact]
    public async Task CreateAsync_ValidRequest_CreatesCodebookAndReturnsDto()
    {
        var request = new CreateCodebookRequest("Novi_Kod", "Novi šifarnik", "Opis", "Kategorija");

        var result = await _sut.CreateAsync(request);

        Assert.Equal("novi_kod", result.Code);
        Assert.Equal("Novi šifarnik", result.Name);
        Assert.False(result.IsSystem);
        Assert.True(result.IsActive);
        Assert.Equal(0, result.ValueCount);
        await _audit.Received(1).RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task CreateAsync_DuplicateCode_ThrowsConflictException()
    {
        SeedCodebook(code: "postojeci_kod");
        var request = new CreateCodebookRequest("postojeci_kod", "Naziv", null, null);

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.CreateAsync(request));

        Assert.Equal(CodebookErrorCodes.CodebookDuplicateCode, ex.ErrorCode);
    }

    [Fact]
    public async Task CreateAsync_EmptyCode_ThrowsValidationException()
    {
        var request = new CreateCodebookRequest("", "Naziv", null, null);

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(request));

        var error = Assert.Single(ex.FieldErrors!);
        Assert.Equal("code", error.Field);
        Assert.Equal("REQUIRED_FIELD", error.Code);
    }

    [Fact]
    public async Task CreateAsync_CodeTooLong_ThrowsValidationException()
    {
        var request = new CreateCodebookRequest(new string('a', 101), "Naziv", null, null);

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(request));

        var error = Assert.Single(ex.FieldErrors!);
        Assert.Equal("code", error.Field);
        Assert.Equal("MAX_LENGTH_EXCEEDED", error.Code);
    }

    [Fact]
    public async Task CreateAsync_InvalidCodeFormat_ThrowsValidationException()
    {
        var request = new CreateCodebookRequest("invalid code!", "Naziv", null, null);

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(request));

        var error = Assert.Single(ex.FieldErrors!);
        Assert.Equal("code", error.Field);
        Assert.Equal("INVALID_FORMAT", error.Code);
    }

    [Fact]
    public async Task CreateAsync_EmptyName_ThrowsValidationException()
    {
        var request = new CreateCodebookRequest("validan_kod", "", null, null);

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(request));

        var error = Assert.Single(ex.FieldErrors!);
        Assert.Equal("name", error.Field);
        Assert.Equal("REQUIRED_FIELD", error.Code);
    }

    [Fact]
    public async Task CreateAsync_NameTooLong_ThrowsValidationException()
    {
        var request = new CreateCodebookRequest("validan_kod", new string('a', 251), null, null);

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(request));

        var error = Assert.Single(ex.FieldErrors!);
        Assert.Equal("name", error.Field);
        Assert.Equal("MAX_LENGTH_EXCEEDED", error.Code);
    }

    // ── GetByCodeAsync ───────────────────────────────────────────────────────

    [Fact]
    public async Task GetByCodeAsync_ExistingCode_ReturnsDto()
    {
        SeedCodebook(code: "kod1", name: "Naziv1");
        SeedCodebookValue("kod1", "vrijednost1");

        var result = await _sut.GetByCodeAsync("kod1");

        Assert.NotNull(result);
        Assert.Equal("kod1", result!.Code);
        Assert.Equal(1, result.ValueCount);
    }

    [Fact]
    public async Task GetByCodeAsync_NonExistentCode_ReturnsNull()
    {
        var result = await _sut.GetByCodeAsync("ne_postoji");

        Assert.Null(result);
    }

    // ── GetAllAsync — filteri ────────────────────────────────────────────────

    [Fact]
    public async Task GetAllAsync_WithSearchFilter_FiltersByCodeNameOrDescription()
    {
        SeedCodebook(code: "tipovi_nekretnina", name: "Tipovi nekretnina", description: "Opis tipova");
        SeedCodebook(code: "gradovi", name: "Gradovi", description: "Opis gradova");

        var result = await _sut.GetAllAsync(new CodebookQueryRequest(Search: "nekretnina"));

        Assert.Single(result.Items);
        Assert.Equal("tipovi_nekretnina", result.Items[0].Code);
    }

    [Fact]
    public async Task GetAllAsync_WithIsActiveFilter_ReturnsOnlyMatchingCodebooks()
    {
        SeedCodebook(code: "aktivan", isActive: true);
        SeedCodebook(code: "neaktivan", isActive: false);

        var result = await _sut.GetAllAsync(new CodebookQueryRequest(IsActive: false));

        Assert.Single(result.Items);
        Assert.Equal("neaktivan", result.Items[0].Code);
    }

    [Fact]
    public async Task GetAllAsync_WithIsSystemFilter_ReturnsOnlyMatchingCodebooks()
    {
        SeedCodebook(code: "sistemski", isSystem: true);
        SeedCodebook(code: "custom", isSystem: false);

        var result = await _sut.GetAllAsync(new CodebookQueryRequest(IsSystem: true));

        Assert.Single(result.Items);
        Assert.Equal("sistemski", result.Items[0].Code);
    }

    [Fact]
    public async Task GetAllAsync_WithCategoryFilter_ReturnsOnlyMatchingCodebooks()
    {
        SeedCodebook(code: "nekretnine_kod", category: "Nekretnine");
        SeedCodebook(code: "limit_kod", category: "Limiti");

        var result = await _sut.GetAllAsync(new CodebookQueryRequest(Category: "Limiti"));

        Assert.Single(result.Items);
        Assert.Equal("limit_kod", result.Items[0].Code);
    }

    [Fact]
    public async Task GetAllAsync_ComputesTotalAndActiveValueCounts()
    {
        SeedCodebook(code: "kod1");
        SeedCodebookValue("kod1", "v1", isActive: true);
        SeedCodebookValue("kod1", "v2", isActive: false);

        var result = await _sut.GetAllAsync(new CodebookQueryRequest());

        var item = Assert.Single(result.Items);
        Assert.Equal(2, item.ValueCount);
        Assert.Equal(1, item.ActiveValueCount);
    }

    // ── GetAllAsync — sortiranje ─────────────────────────────────────────────

    [Theory]
    [InlineData("code", true)]
    [InlineData("code", false)]
    [InlineData("createdat", true)]
    [InlineData("createdat", false)]
    [InlineData("updatedat", true)]
    [InlineData("updatedat", false)]
    [InlineData(null, true)]
    [InlineData(null, false)]
    public async Task GetAllAsync_SortsBySpecifiedFieldWithoutError(string? sortBy, bool sortAsc)
    {
        SeedCodebook(code: "aaa", name: "Zebra");
        SeedCodebook(code: "bbb", name: "Alpha");

        var result = await _sut.GetAllAsync(new CodebookQueryRequest(SortBy: sortBy, SortAsc: sortAsc));

        Assert.Equal(2, result.Items.Count);
    }

    [Fact]
    public async Task GetAllAsync_SortByCodeAscending_OrdersResultsByCode()
    {
        SeedCodebook(code: "bbb", name: "Beta");
        SeedCodebook(code: "aaa", name: "Alpha");

        var result = await _sut.GetAllAsync(new CodebookQueryRequest(SortBy: "code", SortAsc: true));

        Assert.Equal("aaa", result.Items[0].Code);
        Assert.Equal("bbb", result.Items[1].Code);
    }

    // ── UpdateAsync ──────────────────────────────────────────────────────────

    [Fact]
    public async Task UpdateAsync_ValidRequest_UpdatesAndReturnsDto()
    {
        SeedCodebook(code: "kod1", name: "Stari naziv");

        var result = await _sut.UpdateAsync("kod1",
            new UpdateCodebookRequest("Novi naziv", "Novi opis", "Nova kategorija"));

        Assert.Equal("Novi naziv", result.Name);
        Assert.Equal("Novi opis", result.Description);
        Assert.Equal("Nova kategorija", result.Category);
        await _audit.Received(1).RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task UpdateAsync_NonExistentCode_ThrowsNotFoundException()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.UpdateAsync("ne_postoji", new UpdateCodebookRequest("Naziv", null, null)));

        Assert.Equal(CodebookErrorCodes.CodebookNotFound, ex.ErrorCode);
    }

    [Fact]
    public async Task UpdateAsync_EmptyName_ThrowsValidationException()
    {
        SeedCodebook(code: "kod1");

        var ex = await Assert.ThrowsAsync<ValidationException>(
            () => _sut.UpdateAsync("kod1", new UpdateCodebookRequest("", null, null)));

        var error = Assert.Single(ex.FieldErrors!);
        Assert.Equal("name", error.Field);
    }

    // ── Deactivate / Activate ────────────────────────────────────────────────

    [Fact]
    public async Task DeactivateAsync_ActiveCodebook_DeactivatesAndReturnsDto()
    {
        SeedCodebook(code: "kod1", isActive: true);

        var result = await _sut.DeactivateAsync("kod1");

        Assert.False(result.IsActive);
        await _audit.Received(1).RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task DeactivateAsync_AlreadyInactive_ThrowsConflictException()
    {
        SeedCodebook(code: "kod1", isActive: false);

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.DeactivateAsync("kod1"));

        Assert.Equal(CodebookErrorCodes.CodebookAlreadyInactive, ex.ErrorCode);
    }

    [Fact]
    public async Task ActivateAsync_InactiveCodebook_ActivatesAndReturnsDto()
    {
        SeedCodebook(code: "kod1", isActive: false);

        var result = await _sut.ActivateAsync("kod1");

        Assert.True(result.IsActive);
        await _audit.Received(1).RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task ActivateAsync_AlreadyActive_ThrowsConflictException()
    {
        SeedCodebook(code: "kod1", isActive: true);

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ActivateAsync("kod1"));

        Assert.Equal(CodebookErrorCodes.CodebookAlreadyActive, ex.ErrorCode);
    }

    // ── DeleteAsync ──────────────────────────────────────────────────────────

    [Fact]
    public async Task DeleteAsync_SystemCodebook_ThrowsConflictException()
    {
        SeedCodebook(code: "kod1", isSystem: true);

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.DeleteAsync("kod1"));

        Assert.Equal(CodebookErrorCodes.CodebookSystemLocked, ex.ErrorCode);
    }

    [Fact]
    public async Task DeleteAsync_CodebookWithActiveValues_ThrowsConflictException()
    {
        SeedCodebook(code: "kod1", isSystem: false);
        SeedCodebookValue("kod1", "v1", isActive: true);

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.DeleteAsync("kod1"));

        Assert.Equal(CodebookErrorCodes.CodebookHasActiveValues, ex.ErrorCode);
    }

    [Fact]
    public async Task DeleteAsync_CustomCodebookNoActiveValues_SoftDeletes()
    {
        SeedCodebook(code: "kod1", isSystem: false);
        SeedCodebookValue("kod1", "v1", isActive: false);

        await _sut.DeleteAsync("kod1");

        var result = await _sut.GetByCodeAsync("kod1");
        Assert.Null(result);
        await _audit.Received(1).RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task DeleteAsync_NonExistentCode_ThrowsNotFoundException()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.DeleteAsync("ne_postoji"));

        Assert.Equal(CodebookErrorCodes.CodebookNotFound, ex.ErrorCode);
    }
}
