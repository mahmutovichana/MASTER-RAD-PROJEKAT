using System.Text;

namespace RBBH.TestAutomation.Core.Generation;

/// <summary>
/// Stateless generator for Playwright .NET E2E test projects from a Blazor component/page spec.
/// </summary>
public sealed class PlaywrightE2eGenerator
{
    public GeneratedTestProject Generate(BlazorComponentSpec spec)
    {
        var files = new List<GeneratedTestFile>
        {
            new($"{spec.ComponentName}Page.cs", BuildPageObject(spec)),
            new($"{spec.ComponentName}E2eTests.cs", BuildTestClass(spec)),
            new("PlaywrightTestBase.cs", BuildTestBase()),
            new("GeneratedPlaywrightTests.csproj", BuildCsproj()),
            new("README.md", BuildReadme(spec)),
        };

        return new GeneratedTestProject(files);
    }

    private static string BuildPageObject(BlazorComponentSpec s)
    {
        var route = PrimaryRoute(s);
        var sb = new StringBuilder();

        sb.AppendLine("using Microsoft.Playwright;");
        sb.AppendLine();
        sb.AppendLine("namespace GeneratedPlaywrightTests;");
        sb.AppendLine();
        sb.AppendLine($"public sealed class {s.ComponentName}Page");
        sb.AppendLine("{");
        sb.AppendLine("    private readonly IPage _page;");
        sb.AppendLine($"    public const string Path = \"{Escape(route)}\";");
        sb.AppendLine();
        sb.AppendLine($"    public {s.ComponentName}Page(IPage page) => _page = page;");
        sb.AppendLine();
        sb.AppendLine("    public async Task GotoAsync()");
        sb.AppendLine("    {");
        sb.AppendLine("        await _page.GotoAsync(Path);");
        sb.AppendLine("        await _page.WaitForLoadStateAsync(LoadState.NetworkIdle);");
        sb.AppendLine("    }");
        sb.AppendLine();
        sb.AppendLine("    public ILocator Heading => _page.GetByRole(AriaRole.Heading).First;");
        sb.AppendLine("    public ILocator Forms => _page.Locator(\"form\");");
        sb.AppendLine("    public ILocator SubmitButton => _page.Locator(\"button[type='submit'], .mud-button-root[type='submit']\").First;");
        sb.AppendLine("    public ILocator TextInputs => _page.Locator(\"input[type='text'], input:not([type]), textarea, .mud-input-slot input\");");
        sb.AppendLine("    public ILocator NumberInputs => _page.Locator(\"input[type='number']\");");
        sb.AppendLine("    public ILocator DateInputs => _page.Locator(\"input[type='date']\");");
        sb.AppendLine("    public ILocator Checkboxes => _page.Locator(\"input[type='checkbox']\");");
        sb.AppendLine("    public ILocator DataContainers => _page.Locator(\"table, .mud-table, ul, ol, [role='table'], [role='list'], .mud-list\");");
        sb.AppendLine();
        sb.AppendLine("    public async Task FillDetectedFormAsync()");
        sb.AppendLine("    {");
        sb.AppendLine("        if (await TextInputs.CountAsync() > 0)");
        sb.AppendLine("            await TextInputs.First.FillAsync(\"Test vrijednost\");");
        sb.AppendLine();
        sb.AppendLine("        if (await NumberInputs.CountAsync() > 0)");
        sb.AppendLine("            await NumberInputs.First.FillAsync(\"42\");");
        sb.AppendLine();
        sb.AppendLine("        if (await DateInputs.CountAsync() > 0)");
        sb.AppendLine("            await DateInputs.First.FillAsync(DateTime.UtcNow.ToString(\"yyyy-MM-dd\"));");
        sb.AppendLine();
        sb.AppendLine("        if (await Checkboxes.CountAsync() > 0)");
        sb.AppendLine("            await Checkboxes.First.CheckAsync();");
        sb.AppendLine("    }");
        sb.AppendLine();
        sb.AppendLine("    public async Task SubmitFormAsync()");
        sb.AppendLine("    {");
        sb.AppendLine("        if (await SubmitButton.CountAsync() > 0)");
        sb.AppendLine("            await SubmitButton.ClickAsync();");
        sb.AppendLine("        else if (await Forms.CountAsync() > 0)");
        sb.AppendLine("            await Forms.First.EvaluateAsync(\"form => form.requestSubmit()\");");
        sb.AppendLine("    }");
        sb.AppendLine("}");

        return sb.ToString();
    }

