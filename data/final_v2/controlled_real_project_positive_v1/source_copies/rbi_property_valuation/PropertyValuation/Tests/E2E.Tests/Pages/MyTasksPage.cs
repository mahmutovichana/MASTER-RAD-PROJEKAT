using Microsoft.Playwright;

namespace RBBH.CollateralAppraisal.E2E.Tests.Pages;

public sealed class MyTasksPage(IPage page)
{
    public async Task GotoAsync() => await page.GotoAsync("/moji-taskovi");

    public async Task<bool> IsOnPageAsync() =>
        page.Url.Contains("/moji-taskovi");

    public async Task<int> GetTaskCountAsync()
    {
        var rows = page.Locator("tr.mud-table-row, .task-card, .mud-card");
        return await rows.CountAsync();
    }

    public async Task<bool> HasTasksAsync() =>
        await GetTaskCountAsync() > 0;

    public async Task ClickAcceptTaskAsync() =>
        await page.GetByText("Prihvati", new PageGetByTextOptions { Exact = false })
                  .First.ClickAsync();
}
