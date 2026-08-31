using RBBH.CollateralAppraisal.Application.Common.Validation;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Common.Validation;

public sealed class JmbgValidatorTests
{
    // ── Valjani JMBG-ovi ────────────────────────────────────────────────────

    [Theory]
    [InlineData("0101990000019")] // 01/01/1990, K=9
    [InlineData("1506985440012")] // 15/06/1985, K=2
    public void Validate_ValidJmbg_ReturnsNoErrors(string jmbg)
    {
        Assert.Empty(JmbgValidator.Validate(jmbg));
    }

    [Fact]
    public void Validate_ValidJmbg_KEqualsZeroWhenMEqualsEleven()
    {
        // sum=22 → sum%11=0 → m=11 → K=0; datum 01/01/2000 validan
        Assert.Empty(JmbgValidator.Validate("0101000000060"));
    }

    // ── Obavezno polje ──────────────────────────────────────────────────────

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    public void Validate_NullOrEmpty_ReturnsRequiredJmbgError(string? jmbg)
    {
        var error = Assert.Single(JmbgValidator.Validate(jmbg));
        Assert.Equal(ValidationErrorCodes.RequiredJmbg, error.Code);
    }

    // ── Samo cifre ──────────────────────────────────────────────────────────

    [Theory]
    [InlineData("010198510012A")]
    [InlineData("0101985100 23")]
    [InlineData("ABCDEFGHIJKLM")]
    public void Validate_NonDigits_ReturnsInvalidJmbgDigitsOnlyError(string jmbg)
    {
        var error = Assert.Single(JmbgValidator.Validate(jmbg));
        Assert.Equal(ValidationErrorCodes.InvalidJmbgDigitsOnly, error.Code);
    }

    // ── Dužina ──────────────────────────────────────────────────────────────

    [Theory]
    [InlineData("123456789012")]   // 12 cifara
    [InlineData("12345678901234")] // 14 cifara
    [InlineData("0")]              // 1 cifra
    public void Validate_WrongLength_ReturnsInvalidJmbgLengthError(string jmbg)
    {
        var error = Assert.Single(JmbgValidator.Validate(jmbg));
        Assert.Equal(ValidationErrorCodes.InvalidJmbgLength, error.Code);
    }

    // ── Datum ───────────────────────────────────────────────────────────────

    [Theory]
    [InlineData("0113985000019")] // MM=13 → nevažeći mjesec
    [InlineData("3002985000013")] // 30. februar → ne postoji
    [InlineData("0001985000019")] // DD=00 → nevažeći dan
    [InlineData("0100985000019")] // MM=00 → nevažeći mjesec
    [InlineData("0101100000013")] // godina 2100 → budućnost
    public void Validate_InvalidDate_ReturnsInvalidJmbgDatePartError(string jmbg)
    {
        var error = Assert.Single(JmbgValidator.Validate(jmbg));
        Assert.Equal(ValidationErrorCodes.InvalidJmbgDatePart, error.Code);
    }

    // ── Kontrolna cifra ─────────────────────────────────────────────────────

    [Fact]
    public void Validate_WrongChecksumDigit_ReturnsInvalidJmbgChecksumError()
    {
        // "0101990000019" je valjano (K=9); promijeni K na 8 → neispravno
        var error = Assert.Single(JmbgValidator.Validate("0101990000018"));
        Assert.Equal(ValidationErrorCodes.InvalidJmbgChecksum, error.Code);
    }

    [Fact]
    public void Validate_MEqualsTen_ReturnsInvalidJmbgChecksumError()
    {
        // sum=12 → sum%11=1 → m=10 → inherentno nevaljano (K bi bila 10)
        var error = Assert.Single(JmbgValidator.Validate("0101000000010"));
        Assert.Equal(ValidationErrorCodes.InvalidJmbgChecksum, error.Code);
    }

    // ── Parametar field ─────────────────────────────────────────────────────

    [Fact]
    public void Validate_CustomField_ErrorUsesCustomField()
    {
        var error = Assert.Single(JmbgValidator.Validate(null, "mojPolje"));
        Assert.Equal("mojPolje", error.Field);
    }

    [Fact]
    public void Validate_DefaultField_IsJmbg()
    {
        var error = Assert.Single(JmbgValidator.Validate(null));
        Assert.Equal("jmbg", error.Field);
    }
}
