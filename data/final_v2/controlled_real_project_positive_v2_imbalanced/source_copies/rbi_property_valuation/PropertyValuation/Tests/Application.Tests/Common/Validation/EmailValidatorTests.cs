using RBBH.CollateralAppraisal.Application.Common.Validation;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Common.Validation;

public sealed class EmailValidatorTests
{
    [Fact]
    public void Validate_NullOrEmpty_ReturnsNoErrors()
    {
        Assert.Empty(EmailValidator.Validate(null, "contactEmail"));
        Assert.Empty(EmailValidator.Validate("", "contactEmail"));
    }

    [Theory]
    [InlineData("test@test.ba")]
    [InlineData("petar.petrovic@example.com")]
    [InlineData("user+tag@sub.domain.org")]
    public void Validate_ValidEmails_ReturnsNoErrors(string email)
    {
        var errors = EmailValidator.Validate(email, "contactEmail");

        Assert.Empty(errors);
    }

    [Theory]
    [InlineData("test@")]
    [InlineData("@test.ba")]
    [InlineData("test.ba")]
    [InlineData("test@test")]
    public void Validate_InvalidFormat_ReturnsInvalidEmailFormatError(string email)
    {
        var errors = EmailValidator.Validate(email, "contactEmail");

        var error = Assert.Single(errors);
        Assert.Equal(ValidationErrorCodes.InvalidEmailFormat, error.Code);
    }

    [Fact]
    public void Validate_TooLong_ReturnsMaxLengthExceededError()
    {
        var longLocalPart = new string('a', 195);
        var email = $"{longLocalPart}@test.ba"; // > 200 znakova ukupno

        var errors = EmailValidator.Validate(email, "contactEmail");

        var error = Assert.Single(errors);
        Assert.Equal(ValidationErrorCodes.MaxLengthExceeded, error.Code);
    }
}
