namespace RBBH.TestAutomation.Core.Parsing;

/// <summary>
/// Parsira OpenAPI/Swagger spec (JSON ili YAML, v2 ili v3) u listu endpointa
/// spremnih za generisanje test scenarija.
/// </summary>
public interface IOpenApiEndpointParser
{
    /// <summary>
    /// Parsira sadržaj spec-a. Auto-detektuje JSON/YAML. Nikad ne baca — greške
    /// vraća kroz <see cref="OpenApiParseResult.Success"/> = false.
    /// </summary>
    OpenApiParseResult Parse(string content);
}
