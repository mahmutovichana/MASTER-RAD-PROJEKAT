using RBBH.TestAutomation.Core.Parsing;

namespace UnitTests.TestForge;

/// <summary>
/// Pokriva TAG-37 kriterije: prepoznavanje HTTP metoda/kontrolera, čitanje
/// parametara/body-ja/responses, detekciju autentikacije (JWT Bearer / API Key /
/// OAuth2) i podršku za JSON i YAML.
/// </summary>
public class OpenApiEndpointParserTests
{
    private readonly IOpenApiEndpointParser _parser = new OpenApiEndpointParser();

    private const string JsonSpec = """
    {
      "openapi": "3.0.1",
      "info": { "title": "Transactions API", "version": "v1" },
      "paths": {
        "/api/transactions": {
          "get": {
            "tags": ["Transactions"],
            "summary": "Lista transakcija",
            "parameters": [
              { "name": "page", "in": "query", "required": false, "schema": { "type": "integer" } }
            ],
            "responses": { "200": { "description": "OK" }, "401": { "description": "Unauthorized" } }
          },
          "post": {
            "tags": ["Transactions"],
            "requestBody": {
              "content": {
                "application/json": {
                  "schema": {
                    "type": "object",
                    "properties": {
                      "amount": { "type": "number" },
                      "currency": { "type": "string" },
                      "createdAt": { "type": "string", "format": "date-time" }
                    }
                  }
                }
              }
            },
            "responses": { "201": { "description": "Created" }, "400": { "description": "Bad Request" } }
          }
        },
        "/api/transactions/{id}": {
          "get": {
            "tags": ["Transactions"],
            "parameters": [
              { "name": "id", "in": "path", "required": true, "schema": { "type": "string", "format": "uuid" } }
            ],
            "responses": { "200": { "description": "OK" } }
          },
          "put":   { "tags": ["Transactions"], "responses": { "200": { "description": "OK" } } },
          "patch": { "tags": ["Transactions"], "responses": { "200": { "description": "OK" } } },
          "delete":{ "tags": ["Transactions"], "responses": { "204": { "description": "No Content" } } }
        }
      },
      "components": {
        "securitySchemes": {
          "bearerAuth": { "type": "http", "scheme": "bearer", "bearerFormat": "JWT" },
          "apiKey":     { "type": "apiKey", "in": "header", "name": "X-Api-Key" },
          "oauth2":     { "type": "oauth2", "flows": { "clientCredentials": { "tokenUrl": "https://idp/token", "scopes": {} } } }
        }
      },
      "security": [ { "bearerAuth": [] } ]
    }
    """;

    [Fact]
    public void Parse_Json_RecognizesAllHttpMethods()
    {
        var result = _parser.Parse(JsonSpec);

        Assert.True(result.Success, result.Error);
        Assert.Equal("Transactions API", result.Title);

        var methods = result.Endpoints.Select(e => e.HttpMethod).ToHashSet();
        Assert.Superset(new HashSet<string> { "GET", "POST", "PUT", "PATCH", "DELETE" }, methods);
        Assert.Equal(6, result.Endpoints.Count); // 2 na /transactions + 4 na /{id}
    }

    [Fact]
    public void Parse_ReadsControllerTagRouteAndParameters()
    {
        var result = _parser.Parse(JsonSpec);

        var byId = result.Endpoints.Single(e => e.HttpMethod == "GET" && e.Route.Contains("{id}"));
        Assert.Equal("Transactions", byId.Controller);
        var idParam = Assert.Single(byId.Parameters);
        Assert.Equal("id", idParam.Name);
        Assert.Equal("path", idParam.Location);
        Assert.True(idParam.Required);
    }

    [Fact]
    public void Parse_BuildsRequestBodySampleFromSchema()
    {
        var result = _parser.Parse(JsonSpec);

        var post = result.Endpoints.Single(e => e.HttpMethod == "POST");
        Assert.NotNull(post.RequestBodyJsonSample);
        Assert.Contains("\"amount\"", post.RequestBodyJsonSample);
        Assert.Contains("\"currency\"", post.RequestBodyJsonSample);
        // format date-time daje ISO sample
        Assert.Contains("2024-01-01T00:00:00Z", post.RequestBodyJsonSample);
        Assert.Equal(201, post.SuccessStatus);
    }

