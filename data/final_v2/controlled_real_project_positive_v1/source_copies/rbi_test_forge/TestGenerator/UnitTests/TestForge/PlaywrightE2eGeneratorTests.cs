using RBBH.TestAutomation.Core.Generation;
using Xunit;

namespace UnitTests.TestForge;

public class PlaywrightE2eGeneratorTests
{
    private readonly PlaywrightE2eGenerator _sut = new();

    private static BlazorComponentSpec Spec() => new(
        ComponentName: "Grupe",
        Routes: [new BlazorPageRoute("/grupe")],
        Parameters: [],
        EventCallbacks: [],
        OnClickHandlers: [],
        HttpCalls: [],
        Forms: [new BlazorForm(["InputText", "InputNumber"], HasValidationSummary: true)]);

    [Fact]
    public void Generate_ReturnsProjectFiles()
    {
        var result = _sut.Generate(Spec());
        var names = result.Files.Select(f => f.FileName).ToHashSet();

        Assert.Contains("GrupePage.cs", names);
        Assert.Contains("GrupeE2eTests.cs", names);
        Assert.Contains("PlaywrightTestBase.cs", names);
        Assert.Contains("GeneratedPlaywrightTests.csproj", names);
        Assert.Contains("README.md", names);
    }

    [Fact]
    public void Generate_PageObject_ContainsNavigationAndSelectors()
    {
        var pageObject = _sut.Generate(Spec()).Files.Single(f => f.FileName == "GrupePage.cs").Content;

        Assert.Contains("public sealed class GrupePage", pageObject);
        Assert.Contains("GotoAsync", pageObject);
        Assert.Contains("DataContainers", pageObject);
        Assert.Contains("FillDetectedFormAsync", pageObject);
    }

    [Fact]
    public void Generate_TestBase_ContainsLaunchCloseAndScreenshotOnFailure()
    {
        var testBase = _sut.Generate(Spec()).Files.Single(f => f.FileName == "PlaywrightTestBase.cs").Content;

        Assert.Contains("LaunchBrowserAsync", testBase);
        Assert.Contains("CloseBrowserAsync", testBase);
        Assert.Contains("RunWithScreenshotOnFailureAsync", testBase);
        Assert.Contains("page.ScreenshotAsync", testBase);
    }

    [Fact]
    public void Generate_TestClass_ContainsNavigationFormAndDisplayTests()
    {
        var testClass = _sut.Generate(Spec()).Files.Single(f => f.FileName == "GrupeE2eTests.cs").Content;

        Assert.Contains("Grupe_NavigatesAndLoads", testClass);
        Assert.Contains("Grupe_FillAndSubmitForm", testClass);
        Assert.Contains("Grupe_SubmitEmptyForm_ShowsValidationFeedback", testClass);
        Assert.Contains("Grupe_DisplaysDataContainers_WhenPresent", testClass);
    }

    [Fact]
    public void Generate_Csproj_UsesPlaywrightAndHeadlessReadme()
    {
        var result = _sut.Generate(Spec());
        var csproj = result.Files.Single(f => f.FileName == "GeneratedPlaywrightTests.csproj").Content;
        var readme = result.Files.Single(f => f.FileName == "README.md").Content;

        Assert.Contains("Microsoft.Playwright", csproj);
        Assert.Contains("PLAYWRIGHT_HEADLESS", readme);
        Assert.Contains("dotnet test", readme);
    }
}
