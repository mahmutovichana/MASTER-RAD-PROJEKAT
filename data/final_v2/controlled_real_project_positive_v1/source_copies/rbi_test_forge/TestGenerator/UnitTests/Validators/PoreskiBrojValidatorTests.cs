using RBBH.TestAutomation.Api.Validators;

namespace UnitTests.Validators;

public class PoreskiBrojValidatorTests
{
    [Theory]
    [InlineData("123456789")]
    [InlineData("123-456-789")]
    [InlineData("1234567890123")]
    public void Validate_WhenFormatIsAllowed_ReturnsNoErrors(string value)
    {
        var errors = PoreskiBrojValidator.Validate(value).ToArray();

        Assert.Empty(errors);
    }

    [Theory]
    [InlineData("")]
    [InlineData("12345678")]
    [InlineData("12345678901234")]
    [InlineData("12345A789")]
    public void Validate_WhenFormatIsInvalid_ReturnsErrors(string value)
    {
        var errors = PoreskiBrojValidator.Validate(value).ToArray();

        Assert.NotEmpty(errors);
    }
}
