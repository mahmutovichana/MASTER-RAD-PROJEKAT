using RBBH.TestAutomation.Api.Services.Schedules;
using Xunit;

namespace UnitTests.Run;

/// <summary>
/// Unit testovi za <see cref="CronUtil"/> — validacija, human-readable prepis
/// i izračun sljedećih pokretanja preko Cronos-a.
/// </summary>
public class CronUtilTests
{
    [Theory]
    [InlineData("0 8 * * 1-5")]
    [InlineData("0 8 * * *")]
    [InlineData("*/30 * * * *")]
    [InlineData("0 * * * *")]
    public void IsValid_PrihvataValidneIzraze(string cron)
    {
        Assert.True(CronUtil.IsValid(cron));
    }

    [Theory]
    [InlineData("")]
    [InlineData(null)]
    [InlineData("0 8 * *")]          // samo 4 polja
    [InlineData("99 8 * * *")]       // minuta van opsega
    [InlineData("nije cron")]
    public void IsValid_OdbijaNevalidne(string? cron)
    {
        Assert.False(CronUtil.IsValid(cron));
    }

    [Fact]
    public void Describe_RadniDani()
    {
        var opis = CronUtil.Describe("0 8 * * 1-5");
        Assert.Contains("08:00", opis);
        Assert.Contains("radnim danima", opis);
    }

    [Fact]
    public void Describe_SvakihNMinuta()
    {
        var opis = CronUtil.Describe("*/30 * * * *");
        Assert.Contains("30 minuta", opis);
    }

    [Fact]
    public void Describe_NevalidanVraca_Poruku()
    {
        Assert.Equal("Nevažeći Cron izraz", CronUtil.Describe("99 99 * * *"));
    }

    [Fact]
    public void NextOccurrences_VracaTrazeniBroj()
    {
        var next = CronUtil.NextOccurrences("0 8 * * *", "Europe/Sarajevo", 5);
        Assert.Equal(5, next.Count);
    }

    [Fact]
    public void NextOccurrences_SuStrogoRastuca()
    {
        var next = CronUtil.NextOccurrences("0 8 * * *", "Europe/Sarajevo", 3);
        Assert.Equal(3, next.Count);
        Assert.True(next[0] < next[1] && next[1] < next[2]);
    }

    [Fact]
    public void NextOccurrences_SvakodnevnoUOsam_PogadjaSat()
    {
        var next = CronUtil.NextOccurrences("0 8 * * *", "Europe/Sarajevo", 1);
        Assert.Single(next);
        Assert.Equal(8, next[0].Hour);
        Assert.Equal(0, next[0].Minute);
    }

    [Fact]
    public void NextOccurrences_NevalidanIzraz_VracaPrazno()
    {
        var next = CronUtil.NextOccurrences("nije cron", "Europe/Sarajevo", 5);
        Assert.Empty(next);
    }

    [Fact]
    public void NextOccurrences_NepoznataZona_NeBaca()
    {
        // Nepoznata zona → fallback na UTC, i dalje vraća rezultate.
        var next = CronUtil.NextOccurrences("0 8 * * *", "Nepostojeca/Zona", 2);
        Assert.Equal(2, next.Count);
    }
}
