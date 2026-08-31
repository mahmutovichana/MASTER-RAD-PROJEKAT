using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Core.Generation;

namespace RBBH.TestAutomation.Api.DTO;

/// <summary>
/// Mapira <see cref="RestScenarioDto"/> (iz ScenarioDtos) u <see cref="RestEndpointSpec"/>
/// koji generator prima. ClassName se izvodi iz naziva scenarija (PascalCase, bez razmaka).
/// </summary>
public static class GeneratorSpecMapper
{
    public static RestEndpointSpec ToSpec(string scenarioName, RestScenarioDto rest, bool requiresAuth = false)
    {
        var className = ToPascalCase(scenarioName);
        return new RestEndpointSpec(
            ClassName:       className,
            HttpMethod:      rest.Metoda.ToString().ToUpperInvariant(),
            RoutePath:       rest.Url,
            ExpectedStatus:  rest.OcekivaniStatus,
            RequestBodyJson: rest.RequestBody,
            RequiresAuth:    requiresAuth);
    }

    /// <summary>
    /// Kreira <see cref="RestEndpointSpec"/> iz ručno unesenih vrijednosti (bez vezanog scenarija).
    /// </summary>
    public static RestEndpointSpec FromManualInput(
        string className,
        string httpMethod,
        string routePath,
        int expectedStatus,
        string? requestBodyJson,
        bool requiresAuth)
        => new(className, httpMethod.ToUpperInvariant(), routePath, expectedStatus, requestBodyJson, requiresAuth);

    private static string ToPascalCase(string input)
    {
        if (string.IsNullOrWhiteSpace(input)) return "Endpoint";
        var parts = input.Split([' ', '_', '-'], StringSplitOptions.RemoveEmptyEntries);
        return string.Concat(parts.Select(p =>
            p.Length == 0 ? p : char.ToUpperInvariant(p[0]) + p[1..]));
    }
}
