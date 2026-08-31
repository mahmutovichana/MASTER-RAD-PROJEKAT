using Microsoft.Playwright;
using Xunit;

namespace RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;

/// <summary>
/// xUnit class fixture koji dijeli jednu Playwright instancu kroz sve testove kolekcije.
/// Browser se pokreće jednom, auth state se kešira po ulozi.
/// </summary>
public sealed class PlaywrightFixture : IAsyncLifetime
{
    public IPlaywright Playwright { get; private set; } = null!;
    public IBrowser    Browser    { get; private set; } = null!;
    public E2EConfig   Config     { get; }               = E2EConfig.Load();

    public async Task InitializeAsync()
    {
        Playwright = await Microsoft.Playwright.Playwright.CreateAsync();

        Browser = await Playwright.Chromium.LaunchAsync(new BrowserTypeLaunchOptions
        {
            Headless = Config.Headless,
            SlowMo   = Config.SlowMo,
            Args     = ["--no-sandbox", "--disable-dev-shm-usage"]
        });

        // Pre-autentifikuj sve konfigurisane uloge
        foreach (var (role, user) in Config.Users)
        {
            if (!AuthHelper.StateExists(role))
            {
                try { await AuthHelper.LoginAndSaveStateAsync(Browser, user, Config); }
                catch (Exception ex)
                {
                    Console.WriteLine(
                        $"[PlaywrightFixture] Login za ulogu '{role}' nije uspio: {ex.Message}. " +
                        $"Testovi koji zahtijevaju UI auth za ovu ulogu će biti preskočeni.");
                }
            }
        }
    }

    public async Task DisposeAsync()
    {
        await Browser.DisposeAsync();
        Playwright.Dispose();
    }

    /// <summary>Kreira browser context s auth state-om za zadanu ulogu.</summary>
    public async Task<IBrowserContext> NewAuthenticatedContextAsync(string role)
    {
        var stateFile = AuthHelper.StateFilePath(role);

        return await Browser.NewContextAsync(new BrowserNewContextOptions
        {
            BaseURL           = Config.BaseUrl,
            StorageStatePath  = File.Exists(stateFile) ? stateFile : null,
            IgnoreHTTPSErrors = true,
            ViewportSize      = new ViewportSize { Width = 1280, Height = 800 }
        });
    }

    /// <summary>Kreira anonimni context — za testiranje 401/403 scenarija.</summary>
    public async Task<IBrowserContext> NewAnonymousContextAsync() =>
        await Browser.NewContextAsync(new BrowserNewContextOptions
        {
            BaseURL           = Config.BaseUrl,
            IgnoreHTTPSErrors = true,
            ViewportSize      = new ViewportSize { Width = 1280, Height = 800 }
        });
}
