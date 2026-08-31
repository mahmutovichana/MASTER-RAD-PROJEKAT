using RBBH.CollateralAppraisal.Application.Common.Validation;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Common.Validation;

public sealed class TaxNumberValidatorTests
{
    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    public void Validate_NullOrWhitespace_ReturnsRequiredTaxNumberError(string? raw)
    {
        var error = Assert.Single(TaxNumberValidator.Validate(raw, "poreznibroj"));

        Assert.Equal(ValidationErrorCodes.RequiredTaxNumber, error.Code);
        Assert.Equal("poreznibroj", error.Field);
    }

    [Fact]
    public void Validate_DefaultField_IsPoreznibroj()
    {
        var error = Assert.Single(TaxNumberValidator.Validate(null));

        Assert.Equal("poreznibroj", error.Field);
    }

    [Theory]
    [InlineData("123456789012")]   // 12 cifara
    [InlineData("12345678901234")] // 14 cifara
    public void Validate_WrongLength_ReturnsInvalidTaxNumberLengthError(string raw)
    {
        var error = Assert.Single(TaxNumberValidator.Validate(raw));

        Assert.Equal(ValidationErrorCodes.InvalidTaxNumberLength, error.Code);
    }

    [Fact]
    public void Validate_NonDigits_ReturnsInvalidTaxNumberDigitsOnlyError()
    {
        var error = Assert.Single(TaxNumberValidator.Validate("12345678901A2"));

        Assert.Equal(ValidationErrorCodes.InvalidTaxNumberDigitsOnly, error.Code);
    }

    [Fact]
    public void Validate_Valid13Digits_ReturnsNoErrors()
    {
        var errors = TaxNumberValidator.Validate("4200468580006");

        Assert.Empty(errors);
    }

    [Fact]
    public void Validate_StripsSpacesAndDashes()
    {
        var errors = TaxNumberValidator.Validate("420-046-858-0006");

        Assert.Empty(errors);
    }
}
