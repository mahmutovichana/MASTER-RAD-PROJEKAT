using RBBH.TestAutomation.Core.Generation;
using Xunit;

namespace UnitTests.TestForge;

public class RestTestGeneratorTests
{
    private readonly RestTestGenerator _sut = new();

    private static RestEndpointSpec BasicSpec(
        string className   = "CreateTransaction",
        string method      = "POST",
        string route       = "/api/transactions",
        int    status      = 201,
        string? body       = """{"amount":100}""",
        bool   requireAuth = false)
        => new(className, method, route, status, body, requireAuth);

    // ─── Struktura rezultata ──────────────────────────────────────────────────

    [Fact]
    public void Generate_ReturnsExactlyFiveFiles()
    {
        var result = _sut.Generate(BasicSpec());
        Assert.Equal(5, result.Files.Count);
    }

    [Fact]
    public void Generate_FileNamesAreCorrect()
    {
        var result = _sut.Generate(BasicSpec(className: "GetUser"));
        var names  = result.Files.Select(f => f.FileName).ToHashSet();

        Assert.Contains("GetUserTests.cs",                 names);
        Assert.Contains("GeneratedWebApplicationFactory.cs", names);
        Assert.Contains("GeneratedTests.csproj",           names);
        Assert.Contains("WireMockFixture.cs",               names);
        Assert.Contains("SqlServerContainerFixture.cs",      names);
    }

    [Fact]
    public void Generate_NoFileHasEmptyContent()
    {
        var result = _sut.Generate(BasicSpec());
        Assert.All(result.Files, f => Assert.False(string.IsNullOrWhiteSpace(f.Content)));
    }

    // ─── Test klasa — happy path ──────────────────────────────────────────────

    [Fact]
    public void Generate_TestClass_UsesGeneratedFactory()
    {
        var result   = _sut.Generate(BasicSpec());
        var testFile = result.Files.Single(f => f.FileName.EndsWith("Tests.cs")).Content;

        Assert.Contains("IClassFixture<GeneratedWebApplicationFactory>", testFile);
    }

    [Fact]
    public void Generate_Factory_ExtendsWebApplicationFactoryOfProgram()
    {
        var result  = _sut.Generate(BasicSpec());
        var factory = result.Files.Single(f => f.FileName == "GeneratedWebApplicationFactory.cs").Content;

        Assert.Contains("WebApplicationFactory<Program>", factory);
        Assert.Contains("ConfigureWebHost",               factory);
    }

    [Theory]
    [InlineData(200)]
    [InlineData(201)]
    [InlineData(204)]
    public void Generate_TestClass_ContainsExpectedStatusInHappyPath(int status)
    {
        var result   = _sut.Generate(BasicSpec(status: status));
        var testFile = result.Files.Single(f => f.FileName.EndsWith("Tests.cs")).Content;

        Assert.Contains($"Returns{status}", testFile);
        Assert.Contains(status.ToString(),  testFile);
    }

    // ─── Error path — uslovno, ovisno o metodi ────────────────────────────────
    // Malformed-body (400) samo za POST/PUT/PATCH; NotFound (404) samo za GET.
    // Slijepo emitovanje (npr. POST malformed na GET endpoint) daje 405, ne 400 → lažni pad.

    [Fact]
    public void Generate_BodyMethod_Contains400Test()
    {
        var result   = _sut.Generate(BasicSpec(method: "POST"));
        var testFile = result.Files.Single(f => f.FileName.EndsWith("Tests.cs")).Content;

        Assert.Contains("Returns400", testFile);
        Assert.Contains("BadRequest", testFile);
    }

    [Fact]
    public void Generate_GetMethod_DoesNotContain400Test()
    {
        var result   = _sut.Generate(BasicSpec(method: "GET", body: null));
        var testFile = result.Files.Single(f => f.FileName.EndsWith("Tests.cs")).Content;

        Assert.DoesNotContain("MalformedBody", testFile);
    }

    [Fact]
    public void Generate_GetMethod_Contains404Test()
    {
        var result   = _sut.Generate(BasicSpec(method: "GET", body: null));
        var testFile = result.Files.Single(f => f.FileName.EndsWith("Tests.cs")).Content;

        Assert.Contains("Returns404", testFile);
        Assert.Contains("NotFound",   testFile);
    }

