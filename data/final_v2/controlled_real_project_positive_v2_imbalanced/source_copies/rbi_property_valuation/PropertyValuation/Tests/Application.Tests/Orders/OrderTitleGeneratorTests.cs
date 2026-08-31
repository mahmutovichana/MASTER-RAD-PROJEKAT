using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Infrastructure.Orders;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

public sealed class OrderTitleGeneratorTests
{
    private readonly IOrderTitleGenerator _sut = new OrderTitleGenerator();

    // ── Happy path ────────────────────────────────────────────────────────────

    [Fact]
    public void Generate_BasicCollateral_ReturnsCorrectTitle()
    {
        var title = _sut.Generate("APP-stan", null, "Petar Petrović", "Sarajevo");

        Assert.Equal(
            "Narudžba procjene za APP-stan za klijenta Petar Petrović grad Sarajevo",
            title);
    }

    [Fact]
    public void Generate_CombinedCollateral_UsesCombinedLabel()
    {
        var title = _sut.Generate("APP-stan", "APP-stan i garaža", "Amina Bešić", "Tuzla");

        Assert.Equal(
            "Narudžba procjene za APP-stan i garaža za klijenta Amina Bešić grad Tuzla",
            title);
    }

    [Fact]
    public void Generate_TripleCombined_UsesCombinedLabel()
    {
        var title = _sut.Generate("APP-stan", "APP-stan garaža i ostava", "ABC d.o.o.", "Mostar");

        Assert.Equal(
            "Narudžba procjene za APP-stan garaža i ostava za klijenta ABC d.o.o. grad Mostar",
            title);
    }

    [Fact]
    public void Generate_NullCombined_FallsBackToBasic()
    {
        var title = _sut.Generate("Garaža", null, "Test Klijent", "Banja Luka");

        Assert.Equal(
            "Narudžba procjene za Garaža za klijenta Test Klijent grad Banja Luka",
            title);
    }

    // ── Poslovni primjeri iz specifikacije ────────────────────────────────────

    [Theory]
    [InlineData("APP-stan i garaža",        "XY", "Sarajevo",
        "Narudžba procjene za APP-stan i garaža za klijenta XY grad Sarajevo")]
    [InlineData("APP-stan i ostava",         "ZT", "Zenica",
        "Narudžba procjene za APP-stan i ostava za klijenta ZT grad Zenica")]
    [InlineData("APP-stan garaža i ostava",  "ABC", "Mostar",
        "Narudžba procjene za APP-stan garaža i ostava za klijenta ABC grad Mostar")]
    public void Generate_SpecificationExamples(
        string combinedLabel, string client, string city, string expected)
    {
        var title = _sut.Generate("APP-stan", combinedLabel, client, city);
        Assert.Equal(expected, title);
    }
}
