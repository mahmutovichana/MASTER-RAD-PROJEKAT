using FluentAssertions;
using FluentValidation;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.AppraiserAssignment.Commands;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Orders;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.AppraiserAssignment;

// ═══════════════════════════════════════════════════════════════
// TEST MATRIX — RejectOrderCommandValidator
//
// Scenario              | Input                     | Expected          | Type
// ─────────────────────────────────────────────────────────────────────────────
// Valid command          | OrderId=1, Reason="OK"   | No errors         | Happy path
// OrderId = 0            | OrderId=0                | "ID nevažeći"     | BVA lower
// OrderId = -1           | OrderId=-1               | "ID nevažeći"     | Negative
// OrderId = 1 (min ok)   | OrderId=1                | No errors         | BVA lower+1
// Reason empty           | Reason=""                | Required error    | Negative
// Reason null/whitespace | Reason=" "              | Required error    | Null/whitespace
// Reason 500 chars       | Reason=500×'x'           | No errors         | BVA upper
// Reason 501 chars       | Reason=501×'x'           | Length error      | BVA upper+1
// Comment null           | Comment=null             | No errors (optl)  | Optional
// Comment present        | Comment="extra"          | No errors         | Happy path
// ═══════════════════════════════════════════════════════════════

public sealed class RejectOrderCommandValidatorTests
{
    private readonly RejectOrderCommandValidator _sut = new();

    // ── Happy path ────────────────────────────────────────────────────────────

    [Fact]
    public void Validate_WithValidCommand_ShouldPass()
    {
        // Arrange
        var cmd = new RejectOrderCommand(1, "Greška u podacima narudžbe");

        // Act
        var result = _sut.Validate(cmd);

        // Assert
        result.IsValid.Should().BeTrue();
    }

    [Fact]
    public void Validate_WithValidCommandAndComment_ShouldPass()
    {
        var cmd = new RejectOrderCommand(5, "Operativni razlozi", "Detalji razloga...");

        _sut.Validate(cmd).IsValid.Should().BeTrue();
    }

    [Fact]
    public void Validate_WithNullComment_ShouldPass()
    {
        var cmd = new RejectOrderCommand(1, "Razlog", null);

        _sut.Validate(cmd).IsValid.Should().BeTrue();
    }

    // ── OrderId — Boundary Value Analysis ────────────────────────────────────

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(-999)]
    public void Validate_WithInvalidOrderId_ShouldFailWithIdMessage(int invalidId)
    {
        var cmd = new RejectOrderCommand(invalidId, "Razlog");

        var result = _sut.Validate(cmd);

        result.IsValid.Should().BeFalse();
        result.Errors.Should().ContainSingle(e =>
            e.PropertyName == "OrderId" &&
            e.ErrorMessage  == "ID narudžbe je nevažeći.");
    }

    [Theory]
    [InlineData(1)]
    [InlineData(42)]
    [InlineData(int.MaxValue)]
    public void Validate_WithValidOrderId_ShouldPass(int validId)
    {
        var cmd = new RejectOrderCommand(validId, "Razlog");

        _sut.Validate(cmd).IsValid.Should().BeTrue();
    }

    // ── RejectionReason — Required + Max Length ───────────────────────────────

    [Theory]
    [InlineData("")]
    [InlineData("   ")]
    [InlineData(null)]
    public void Validate_WithEmptyOrWhitespaceReason_ShouldFailRequired(string? reason)
    {
        var cmd = new RejectOrderCommand(1, reason!);

        var result = _sut.Validate(cmd);

        result.IsValid.Should().BeFalse();
        result.Errors.Should().ContainSingle(e =>
            e.PropertyName == "RejectionReason" &&
            e.ErrorMessage  == "Razlog odbijanja je obavezan.");
    }

    [Fact]
    public void Validate_WithReasonExactly500Chars_ShouldPass()
    {
        // BVA: upper boundary (inclusive)
        var reason = new string('x', 500);
        var cmd = new RejectOrderCommand(1, reason);

        _sut.Validate(cmd).IsValid.Should().BeTrue();
    }

    [Fact]
    public void Validate_WithReason501Chars_ShouldFailMaxLength()
    {
        // BVA: upper boundary + 1 (exclusive)
        var reason = new string('x', 501);
        var cmd = new RejectOrderCommand(1, reason);

        var result = _sut.Validate(cmd);

        result.IsValid.Should().BeFalse();
        result.Errors.Should().ContainSingle(e =>
            e.PropertyName == "RejectionReason" &&
            e.ErrorMessage  == "Razlog odbijanja ne smije biti duži od 500 znakova.");
    }

    [Fact]
    public void Validate_WithReason1Char_ShouldPass()
    {
        // BVA: min valid boundary
        _sut.Validate(new RejectOrderCommand(1, "x")).IsValid.Should().BeTrue();
    }

    // ── Decision table: multiple errors at once ───────────────────────────────

    [Fact]
    public void Validate_WithBothFieldsInvalid_ShouldReturnTwoErrors()
    {
        var cmd = new RejectOrderCommand(0, "");

        var result = _sut.Validate(cmd);

        result.IsValid.Should().BeFalse();
        result.Errors.Should().HaveCount(2);
        result.Errors.Select(e => e.PropertyName)
            .Should().BeEquivalentTo(["OrderId", "RejectionReason"]);
    }
}