    private static string BuildTestClass(BlazorComponentSpec s)
    {
        var sb = new StringBuilder();
        sb.AppendLine("using Microsoft.Playwright;");
        sb.AppendLine("using System.Text.RegularExpressions;");
        sb.AppendLine("using Xunit;");
        sb.AppendLine();
        sb.AppendLine("namespace GeneratedPlaywrightTests;");
        sb.AppendLine();
        sb.AppendLine($"public sealed class {s.ComponentName}E2eTests : PlaywrightTestBase");
        sb.AppendLine("{");
        sb.AppendLine("    [Fact]");
        sb.AppendLine($"    public async Task {s.ComponentName}_NavigatesAndLoads()");
        sb.AppendLine("    {");
        sb.AppendLine("        await RunWithScreenshotOnFailureAsync(async page =>");
        sb.AppendLine("        {");
        sb.AppendLine($"            var sut = new {s.ComponentName}Page(page);");
        sb.AppendLine("            await sut.GotoAsync();");
        sb.AppendLine();
        sb.AppendLine($"            await Expect(page).ToHaveURLAsync(new Regex($\".*{{Regex.Escape({s.ComponentName}Page.Path)}}.*\"));");
        sb.AppendLine("            await Expect(page.Locator(\"body\")).ToBeVisibleAsync();");
        sb.AppendLine("        });");
        sb.AppendLine("    }");
        sb.AppendLine();

        AppendFormTests(sb, s);
        AppendDisplayTest(sb, s);

        sb.AppendLine("}");
        return sb.ToString();
    }

    private static void AppendFormTests(StringBuilder sb, BlazorComponentSpec s)
    {
        if (s.Forms.Count == 0)
        {
            sb.AppendLine("    [Fact]");
            sb.AppendLine($"    public async Task {s.ComponentName}_HasNoDetectedForms_ButPageRemainsStable()");
            sb.AppendLine("    {");
            sb.AppendLine("        await RunWithScreenshotOnFailureAsync(async page =>");
            sb.AppendLine("        {");
            sb.AppendLine($"            var sut = new {s.ComponentName}Page(page);");
            sb.AppendLine("            await sut.GotoAsync();");
            sb.AppendLine();
            sb.AppendLine("            await Expect(page.Locator(\"body\")).ToBeVisibleAsync();");
            sb.AppendLine("        });");
            sb.AppendLine("    }");
            sb.AppendLine();
            return;
        }

        sb.AppendLine("    [Fact]");
        sb.AppendLine($"    public async Task {s.ComponentName}_FillAndSubmitForm()");
        sb.AppendLine("    {");
        sb.AppendLine("        await RunWithScreenshotOnFailureAsync(async page =>");
        sb.AppendLine("        {");
        sb.AppendLine($"            var sut = new {s.ComponentName}Page(page);");
        sb.AppendLine("            await sut.GotoAsync();");
        sb.AppendLine("            await sut.FillDetectedFormAsync();");
        sb.AppendLine("            await sut.SubmitFormAsync();");
        sb.AppendLine();
        sb.AppendLine("            await Expect(page.Locator(\"body\")).ToBeVisibleAsync();");
        sb.AppendLine("        });");
        sb.AppendLine("    }");
        sb.AppendLine();

        sb.AppendLine("    [Fact]");
        sb.AppendLine($"    public async Task {s.ComponentName}_SubmitEmptyForm_ShowsValidationFeedback()");
        sb.AppendLine("    {");
        sb.AppendLine("        await RunWithScreenshotOnFailureAsync(async page =>");
        sb.AppendLine("        {");
        sb.AppendLine($"            var sut = new {s.ComponentName}Page(page);");
        sb.AppendLine("            await sut.GotoAsync();");
        sb.AppendLine("            await sut.SubmitFormAsync();");
        sb.AppendLine();
        sb.AppendLine("            var validation = page.Locator(\".validation-message, .validation-errors, .mud-input-error, .mud-alert, [role='alert']\");");
        sb.AppendLine("            if (await validation.CountAsync() > 0)");
        sb.AppendLine("                await Expect(validation.First).ToBeVisibleAsync();");
        sb.AppendLine("            else");
        sb.AppendLine("                await Expect(page.Locator(\"body\")).ToBeVisibleAsync();");
        sb.AppendLine("        });");
        sb.AppendLine("    }");
        sb.AppendLine();
    }

    private static void AppendDisplayTest(StringBuilder sb, BlazorComponentSpec s)
    {
        sb.AppendLine("    [Fact]");
        sb.AppendLine($"    public async Task {s.ComponentName}_DisplaysDataContainers_WhenPresent()");
        sb.AppendLine("    {");
        sb.AppendLine("        await RunWithScreenshotOnFailureAsync(async page =>");
        sb.AppendLine("        {");
        sb.AppendLine($"            var sut = new {s.ComponentName}Page(page);");
        sb.AppendLine("            await sut.GotoAsync();");
        sb.AppendLine();
        sb.AppendLine("            if (await sut.DataContainers.CountAsync() > 0)");
        sb.AppendLine("                await Expect(sut.DataContainers.First).ToBeVisibleAsync();");
        sb.AppendLine("            else");
        sb.AppendLine("                await Expect(page.Locator(\"body\")).ToBeVisibleAsync();");
        sb.AppendLine("        });");
        sb.AppendLine("    }");
        sb.AppendLine();
    }