    [Fact]
    public void Generate_PostMethod_DoesNotContain404Test()
    {
        var result   = _sut.Generate(BasicSpec(method: "POST"));
        var testFile = result.Files.Single(f => f.FileName.EndsWith("Tests.cs")).Content;

        Assert.DoesNotContain("NotFound", testFile);
    }

    // ─── 401 — samo kad RequiresAuth = true ──────────────────────────────────

    [Fact]
    public void Generate_TestClass_Contains401Test_WhenRequiresAuthTrue()
    {
        var result   = _sut.Generate(BasicSpec(requireAuth: true));
        var testFile = result.Files.Single(f => f.FileName.EndsWith("Tests.cs")).Content;

        Assert.Contains("Returns401",   testFile);
        Assert.Contains("Unauthorized", testFile);
    }

    [Fact]
    public void Generate_TestClass_DoesNotContain401Test_WhenRequiresAuthFalse()
    {
        var result   = _sut.Generate(BasicSpec(requireAuth: false));
        var testFile = result.Files.Single(f => f.FileName.EndsWith("Tests.cs")).Content;

        Assert.DoesNotContain("Returns401",   testFile);
        Assert.DoesNotContain("Unauthorized", testFile);
    }

    // ─── .csproj — paketi ────────────────────────────────────────────────────

    [Fact]
    public void Generate_Csproj_ContainsWireMock()
    {
        var result = _sut.Generate(BasicSpec());
        var csproj = result.Files.Single(f => f.FileName == "GeneratedTests.csproj").Content;

        Assert.Contains("WireMock.Net", csproj);
    }

    [Fact]
    public void Generate_Csproj_ContainsTestcontainersSqlServer()
    {
        var result = _sut.Generate(BasicSpec());
        var csproj = result.Files.Single(f => f.FileName == "GeneratedTests.csproj").Content;

        Assert.Contains("Testcontainers.MsSql", csproj);
    }

    [Fact]
    public void Generate_Csproj_ContainsMvcTesting()
    {
        var result = _sut.Generate(BasicSpec());
        var csproj = result.Files.Single(f => f.FileName == "GeneratedTests.csproj").Content;

        Assert.Contains("Microsoft.AspNetCore.Mvc.Testing", csproj);
    }

    // ─── HTTP metode ─────────────────────────────────────────────────────────

    [Theory]
    [InlineData("GET")]
    [InlineData("POST")]
    [InlineData("PUT")]
    [InlineData("DELETE")]
    [InlineData("PATCH")]
    public void Generate_TestClass_ContainsCorrectHttpMethod(string method)
    {
        var result   = _sut.Generate(BasicSpec(method: method, body: method is "POST" or "PUT" or "PATCH" ? "{}" : null));
        var testFile = result.Files.Single(f => f.FileName.EndsWith("Tests.cs")).Content;

        // Provjeri da se metoda pojavljuje u generisanom kodu (kao string ili dio poziva)
        Assert.Contains(method.ToLowerInvariant()[0].ToString().ToUpperInvariant() + method[1..].ToLowerInvariant() + "Async",
                        testFile, StringComparison.OrdinalIgnoreCase);
    }

    // ─── WireMock i SQL Server fixture ─────────────────────────────────────────

    [Fact]
    public void Generate_WireMockFixture_ContainsWireMockServer()
    {
        var result  = _sut.Generate(BasicSpec());
        var fixture = result.Files.Single(f => f.FileName == "WireMockFixture.cs").Content;

        Assert.Contains("WireMockServer", fixture);
        Assert.Contains("IAsyncLifetime",  fixture);
    }

    [Fact]
    public void Generate_SqlServerFixture_ContainsMsSqlContainer()
    {
        var result  = _sut.Generate(BasicSpec());
        var fixture = result.Files.Single(f => f.FileName == "SqlServerContainerFixture.cs").Content;

        Assert.Contains("MsSqlContainer", fixture);
        Assert.Contains("IAsyncLifetime",       fixture);
        Assert.Contains("ConnectionString",     fixture);
    }
}
