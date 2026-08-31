namespace RBBH.TestAutomation.Core.Generation;

/// <summary>Specifikacija jednog REST endpointa za generisanje xUnit testova.</summary>
public sealed record RestEndpointSpec(
    /// <summary>Ime klase (PascalCase, npr. "CreateTransaction"). Koristi se kao prefiks test klase i metoda.</summary>
    string ClassName,
    /// <summary>HTTP metoda velikim slovima: GET, POST, PUT, PATCH, DELETE.</summary>
    string HttpMethod,
    /// <summary>Ruta endpointa, npr. "/api/transactions".</summary>
    string RoutePath,
    /// <summary>Očekivani HTTP status za happy-path test, npr. 200 ili 201.</summary>
    int ExpectedStatus,
    /// <summary>Opcionalni JSON request body za POST/PUT/PATCH. Null = tijelo se ne šalje.</summary>
    string? RequestBodyJson,
    /// <summary>Ako true, generišu se i testovi za 401 Unauthorized.</summary>
    bool RequiresAuth);

/// <summary>Jedan generisani fajl — naziv i sadržaj.</summary>
public sealed record GeneratedTestFile(string FileName, string Content);

/// <summary>Rezultat generisanja — lista fajlova koji čine xUnit test projekat.</summary>
public sealed record GeneratedTestProject(IReadOnlyList<GeneratedTestFile> Files);

/// <summary>
/// Stateless generator xUnit test projekta iz REST endpoint specifikacije.
/// Koristi string templating (bez Roslyn-a) — emituje validan C# tekst za preview/download.
/// Registruje se kao Singleton jer nema stanja.
/// </summary>
public sealed class RestTestGenerator
{
    /// <summary>
    /// Generiše kompletan xUnit test projekat za dati REST endpoint.
    /// Vraća 4 fajla: test klasa, .csproj, WireMock fixture, Testcontainers fixture.
    /// </summary>
    public GeneratedTestProject Generate(RestEndpointSpec spec)
    {
        var files = new List<GeneratedTestFile>
        {
            new($"{spec.ClassName}Tests.cs",          BuildTestClass(spec)),
            new("GeneratedWebApplicationFactory.cs",  BuildFactory()),
            new("GeneratedTests.csproj",              BuildCsproj()),
            new("WireMockFixture.cs",                 BuildWireMockFixture()),
            new("SqlServerContainerFixture.cs",       BuildSqlServerFixture()),
        };
        return new GeneratedTestProject(files);
    }

    // ─── Privatne metode — svaka vraća string template jednog fajla ──────────

    private static string BuildTestClass(RestEndpointSpec s)
    {
        var happyCall = BuildHappyCall(s);

        // Error-path testovi se emituju samo kad imaju smisla za datu metodu — slijepe
        // pretpostavke (npr. POST malformed-body na GET endpoint) daju 405, ne 400, i lažno padaju.
        var malformedTest = BuildMalformedBodyTest(s);   // samo POST/PUT/PATCH
        var notFoundTest  = BuildNotFoundTest(s);          // samo GET
        var authTest      = s.RequiresAuth ? BuildAuthTest(s) : string.Empty;

        var happy = new System.Text.StringBuilder();
        happy.Append("    [Fact]\n");
        happy.Append($"    public async Task {s.ClassName}_HappyPath_Returns{s.ExpectedStatus}()\n");
        happy.Append("    {\n");
        if (s.RequestBodyJson is not null)
        {
            happy.Append("        var body = new StringContent(\n");
            happy.Append($"            {ToCSharpStringLiteral(s.RequestBodyJson)},\n");
            happy.Append("            System.Text.Encoding.UTF8,\n");
            happy.Append("            \"application/json\");\n");
        }
        happy.Append($"        var response = await {happyCall};\n");
        happy.Append($"        Assert.Equal((HttpStatusCode){s.ExpectedStatus}, response.StatusCode);\n");
        happy.Append("    }\n");

        return
            "using System.Net;\n" +
            "using Microsoft.AspNetCore.Mvc.Testing;\n" +
            "using Xunit;\n\n" +
            "namespace GeneratedTests;\n\n" +
            $"public class {s.ClassName}Tests : IClassFixture<GeneratedWebApplicationFactory>\n" +
            "{\n" +
            "    private readonly HttpClient _client;\n\n" +
            $"    public {s.ClassName}Tests(GeneratedWebApplicationFactory factory)\n" +
            "        => _client = factory.CreateClient();\n\n" +
            happy +
            malformedTest + notFoundTest + authTest +
            "}\n";
    }

