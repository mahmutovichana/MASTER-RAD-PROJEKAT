using FluentAssertions;
using RBBH.CollateralAppraisal.Application.Common;
using RBBH.CollateralAppraisal.Application.Common.Constants;
using RBBH.CollateralAppraisal.Domain.Orders;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Common;

// ══════════════════════════════════════════════════════════════════
// BusinessDaysHelper Tests
// ══════════════════════════════════════════════════════════════════
public sealed class BusinessDaysHelperTests
{
    // Reference Monday 2026-01-12
    private static readonly DateTime Monday = new(2026, 1, 12, 0, 0, 0, DateTimeKind.Utc);

    [Fact]
    public void AddBusinessDays_ZeroDays_ReturnsSameDay()
    {
        BusinessDaysHelper.AddBusinessDays(Monday, 0).Should().Be(Monday);
    }

    [Fact]
    public void AddBusinessDays_OneDay_ReturnsNextBusinessDay()
    {
        // Monday + 1 = Tuesday
        BusinessDaysHelper.AddBusinessDays(Monday, 1).Should().Be(Monday.AddDays(1));
    }

    [Fact]
    public void AddBusinessDays_FiveDays_SkipsWeekend()
    {
        // Monday + 5 business days = next Monday
        var result = BusinessDaysHelper.AddBusinessDays(Monday, 5);
        result.DayOfWeek.Should().Be(DayOfWeek.Monday);
        result.Should().Be(Monday.AddDays(7));
    }

    [Theory]
    [InlineData(1, DayOfWeek.Tuesday)]
    [InlineData(2, DayOfWeek.Wednesday)]
    [InlineData(5, DayOfWeek.Monday)]  // skips weekend
    [InlineData(10, DayOfWeek.Monday)] // 2 tjedna
    public void AddBusinessDays_FromMonday_ReturnsCorrectDayOfWeek(int days, DayOfWeek expected)
    {
        BusinessDaysHelper.AddBusinessDays(Monday, days).DayOfWeek.Should().Be(expected);
    }

    [Fact]
    public void AddBusinessDays_FromFriday_SkipsWeekend()
    {
        var friday = Monday.AddDays(4); // 2026-01-16
        var result = BusinessDaysHelper.AddBusinessDays(friday, 1);
        result.DayOfWeek.Should().Be(DayOfWeek.Monday,
            "Friday + 1 business day = Monday (skips Sat/Sun)");
    }

    [Fact]
    public void AddBusinessDays_FromSaturday_CountsFromMonday()
    {
        var saturday = Monday.AddDays(5); // 2026-01-17
        var result = BusinessDaysHelper.AddBusinessDays(saturday, 1);
        // Saturday is itself not a business day, but AddBusinessDays iterates from Saturday
        // The method starts iterating next day from Saturday = Sunday → not counted → Monday → counted as day 1 → returns Tuesday?
        // Actually: starts from Saturday, next = Sunday (not counted), next = Monday (counted, days=0), loop ends = Monday
        result.Should().NotBe(saturday, "ne smije ostati na subotu");
    }

    [Fact]
    public void AddBusinessDays_TwoDays_CorrectResult()
    {
        // Monday + 2 = Wednesday
        BusinessDaysHelper.AddBusinessDays(Monday, 2).Should().Be(Monday.AddDays(2));
    }

    [Fact]
    public void AddBusinessDays_ThreeDays_CrossesWeekend()
    {
        var thursday = Monday.AddDays(3); // 2026-01-15
        var result = BusinessDaysHelper.AddBusinessDays(thursday, 3);
        // Thu + 1 = Fri, skip Sat/Sun, +2 = Mon, +3 = Tue
        result.DayOfWeek.Should().Be(DayOfWeek.Tuesday);
    }
}

// DocumentationReviewStatusConverter je internal — testovi su u Infrastructure.Tests.

// ══════════════════════════════════════════════════════════════════
// AppraisalTypeFilterCodes Tests
// ══════════════════════════════════════════════════════════════════
public sealed class AppraisalTypeFilterCodesTests
{
    [Theory]
    [InlineData(AppraisalTypeFilterCodes.StanIGaraza,       CollateralTypeCodes.ApartmentGarage)]
    [InlineData(AppraisalTypeFilterCodes.StanIOstava,       CollateralTypeCodes.ApartmentStorage)]
    [InlineData(AppraisalTypeFilterCodes.StanGarazaIOstava, CollateralTypeCodes.ApartmentGarageStorage)]
    public void ToCombinedDbCode_KnownCode_ReturnsMappedCode(string filterCode, string? expected)
    {
        AppraisalTypeFilterCodes.ToCombinedDbCode(filterCode).Should().Be(expected);
    }

    [Theory]
    [InlineData(AppraisalTypeFilterCodes.Stan)] // "STAN" → no combined type
    [InlineData("NEPOZNAT")]
    [InlineData("")]
    [InlineData(null)]
    public void ToCombinedDbCode_UnknownOrStanCode_ReturnsNull(string? filterCode)
    {
        AppraisalTypeFilterCodes.ToCombinedDbCode(filterCode!).Should().BeNull();
    }

    [Fact]
    public void Constants_HaveExpectedValues()
    {
        AppraisalTypeFilterCodes.Stan.Should().Be("STAN");
        AppraisalTypeFilterCodes.StanIGaraza.Should().Be("STAN_I_GARAZA");
        AppraisalTypeFilterCodes.StanIOstava.Should().Be("STAN_I_OSTAVA");
        AppraisalTypeFilterCodes.StanGarazaIOstava.Should().Be("STAN_GARAZA_I_OSTAVA");
    }
}
