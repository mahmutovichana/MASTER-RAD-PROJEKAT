using Microsoft.Playwright;

namespace E2ETests.Fixtures;

public sealed class PlaywrightFixture : IAsyncLifetime
{
    public IPlaywright Playwright { get; private set; } = null!;
    public IBrowser Browser { get; private set; } = null!;

    public async Task InitializeAsync()
    {
        Playwright = await Microsoft.Playwright.Playwright.CreateAsync();
        Browser = await Playwright.Chromium.LaunchAsync(new BrowserTypeLaunchOptions
        {
            Headless = true,
        });
    }

    public async Task DisposeAsync()
    {
        await Browser.DisposeAsync();
        Playwright.Dispose();
    }

    public async Task<IBrowserContext> NewContextAsync(string testName)
    {
        var artifactDir = ArtifactPaths.For(testName);
        Directory.CreateDirectory(artifactDir);

        return await Browser.NewContextAsync(new BrowserNewContextOptions
        {
            RecordVideoDir = artifactDir,
            RecordVideoSize = new RecordVideoSize { Width = 1280, Height = 720 },
        });
    }
}
