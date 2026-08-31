using Microsoft.Playwright;

namespace RBBH.CollateralAppraisal.E2E.Tests.Pages;

public sealed class MyOrdersPage(IPage page)
{
    public async Task GotoAsync() => await page.GotoAsync("/narudzbe");

    public async Task<bool> IsOnPageAsync() =>
        page.Url.Contains("/narudzbe");

    public async Task<int> GetOrderCountAsync()
    {
        var rows = page.Locator("tr.mud-table-row, .order-card, .mud-card");
        return await rows.CountAsync();
    }

    public async Task ClickOrderAsync(int orderId) =>
        await page.ClickAsync($"[href*='/narudzbe/{orderId}'], a:has-text('{orderId}')");
}
