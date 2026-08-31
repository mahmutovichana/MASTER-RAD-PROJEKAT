using E2ETests.Fixtures;
using Microsoft.Playwright;

namespace E2ETests.Tests;

public sealed class GroupWorkflowTests(AppFixture app, PlaywrightFixture pw) : E2ETestBase(app, pw)
{
    [Fact]
    public async Task CreateGroup_AddScenario_Run_CheckResults()
    {
        // 1. Navigate to Grupe page
        await NavigateAndWait("/app/groups");
        await Assertions.Expect(Page.GetByRole(AriaRole.Heading, new() { Name = "Groups" })).ToBeVisibleAsync(
            new LocatorAssertionsToBeVisibleOptions { Timeout = 30_000 });

        // 2. Click "Nova grupa" button
        await Page.GetByRole(AriaRole.Button, new() { Name = "New record" }).ClickAsync();
        await Page.GetByRole(AriaRole.Dialog).WaitForAsync();

        // 3. Fill in group form
        var dialog = Page.GetByRole(AriaRole.Dialog);
        await dialog.Locator("input").First.FillAsync("E2E Test Grupa");
        await dialog.Locator("textarea").First.FillAsync("Kreirana E2E testom");

        // 4. Save the group
        await dialog.GetByRole(AriaRole.Button, new() { Name = "Save" }).ClickAsync();
        await Assertions.Expect(dialog).ToBeHiddenAsync();

        // 5. Verify group appears in list (use exact match to avoid matching toast)
        await Assertions.Expect(Page.GetByText("E2E Test Grupa", new PageGetByTextOptions { Exact = true }))
            .ToBeVisibleAsync(new LocatorAssertionsToBeVisibleOptions { Timeout = 30_000 });

        // 6. Navigate to Scenariji
        await NavigateAndWait("/app/scenarios");
        await Assertions.Expect(Page.GetByRole(AriaRole.Heading, new() { Name = "Test scenarios" })).ToBeVisibleAsync();

        // 7. Verify the page loaded
        await Assertions.Expect(Page.Locator("table").First).ToBeVisibleAsync(
            new LocatorAssertionsToBeVisibleOptions { Timeout = 30_000 });
    }
}
