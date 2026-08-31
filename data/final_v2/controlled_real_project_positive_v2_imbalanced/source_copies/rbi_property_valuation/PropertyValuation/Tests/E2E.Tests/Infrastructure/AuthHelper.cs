using Microsoft.Playwright;

namespace RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;

/// <summary>
/// Upravlja Keycloak OIDC login flowom i čuvanjem auth state-a po ulozi.
/// Storage state (cookies) se kešira na disku da se login ne ponavlja pri svakom testu.
/// </summary>
public static class AuthHelper
{
    private static readonly string StateDir =
        Path.Combine(AppContext.BaseDirectory, "Infrastructure", "auth-state");

    public static string StateFilePath(string role) =>
        Path.Combine(StateDir, $"auth-state-{role.ToLowerInvariant()}.json");

    public static bool StateExists(string role) =>
        File.Exists(StateFilePath(role));

    /// <summary>
    /// Puni OIDC login kroz Keycloak browser flow i snima storage state.
    /// Poziva se jednom po ulozi po test sesiji.
    /// </summary>
    public static async Task LoginAndSaveStateAsync(
        IBrowser browser, UserCredentials user, E2EConfig config)
    {
        Directory.CreateDirectory(StateDir);

        await using var context = await browser.NewContextAsync(new BrowserNewContextOptions
        {
            BaseURL           = config.BaseUrl,
            IgnoreHTTPSErrors = true
        });

        var page = await context.NewPageAsync();
        page.SetDefaultTimeout(config.Timeout);

        // Korak 1: Otvori login stranicu
        await page.GotoAsync("/login");
        await page.WaitForLoadStateAsync(LoadState.NetworkIdle);

        // Korak 2: Unesi email u Web login formu
        var emailInput = page.Locator("input").First;
        await emailInput.FillAsync(user.Username);

        // Korak 3: Klikni dugme za prijavu → redirect na Keycloak
        await page.ClickAsync("button[type='submit'], button.login-btn, button:has-text('Prijavi')");

        // Korak 4: Čekaj Keycloak stranicu
        await page.WaitForURLAsync(
            url => url.Contains(config.KeycloakUrl) || url.Contains("/realms/"),
            new PageWaitForURLOptions { Timeout = config.Timeout });

        // Korak 5: Unesi Keycloak kredencijale
        await page.FillAsync("#username", user.Username);
        await page.FillAsync("#password", user.Password);
        await page.ClickAsync("#kc-login");

        // Korak 6: Čekaj povratak na aplikaciju
        await page.WaitForURLAsync(
            url => url.Contains(config.BaseUrl) && !url.Contains(config.KeycloakUrl),
            new PageWaitForURLOptions { Timeout = config.Timeout });

        // Korak 7: Odaberi ulogu ako postoji /select-role
        if (page.Url.Contains("/select-role"))
            await SelectRoleAsync(page, user.Role, config);

        await page.WaitForLoadStateAsync(LoadState.NetworkIdle);

        // Korak 8: Snimi storage state
        await context.StorageStateAsync(new BrowserContextStorageStateOptions
        {
            Path = StateFilePath(user.Role)
        });
    }

    private static async Task SelectRoleAsync(IPage page, string role, E2EConfig config)
    {
        await page.WaitForLoadStateAsync(LoadState.DOMContentLoaded);
        await page.WaitForTimeoutAsync(1000);

        var roleButton = page.GetByText(role, new PageGetByTextOptions { Exact = false });
        if (await roleButton.CountAsync() > 0)
        {
            await roleButton.First.ClickAsync();
            await page.WaitForLoadStateAsync(LoadState.NetworkIdle);
        }
    }
}
