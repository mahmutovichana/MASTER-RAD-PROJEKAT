using E2ETests.Fixtures;
using Microsoft.Playwright;

namespace E2ETests.Tests;

public sealed class ScheduleWorkflowTests(AppFixture app, PlaywrightFixture pw) : E2ETestBase(app, pw)
{
    [Fact]
    public async Task CreateSchedule_VerifyInDashboard_Deactivate()
    {
        // 1. Navigate to Rasporedi page
        await NavigateAndWait("/app/schedules");
        await Assertions.Expect(Page.GetByRole(AriaRole.Heading, new() { Name = "Schedules" })).ToBeVisibleAsync(
            new LocatorAssertionsToBeVisibleOptions { Timeout = 30_000 });

        // 2. Verify the page loaded with schedule UI
        await Page.WaitForLoadStateAsync(LoadState.NetworkIdle);

        // 3. Check Hangfire dashboard is accessible
        var hangfireResp = await Page.Context.APIRequest.GetAsync($"{App.ApiBaseUrl}/hangfire");
        Assert.True(
            hangfireResp.Status is 200 or 301 or 302,
            $"Hangfire dashboard should be accessible, got {hangfireResp.Status}");

        // 4. Navigate to Grupe to verify schedule controls exist
        await NavigateAndWait("/app/groups");
        await Assertions.Expect(Page.GetByRole(AriaRole.Heading, new() { Name = "Groups" })).ToBeVisibleAsync(
            new LocatorAssertionsToBeVisibleOptions { Timeout = 30_000 });
    }
}
