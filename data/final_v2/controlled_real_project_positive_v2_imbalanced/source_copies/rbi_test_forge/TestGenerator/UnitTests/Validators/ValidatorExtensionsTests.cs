using RBBH.TestAutomation.Api.Validators;

namespace UnitTests.Validators;

public class ValidatorExtensionsTests
{
    [Theory]
    [InlineData("\u0160\u0107epan", "scepan")]
    [InlineData("\u0160\u0107epan", "SCEPAN")]
    [InlineData("\u0160\u0107epan", "\u0107ep")]
    [InlineData("\u0110or\u0111e", "djordje")]
    public void ContainsNormalized_WhenTextMatchesIgnoringCaseAndDiacritics_ReturnsTrue(
        string value,
        string searchTerm
    )
    {
        Assert.True(value.ContainsNormalized(searchTerm));
    }

    [Fact]
    public void ContainsNormalized_WhenSearchTermIsEmpty_ReturnsTrue()
    {
        Assert.True("Naziv".ContainsNormalized(""));
    }
}
