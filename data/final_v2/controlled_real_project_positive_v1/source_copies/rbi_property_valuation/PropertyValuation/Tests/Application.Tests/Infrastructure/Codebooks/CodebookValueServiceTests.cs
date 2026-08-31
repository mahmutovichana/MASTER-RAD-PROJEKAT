using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Codebooks;
using RBBH.CollateralAppraisal.Application.Codebooks.Interfaces;
using RBBH.CollateralAppraisal.Application.Codebooks.Models;
using RBBH.CollateralAppraisal.Application.Codebooks.Requests;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Infrastructure.Codebooks;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Codebooks;

public sealed class CodebookValueServiceTests : IDisposable
{
    private const string Key = "tipovi_kolaterala";

    private readonly ApplicationDbContext      _db;
    private readonly ICurrentUserService       _user;
    private readonly ICodebookUsageService     _usageService;
    private readonly ICodebookCacheInvalidator _cache;
    private readonly IAuditService             _audit;
    private readonly CodebookValueService      _sut;

    public CodebookValueServiceTests()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .ConfigureWarnings(w => w.Ignore(
                Microsoft.EntityFrameworkCore.Diagnostics.InMemoryEventId.TransactionIgnoredWarning))
            .Options;
        _db           = new ApplicationDbContext(options);
        _user         = Substitute.For<ICurrentUserService>();
        _usageService = Substitute.For<ICodebookUsageService>();
        _cache        = Substitute.For<ICodebookCacheInvalidator>();
        _audit        = Substitute.For<IAuditService>();
        _user.UserId.Returns("user-admin-1");

