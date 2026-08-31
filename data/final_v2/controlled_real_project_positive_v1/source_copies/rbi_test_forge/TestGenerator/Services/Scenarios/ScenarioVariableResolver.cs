using System.Text.RegularExpressions;
using RBBH.TestAutomation.Api.DTO;

namespace RBBH.TestAutomation.Api.Services.Scenarios;

/// <summary>
/// Zamjena <c>{{naziv}}</c> placeholdera u tekstu konkretnim vrijednostima iz <see cref="RunConfigDto"/>.
///
/// Čista klasa bez side-efekata i I/O — laka za unit testove i sigurna za poziv iz UI-a.
/// Regex se kompajlira jednom pri učitavanju klase (ne po pozivu).
/// </summary>
public static class ScenarioVariableResolver
{
    // Podudara {{naziv}} i {{ naziv }} (whitespace unutar vitičastih zagrada — trim se radi u evaluatoru).
    private static readonly Regex TokenRegex =
        new(@"\{\{\s*(\w+)\s*\}\}", RegexOptions.Compiled | RegexOptions.IgnoreCase);

    /// <summary>
    /// Zamjenjuje sve <c>{{naziv}}</c> tokene u <paramref name="template"/> vrijednostima
    /// iz <paramref name="config"/>. Poređenje naziva je case-insensitive.
    /// Nepoznati token ostaje doslovan u izlazu (ne baca iznimku).
    /// Null ili prazan template vraća prazan string.
    /// </summary>
    public static string Resolve(string? template, RunConfigDto config)
    {
        if (string.IsNullOrEmpty(template))
            return string.Empty;

        var lookup = config.Varijable
            .ToDictionary(v => v.Naziv, v => v.Vrijednost, StringComparer.OrdinalIgnoreCase);

        return TokenRegex.Replace(template, m =>
        {
            var naziv = m.Groups[1].Value.Trim();
            return lookup.TryGetValue(naziv, out var val) ? val : m.Value;
        });
    }

    /// <summary>
    /// Vraća jedinstvena imena svih varijabli korištenih u <paramref name="template"/>
    /// (npr. <c>["baseUrl", "token"]</c>). Bez duplikata, bez obzira na redoslijed pojavljivanja.
    /// Null ili prazan template vraća praznu listu.
    /// </summary>
    public static IReadOnlyList<string> ExtractTokens(string? template)
    {
        if (string.IsNullOrEmpty(template))
            return [];

        return TokenRegex
            .Matches(template)
            .Select(m => m.Groups[1].Value.Trim())
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .ToList();
    }

    /// <summary>
    /// Vraća nazive varijabli koje su korištene u <paramref name="template"/> ali
    /// <b>nemaju</b> vrijednost u <paramref name="config"/>. Koristi se u UI
    /// za prikaz upozorenja "Nerazriješene varijable".
    /// Null ili prazan template vraća praznu listu.
    /// </summary>
    public static IReadOnlyList<string> FindUnknownTokens(string? template, RunConfigDto config)
    {
        if (string.IsNullOrEmpty(template))
            return [];

        var known = config.Varijable
            .Select(v => v.Naziv)
            .ToHashSet(StringComparer.OrdinalIgnoreCase);

        return ExtractTokens(template)
            .Where(t => !known.Contains(t))
            .ToList();
    }
}
