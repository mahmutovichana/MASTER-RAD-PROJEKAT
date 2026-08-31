using Microsoft.Playwright;
using System.Text.RegularExpressions;
using Xunit;

namespace RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;

/// <summary>
/// Bazna klasa za E2E testove koji koriste browser UI.
/// Osigurava kreiranje i disposing browser contexta po testu.
/// </summary>
public abstract class E2ETestBase : IClassFixture<PlaywrightFixture>, IAsyncLifetime
{
    protected readonly PlaywrightFixture Fixture;
    protected IBrowserContext Context  { get; set; } = null!;
    protected IPage           Page     { get; set; } = null!;
    protected E2EConfig       Config   => Fixture.Config;

    protected E2ETestBase(PlaywrightFixture fixture) => Fixture = fixture;

    public virtual async Task InitializeAsync()
    {
        Context = await Fixture.NewAuthenticatedContextAsync(RequiredRole);
        Page    = await Context.NewPageAsync();
        Page.SetDefaultTimeout(Config.Timeout);

        await Page.GotoAsync("/");
        await WaitForBlazorAsync();
    }

    public virtual async Task DisposeAsync()
    {
        await Context.DisposeAsync();
    }

    /// <summary>Uloga korisnika za ovaj test. Override u svakoj test klasi.</summary>
    protected virtual string RequiredRole => "AM";

    protected async Task WaitForBlazorAsync()
    {
        await Page.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await Page.WaitForTimeoutAsync(500);
    }

    protected async Task<ILocator> WaitForElementAsync(string selector, int timeoutMs = 8000)
    {
        var locator = Page.Locator(selector);
        await locator.WaitForAsync(new LocatorWaitForOptions { Timeout = timeoutMs });
        return locator;
    }

    protected async Task AssertPageContainsAsync(string text)
        => await Assertions.Expect(Page.GetByText(text)).ToBeVisibleAsync();

    protected async Task AssertUrlContainsAsync(string path)
        => await Assertions.Expect(Page).ToHaveURLAsync(new Regex(Regex.Escape(path)));

    protected async Task<string> CaptureScreenshotAsync(string name)
    {
        var dir  = Path.Combine(AppContext.BaseDirectory, "screenshots");
        Directory.CreateDirectory(dir);
        var path = Path.Combine(dir, $"{name}-{DateTime.Now:yyyyMMdd-HHmmss}.png");
        await Page.ScreenshotAsync(new PageScreenshotOptions { Path = path });
        return path;
    }
}