    /// <summary>Malformed-body → 400, samo za metode koje primaju tijelo (POST/PUT/PATCH).</summary>
    private static string BuildMalformedBodyTest(RestEndpointSpec s)
    {
        var method = s.HttpMethod.ToUpperInvariant();
        if (method is not ("POST" or "PUT" or "PATCH"))
            return string.Empty;

        var call = method switch
        {
            "PUT"   => $"_client.PutAsync(\"{s.RoutePath}\", content)",
            "PATCH" => $"_client.PatchAsync(\"{s.RoutePath}\", content)",
            _       => $"_client.PostAsync(\"{s.RoutePath}\", content)",
        };

        return "\n" +
            "    [Fact]\n" +
            $"    public async Task {s.ClassName}_MalformedBody_Returns400()\n" +
            "    {\n" +
            "        var content = new StringContent(\n" +
            "            \"{ not valid json\",\n" +
            "            System.Text.Encoding.UTF8,\n" +
            "            \"application/json\");\n" +
            $"        var response = await {call};\n" +
            "        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);\n" +
            "    }\n";
    }

    /// <summary>NotFound → 404, samo za GET (nepostojeći resurs na ruti).</summary>
    private static string BuildNotFoundTest(RestEndpointSpec s)
    {
        if (s.HttpMethod.ToUpperInvariant() != "GET")
            return string.Empty;

        return "\n" +
            "    [Fact]\n" +
            $"    public async Task {s.ClassName}_NotFound_Returns404()\n" +
            "    {\n" +
            "        var response = await _client.GetAsync(\n" +
            $"            \"{s.RoutePath}/00000000-0000-0000-0000-000000000000\");\n" +
            "        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);\n" +
            "    }\n";
    }

    private static string BuildHappyCall(RestEndpointSpec s)
    {
        return s.HttpMethod.ToUpperInvariant() switch
        {
            "GET"    => $"_client.GetAsync(\"{s.RoutePath}\")",
            "DELETE" => $"_client.DeleteAsync(\"{s.RoutePath}\")",
            "POST"   => s.RequestBodyJson is not null
                            ? $"_client.PostAsync(\"{s.RoutePath}\", body)"
                            : $"_client.PostAsync(\"{s.RoutePath}\", null)",
            "PUT"    => s.RequestBodyJson is not null
                            ? $"_client.PutAsync(\"{s.RoutePath}\", body)"
                            : $"_client.PutAsync(\"{s.RoutePath}\", null)",
            "PATCH"  => s.RequestBodyJson is not null
                            ? $"_client.PatchAsync(\"{s.RoutePath}\", body)"
                            : $"_client.PatchAsync(\"{s.RoutePath}\", null)",
            _        => $"_client.SendAsync(new System.Net.Http.HttpRequestMessage(new System.Net.Http.HttpMethod(\"{s.HttpMethod}\"), \"{s.RoutePath}\"))",
        };
    }

    private static string BuildAuthTest(RestEndpointSpec s) =>
        "\n" +
        "    [Fact]\n" +
        $"    public async Task {s.ClassName}_MissingToken_Returns401()\n" +
        "    {\n" +
        "        using var unauthClient = new System.Net.Http.HttpClient\n" +
        "        {\n" +
        "            BaseAddress = _client.BaseAddress\n" +
        "        };\n" +
        $"        var response = await unauthClient.GetAsync(\"{s.RoutePath}\");\n" +
        "        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);\n" +
        "    }\n";

    private static string BuildFactory() => """
        using Microsoft.AspNetCore.Hosting;
        using Microsoft.AspNetCore.Mvc.Testing;

        namespace GeneratedTests;

        /// <summary>
        /// Diže aplikaciju pod testom in-process (WebApplicationFactory) za REST integracijske testove.
        /// VAŽNO: aplikacija može imati startup-konfiguraciju (connection stringovi, env varijable,
        /// eksterni servisi) koju generator NE može pogoditi automatski. Popuni je u ConfigureWebHost
        /// ispod — inače host možda neće startovati (npr. "Connection string ... nije pronađen").
        /// </summary>
        public sealed class GeneratedWebApplicationFactory : WebApplicationFactory<Program>
        {
            protected override void ConfigureWebHost(IWebHostBuilder builder)
            {
                // TODO (app-specifično): postavi konfiguraciju potrebnu da host startuje.
                // Primjer — connection string koji se čita tokom registracije servisa:
                // Environment.SetEnvironmentVariable(
                //     "ConnectionStrings__<IME>",
                //     "Host=localhost;Database=test;Username=test;Password=test");
                //
                // Za izolaciju zavisnosti mockaj servise (npr. NSubstitute) preko:
                // builder.ConfigureServices(services => { /* zamijeni registracije */ });
            }
        }
        """;

