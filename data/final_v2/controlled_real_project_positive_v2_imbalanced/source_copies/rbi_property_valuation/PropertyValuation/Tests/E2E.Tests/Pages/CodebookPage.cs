using Microsoft.Playwright;

namespace RBBH.CollateralAppraisal.E2E.Tests.Pages;

public sealed class CodebookPage(IPage page)
{
    public IDownload? LastDownload { get; private set; }

    public async Task GotoAsync() => await page.GotoAsync("/admin/sifarnici");

    public async Task<bool> IsOnPageAsync() =>
        page.Url.Contains("/admin/sifarnici");

    public async Task<int> GetCodebookCountAsync()
    {
        var rows = page.Locator("tr.mud-table-row, .mud-card");
        return await rows.CountAsync();
    }

    public async Task ClickExportAsync()
    {
        var downloadTask = page.WaitForDownloadAsync();
        await page.ClickAsync("button:has-text('Export'), button:has-text('Izvoz')");
        LastDownload = await downloadTask;
    }

    public async Task ClickImportAsync() =>
        await page.ClickAsync("button:has-text('Import'), button:has-text('Uvoz')");

    public async Task ClickAddCodebookAsync() =>
        await page.ClickAsync("button:has-text('Dodaj'), button:has-text('Novi')");

    public async Task FillNewCodebookAsync(string code, string label)
    {
        await page.Locator("input[placeholder*='kod'], input[label*='Kod']").First.FillAsync(code);
        await page.Locator("input[placeholder*='naziv'], input[label*='Naziv']").First.FillAsync(label);
    }

    public async Task ClickSaveAsync() =>
        await page.ClickAsync("button:has-text('Sačuvaj'), button:has-text('Potvrdi')");

    public async Task<bool> HasSuccessSnackbarAsync() =>
        await page.GetByText("uspješno", new PageGetByTextOptions { Exact = false })
                  .IsVisibleAsync();

    public async Task<bool> ImportPreviewIsVisibleAsync() =>
        await page.Locator(".mud-dialog, .preview-table, [class*='preview']")
                  .IsVisibleAsync();
}