    [Fact]
    public void Parse_DetectsAuthSchemes_BearerApiKeyOAuth2()
    {
        // Globalni security je bearerAuth → svi endpointi imaju JWT Bearer.
        var result = _parser.Parse(JsonSpec);

        var get = result.Endpoints.First(e => e.HttpMethod == "GET");
        Assert.True(get.RequiresAuth);
        Assert.Contains("JWT Bearer", get.AuthSchemes);
    }

    [Fact]
    public void Parse_DetectsApiKeyAndOAuth2_WhenOperationOverridesSecurity()
    {
        const string spec = """
        {
          "openapi": "3.0.1",
          "info": { "title": "X", "version": "1" },
          "paths": {
            "/secure": {
              "get": {
                "tags": ["Sec"],
                "security": [ { "apiKey": [] }, { "oauth2": ["read"] } ],
                "responses": { "200": { "description": "OK" } }
              }
            }
          },
          "components": {
            "securitySchemes": {
              "apiKey": { "type": "apiKey", "in": "header", "name": "X-Api-Key" },
              "oauth2": { "type": "oauth2", "flows": { "implicit": { "authorizationUrl": "https://idp/auth", "scopes": { "read": "r" } } } }
            }
          }
        }
        """;

        var result = _parser.Parse(spec);
        var ep = Assert.Single(result.Endpoints);
        Assert.Contains("API Key", ep.AuthSchemes);
        Assert.Contains("OAuth2", ep.AuthSchemes);
    }

    [Fact]
    public void Parse_SupportsYaml()
    {
        const string yaml = """
        openapi: 3.0.1
        info:
          title: YAML API
          version: v2
        paths:
          /api/ping:
            get:
              tags: [Health]
              responses:
                '200':
                  description: OK
        """;

        var result = _parser.Parse(yaml);

        Assert.True(result.Success, result.Error);
        Assert.Equal("YAML API", result.Title);
        var ep = Assert.Single(result.Endpoints);
        Assert.Equal("GET", ep.HttpMethod);
        Assert.Equal("/api/ping", ep.Route);
        Assert.Equal("Health", ep.Controller);
    }

    [Fact]
    public void Parse_OpenApi31_IsCoercedAndParses()
    {
        // Microsoft.OpenApi.Readers 1.6 ne podržava 3.1 — parser koercira verziju na 3.0.
        const string spec = """
        {
          "openapi": "3.1.0",
          "info": { "title": "V31 API", "version": "1.0" },
          "paths": {
            "/api/items": {
              "get": { "tags": ["Items"], "responses": { "200": { "description": "OK" } } }
            }
          }
        }
        """;

        var result = _parser.Parse(spec);

        Assert.True(result.Success, result.Error);
        Assert.Equal("V31 API", result.Title);
        var ep = Assert.Single(result.Endpoints);
        Assert.Equal("GET", ep.HttpMethod);
        Assert.Contains(result.Warnings, w => w.Contains("3.1"));
    }

    [Fact]
    public void Parse_OpenApi31_Yaml_IsCoercedAndParses()
    {
        const string yaml = """
        openapi: 3.1.0
        info:
          title: V31 YAML
          version: '1'
        paths:
          /ping:
            get:
              tags: [Health]
              responses:
                '200':
                  description: OK
        """;

        var result = _parser.Parse(yaml);

        Assert.True(result.Success, result.Error);
        Assert.Equal("V31 YAML", result.Title);
        Assert.Single(result.Endpoints);
    }

    [Fact]
    public void Parse_InvalidContent_ReturnsFailureNotThrow()
    {
        var result = _parser.Parse("ovo nije ni json ni yaml spec {{{");
        Assert.False(result.Success);
        Assert.NotNull(result.Error);
    }

    [Fact]
    public void Parse_Empty_ReturnsFailure()
    {
        Assert.False(_parser.Parse("").Success);
        Assert.False(_parser.Parse("   ").Success);
    }
}
