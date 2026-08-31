using Microsoft.Playwright;
using RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;

namespace RBBH.CollateralAppraisal.E2E.Tests.Pages;

public sealed class LoginPage(IPage page)
{
    public async Task GotoAsync() => await page.GotoAsync("/login");

    public async Task FillUsernameAsync(string username) =>
        await page.Locator("input").First.FillAsync(username);

    public async Task ClickLoginButtonAsync() =>
        await page.ClickAsync("button[type='submit'], button.login-btn, button:has-text('Prijavi')");

    public static async Task CompleteKeycloakLoginAsync(IPage page, string username, string password)
    {
        await page.FillAsync("#username", username);
        await page.FillAsync("#password", password);
        await page.ClickAsync("#kc-login");
    }
}
