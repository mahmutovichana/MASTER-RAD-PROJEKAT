using Microsoft.Playwright;
using RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;
using RBBH.CollateralAppraisal.E2E.Tests.Pages;
using Xunit;

namespace RBBH.CollateralAppraisal.E2E.Tests.Tests;

/// <summary>E2E testovi za Keycloak OIDC login flow.</summary>
[Collection("E2E")]
public sealed class LoginTests : IClassFixture<PlaywrightFixture>, IAsyncLifetime
{
    private readonly PlaywrightFixture _fixture;
    private IBrowserContext _ctx = null!;
    private IPage           _page = null!;

    public LoginTests(PlaywrightFixture fixture) => _fixture = fixture;

    public async Task InitializeAsync()
    {
        _ctx  = await _fixture.NewAnonymousContextAsync();
        _page = await _ctx.NewPageAsync();
        _page.SetDefaultTimeout(_fixture.Config.Timeout);
    }

    public async Task DisposeAsync() => await _ctx.DisposeAsync();

    [Fact]
    public async Task Login_AsAM_SuccessfullyRedirectsToDashboard()
    {
        var user = _fixture.Config.GetUser("AM");
        var login = new LoginPage(_page);

        await login.GotoAsync();
        await _page.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await login.FillUsernameAsync(user.Username);
        await login.ClickLoginButtonAsync();

        await _page.WaitForURLAsync(
            url => url.Contains(_fixture.Config.KeycloakUrl) || url.Contains("/realms/"),
            new PageWaitForURLOptions { Timeout = _fixture.Config.Timeout });

        await LoginPage.CompleteKeycloakLoginAsync(_page, user.Username, user.Password);

        await _page.WaitForLoadStateAsync(LoadState.NetworkIdle);
        Assert.False(_page.Url.Contains("/login"), $"AM ostao na /login. URL: {_page.Url}");
    }

    [Fact]
    public async Task Login_WrongPassword_StaysOnKeycloak()
    {
        var user = _fixture.Config.GetUser("AM");
        var login = new LoginPage(_page);

        await login.GotoAsync();
        await _page.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await login.FillUsernameAsync(user.Username);
        await login.ClickLoginButtonAsync();

        await _page.WaitForURLAsync(
            url => url.Contains(_fixture.Config.KeycloakUrl) || url.Contains("/realms/"),
            new PageWaitForURLOptions { Timeout = _fixture.Config.Timeout });

        await LoginPage.CompleteKeycloakLoginAsync(_page, user.Username, "PogrešnaLozinka123!");
        await _page.WaitForTimeoutAsync(1500);

        Assert.True(
            _page.Url.Contains(_fixture.Config.KeycloakUrl) ||
            _page.Url.Contains("/realms/"),
            "Korisnik s pogrešnom lozinkom prošao login.");
    }

    [Fact]
    public async Task ProtectedPage_WithoutLogin_RedirectsToLogin()
    {
        await _page.GotoAsync("/narudzbe");
        await _page.WaitForLoadStateAsync(LoadState.NetworkIdle);

        Assert.True(
            _page.Url.Contains("/login") ||
            _page.Url.Contains(_fixture.Config.KeycloakUrl),
            $"Nezalogiran korisnik pristupio zaštićenoj stranici. URL: {_page.Url}");
    }
}
