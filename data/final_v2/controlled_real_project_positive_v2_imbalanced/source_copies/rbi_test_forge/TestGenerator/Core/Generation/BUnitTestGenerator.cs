using System.Text;

namespace RBBH.TestAutomation.Core.Generation;

/// <summary>
/// Stateless generator bUnit test projekta iz <see cref="BlazorComponentSpec"/>.
/// Koristi string templating — emituje validan C# tekst za preview/download.
/// Registruje se kao Singleton jer nema stanja.
/// </summary>
public sealed class BUnitTestGenerator
{
    public GeneratedTestProject Generate(BlazorComponentSpec spec)
    {
        var files = new List<GeneratedTestFile>
        {
            new("TestServiceCollectionSetup.cs", BuildTestContextSetup(spec)),
            new($"{spec.ComponentName}Tests.cs", BuildTestClass(spec)),
            new($"{spec.ComponentName}Tests.csproj",  BuildCsproj(spec)),
        };
        return new GeneratedTestProject(files);
    }

    private static string BuildTestContextSetup(BlazorComponentSpec s) => $$"""
        // GENERATED — bazna klasa TestContext-a sa zajedničkim DI registracijama.
        // Svi testovi nasljeđuju ovu klasu umjesto direktnog bunit TestContext-a.
        // Dodajte vlastite servise (mocked ili pravi) u metodu SetupServices().

        using Bunit;
        using Microsoft.Extensions.DependencyInjection;

        namespace GeneratedBUnitTests;

        /// <summary>
        /// Zajednički TestContext za komponentu {{s.ComponentName}}.
        /// Registruje servise koji su potrebni komponenti za renderovanje.
        /// </summary>
        public class {{s.ComponentName}}TestContext : TestContext
        {
            public {{s.ComponentName}}TestContext()
            {
                SetupServices(Services);
            }

            /// <summary>
            /// Registrujte mock servise koje komponenta injektuje.
            /// Primjer: Services.AddSingleton(new Mock&lt;IMyService&gt;().Object);
            /// </summary>
            protected virtual void SetupServices(IServiceCollection services)
            {
                // TODO: registrujte mock servise potrebne komponenti {{s.ComponentName}}.
                // Primjeri:
                // services.AddSingleton<IGroupService>(new MockGroupService());
                // services.AddSingleton<HttpClient>(new HttpClient());
            }
        }
        """;

    private static string BuildTestClass(BlazorComponentSpec s)
    {
        var sb = new StringBuilder();

        sb.AppendLine("// GENERATED — prilagodite namespace, using direktive i assert vrijednosti.");
        sb.AppendLine("// Referencirajte projekat koji sadrži komponentu i dodajte _Imports.razor.");
        sb.AppendLine();
        sb.AppendLine("using Bunit;");
        sb.AppendLine("using FluentAssertions;");
        sb.AppendLine("using Xunit;");

        if (s.EventCallbacks.Count > 0)
            sb.AppendLine("using Microsoft.AspNetCore.Components;");

        sb.AppendLine();
        sb.AppendLine("namespace GeneratedBUnitTests;");
        sb.AppendLine();
        sb.AppendLine($"public class {s.ComponentName}Tests : {s.ComponentName}TestContext");
        sb.AppendLine("{");

        // Render test — uvijek
        AppendRenderTest(sb, s);

        // Parameter tests
        foreach (var p in s.Parameters)
            AppendParameterTest(sb, s, p);

        // EventCallback tests
        foreach (var ec in s.EventCallbacks)
            AppendEventCallbackTest(sb, s, ec);

        // @onclick tests
        foreach (var handler in s.OnClickHandlers)
            AppendOnClickTest(sb, s, handler);

        // HttpClient mock test
        if (s.HttpCalls.Count > 0)
            AppendHttpTest(sb, s);

        // Form validation tests
        if (s.Forms.Count > 0)
            AppendFormTest(sb, s);

        sb.AppendLine("}");
        return sb.ToString();
    }

    private static void AppendRenderTest(StringBuilder sb, BlazorComponentSpec s)
    {
        sb.AppendLine("    [Fact]");
        sb.AppendLine($"    public void {s.ComponentName}_Renders_WithoutErrors()");
        sb.AppendLine("    {");
        sb.AppendLine($"        var cut = RenderComponent<{s.ComponentName}>();");
        sb.AppendLine();
        sb.AppendLine("        cut.Markup.Should().NotBeNullOrEmpty();");
        sb.AppendLine("    }");
        sb.AppendLine();
    }

