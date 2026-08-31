namespace RBBH.CollateralAppraisal.Application.Common;

public static class BusinessDaysHelper
{
    /// <summary>Dodaje N radnih dana preskačući subotu i nedjelju.</summary>
    public static DateTime AddBusinessDays(DateTime start, int days)
    {
        var date  = start;
        var added = 0;
        while (added < days)
        {
            date = date.AddDays(1);
            if (date.DayOfWeek != DayOfWeek.Saturday && date.DayOfWeek != DayOfWeek.Sunday)
                added++;
        }
        return date;
    }

    /// <summary>Oduzima N radnih dana od datuma (preskače vikende).</summary>
    public static DateTime SubtractBusinessDays(DateTime start, int days)
    {
        var date      = start;
        var subtracted = 0;
        while (subtracted < days)
        {
            date = date.AddDays(-1);
            if (date.DayOfWeek != DayOfWeek.Saturday && date.DayOfWeek != DayOfWeek.Sunday)
                subtracted++;
        }
        return date;
    }

    /// <summary>Vraća broj radnih dana između dvije datetime vrijednosti.</summary>
    public static int BusinessDaysBetween(DateTime from, DateTime to)
    {
        if (to <= from) return 0;
        var count = 0;
        var date  = from.Date.AddDays(1);
        while (date <= to.Date)
        {
            if (date.DayOfWeek != DayOfWeek.Saturday && date.DayOfWeek != DayOfWeek.Sunday)
                count++;
            date = date.AddDays(1);
        }
        return count;
    }
}