using System.IO;

namespace RBBH.TestAutomation.Core.Generation;

/// <summary>
/// Analizira cijeli Blazor projekat: za svaki <c>.razor</c> fajl (spojen sa eventualnim
/// <c>.razor.cs</c> code-behindom) poziva <see cref="BlazorComponentAnalyzer"/> i agregira
/// rezultate u <see cref="BlazorProjectAnalysis"/> — listu svih stranica i komponenti.
///
/// Stateless i bez IO ovisnosti (kao i <see cref="BlazorComponentAnalyzer"/>): pozivatelj
/// dostavlja već učitane fajlove, a čitanje ZIP-a/upload-a ostaje na UI sloju. Nikad ne baca.
/// </summary>
public static class BlazorProjectAnalyzer
{
    private const string RazorExt = ".razor";
    private const string CodeBehindExt = ".razor.cs";

    /// <summary>
    /// Analizira kolekciju učitanih fajlova. <c>.razor.cs</c> code-behind se spaja sa istoimenim
    /// <c>.razor</c> fajlom prije analize kako bi se tačno detektovali <c>[Parameter]</c>,
    /// <c>EventCallback</c> i HttpClient pozivi deklarisani u code-behindu.
    /// </summary>
    /// <param name="files">Učitani fajlovi projekta (relativna putanja + sadržaj).</param>
    /// <returns>Agregirani rezultat sa stranicama, komponentama i upozorenjima.</returns>
    public static BlazorProjectAnalysis Analyze(IReadOnlyCollection<BlazorRazorFile> files)
    {
        if (files is null || files.Count == 0)
            return BlazorProjectAnalysis.Empty("Projekat ne sadrži nijedan fajl.");

        // Indeks code-behind sadržaja po baznoj putanji (npr. "Pages/Foo.razor.cs" → ključ "Pages/Foo").
        var codeBehind = files
            .Where(f => IsCodeBehind(f.RelativePath))
            .GroupBy(f => StripExt(f.RelativePath, CodeBehindExt), StringComparer.OrdinalIgnoreCase)
            .ToDictionary(g => g.Key, g => g.First().Content, StringComparer.OrdinalIgnoreCase);

        var razorFiles = files
            .Where(f => IsRazor(f.RelativePath))
            .ToList();

        if (razorFiles.Count == 0)
            return BlazorProjectAnalysis.Empty("U učitanom projektu nije pronađen nijedan .razor fajl.");

        var warnings = new List<string>();
        var components = new List<BlazorComponentInfo>();

        foreach (var file in razorFiles)
        {
            if (string.IsNullOrWhiteSpace(file.Content))
            {
                warnings.Add($"Preskočen prazan fajl: {file.RelativePath}");
                continue;
            }

            var componentName = DeriveComponentName(file.RelativePath);
            var baseKey = StripExt(file.RelativePath, RazorExt);

            // Spoji code-behind ako postoji — regex analyzer radi nad konkatenacijom bez izmjena.
            var contentToAnalyze = codeBehind.TryGetValue(baseKey, out var cb)
                ? file.Content + "\n" + cb
                : file.Content;

            var spec = BlazorComponentAnalyzer.Analyze(componentName, contentToAnalyze);
            components.Add(new BlazorComponentInfo(file.RelativePath, spec, file.Content));
        }

        if (components.Count == 0)
            return new BlazorProjectAnalysis([], warnings);

        // Stranice prvo (imaju @page), pa komponente; unutar grupe alfabetski po nazivu.
        var ordered = components
            .OrderByDescending(c => c.IsPage)
            .ThenBy(c => c.Spec.ComponentName, StringComparer.OrdinalIgnoreCase)
            .ToList();

        return new BlazorProjectAnalysis(ordered, warnings);
    }

    /// <summary>Naziv komponente = ime fajla bez <c>.razor</c> ekstenzije (npr. "Pages/Grupe.razor" → "Grupe").</summary>
    private static string DeriveComponentName(string relativePath)
    {
        var name = Path.GetFileName(relativePath);
        if (name.EndsWith(RazorExt, StringComparison.OrdinalIgnoreCase))
            name = name[..^RazorExt.Length];
        return string.IsNullOrWhiteSpace(name) ? "Komponenta" : name;
    }

    private static bool IsCodeBehind(string path) =>
        path.EndsWith(CodeBehindExt, StringComparison.OrdinalIgnoreCase);

    private static bool IsRazor(string path) =>
        path.EndsWith(RazorExt, StringComparison.OrdinalIgnoreCase) && !IsCodeBehind(path);

    private static string StripExt(string path, string ext) =>
        path.EndsWith(ext, StringComparison.OrdinalIgnoreCase) ? path[..^ext.Length] : path;
}
