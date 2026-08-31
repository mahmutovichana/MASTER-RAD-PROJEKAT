namespace RBBH.TestAutomation.Core.Generation;

/// <summary>
/// Jedan učitani fajl Blazor projekta — relativna putanja unutar projekta + sirovi sadržaj.
/// Pozivatelj (UI sloj) puni ovu kolekciju iz ZIP-a ili odabranih fajlova; Core ne radi IO.
/// </summary>
public sealed record BlazorRazorFile(string RelativePath, string Content);

/// <summary>
/// Rezultat analize jedne komponente unutar projekta: putanja fajla, njen
/// <see cref="BlazorComponentSpec"/> i sirovi sadržaj <c>.razor</c> fajla (za spremanje/preview).
/// </summary>
/// <param name="FilePath">Relativna putanja <c>.razor</c> fajla unutar projekta.</param>
/// <param name="Spec">Detektovane karakteristike komponente (rute, parametri, callbacki, HTTP, forme).</param>
/// <param name="RawContent">Originalni sadržaj <c>.razor</c> fajla (bez spojenog code-behinda).</param>
public sealed record BlazorComponentInfo(string FilePath, BlazorComponentSpec Spec, string RawContent)
{
    /// <summary>True ako komponenta ima bar jednu <c>@page</c> rutu (routabilna stranica).</summary>
    public bool IsPage => Spec.Routes.Count > 0;
}

/// <summary>
/// Agregirani rezultat analize cijelog Blazor projekta — lista svih stranica i komponenti,
/// uz ne-fatalna upozorenja (npr. preskočeni prazni fajlovi). Analiza nikad ne baca;
/// problemi se signaliziraju kroz <see cref="Warnings"/> i praznu <see cref="Components"/> listu.
/// </summary>
public sealed record BlazorProjectAnalysis(
    IReadOnlyList<BlazorComponentInfo> Components,
    IReadOnlyList<string> Warnings)
{
    /// <summary>Broj routabilnih stranica (komponente s <c>@page</c> direktivom).</summary>
    public int PageCount => Components.Count(c => c.IsPage);

    /// <summary>Broj običnih komponenti (bez <c>@page</c> direktive).</summary>
    public int ComponentCount => Components.Count(c => !c.IsPage);

    /// <summary>Ukupan broj detektovanih ruta kroz cijeli projekat.</summary>
    public int TotalRoutes => Components.Sum(c => c.Spec.Routes.Count);

    /// <summary>Ukupan broj detektovanih formi kroz cijeli projekat.</summary>
    public int TotalForms => Components.Sum(c => c.Spec.Forms.Count);

    /// <summary>Ukupan broj detektovanih HttpClient poziva kroz cijeli projekat.</summary>
    public int TotalHttpCalls => Components.Sum(c => c.Spec.HttpCalls.Count);

    /// <summary>Prazan rezultat s jednim upozorenjem — za slučaj da projekat nema upotrebljivih fajlova.</summary>
    public static BlazorProjectAnalysis Empty(string warning) => new([], [warning]);
}
