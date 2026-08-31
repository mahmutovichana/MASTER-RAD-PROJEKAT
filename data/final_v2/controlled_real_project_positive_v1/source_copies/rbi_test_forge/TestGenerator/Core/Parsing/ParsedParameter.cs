namespace RBBH.TestAutomation.Core.Parsing;

/// <summary>
/// Jedan parametar endpointa pročitan iz OpenAPI spec-a.
/// </summary>
/// <param name="Name">Naziv parametra.</param>
/// <param name="Location">Lokacija: <c>path</c>, <c>query</c>, <c>header</c> ili <c>cookie</c>.</param>
/// <param name="Type">Tip iz scheme (npr. <c>string</c>, <c>integer</c>); prazno ako nije naveden.</param>
/// <param name="Required">Da li je parametar obavezan.</param>
public sealed record ParsedParameter(
    string Name,
    string Location,
    string Type,
    bool Required);