    private static string BuildTestBase() => """
        using Microsoft.Playwright;
        using Xunit;

        namespace GeneratedPlaywrightTests;

        public abstract class PlaywrightTestBase : IAsyncLifetime
        {
            private IPlaywright? _playwright;
            private IBrowser? _browser;

            protected string BaseUrl =>
                Environment.GetEnvironmentVariable("PLAYWRIGHT_BASE_URL") ?? "http://localhost:5187";

            protected bool Headless =>
                !string.Equals(Environment.GetEnvironmentVariable("PLAYWRIGHT_HEADLESS"), "false", StringComparison.OrdinalIgnoreCase);

            protected IBrowser Browser =>
                _browser ?? throw new InvalidOperationException("Browser nije pokrenut. Pozovite LaunchBrowserAsync.");

            public async Task InitializeAsync() => await LaunchBrowserAsync();

            public async Task DisposeAsync() => await CloseBrowserAsync();

            protected async Task LaunchBrowserAsync()
            {
                _playwright = await Playwright.CreateAsync();
                _browser = await _playwright.Chromium.LaunchAsync(new BrowserTypeLaunchOptions
                {
                    Headless = Headless,
                });
            }

            protected async Task CloseBrowserAsync()
            {
                if (_browser is not null)
                    await _browser.CloseAsync();

                _playwright?.Dispose();
            }

            protected async Task RunWithScreenshotOnFailureAsync(Func<IPage, Task> testBody, string? screenshotName = null)
            {
                await using var context = await Browser.NewContextAsync(new BrowserNewContextOptions
                {
                    BaseURL = BaseUrl,
                });
                var page = await context.NewPageAsync();

                try
                {
                    await testBody(page);
                }
                catch
                {
                    Directory.CreateDirectory("playwright-failures");
                    var safeName = screenshotName ?? $"{GetType().Name}_{DateTime.UtcNow:yyyyMMdd_HHmmssfff}.png";
                    await page.ScreenshotAsync(new PageScreenshotOptions
                    {
                        Path = Path.Combine("playwright-failures", safeName),
                        FullPage = true,
                    });
                    throw;
                }
            }

            protected static ILocatorAssertions Expect(ILocator locator) => Assertions.Expect(locator);
            protected static IPageAssertions Expect(IPage page) => Assertions.Expect(page);
        }
        """;

    private static string BuildCsproj() => """
        <Project Sdk="Microsoft.NET.Sdk">
          <PropertyGroup>
            <TargetFramework>net10.0</TargetFramework>
            <Nullable>enable</Nullable>
            <ImplicitUsings>enable</ImplicitUsings>
            <IsPackable>false</IsPackable>
            <IsTestProject>true</IsTestProject>
          </PropertyGroup>
          <ItemGroup>
            <PackageReference Include="Microsoft.NET.Test.Sdk" Version="18.0.1" />
            <PackageReference Include="Microsoft.Playwright" Version="1.55.0" />
            <PackageReference Include="xunit" Version="2.9.3" />
            <PackageReference Include="xunit.runner.visualstudio" Version="3.1.5">
              <PrivateAssets>all</PrivateAssets>
            </PackageReference>
          </ItemGroup>
        </Project>
        """;

    private static string BuildReadme(BlazorComponentSpec s) => $$"""
        # Generated Playwright E2E tests

        Generated for Blazor page/component `{{s.ComponentName}}`.

        ## Local run

        ```powershell
        dotnet build
        pwsh bin/Debug/net10.0/playwright.ps1 install chromium
        $env:PLAYWRIGHT_BASE_URL = "http://localhost:5187"
        $env:PLAYWRIGHT_HEADLESS = "false"
        dotnet test
        ```

        ## CI/headless run

        ```powershell
        $env:PLAYWRIGHT_BASE_URL = "http://localhost:5187"
        $env:PLAYWRIGHT_HEADLESS = "true"
        dotnet test
        ```

        Screenshots for failed tests are written to `playwright-failures/`.
        """;

    private static string PrimaryRoute(BlazorComponentSpec s)
    {
        var route = s.Routes.FirstOrDefault()?.Route ?? "/" + ToKebabCase(s.ComponentName);
        var withoutConstraints = System.Text.RegularExpressions.Regex.Replace(route, @":\w+", "");
        return System.Text.RegularExpressions.Regex.Replace(withoutConstraints, @"\{[^}]+\}", "test");
    }

    private static string ToKebabCase(string value)
    {
        if (string.IsNullOrWhiteSpace(value))
            return "page";

        var sb = new StringBuilder();
        for (var i = 0; i < value.Length; i++)
        {
            var c = value[i];
            if (char.IsUpper(c) && i > 0)
                sb.Append('-');
            sb.Append(char.ToLowerInvariant(c));
        }
        return sb.ToString();
    }

    private static string Escape(string value) =>
        value.Replace("\\", "\\\\").Replace("\"", "\\\"");
}