    private static void AppendParameterTest(StringBuilder sb, BlazorComponentSpec s, BlazorParameter p)
    {
        var testValue = DefaultValue(p.Type);
        sb.AppendLine("    [Fact]");
        sb.AppendLine($"    public void {s.ComponentName}_With{p.Name}_SetsParameter()");
        sb.AppendLine("    {");
        sb.AppendLine($"        var cut = RenderComponent<{s.ComponentName}>(p => p");
        sb.AppendLine($"            .Add(c => c.{p.Name}, {testValue}));");
        sb.AppendLine();
        sb.AppendLine($"        cut.Instance.{p.Name}.Should().Be({testValue});");
        sb.AppendLine("    }");
        sb.AppendLine();
    }

    private static void AppendEventCallbackTest(StringBuilder sb, BlazorComponentSpec s, BlazorEventCallback ec)
    {
        var hasArg  = !string.IsNullOrEmpty(ec.GenericArg);
        var argType = hasArg ? ec.GenericArg : "";
        var invoked = $"_{ToCamelCase(ec.Name)}Invoked";

        sb.AppendLine("    [Fact]");
        sb.AppendLine($"    public async Task {s.ComponentName}_{ec.Name}_InvokesCallback()");
        sb.AppendLine("    {");
        sb.AppendLine($"        var {invoked} = false;");
        sb.AppendLine($"        var cut = RenderComponent<{s.ComponentName}>(p => p");

        if (hasArg)
        {
            sb.AppendLine($"            .Add(c => c.{ec.Name},");
            sb.AppendLine($"                EventCallback.Factory.Create<{argType}>(this, _ => {invoked} = true)));");
        }
        else
        {
            sb.AppendLine($"            .Add(c => c.{ec.Name},");
            sb.AppendLine($"                EventCallback.Factory.Create(this, () => {invoked} = true)));");
        }

        sb.AppendLine();
        sb.AppendLine($"        await cut.InvokeAsync(() => cut.Instance.{ec.Name}.InvokeAsync({(hasArg ? DefaultValue(argType) : "")}));");
        sb.AppendLine();
        sb.AppendLine($"        {invoked}.Should().BeTrue();");
        sb.AppendLine("    }");
        sb.AppendLine();
    }

    private static void AppendOnClickTest(StringBuilder sb, BlazorComponentSpec s, BlazorOnClickHandler h)
    {
        sb.AppendLine("    [Fact]");
        sb.AppendLine($"    public void {s.ComponentName}_{h.MethodName}_ButtonClick_DoesNotThrow()");
        sb.AppendLine("    {");
        sb.AppendLine($"        var cut = RenderComponent<{s.ComponentName}>();");
        sb.AppendLine();
        sb.AppendLine("        // Prilagodite selektor prema stvarnom dugmetu koje poziva handler.");
        sb.AppendLine($"        var act = () => cut.Find(\"[onclick]\").Click();");
        sb.AppendLine();
        sb.AppendLine("        act.Should().NotThrow();");
        sb.AppendLine("    }");
        sb.AppendLine();
    }

    private static void AppendHttpTest(StringBuilder sb, BlazorComponentSpec s)
    {
        var firstCall = s.HttpCalls[0];
        sb.AppendLine("    [Fact]");
        sb.AppendLine($"    public async Task {s.ComponentName}_OnInit_CallsHttpEndpoint()");
        sb.AppendLine("    {");
        sb.AppendLine("        // Registrujte mock HttpClient prije renderovanja komponente.");
        sb.AppendLine("        // Primjer s RichardSzalay.MockHttp:");
        sb.AppendLine("        // var mockHttp = new MockHttpMessageHandler();");
        sb.AppendLine($"        // mockHttp.When(\"*{firstCall.UrlFragment}*\")");
        sb.AppendLine("        //         .Respond(\"application/json\", \"[]\");");
        sb.AppendLine("        // Services.AddSingleton(new HttpClient(mockHttp));");
        sb.AppendLine();
        sb.AppendLine($"        var cut = RenderComponent<{s.ComponentName}>();");
        sb.AppendLine("        await cut.InvokeAsync(() => Task.CompletedTask);");
        sb.AppendLine();
        sb.AppendLine("        // Assert: provjerite da se podaci prikazuju u markupu.");
        sb.AppendLine("        cut.Markup.Should().NotBeNullOrEmpty();");
        sb.AppendLine("    }");
        sb.AppendLine();
    }

