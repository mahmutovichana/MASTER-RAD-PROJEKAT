using System.Text.Json;
using System.Text.RegularExpressions;
using Microsoft.OpenApi.Models;
using Microsoft.OpenApi.Readers;

namespace RBBH.TestAutomation.Core.Parsing;

/// <summary>
/// Parsira OpenAPI/Swagger spec preko <c>Microsoft.OpenApi.Readers</c> (JSON + YAML,
/// Swagger 2.0 i OpenAPI 3.x). Pretvara svaku operaciju u <see cref="ParsedEndpoint"/>:
/// metoda, ruta, parametri, primjer request body-ja (sintetizovan iz scheme), response
/// status kodovi i zahtijevane sigurnosne sheme (JWT Bearer / API Key / OAuth2...).
///
/// Stateless i thread-safe → registruje se kao Singleton.
/// </summary>
public sealed class OpenApiEndpointParser : IOpenApiEndpointParser
{
    private static readonly JsonSerializerOptions _jsonOpts = new() { WriteIndented = true };

    public OpenApiParseResult Parse(string content)
    {
        if (string.IsNullOrWhiteSpace(content))
            return OpenApiParseResult.Fail("Spec je prazan.");

        // OpenAPI 3.1 nije podržan u Microsoft.OpenApi.Readers 1.6 — koercirај deklarisanu
        // verziju na 3.0.x. Dijelovi koje čitamo (paths/operations/parametri/body/responses/
        // securitySchemes) su kompatibilni, pa spec deklarisan kao 3.1.x svejedno prolazi.
        var (effective, coerced) = CoerceVersionTo30(content);

        OpenApiDocument doc;
        OpenApiDiagnostic diagnostic;
        try
        {
            doc = new OpenApiStringReader().Read(effective, out diagnostic);
        }
        catch (Exception ex)
        {
            return OpenApiParseResult.Fail($"Spec se ne može parsirati: {ex.Message}");
        }

        if (doc is null)
            return OpenApiParseResult.Fail("Spec se ne može parsirati (nije validan OpenAPI/Swagger dokument).");

        // Fatalne greške parsiranja → fail; ne-fatalne → warnings.
        var warnings = diagnostic?.Warnings.Select(w => w.Message).ToList() ?? [];
        if (coerced)
            warnings.Insert(0, "Spec je deklarisan kao OpenAPI 3.1 — parsiran u 3.0-kompatibilnom modu.");
        if (doc.Paths is null || doc.Paths.Count == 0)
        {
            var errs = diagnostic?.Errors.Select(e => e.Message).ToList() ?? [];
            return OpenApiParseResult.Fail(errs.Count > 0
                ? "Spec nije validan: " + string.Join("; ", errs)
                : "Spec ne sadrži nijednu rutu (paths).");
        }

        // Mapa: ime sigurnosne sheme → čitljiv naziv (za auth detekciju).
        var schemes = doc.Components?.SecuritySchemes
            ?? new Dictionary<string, OpenApiSecurityScheme>();

        var endpoints = new List<ParsedEndpoint>();

        foreach (var (route, pathItem) in doc.Paths)
        {
            if (pathItem?.Operations is null) continue;

            foreach (var (opType, operation) in pathItem.Operations)
            {
                var method = opType.ToString().ToUpperInvariant();

                // Parametri: dijeljeni (path-level) + operation-level, dedupe po (naziv, lokacija).
                var allParams = (pathItem.Parameters ?? [])
                    .Concat(operation.Parameters ?? [])
                    .Where(p => p is not null)
                    .GroupBy(p => (p.Name, p.In))
                    .Select(g => g.First())
                    .Select(p => new ParsedParameter(
                        Name:     p.Name ?? "",
                        Location: p.In?.ToString().ToLowerInvariant() ?? "query",
                        Type:     p.Schema?.Type ?? "",
                        Required: p.Required))
                    .ToList();

                // Primjer JSON request body-ja iz scheme (preferiraj application/json).
                var bodySample = BuildRequestBodySample(operation.RequestBody);

                // Response status kodovi.
                var responseKeys = operation.Responses is null
                    ? Enumerable.Empty<string>()
                    : operation.Responses.Keys;
                var statuses = responseKeys
                    .Select(k => int.TryParse(k, out var c) ? c : -1)
                    .Where(c => c >= 100)
                    .OrderBy(c => c)
                    .ToList();
                var success = statuses.FirstOrDefault(s => s is >= 200 and < 300);
                if (success == 0) success = 200;

                // Auth: operation-level override, inače globalni requirements.
                var requirements = (operation.Security is { Count: > 0 })
                    ? operation.Security
                    : doc.SecurityRequirements;
                var auth = ResolveAuthSchemes(requirements, schemes);

                // Kontroler = prvi tag (Swashbuckle koristi ime kontrolera), fallback iz rute.
                var controller = operation.Tags?.FirstOrDefault()?.Name
                    ?? ControllerFromRoute(route);

                endpoints.Add(new ParsedEndpoint(
                    HttpMethod:            method,
                    Route:                 route,
                    Controller:            controller,
                    OperationId:           operation.OperationId,
                    Summary:               operation.Summary ?? operation.OperationId,
                    Parameters:            allParams,
                    RequestBodyJsonSample: bodySample,
                    SuccessStatus:         success,
                    ResponseStatuses:      statuses,
                    AuthSchemes:           auth));
            }
        }

        var ordered = endpoints
            .OrderBy(e => e.Controller, StringComparer.OrdinalIgnoreCase)
            .ThenBy(e => e.Route, StringComparer.OrdinalIgnoreCase)
            .ToList();

        return new OpenApiParseResult(
            Success:   true,
            Error:     null,
            Title:     doc.Info?.Title ?? "API",
            Version:   doc.Info?.Version ?? "",
            Endpoints: ordered,
            Warnings:  warnings);
    }