        _sut = new CodebookValueService(
            _db, _user, _usageService, _cache, _audit, Substitute.For<ILogger<CodebookValueService>>());
    }

    public void Dispose() => _db.Dispose();

    private CodebookValue SeedValue(
        string codebookKey, string code, bool isActive = true,
        bool isSystem = false, bool isCritical = false, int sortOrder = 0)
    {
        var entity = CodebookValue.Create(
            codebookKey, code, code + "_label", null, sortOrder, "user-admin-1", isSystem, isCritical);

        if (!isActive)
            entity.Deactivate(DateTime.UtcNow, "user-admin-1", "test");

        _db.CodebookValues.Add(entity);
        _db.SaveChanges();
        return entity;
    }

    // ── CreateAsync ──────────────────────────────────────────────────────────

    [Fact]
    public async Task CreateAsync_ValidRequest_CreatesValueAndReturnsDto()
    {
        var request = new CreateCodebookValueRequest("novi_kod", "Novi naziv", "Opis", 10);

        var result = await _sut.CreateAsync(Key, request);

        Assert.Equal("novi_kod", result.Code);
        Assert.Equal("Novi naziv", result.Label);
        Assert.True(result.IsActive);
        await _cache.Received(1).InvalidateAsync(Key, Arg.Any<CancellationToken>());
        await _audit.Received(1).RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task CreateAsync_DuplicateCode_ThrowsConflictException()
    {
        SeedValue(Key, "postojeci");
        var request = new CreateCodebookValueRequest("postojeci", "Naziv", null, 0);

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.CreateAsync(Key, request));

        Assert.Equal(CodebookErrorCodes.DuplicateCode, ex.ErrorCode);
    }

    [Theory]
    [InlineData("", "Naziv", null, 0, "code", "REQUIRED_FIELD")]
    [InlineData("invalid code!", "Naziv", null, 0, "code", "INVALID_CODE_FORMAT")]
    [InlineData("validan", "", null, 0, "label", "REQUIRED_FIELD")]
    [InlineData("validan", "Naziv", null, -1, "sortOrder", "INVALID_INPUT")]
    public async Task CreateAsync_InvalidRequest_ThrowsValidationException(
        string code, string label, string? description, int sortOrder, string expectedField, string expectedCode)
    {
        var request = new CreateCodebookValueRequest(code, label, description, sortOrder);

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(Key, request));

        Assert.Contains(ex.FieldErrors!, e => e.Field == expectedField && e.Code == expectedCode);
    }

    [Fact]
    public async Task CreateAsync_CodeTooLong_ThrowsValidationException()
    {
        var request = new CreateCodebookValueRequest(new string('a', 101), "Naziv", null, 0);

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(Key, request));

        Assert.Contains(ex.FieldErrors!, e => e.Field == "code" && e.Code == "MAX_LENGTH_EXCEEDED");
    }

    [Fact]
    public async Task CreateAsync_LabelTooLong_ThrowsValidationException()
    {
        var request = new CreateCodebookValueRequest("validan", new string('a', 301), null, 0);

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(Key, request));

        Assert.Contains(ex.FieldErrors!, e => e.Field == "label" && e.Code == "MAX_LENGTH_EXCEEDED");
    }

    [Fact]
    public async Task CreateAsync_DescriptionTooLong_ThrowsValidationException()
    {
        var request = new CreateCodebookValueRequest("validan", "Naziv", new string('a', 1001), 0);

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.CreateAsync(Key, request));

        Assert.Contains(ex.FieldErrors!, e => e.Field == "description" && e.Code == "MAX_LENGTH_EXCEEDED");
    }

    [Fact]
    public async Task CreateAsync_CacheInvalidationThrows_DoesNotPropagateException()
    {
        _cache.When(x => x.InvalidateAsync(Arg.Any<string>(), Arg.Any<CancellationToken>()))
            .Do(_ => throw new InvalidOperationException("cache down"));

        var request = new CreateCodebookValueRequest("novi_kod", "Naziv", null, 0);

        var result = await _sut.CreateAsync(Key, request);

        Assert.Equal("novi_kod", result.Code);
    }

    [Fact]
    public async Task CreateAsync_AuditRecordThrows_DoesNotPropagateException()
    {
        _audit.When(x => x.RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>()))
            .Do(_ => throw new InvalidOperationException("audit down"));

        var request = new CreateCodebookValueRequest("novi_kod", "Naziv", null, 0);

        var result = await _sut.CreateAsync(Key, request);

        Assert.Equal("novi_kod", result.Code);
    }

    // ── UpdateAsync ──────────────────────────────────────────────────────────

    [Fact]
    public async Task UpdateAsync_ValidRequest_UpdatesAndReturnsDto()
    {
        var value = SeedValue(Key, "kod1");

        var result = await _sut.UpdateAsync(Key, value.Id, new UpdateCodebookValueRequest("Novi naziv", "Novi opis", 5));

        Assert.Equal("Novi naziv", result.Label);
        Assert.Equal("Novi opis", result.Description);
        Assert.Equal(5, result.SortOrder);
        await _cache.Received(1).InvalidateAsync(Key, Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task UpdateAsync_NonExistentId_ThrowsNotFoundException()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.UpdateAsync(Key, 999, new UpdateCodebookValueRequest("Naziv", null, 0)));

        Assert.Equal(CodebookErrorCodes.ValueNotFound, ex.ErrorCode);
    }

    [Theory]
    [InlineData("", null, 0, "label", "REQUIRED_FIELD")]
    [InlineData("Naziv", null, -1, "sortOrder", "INVALID_INPUT")]
    public async Task UpdateAsync_InvalidRequest_ThrowsValidationException(
        string label, string? description, int sortOrder, string expectedField, string expectedCode)
    {
        var value = SeedValue(Key, "kod1");
        var request = new UpdateCodebookValueRequest(label, description, sortOrder);

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.UpdateAsync(Key, value.Id, request));

        Assert.Contains(ex.FieldErrors!, e => e.Field == expectedField && e.Code == expectedCode);
    }

    [Fact]
    public async Task UpdateAsync_LabelTooLong_ThrowsValidationException()
    {
        var value = SeedValue(Key, "kod1");
        var request = new UpdateCodebookValueRequest(new string('a', 301), null, 0);

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.UpdateAsync(Key, value.Id, request));

        Assert.Contains(ex.FieldErrors!, e => e.Field == "label" && e.Code == "MAX_LENGTH_EXCEEDED");
    }

    [Fact]
    public async Task UpdateAsync_DescriptionTooLong_ThrowsValidationException()
    {
        var value = SeedValue(Key, "kod1");
        var request = new UpdateCodebookValueRequest("Naziv", new string('a', 1001), 0);

        var ex = await Assert.ThrowsAsync<ValidationException>(() => _sut.UpdateAsync(Key, value.Id, request));

        Assert.Contains(ex.FieldErrors!, e => e.Field == "description" && e.Code == "MAX_LENGTH_EXCEEDED");
    }

    // ── GetActiveAsync / GetAllAsync / GetByIdAsync ─────────────────────────────

    [Fact]
    public async Task GetActiveAsync_ReturnsOnlyActiveValuesOrderedBySortOrder()
    {
        SeedValue(Key, "b", isActive: true, sortOrder: 20);
        SeedValue(Key, "a", isActive: true, sortOrder: 10);
        SeedValue(Key, "c", isActive: false, sortOrder: 5);

        var result = await _sut.GetActiveAsync(Key);

        Assert.Equal(2, result.Count);
        Assert.Equal("a", result[0].Code);
        Assert.Equal("b", result[1].Code);
    }

    [Fact]
    public async Task GetAllAsync_ReturnsAllValuesIncludingInactive()
    {
        SeedValue(Key, "a", isActive: true);
        SeedValue(Key, "b", isActive: false);

        var result = await _sut.GetAllAsync(Key);

        Assert.Equal(2, result.Count);
    }

    [Fact]
    public async Task GetByIdAsync_ExistingId_ReturnsDto()
    {
        var value = SeedValue(Key, "kod1");

        var result = await _sut.GetByIdAsync(Key, value.Id);

        Assert.Equal("kod1", result.Code);
        Assert.Equal("kod1_label", result.Label);
    }

    // ── CheckUsageAsync ──────────────────────────────────────────────────────

    [Fact]
    public async Task CheckUsageAsync_ExistingValue_DelegatesToUsageService()
    {
        var value = SeedValue(Key, "kod1");
        _usageService.CheckUsageAsync(Key, value.Id, Arg.Any<CancellationToken>())
            .Returns(new CodebookUsageResult { IsInUse = true, UsageCount = 3, IsReliable = true });

        var result = await _sut.CheckUsageAsync(Key, value.Id);

        Assert.True(result.IsInUse);
        Assert.Equal(3, result.UsageCount);
    }

    [Fact]
    public async Task CheckUsageAsync_NonExistentValue_ThrowsNotFoundException()
    {
        var ex = await Assert.ThrowsAsync<NotFoundException>(() => _sut.CheckUsageAsync(Key, 999));

        Assert.Equal(CodebookErrorCodes.ValueNotFound, ex.ErrorCode);
    }

    // ── Deactivate / Activate ────────────────────────────────────────────────

    [Fact]
    public async Task DeactivateAsync_ActiveValue_DeactivatesAndReturnsDto()
    {
        var value = SeedValue(Key, "kod1");

        var result = await _sut.DeactivateAsync(Key, value.Id, new DeactivateCodebookValueRequest("Razlog"));

        Assert.False(result.IsActive);
        Assert.Equal("Razlog", result.DeactivationReason);
        await _cache.Received(1).InvalidateAsync(Key, Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task DeactivateAsync_AlreadyInactive_ThrowsConflictException()
    {
        var value = SeedValue(Key, "kod1", isActive: false);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.DeactivateAsync(Key, value.Id, new DeactivateCodebookValueRequest()));

        Assert.Equal(CodebookErrorCodes.ValueAlreadyInactive, ex.ErrorCode);
    }

    [Fact]
    public async Task DeactivateAsync_CriticalValue_ThrowsConflictException()
    {
        var value = SeedValue(Key, "kod1", isCritical: true);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.DeactivateAsync(Key, value.Id, new DeactivateCodebookValueRequest()));

        Assert.Equal(CodebookErrorCodes.CriticalLocked, ex.ErrorCode);
    }

    [Fact]
    public async Task ActivateAsync_InactiveValue_ActivatesAndReturnsDto()
    {
        var value = SeedValue(Key, "kod1", isActive: false);

        var result = await _sut.ActivateAsync(Key, value.Id);

        Assert.True(result.IsActive);
        await _cache.Received(1).InvalidateAsync(Key, Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task ActivateAsync_AlreadyActive_ThrowsConflictException()
    {
        var value = SeedValue(Key, "kod1", isActive: true);

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.ActivateAsync(Key, value.Id));

        Assert.Equal(CodebookErrorCodes.ValueAlreadyActive, ex.ErrorCode);
    }

    // ── DeleteAsync ──────────────────────────────────────────────────────────

    [Fact]
    public async Task DeleteAsync_SystemValue_ThrowsConflictException()
    {
        var value = SeedValue(Key, "kod1", isSystem: true);

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.DeleteAsync(Key, value.Id));

        Assert.Equal(CodebookErrorCodes.SystemLocked, ex.ErrorCode);
    }

    [Fact]
    public async Task DeleteAsync_CriticalValue_ThrowsConflictException()
    {
        var value = SeedValue(Key, "kod1", isCritical: true);

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.DeleteAsync(Key, value.Id));

        Assert.Equal(CodebookErrorCodes.CriticalLocked, ex.ErrorCode);
    }

    [Fact]
    public async Task DeleteAsync_UsageCheckThrows_ThrowsConflictExceptionWithUsageCheckFailed()
    {
        var value = SeedValue(Key, "kod1");
        _usageService.CheckUsageAsync(Key, value.Id, Arg.Any<CancellationToken>())
            .Returns(Task.FromException<CodebookUsageResult>(new InvalidOperationException("boom")));

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.DeleteAsync(Key, value.Id));

        Assert.Equal(CodebookErrorCodes.UsageCheckFailed, ex.ErrorCode);
    }

    [Fact]
    public async Task DeleteAsync_UsageNotReliable_ThrowsConflictExceptionWithUsageCheckFailed()
    {
        var value = SeedValue(Key, "kod1");
        _usageService.CheckUsageAsync(Key, value.Id, Arg.Any<CancellationToken>())
            .Returns(new CodebookUsageResult { IsInUse = false, IsReliable = false });

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.DeleteAsync(Key, value.Id));

        Assert.Equal(CodebookErrorCodes.UsageCheckFailed, ex.ErrorCode);
    }

    [Fact]
    public async Task DeleteAsync_ValueInUse_ThrowsConflictExceptionWithValueInUse()
    {
        var value = SeedValue(Key, "kod1");
        _usageService.CheckUsageAsync(Key, value.Id, Arg.Any<CancellationToken>())
            .Returns(new CodebookUsageResult { IsInUse = true, UsageCount = 5, IsReliable = true });

        var ex = await Assert.ThrowsAsync<ConflictException>(() => _sut.DeleteAsync(Key, value.Id));

        Assert.Equal(CodebookErrorCodes.ValueInUse, ex.ErrorCode);
    }

    [Fact]
    public async Task DeleteAsync_ValueNotInUse_SoftDeletesAndInvalidatesCache()
    {
        var value = SeedValue(Key, "kod1");
        _usageService.CheckUsageAsync(Key, value.Id, Arg.Any<CancellationToken>())
            .Returns(new CodebookUsageResult { IsInUse = false, IsReliable = true });

        await _sut.DeleteAsync(Key, value.Id);

        await Assert.ThrowsAsync<NotFoundException>(() => _sut.GetByIdAsync(Key, value.Id));
        await _cache.Received(1).InvalidateAsync(Key, Arg.Any<CancellationToken>());
    }
}