    private static void AppendFormTest(StringBuilder sb, BlazorComponentSpec s)
    {
        var form = s.Forms[0];
        sb.AppendLine("    [Fact]");
        sb.AppendLine($"    public async Task {s.ComponentName}_SubmitEmptyForm_ShowsValidationErrors()");
        sb.AppendLine("    {");
        sb.AppendLine($"        var cut = RenderComponent<{s.ComponentName}>();");
        sb.AppendLine();
        sb.AppendLine("        // Pokušaj submit praznog formulara.");
        sb.AppendLine("        await cut.InvokeAsync(() =>");
        sb.AppendLine("        {");
        sb.AppendLine("            var form = cut.Find(\"form\");");
        sb.AppendLine("            form.Submit();");
        sb.AppendLine("        });");
        sb.AppendLine();

        if (form.HasValidationSummary)
        {
            sb.AppendLine("        // ValidationSummary je detektovan — provjeri da se validacijske poruke prikazuju.");
            sb.AppendLine("        cut.Find(\".validation-errors, .mud-alert\").Should().NotBeNull();");
        }
        else
        {
            sb.AppendLine("        // Provjeri stranicu na prisustvo poruke o grešci.");
            sb.AppendLine("        cut.Markup.Should().ContainAny(\"obavezno\", \"required\", \"error\");");
        }

        sb.AppendLine("    }");

        if (form.InputTypes.Count > 0)
        {
            sb.AppendLine();
            sb.AppendLine("    [Fact]");
            sb.AppendLine($"    public async Task {s.ComponentName}_FillAndSubmitForm_Succeeds()");
            sb.AppendLine("    {");
            sb.AppendLine($"        var cut = RenderComponent<{s.ComponentName}>();");
            sb.AppendLine();
            sb.AppendLine("        // Popunite input polja — prilagodite selektore.");

            foreach (var inputType in form.InputTypes.Take(3))
            {
                var selector = inputType switch
                {
                    "InputText"     => "input[type='text']",
                    "InputDate"     => "input[type='date']",
                    "InputNumber"   => "input[type='number']",
                    "InputCheckbox" => "input[type='checkbox']",
                    _               => "input"
                };
                sb.AppendLine($"        cut.Find(\"{selector}\").Change(\"TestVrijednost\");");
            }

            sb.AppendLine();
            sb.AppendLine("        await cut.InvokeAsync(() => cut.Find(\"form\").Submit());");
            sb.AppendLine();
            sb.AppendLine("        // Assert: prilagodite prema očekivanom stanju nakon submita.");
            sb.AppendLine("        cut.Markup.Should().NotContainAny(\"greška\", \"error\");");
            sb.AppendLine("    }");
        }
        sb.AppendLine();
    }

    private static string BuildCsproj(BlazorComponentSpec s) => $"""
        <Project Sdk="Microsoft.NET.Sdk">
          <PropertyGroup>
            <TargetFramework>net10.0</TargetFramework>
            <Nullable>enable</Nullable>
            <ImplicitUsings>enable</ImplicitUsings>
            <IsPackable>false</IsPackable>
          </PropertyGroup>
          <ItemGroup>
            <PackageReference Include="Microsoft.NET.Test.Sdk"       Version="17.12.0" />
            <PackageReference Include="xunit"                         Version="2.9.2"  />
            <PackageReference Include="xunit.runner.visualstudio"     Version="2.8.2"  >
              <PrivateAssets>all</PrivateAssets>
            </PackageReference>
            <PackageReference Include="bunit"                         Version="1.35.6" />
            <PackageReference Include="FluentAssertions"              Version="6.12.2" />
            <PackageReference Include="RichardSzalay.MockHttp"        Version="8.0.0" />
          </ItemGroup>
          <ItemGroup>
            <!--
              Dodajte referencu na projekat koji sadrži komponentu {s.ComponentName}.
              Primjer (prilagodite putanju):
            -->
            <!-- <ProjectReference Include="..\ApplicationUnderTest\ApplicationUnderTest.csproj" /> -->
          </ItemGroup>
        </Project>
        """;

    // ─── Helpers ─────────────────────────────────────────────────────────────

    private static string DefaultValue(string type) => type.TrimEnd('?') switch
    {
        "string"  => "\"TestVrijednost\"",
        "int"     => "42",
        "long"    => "42L",
        "double"  => "3.14",
        "float"   => "3.14f",
        "decimal" => "9.99m",
        "bool"    => "true",
        "Guid"    => "Guid.NewGuid()",
        "DateTime"=> "DateTime.UtcNow",
        _         => "default"
    };

    private static string ToCamelCase(string name) =>
        string.IsNullOrEmpty(name) ? name : char.ToLowerInvariant(name[0]) + name[1..];
}
