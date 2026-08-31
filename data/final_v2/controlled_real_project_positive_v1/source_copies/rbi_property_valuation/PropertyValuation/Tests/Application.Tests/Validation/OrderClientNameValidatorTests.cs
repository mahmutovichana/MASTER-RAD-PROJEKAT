using FluentAssertions;
using RBBH.CollateralAppraisal.Application.Common.Validation;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Validation;

public sealed class OrderClientNameValidatorTests
{
    // ── FL — delegira PersonNameValidator ────────────────────────────────────

    [Fact]
    public void Validate_FL_ValidName_ShouldReturnEmpty()
    {
        var errors = OrderClientNameValidator.Validate("Amar Amarović", "FL", "clientName");
        errors.Should().BeEmpty();
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("  ")]
    public void Validate_FL_EmptyName_ShouldReturnError(string? name)
    {
        var errors = OrderClientNameValidator.Validate(name, "FL", "clientName");
        errors.Should().HaveCount(1);
        errors[0].Field.Should().Be("clientName");
    }

    [Fact]
    public void Validate_FL_NameTooShort_ShouldReturnError()
    {
        var errors = OrderClientNameValidator.Validate("A", "FL", "clientName");
        errors.Should().HaveCount(1);
    }

    // ── PL — slobodniji format (firma) ────────────────────────────────────────

    [Fact]
    public void Validate_PL_ValidCompanyName_ShouldReturnEmpty()
    {
        var errors = OrderClientNameValidator.Validate("Firma d.o.o.", "PL", "clientName");
        errors.Should().BeEmpty();
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    public void Validate_PL_EmptyName_ShouldReturnRequired(string? name)
    {
        var errors = OrderClientNameValidator.Validate(name, "PL", "clientName");
        errors.Should().HaveCount(1);
        errors[0].Code.Should().Be(ValidationErrorCodes.RequiredField);
    }

    [Fact]
    public void Validate_PL_NameTooShort_ShouldReturnError()
    {
        // Manje od 2 znaka
        var errors = OrderClientNameValidator.Validate("A", "PL", "clientName");
        errors.Should().HaveCount(1);
        errors[0].Code.Should().Be(ValidationErrorCodes.InvalidFormat);
    }

    [Fact]
    public void Validate_PL_NameExactly2Chars_ShouldPass()
    {
        // BVA: min boundary
        var errors = OrderClientNameValidator.Validate("AB", "PL", "clientName");
        errors.Should().BeEmpty();
    }

    [Fact]
    public void Validate_PL_NameExactly300Chars_ShouldPass()
    {
        // BVA: max boundary
        var errors = OrderClientNameValidator.Validate(new string('A', 300), "PL", "clientName");
        errors.Should().BeEmpty();
    }

    [Fact]
    public void Validate_PL_Name301Chars_ShouldReturnError()
    {
        // BVA: max+1
        var errors = OrderClientNameValidator.Validate(new string('A', 301), "PL", "clientName");
        errors.Should().HaveCount(1);
        errors[0].Code.Should().Be(ValidationErrorCodes.InvalidFormat);
    }

    // ── PL — dangerous chars (XSS prevencija) ────────────────────────────────

    [Theory]
    [InlineData("<script>")]
    [InlineData(">alert")]
    [InlineData("Firma & Co")]
    [InlineData("Firma \"test\"")]
    [InlineData("O'Brien Ltd")]
    public void Validate_PL_NameWithDangerousChar_ShouldReturnInvalidChars(string name)
    {
        var errors = OrderClientNameValidator.Validate(name, "PL", "clientName");
        errors.Should().HaveCount(1);
        errors[0].Code.Should().Be(ValidationErrorCodes.InvalidCharacters);
    }

    [Fact]
    public void Validate_PL_NameWithSafeSpecialChars_ShouldPass()
    {
        // Tačka i zarez su OK za firma naziv
        var errors = OrderClientNameValidator.Validate("Firma d.o.o., Sarajevo", "PL", "clientName");
        errors.Should().BeEmpty();
    }

    // ── ContainsDangerousChars ────────────────────────────────────────────────

    [Theory]
    [InlineData("clean text", false)]
    [InlineData("<inject>", true)]
    [InlineData(">inject", true)]
    [InlineData("AT&T", true)]
    [InlineData("say \"hello\"", true)]
    [InlineData("it's", true)]
    public void ContainsDangerousChars_ShouldReturnExpected(string input, bool expected)
    {
        var result = OrderClientNameValidator.ContainsDangerousChars(input);
        result.Should().Be(expected);
    }

    // ── Null clientType (PL fallback) ────────────────────────────────────────

    [Fact]
    public void Validate_NullClientType_ShouldUsePlLogic()
    {
        // null clientType → PL putanja (ne FL)
        var errors = OrderClientNameValidator.Validate("Firma", null, "clientName");
        errors.Should().BeEmpty("null clientType koristi PL logiku, 'Firma' je validan");
    }

    [Fact]
    public void Validate_NullClientType_WithDangerousChar_ShouldFail()
    {
        var errors = OrderClientNameValidator.Validate("Firma<test>", null, "clientName");
        errors.Should().HaveCount(1);
        errors[0].Code.Should().Be(ValidationErrorCodes.InvalidCharacters);
    }
}
