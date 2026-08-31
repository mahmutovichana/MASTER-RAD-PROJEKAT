using Microsoft.Playwright;

namespace E2ETests.Fixtures;

[Collection("E2E")]
public abstract class E2ETestBase : IAsyncLifetime
{
    protected readonly AppFixture App;
    protected readonly PlaywrightFixture Pw;
    protected IBrowserContext Context = null!;
    protected IPage Page = null!;

    private readonly string _testName;
    private string _artifactDir = "";

    protected E2ETestBase(AppFixture app, PlaywrightFixture pw)
    {
        App = app;
        Pw = pw;
        _testName = GetType().Name + "_" + Guid.NewGuid().ToString("N")[..8];
    }

    public async Task InitializeAsync()
    {
        _artifactDir = ArtifactPaths.For(_testName);
        Directory.CreateDirectory(_artifactDir);

        Context = await Pw.NewContextAsync(_testName);
        Page = await Context.NewPageAsync();
    }

    public async Task DisposeAsync()
    {
        try
        {
            var screenshotPath = Path.Combine(_artifactDir, "screenshot.png");
            await Page.ScreenshotAsync(new PageScreenshotOptions
            {
                Path = screenshotPath,
                FullPage = true,
            });
        }
        catch { /* best-effort */ }

        await Context.CloseAsync();
    }

    protected async Task NavigateAndWait(string path)
    {
        await Page.GotoAsync($"{App.BaseUrl}{path}", new PageGotoOptions
        {
            WaitUntil = WaitUntilState.Load,
            Timeout = 60_000,
        });
        await Page.WaitForLoadStateAsync(LoadState.NetworkIdle);
    }
}
