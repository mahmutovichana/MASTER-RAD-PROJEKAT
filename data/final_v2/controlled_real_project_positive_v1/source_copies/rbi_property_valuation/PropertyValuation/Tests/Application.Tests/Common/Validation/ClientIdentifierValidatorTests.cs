using RBBH.CollateralAppraisal.Application.Common.Validation;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Common.Validation;

public sealed class ClientIdentifierValidatorTests
{
    [Theory]
    [InlineData("FL")]
    [InlineData("PL")]
    [InlineData(null)]
    public void Validate_NullOrEmpty_ReturnsRequiredJmbgError(string? clientType)
    {
        var errorsNull  = ClientIdentifierValidator.Validate(null, clientType, "clientIdentifier");
        var errorsEmpty = ClientIdentifierValidator.Validate("", clientType, "clientIdentifier");

        Assert.Equal(ValidationErrorCodes.RequiredJmbg, Assert.Single(errorsNull).Code);
        Assert.Equal(ValidationErrorCodes.RequiredJmbg, Assert.Single(errorsEmpty).Code);
    }

    [Theory]
    [InlineData("FL")]
    [InlineData("PL")]
    public void Validate_WithValidJmbg_ReturnsNoErrors(string clientType)
    {
        // 0101990000019: datum 01/01/1990, K=9 (valjano)
        var errors = ClientIdentifierValidator.Validate("0101990000019", clientType, "clientIdentifier");

        Assert.Empty(errors);
    }

    [Theory]
    [InlineData("FL", "123456789012")]   // 12 cifara
    [InlineData("FL", "12345678901234")] // 14 cifara
    [InlineData("PL", "123456789012")]   // 12 cifara
    [InlineData("PL", "12345678901234")] // 14 cifara
    public void Validate_WrongLength_ReturnsInvalidJmbgLengthError(string clientType, string value)
    {
        var errors = ClientIdentifierValidator.Validate(value, clientType, "clientIdentifier");

        var error = Assert.Single(errors);
        Assert.Equal(ValidationErrorCodes.InvalidJmbgLength, error.Code);
    }

    [Theory]
    [InlineData("FL")]
    [InlineData("PL")]
    public void Validate_NonDigits_ReturnsInvalidJmbgDigitsOnlyError(string clientType)
    {
        var errors = ClientIdentifierValidator.Validate("010198510012A", clientType, "clientIdentifier");

        var error = Assert.Single(errors);
        Assert.Equal(ValidationErrorCodes.InvalidJmbgDigitsOnly, error.Code);
    }
}