// ═══════════════════════════════════════════════════════════════
// TEST MATRIX — RejectOrderCommandHandler
//
// Scenario                      | Expected
// ─────────────────────────────────────────────────────────────
// Valid command                  | Delegates to service with correct params
// Service call returns result    | Handler returns service result unchanged
// Cancellation token propagated  | CT passed through to service
// ═══════════════════════════════════════════════════════════════

public sealed class RejectOrderCommandHandlerTests
{
    private readonly IAppraiserAssignmentService _service
        = Substitute.For<IAppraiserAssignmentService>();
    private readonly RejectOrderCommandHandler _sut;

    public RejectOrderCommandHandlerTests()
        => _sut = new RejectOrderCommandHandler(_service);

    [Fact]
    public async Task Handle_WithValidCommand_ShouldDelegateToServiceWithExactParams()
    {
        // Arrange
        var cmd = new RejectOrderCommand(42, "Greška u podacima", "Detalji");
        var expected = new SendToAppraiserResultDto(
            42, "PN-2026-000042", "AppraiserRejected", 300, 0,
            null, null, false, "Odbijeno.");
        _service.RejectOrderAsync(42, "Greška u podacima", "Detalji", Arg.Any<CancellationToken>())
            .Returns(expected);

        // Act
        var result = await _sut.Handle(cmd, CancellationToken.None);

        // Assert
        result.Should().Be(expected);
        await _service.Received(1)
            .RejectOrderAsync(42, "Greška u podacima", "Detalji", Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task Handle_WithNullComment_ShouldPassNullToService()
    {
        // Arrange
        var cmd = new RejectOrderCommand(10, "Razlog", null);
        _service.RejectOrderAsync(10, "Razlog", null, Arg.Any<CancellationToken>())
            .Returns(new SendToAppraiserResultDto(
                10, "PN-2026-000010", "AppraiserRejected", 300, 0,
                null, null, false, "OK"));

        // Act
        await _sut.Handle(cmd, CancellationToken.None);

        // Assert
        await _service.Received(1)
            .RejectOrderAsync(10, "Razlog", null, Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task Handle_WithCancellationToken_ShouldPropagateThroughToService()
    {
        // Arrange
        var cts = new CancellationTokenSource();
        var ct  = cts.Token;
        var cmd = new RejectOrderCommand(1, "Razlog");
        _service.RejectOrderAsync(Arg.Any<int>(), Arg.Any<string>(), Arg.Any<string?>(), ct)
            .Returns(new SendToAppraiserResultDto(
                1, "ORD", "AppraiserRejected", 300, 0,
                null, null, false, "OK"));

        // Act
        await _sut.Handle(cmd, ct);

        // Assert — cancellationToken se tačno prosljeđuje servisu
        await _service.Received(1)
            .RejectOrderAsync(Arg.Any<int>(), Arg.Any<string>(), Arg.Any<string?>(), ct);
    }
}
