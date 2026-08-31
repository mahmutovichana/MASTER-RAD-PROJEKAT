using FluentAssertions;
using FluentValidation;
using RBBH.CollateralAppraisal.Application.Common.Validation;
using RBBH.CollateralAppraisal.Application.Orders.Commands;
using RBBH.CollateralAppraisal.Application.Orders.Requests;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Validation;

public sealed class CreateOrderCommandValidatorTests
{
    private readonly CreateOrderCommandValidator _sut = new();

    private static CreateOrderRequest ValidRequest() => new(
        ClientName: "Amar Amarovic",
        ClientType: "FL",
        ClientIdentifier: "0101985100129",
        CollateralTypeId: 1,
        CombinedCollateralTypeId: null,
        City: "Sarajevo",
        PropertyAddress: "Obala 1",
        Branch: "POS_SARAJEVO_CENTAR",
        BranchAddress: "Zmaja od Bosne 74",
        ContactName: "Amar Kontakt",
        ContactPhone: "061123456",
        ContactEmail: null,
        InternalNote: null,
        DeliveryContactName: "Dostava",
        AmRecipientName: "AM Primalac",
        RequestReceivedAt: new DateTime(2026, 1, 10, 10, 0, 0, DateTimeKind.Utc));

    // ── Happy path ────────────────────────────────────────────────────────────

    [Fact]
    public void Validate_ValidRequest_ShouldPass()
    {
        var cmd = new CreateOrderCommand(ValidRequest());
        var result = _sut.Validate(cmd);
        result.IsValid.Should().BeTrue();
    }

    // ── Greška sa FieldErrors (novi format) ──────────────────────────────────

    [Fact]
    public void Validate_MissingClientName_ShouldFailWithFieldErrors()
    {
        var request = ValidRequest() with { ClientName = "" };
        var cmd     = new CreateOrderCommand(request);

        var result = _sut.Validate(cmd);

        result.IsValid.Should().BeFalse();
        result.Errors.Should().Contain(e => e.PropertyName.Contains("clientName"));
    }

    [Fact]
    public void Validate_MissingCity_ShouldFailWithCityError()
    {
        var request = ValidRequest() with { City = "" };
        var cmd     = new CreateOrderCommand(request);

        var result = _sut.Validate(cmd);

        result.IsValid.Should().BeFalse();
        result.Errors.Should().Contain(e => e.PropertyName.Contains("city"));
    }

    [Fact]
    public void Validate_InvalidBranchForCity_ShouldFailWithBranchError()
    {
        var request = ValidRequest() with { City = "Sarajevo", Branch = "POS_BANJA_LUKA" };
        var cmd     = new CreateOrderCommand(request);

        var result = _sut.Validate(cmd);

        result.IsValid.Should().BeFalse();
        result.Errors.Should().Contain(e => e.PropertyName.Contains("branch"));
    }

    [Fact]
    public void Validate_InvalidJmbgChecksum_ShouldFailWithIdentifierError()
    {
        // JMBG s pogrešnom kontrolnom cifrom
        var request = ValidRequest() with { ClientIdentifier = "0101985100123" };
        var cmd     = new CreateOrderCommand(request);

        var result = _sut.Validate(cmd);

        result.IsValid.Should().BeFalse();
        result.Errors.Should().Contain(e => e.PropertyName.Contains("clientIdentifier"));
    }

    [Fact]
    public void Validate_MissingRequestReceivedAt_ShouldFail()
    {
        var request = ValidRequest() with { RequestReceivedAt = null };
        var cmd     = new CreateOrderCommand(request);

        var result = _sut.Validate(cmd);

        result.IsValid.Should().BeFalse();
        result.Errors.Should().Contain(e => e.PropertyName.Contains("requestReceivedAt"));
    }

    [Fact]
    public void Validate_MultipleErrors_ShouldReportAll()
    {
        var request = ValidRequest() with { ClientName = "", City = "" };
        var cmd     = new CreateOrderCommand(request);

        var result = _sut.Validate(cmd);

        result.IsValid.Should().BeFalse();
        result.Errors.Should().HaveCountGreaterThan(1);
    }

    // ── PL narudžba ───────────────────────────────────────────────────────────

    [Fact]
    public void Validate_ValidPLRequest_ShouldPass()
    {
        var request = new CreateOrderRequest(
            ClientName: "Firma d.o.o.",
            ClientType: "PL",
            ClientIdentifier: "0101985100129",
            CollateralTypeId: 1,
            CombinedCollateralTypeId: null,
            City: "Sarajevo",
            PropertyAddress: "Obala 1",
            Branch: "POS_SARAJEVO_CENTAR",
            BranchAddress: "Zmaja od Bosne 74",
            ContactName: "Kontakt",
            ContactPhone: "061123456",
            ContactEmail: null,
            InternalNote: null,
            DeliveryContactName: "Dostava",
            AmRecipientName: "AM",
            RequestReceivedAt: new DateTime(2026, 1, 10, 10, 0, 0, DateTimeKind.Utc));

        var result = _sut.Validate(new CreateOrderCommand(request));
        result.IsValid.Should().BeTrue();
    }
}
