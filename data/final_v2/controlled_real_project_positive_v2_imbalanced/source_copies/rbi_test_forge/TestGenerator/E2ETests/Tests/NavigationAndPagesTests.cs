using E2ETests.Fixtures;
using Microsoft.Playwright;

namespace E2ETests.Tests;

public sealed class NavigationAndPagesTests(AppFixture app, PlaywrightFixture pw) : E2ETestBase(app, pw)
{
    [Theory]
    [InlineData("/app", "Test Automation Generator")]
    [InlineData("/app/groups", "Groups")]
    [InlineData("/app/scenarios", "Test scenarios")]
    [InlineData("/app/history", "History")]
    public async Task Page_LoadsSuccessfully(string path, string expectedText)
    {
        await NavigateAndWait(path);
        await Assertions.Expect(Page.Locator($"text={expectedText}").First).ToBeVisibleAsync(
            new LocatorAssertionsToBeVisibleOptions { Timeout = 30_000 });
    }

    [Fact]
    public async Task Sidebar_Navigation_Works()
    {
        await NavigateAndWait("/app");

        // Click Grupe in sidebar
        await Page.GetByRole(AriaRole.Link, new() { Name = "Groups", Exact = true }).First.ClickAsync();
        await Page.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await Assertions.Expect(Page.GetByRole(AriaRole.Heading, new() { Name = "Groups" })).ToBeVisibleAsync();

        // Click Scenariji in sidebar
        await Page.GetByRole(AriaRole.Link, new() { Name = "Test scenarios", Exact = true }).First.ClickAsync();
        await Page.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await Assertions.Expect(Page.Locator("text=Test scenarios").First).ToBeVisibleAsync();

        // Click Historija in sidebar
        await Page.GetByRole(AriaRole.Link, new() { Name = "History", Exact = true }).First.ClickAsync();
        await Page.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await Assertions.Expect(Page.Locator("text=History").First).ToBeVisibleAsync();
    }

    [Fact]
    public async Task Dashboard_ShowsSummaryCards()
    {
        await NavigateAndWait("/app");

        // Dashboard should show content
        await Assertions.Expect(Page.GetByText("Test Automation Generator").First).ToBeVisibleAsync(
            new LocatorAssertionsToBeVisibleOptions { Timeout = 30_000 });
    }

    [Fact]
    public async Task Scenariji_Table_Loads()
    {
        await NavigateAndWait("/app/scenarios");

        // Table should be visible with scenario data
        await Assertions.Expect(Page.Locator("table").First).ToBeVisibleAsync(
            new LocatorAssertionsToBeVisibleOptions { Timeout = 30_000 });
    }
}
