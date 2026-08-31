using RBBH.CollateralAppraisal.Application.Common.Validation;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Common.Validation;

public sealed class PersonNameValidatorTests
{
    [Theory]
    [InlineData("Petar Petrović")]
    [InlineData("Šćepan Đurić-Žužić")]
    [InlineData("Ana-Marija")]
    [InlineData("Mile")]
    public void Validate_ValidNames_ReturnsNoErrors(string name)
    {
        var errors = PersonNameValidator.Validate(name, "contactName");

        Assert.Empty(errors);
    }

    [Fact]
    public void Validate_Empty_ReturnsRequiredFieldError()
    {
        var errors = PersonNameValidator.Validate("", "contactName");

        var error = Assert.Single(errors);
        Assert.Equal(ValidationErrorCodes.RequiredField, error.Code);
    }

    [Fact]
    public void Validate_Null_ReturnsRequiredFieldError()
    {
        var errors = PersonNameValidator.Validate(null, "contactName");

        var error = Assert.Single(errors);
        Assert.Equal(ValidationErrorCodes.RequiredField, error.Code);
    }

    [Theory]
    [InlineData("Petar123")]
    [InlineData("Petar@Petrović")]
    [InlineData("Petar_Petrović")]
    [InlineData("Petar😀")]
    public void Validate_DigitsOrSpecialCharacters_ReturnsInvalidFormatError(string name)
    {
        var errors = PersonNameValidator.Validate(name, "contactName");

        var error = Assert.Single(errors);
        Assert.Equal(ValidationErrorCodes.InvalidNameFormat, error.Code);
    }

    [Fact]
    public void Validate_TooShort_ReturnsInvalidFormatError()
    {
        var errors = PersonNameValidator.Validate("A", "contactName", minLength: 2, maxLength: 300);

        var error = Assert.Single(errors);
        Assert.Equal(ValidationErrorCodes.InvalidFormat, error.Code);
    }

    [Fact]
    public void Validate_TooLong_ReturnsInvalidFormatError()
    {
        var errors = PersonNameValidator.Validate(new string('A', 301), "contactName", minLength: 2, maxLength: 300);

        var error = Assert.Single(errors);
        Assert.Equal(ValidationErrorCodes.InvalidFormat, error.Code);
    }

    // ── Boundary additions ────────────────────────────────────────────────────

    [Fact]
    public void Validate_ExactlyMinLength_ReturnsNoErrors()
    {
        var errors = PersonNameValidator.Validate("AB", "contactName", minLength: 2, maxLength: 300);

        Assert.Empty(errors);
    }

    [Fact]
    public void Validate_ExactlyMaxLength_ReturnsNoErrors()
    {
        var errors = PersonNameValidator.Validate(new string('A', 300), "contactName", minLength: 2, maxLength: 300);

        Assert.Empty(errors);
    }

    [Theory]
    [InlineData("Muhamed-Armin Čaušević")]
    [InlineData("Džan")]
    [InlineData("Štefica Žunić")]
    public void Validate_BHSpecificCharacters_ReturnsNoErrors(string name)
    {
        var errors = PersonNameValidator.Validate(name, "contactName");

        Assert.Empty(errors);
    }

    [Fact]
    public void Validate_WhitespaceOnly_ReturnsRequiredFieldError()
    {
        var errors = PersonNameValidator.Validate("   ", "contactName");

        var error = Assert.Single(errors);
        Assert.Equal(ValidationErrorCodes.RequiredField, error.Code);
    }
}
