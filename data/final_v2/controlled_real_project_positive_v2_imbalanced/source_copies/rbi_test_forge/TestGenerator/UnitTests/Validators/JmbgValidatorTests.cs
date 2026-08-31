using RBBH.TestAutomation.Api.Validators;

namespace UnitTests.Validators;

public class JmbgValidatorTests
{
    [Fact]
    public void Validate_WhenChecksumIsValid_ReturnsNoErrors()
    {
        var errors = JmbgValidator.Validate("0101006500006").ToArray();

        Assert.Empty(errors);
    }

    [Theory]
    [InlineData("")]
    [InlineData("010100650000")]
    [InlineData("0101006500007")]
    [InlineData("01010065000A6")]
    public void Validate_WhenValueIsInvalid_ReturnsErrors(string value)
    {
        var errors = JmbgValidator.Validate(value).ToArray();

        Assert.NotEmpty(errors);
    }
}