    // ── Auth ────────────────────────────────────────────────────────────────

    private static IReadOnlyList<string> ResolveAuthSchemes(
        IList<OpenApiSecurityRequirement>? requirements,
        IDictionary<string, OpenApiSecurityScheme> componentSchemes)
    {
        if (requirements is null || requirements.Count == 0) return [];

        var names = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var req in requirements)
        {
            foreach (var key in req.Keys)
            {
                // Requirement key je često referenca (stub) — razriješi na komponentnu shemu.
                var resolved = key;
                var refId = key.Reference?.Id;
                if (refId is not null && componentSchemes.TryGetValue(refId, out var full))
                    resolved = full;

                names.Add(FriendlyAuthName(resolved));
            }
        }
        return names.ToList();
    }

    private static string FriendlyAuthName(OpenApiSecurityScheme scheme) => scheme.Type switch
    {
        SecuritySchemeType.Http when Eq(scheme.Scheme, "bearer") => "JWT Bearer",
        SecuritySchemeType.Http when Eq(scheme.Scheme, "basic")  => "Basic Auth",
        SecuritySchemeType.Http          => "HTTP " + (scheme.Scheme ?? "auth"),
        SecuritySchemeType.ApiKey        => "API Key",
        SecuritySchemeType.OAuth2        => "OAuth2",
        SecuritySchemeType.OpenIdConnect => "OpenID Connect",
        _                                => scheme.Type.ToString(),
    };

    private static bool Eq(string? a, string b) =>
        string.Equals(a, b, StringComparison.OrdinalIgnoreCase);

    // ── Request body sample ──────────────────────────────────────────────────

    private static string? BuildRequestBodySample(OpenApiRequestBody? body)
    {
        var content = body?.Content;
        if (content is null || content.Count == 0) return null;

        // Preferiraj application/json; inače prvi tip koji ima schemu.
        var media = content.TryGetValue("application/json", out var json)
            ? json
            : content.Values.FirstOrDefault(m => m?.Schema is not null);

        if (media?.Schema is null) return null;

        var sample = BuildSample(media.Schema, 0);
        return sample is null ? null : JsonSerializer.Serialize(sample, _jsonOpts);
    }

    /// <summary>Rekurzivno sintetizuje primjer vrijednosti iz OpenAPI scheme (depth-guard protiv cikličnih $ref).</summary>
    private static object? BuildSample(OpenApiSchema? schema, int depth)
    {
        if (schema is null || depth > 5) return null;

        var type = schema.Type;
        if (string.IsNullOrEmpty(type) && schema.Properties is { Count: > 0 })
            type = "object";

        switch (type)
        {
            case "object":
                var obj = new Dictionary<string, object?>();
                if (schema.Properties is not null)
                    foreach (var (name, prop) in schema.Properties)
                        obj[name] = BuildSample(prop, depth + 1);
                return obj;

            case "array":
                var item = BuildSample(schema.Items, depth + 1);
                return item is null ? new List<object?>() : new List<object?> { item };

            case "integer": return 0;
            case "number":  return 0.0;
            case "boolean": return true;
            case "string":  return SampleString(schema.Format);
            default:        return null;
        }
    }

    private static string SampleString(string? format) => format switch
    {
        "date-time"     => "2024-01-01T00:00:00Z",
        "date"          => "2024-01-01",
        "uuid" or "guid" => "00000000-0000-0000-0000-000000000000",
        "email"         => "user@example.com",
        "uri" or "url"  => "https://example.com",
        "byte"          => "U3RyaW5n",
        _               => "string",
    };

    // ── Helpers ──────────────────────────────────────────────────────────────

    // Zamijeni deklaraciju "openapi: 3.1.x" → "3.0.3" (i u JSON i u YAML obliku).
    // Anchor na `openapi` ključ da ne diramo info.version. Vraća (sadržaj, da_li_je_koercirano).
    private static readonly Regex _v31 = new(
        @"(openapi""?\s*:\s*""?)3\.1(?:\.\d+)?",
        RegexOptions.IgnoreCase | RegexOptions.Compiled);

    private static (string content, bool coerced) CoerceVersionTo30(string content)
    {
        var replaced = _v31.Replace(content, "${1}3.0.3", 1);
        return (replaced, !ReferenceEquals(replaced, content) && replaced != content);
    }

    private static string ControllerFromRoute(string route)
    {
        // /api/transactions/{id} → "transactions"; uzmi prvi segment koji nije {param} ni "api".
        var seg = route.Split('/', StringSplitOptions.RemoveEmptyEntries)
            .FirstOrDefault(s => !s.StartsWith('{') && !Eq(s, "api"));
        return seg ?? "API";
    }
}
