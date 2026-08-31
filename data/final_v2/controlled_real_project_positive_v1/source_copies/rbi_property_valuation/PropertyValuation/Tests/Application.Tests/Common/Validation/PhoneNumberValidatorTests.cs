using RBBH.CollateralAppraisal.Application.Common.Validation;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Common.Validation;

public sealed class PhoneNumberValidatorTests
{
    [Theory]
    [InlineData("+38761123456")]
    [InlineData("061123456")]
    [InlineData("062123456")]
    [InlineData("061-123-456")]
    [InlineData("061 123 456")]
    [InlineData("(061) 123-456")]
    public void Validate_ValidPhoneNumbers_ReturnsNoErrors(string phone)
    {
        var errors = PhoneNumberValidator.Validate(phone, "contactPhone");

        Assert.Empty(errors);
    }

    [Fact]
    public void Validate_Empty_ReturnsRequiredFieldError()
    {
        var errors = PhoneNumberValidator.Validate("", "contactPhone");

        var error = Assert.Single(errors);
        Assert.Equal(ValidationErrorCodes.RequiredField, error.Code);
    }

    [Theory]
    [InlineData("123")]
    [InlineData("+1234567890123")]
    [InlineData("0611234567")]
    [InlineData("+38661123456")]
    [InlineData("abc123456")]
    public void Validate_InvalidFormat_ReturnsInvalidPhoneFormatError(string phone)
    {
        var errors = PhoneNumberValidator.Validate(phone, "contactPhone");

        var error = Assert.Single(errors);
        Assert.Equal(ValidationErrorCodes.InvalidPhoneFormat, error.Code);
    }

    // ── Boundary additions ────────────────────────────────────────────────────

    [Fact]
    public void Validate_Null_ReturnsRequiredFieldError()
    {
        var errors = PhoneNumberValidator.Validate(null, "contactPhone");

        var error = Assert.Single(errors);
        Assert.Equal(ValidationErrorCodes.RequiredField, error.Code);
    }

    [Fact]
    public void Validate_Whitespace_ReturnsRequiredFieldError()
    {
        var errors = PhoneNumberValidator.Validate("   ", "contactPhone");

        var error = Assert.Single(errors);
        Assert.Equal(ValidationErrorCodes.RequiredField, error.Code);
    }

    [Theory]
    [InlineData("+38765123456")]
    [InlineData("+38762123456")]
    [InlineData("+38763123456")]
    public void Validate_OtherBHNetworks_ReturnsNoErrors(string phone)
    {
        var errors = PhoneNumberValidator.Validate(phone, "contactPhone");

        Assert.Empty(errors);
    }
}
