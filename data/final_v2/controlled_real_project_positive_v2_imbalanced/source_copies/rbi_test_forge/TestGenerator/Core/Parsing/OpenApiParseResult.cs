namespace RBBH.TestAutomation.Core.Parsing;

/// <summary>
/// Rezultat parsiranja OpenAPI/Swagger spec-a.
/// </summary>
/// <param name="Success">True ako je spec uspješno parsiran (dokument je validan).</param>
/// <param name="Error">Poruka greške kad <paramref name="Success"/> je false; inače null.</param>
/// <param name="Title">Naslov API-ja iz <c>info.title</c>.</param>
/// <param name="Version">Verzija iz <c>info.version</c>.</param>
/// <param name="Endpoints">Pronađeni endpointi.</param>
/// <param name="Warnings">Ne-fatalna upozorenja parsera (spec ima sitne probleme ali je upotrebljiv).</param>
public sealed record OpenApiParseResult(
    bool Success,
    string? Error,
    string Title,
    string Version,
    IReadOnlyList<ParsedEndpoint> Endpoints,
    IReadOnlyList<string> Warnings)
{
    public static OpenApiParseResult Fail(string error) =>
        new(false, error, "", "", [], []);
}
