using System.Globalization;
using Cronos;

namespace RBBH.TestAutomation.Api.Services.Schedules;

/// <summary>
/// Pomoćne funkcije za rad s 5-poljnim Cron izrazima: validacija, human-readable
/// prepis na bosanski i izračun sljedećih planiranih pokretanja (preko Cronos-a,
/// iste biblioteke koju Hangfire interno koristi).
/// </summary>
public static class CronUtil
{
    private static readonly string[] DaniSedmice =
        ["nedjeljom", "ponedjeljkom", "utorkom", "srijedom", "četvrtkom", "petkom", "subotom"];

    private static readonly string[] Mjeseci =
        ["", "januar", "februar", "mart", "april", "maj", "juni",
         "juli", "august", "septembar", "oktobar", "novembar", "decembar"];

    /// <summary>Vraća true ako je izraz validan 5-poljni Cron.</summary>
    public static bool IsValid(string? cron)
    {
        if (string.IsNullOrWhiteSpace(cron)) return false;
        try
        {
            CronExpression.Parse(cron.Trim(), CronFormat.Standard);
            return true;
        }
        catch
        {
            return false;
        }
    }

    /// <summary>
    /// Sljedećih <paramref name="count"/> planiranih pokretanja u zadatoj vremenskoj zoni.
    /// Vraća praznu listu ako je izraz nevažeći ili zona nepoznata.
    /// </summary>
    public static IReadOnlyList<DateTime> NextOccurrences(string? cron, string timezone, int count = 5)
    {
        if (!IsValid(cron) || count <= 0) return [];

        var tz = ParseTimezone(timezone);
        var expr = CronExpression.Parse(cron!.Trim(), CronFormat.Standard);

        var result = new List<DateTime>(count);
        var from = DateTimeOffset.UtcNow;

        for (var i = 0; i < count; i++)
        {
            var next = expr.GetNextOccurrence(from, tz);
            if (next is null) break;

            // Prikazujemo u lokalnom vremenu odabrane zone.
            result.Add(TimeZoneInfo.ConvertTime(next.Value, tz).DateTime);
            from = next.Value;
        }

        return result;
    }

    /// <summary>
    /// Human-readable prepis Cron izraza na bosanski. Pokriva uobičajene obrasce
    /// (fiksno vrijeme, radni dani, koraci); za složene izraze degradira na
    /// generičku poruku uz sam izraz.
    /// </summary>
    public static string Describe(string? cron)
    {
        if (string.IsNullOrWhiteSpace(cron)) return "—";
        if (!IsValid(cron)) return "Nevažeći Cron izraz";

        var parts = cron.Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries);
        var (min, hour, dom, mon, dow) = (parts[0], parts[1], parts[2], parts[3], parts[4]);

        var vrijeme = OpisiVrijeme(min, hour);
        var dani    = OpisiDane(dom, mon, dow);

        return string.IsNullOrEmpty(dani) ? vrijeme : $"{vrijeme}, {dani}";
    }

    private static string OpisiVrijeme(string min, string hour)
    {
        // Koraci po minuti: */15 * ...
        if (hour == "*" && min.StartsWith("*/"))
            return $"svakih {min[2..]} minuta";

        if (min == "*" && hour == "*")
            return "svake minute";

        // Svaki sat u fiksnoj minuti: 30 * ...
        if (hour == "*" && int.TryParse(min, out var m0))
            return $"svakog sata u {m0:D2} minuta";

        // Fiksno vrijeme: 0 8 ...
        if (int.TryParse(min, out var m) && int.TryParse(hour, out var h))
            return $"u {h:D2}:{m:D2}";

        // Raspon sati: 0 9-17 ...
        if (int.TryParse(min, out var mm) && hour.Contains('-'))
            return $"u {mm:D2} minuta, u satima {hour}";

        return $"min={min}, sat={hour}";
    }

    private static string OpisiDane(string dom, string mon, string dow)
    {
        // Radni dani
        if (dow is "1-5") return "radnim danima (pon–pet)";
        if (dow is "6,0" or "0,6" or "6,7") return "vikendom";

        // Jedan dan u sedmici
        if (int.TryParse(dow, out var d) && d is >= 0 and <= 7)
            return DaniSedmice[d == 7 ? 0 : d];

        // Lista dana u sedmici: 1,3,5
        if (dow != "*" && dow.Contains(',') && dow.Split(',').All(x => int.TryParse(x, out _)))
        {
            var imena = dow.Split(',')
                .Select(x => int.Parse(x, CultureInfo.InvariantCulture))
                .Select(x => DaniSedmice[x == 7 ? 0 : x]);
            return string.Join(", ", imena);
        }

        var dijelovi = new List<string>();

        // Dan u mjesecu
        if (dom != "*")
            dijelovi.Add(dom.StartsWith("*/") ? $"svakih {dom[2..]} dana" : $"{dom}. u mjesecu");

        // Mjesec
        if (mon != "*" && int.TryParse(mon, out var mo) && mo is >= 1 and <= 12)
            dijelovi.Add($"u mjesecu {Mjeseci[mo]}");

        return dijelovi.Count > 0 ? string.Join(", ", dijelovi) : "svaki dan";
    }

    private static TimeZoneInfo ParseTimezone(string tz)
    {
        try   { return TimeZoneInfo.FindSystemTimeZoneById(tz); }
        catch { return TimeZoneInfo.Utc; }
    }
}
