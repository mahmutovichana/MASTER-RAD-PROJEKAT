using RBBH.CollateralAppraisal.Domain.Orders;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Domain;

public sealed class WorkflowTypeTests
{
    // ── ToClientType ─────────────────────────────────────────────────────────

    [Fact]
    public void ToClientType_PravnaLica_ReturnsPL()
    {
        Assert.Equal("PL", WorkflowTypes.ToClientType(WorkflowType.PravnaLica));
    }

    [Fact]
    public void ToClientType_FizickaLica_ReturnsFL()
    {
        Assert.Equal("FL", WorkflowTypes.ToClientType(WorkflowType.FizickaLica));
    }

    // ── FromClientType ───────────────────────────────────────────────────────

    [Fact]
    public void FromClientType_PL_ReturnsPravnaLica()
    {
        Assert.Equal(WorkflowType.PravnaLica, WorkflowTypes.FromClientType("PL"));
    }

    [Theory]
    [InlineData("pl")]
    [InlineData("Pl")]
    [InlineData("pL")]
    public void FromClientType_PLCaseInsensitive_ReturnsPravnaLica(string code)
    {
        Assert.Equal(WorkflowType.PravnaLica, WorkflowTypes.FromClientType(code));
    }

    [Fact]
    public void FromClientType_FL_ReturnsFizickaLica()
    {
        Assert.Equal(WorkflowType.FizickaLica, WorkflowTypes.FromClientType("FL"));
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("XYZ")]
    [InlineData("fl")]
    public void FromClientType_NullOrUnrecognized_DefaultsToFizickaLica(string? code)
    {
        Assert.Equal(WorkflowType.FizickaLica, WorkflowTypes.FromClientType(code));
    }

    // ── Parse ────────────────────────────────────────────────────────────────

    [Theory]
    [InlineData("FL", WorkflowType.FizickaLica)]
    [InlineData("fl", WorkflowType.FizickaLica)]
    [InlineData("Fl", WorkflowType.FizickaLica)]
    [InlineData("FIZICKALICA", WorkflowType.FizickaLica)]
    [InlineData("FizickaLica", WorkflowType.FizickaLica)]
    [InlineData("FIZICKA", WorkflowType.FizickaLica)]
    [InlineData("fizicka", WorkflowType.FizickaLica)]
    public void Parse_FLVariants_ReturnsFizickaLica(string code, WorkflowType expected)
    {
        Assert.Equal(expected, WorkflowTypes.Parse(code));
    }

    [Theory]
    [InlineData("PL", WorkflowType.PravnaLica)]
    [InlineData("pl", WorkflowType.PravnaLica)]
    [InlineData("Pl", WorkflowType.PravnaLica)]
    [InlineData("PRAVNALICA", WorkflowType.PravnaLica)]
    [InlineData("PravnaLica", WorkflowType.PravnaLica)]
    [InlineData("PRAVNA", WorkflowType.PravnaLica)]
    [InlineData("pravna", WorkflowType.PravnaLica)]
    public void Parse_PLVariants_ReturnsPravnaLica(string code, WorkflowType expected)
    {
        Assert.Equal(expected, WorkflowTypes.Parse(code));
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("UNKNOWN")]
    [InlineData("FIZ")]
    [InlineData("PRAV")]
    [InlineData(" ")]
    [InlineData("F")]
    [InlineData("P")]
    public void Parse_InvalidOrNull_ReturnsNull(string? code)
    {
        Assert.Null(WorkflowTypes.Parse(code));
    }

    // ── DisplayName ──────────────────────────────────────────────────────────

    [Fact]
    public void DisplayName_FizickaLica_ReturnsExpected()
    {
        Assert.Equal("Fizička lica", WorkflowTypes.DisplayName(WorkflowType.FizickaLica));
    }

    [Fact]
    public void DisplayName_PravnaLica_ReturnsExpected()
    {
        Assert.Equal("Pravna lica", WorkflowTypes.DisplayName(WorkflowType.PravnaLica));
    }

    // ── Enum values ──────────────────────────────────────────────────────────

    [Fact]
    public void WorkflowType_HasExpectedIntValues()
    {
        Assert.Equal(1, (int)WorkflowType.FizickaLica);
        Assert.Equal(2, (int)WorkflowType.PravnaLica);
    }

    [Fact]
    public void WorkflowType_HasExactlyTwoMembers()
    {
        var values = Enum.GetValues<WorkflowType>();
        Assert.Equal(2, values.Length);
    }

    // ── Roundtrip: ToClientType -> FromClientType ────────────────────────────

    [Theory]
    [InlineData(WorkflowType.FizickaLica)]
    [InlineData(WorkflowType.PravnaLica)]
    public void ToClientType_FromClientType_Roundtrips(WorkflowType original)
    {
        var code = WorkflowTypes.ToClientType(original);
        var restored = WorkflowTypes.FromClientType(code);
        Assert.Equal(original, restored);
    }

    // ── Roundtrip: Parse -> ToClientType ─────────────────────────────────────

    [Theory]
    [InlineData("FL", "FL")]
    [InlineData("PL", "PL")]
    public void Parse_ToClientType_Roundtrips(string code, string expectedClientType)
    {
        var parsed = WorkflowTypes.Parse(code);
        Assert.NotNull(parsed);
        var clientType = WorkflowTypes.ToClientType(parsed!.Value);
        Assert.Equal(expectedClientType, clientType);
    }
}
