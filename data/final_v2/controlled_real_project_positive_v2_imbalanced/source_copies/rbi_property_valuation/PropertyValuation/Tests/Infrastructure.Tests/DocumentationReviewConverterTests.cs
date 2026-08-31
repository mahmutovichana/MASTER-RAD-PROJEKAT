using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;
using Xunit;

namespace RBBH.CollateralAppraisal.Infrastructure.Tests;

public sealed class DocumentationReviewStatusConverterTests
{
    // ── ToDbValue ─────────────────────────────────────────────────────────────

    [Theory]
    [InlineData(DocumentationReviewStatus.NijePregledano, "Nije pregledano")]
    [InlineData(DocumentationReviewStatus.UToku,          "U toku")]
    [InlineData(DocumentationReviewStatus.Vraceno,        "Vraćeno")]
    [InlineData(DocumentationReviewStatus.Odobreno,       "Odobreno")]
    public void ToDbValue_KnownStatus_ReturnsCorrectBosnianString(
        DocumentationReviewStatus input, string expected)
    {
        Assert.Equal(expected, DocumentationReviewStatusConverter.ToDbValue(input));
    }

    [Fact]
    public void ToDbValue_UnknownStatus_ThrowsArgumentOutOfRange()
    {
        var unknown = (DocumentationReviewStatus)99;
        Assert.Throws<ArgumentOutOfRangeException>(
            () => DocumentationReviewStatusConverter.ToDbValue(unknown));
    }

    // ── FromDbValue ───────────────────────────────────────────────────────────

    [Theory]
    [InlineData("Nije pregledano", DocumentationReviewStatus.NijePregledano)]
    [InlineData("U toku",          DocumentationReviewStatus.UToku)]
    [InlineData("Vraćeno",         DocumentationReviewStatus.Vraceno)]
    [InlineData("Odobreno",        DocumentationReviewStatus.Odobreno)]
    public void FromDbValue_KnownString_ReturnsCorrectEnum(
        string input, DocumentationReviewStatus expected)
    {
        Assert.Equal(expected, DocumentationReviewStatusConverter.FromDbValue(input));
    }

    [Theory]
    [InlineData("nepoznato")]
    [InlineData("")]
    [InlineData("NIJE PREGLEDANO")]
    public void FromDbValue_UnknownString_ReturnsFallbackNijePregledano(string unknown)
    {
        Assert.Equal(DocumentationReviewStatus.NijePregledano,
            DocumentationReviewStatusConverter.FromDbValue(unknown));
    }

    // ── Roundtrip ─────────────────────────────────────────────────────────────

    [Theory]
    [InlineData(DocumentationReviewStatus.NijePregledano)]
    [InlineData(DocumentationReviewStatus.UToku)]
    [InlineData(DocumentationReviewStatus.Vraceno)]
    [InlineData(DocumentationReviewStatus.Odobreno)]
    public void ToDbValue_ThenFromDbValue_RoundTrip(DocumentationReviewStatus status)
    {
        var dbValue = DocumentationReviewStatusConverter.ToDbValue(status);
        Assert.Equal(status, DocumentationReviewStatusConverter.FromDbValue(dbValue));
    }
}