    private static string BuildCsproj() => """
        <Project Sdk="Microsoft.NET.Sdk">
          <PropertyGroup>
            <TargetFramework>net10.0</TargetFramework>
            <Nullable>enable</Nullable>
            <ImplicitUsings>enable</ImplicitUsings>
            <IsPackable>false</IsPackable>
          </PropertyGroup>
          <ItemGroup>
            <PackageReference Include="Microsoft.NET.Test.Sdk"                Version="17.12.0" />
            <PackageReference Include="xunit"                                  Version="2.9.2"  />
            <PackageReference Include="xunit.runner.visualstudio"             Version="2.8.2"  >
              <PrivateAssets>all</PrivateAssets>
            </PackageReference>
            <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing"      Version="10.0.0" />
            <PackageReference Include="WireMock.Net"                          Version="1.6.8"  />
            <PackageReference Include="Testcontainers.MsSql"                  Version="4.1.0"  />
          </ItemGroup>
          <ItemGroup>
            <!-- WebApplicationFactory<Program> diže API in-process, pa generisani projekat
                 MORA referencirati projekat aplikacije koja se testira. Podesi putanju: -->
            <!-- <ProjectReference Include="..\ApplicationUnderTest\ApplicationUnderTest.csproj" /> -->
          </ItemGroup>
        </Project>
        """;

    private static string BuildWireMockFixture() => """
        using WireMock.Server;
        using Xunit;

        namespace GeneratedTests;

        /// <summary>
        /// xUnit fixture koji pokreće WireMock.NET server za stubovanje eksternih HTTP zavisnosti.
        /// Koristiti uz IClassFixture&lt;WireMockFixture&gt; u test klasama koje pozivaju vanjske servise.
        /// </summary>
        public sealed class WireMockFixture : IAsyncLifetime
        {
            public WireMockServer Server { get; private set; } = null!;
            public string BaseUrl => Server.Urls[0];

            public Task InitializeAsync()
            {
                Server = WireMockServer.Start();
                return Task.CompletedTask;
            }

            public Task DisposeAsync()
            {
                Server?.Stop();
                Server?.Dispose();
                return Task.CompletedTask;
            }
        }
        """;

    private static string BuildSqlServerFixture() => """
        using Testcontainers.MsSql;
        using Xunit;

        namespace GeneratedTests;

        /// <summary>
        /// xUnit fixture koji pokreće SQL Server kontejner za integracijske testove.
        /// Koristiti uz IClassFixture&lt;SqlServerContainerFixture&gt; i proslijediti
        /// ConnectionString u WebApplicationFactory konfiguraciju.
        /// </summary>
        public sealed class SqlServerContainerFixture : IAsyncLifetime
        {
            private readonly MsSqlContainer _container = new MsSqlBuilder()
                .WithPassword("Test_Forge_123!")
                .Build();

            public string ConnectionString => _container.GetConnectionString();

            public Task InitializeAsync() => _container.StartAsync();

            public Task DisposeAsync() => _container.DisposeAsync().AsTask();
        }
        """;

    /// <summary>Pretvara proizvoljan string u validan C# string literal (escape \, ", i kontrolnih znakova).</summary>
    private static string ToCSharpStringLiteral(string value)
    {
        var sb = new System.Text.StringBuilder(value.Length + 2);
        sb.Append('"');
        foreach (var c in value)
        {
            switch (c)
            {
                case '\\': sb.Append("\\\\"); break;
                case '"':  sb.Append("\\\""); break;
                case '\r': sb.Append("\\r");  break;
                case '\n': sb.Append("\\n");  break;
                case '\t': sb.Append("\\t");  break;
                default:   sb.Append(c);       break;
            }
        }
        sb.Append('"');
        return sb.ToString();
    }
}
