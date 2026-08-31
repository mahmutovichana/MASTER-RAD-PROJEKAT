using Microsoft.Playwright;
using RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;
using Xunit;

namespace RBBH.CollateralAppraisal.E2E.Tests.Tests;

/// <summary>
/// E2E testovi za access control — rola vidi samo to što treba.
/// Pokriva: zaštićene rute, API 401 bez auth, role isolation.
/// </summary>
[Collection("E2E")]
public sealed class AccessControlTests : IClassFixture<PlaywrightFixture>, IAsyncLifetime
{
    private readonly PlaywrightFixture _fixture;
    private IBrowserContext _anonCtx = null!;

    public AccessControlTests(PlaywrightFixture fixture) => _fixture = fixture;

    public async Task InitializeAsync()
    {
        _anonCtx = await _fixture.NewAnonymousContextAsync();
    }

    public async Task DisposeAsync() => await _anonCtx.DisposeAsync();

    [Theory]
    [InlineData("/narudzbe")]
    [InlineData("/moji-taskovi")]
    [InlineData("/admin/sifarnici")]
    [InlineData("/admin/upravljanje-rolama")]
    public async Task ProtectedPage_WithoutAuth_RedirectsToLogin(string path)
    {
        var page = await _anonCtx.NewPageAsync();
        page.SetDefaultTimeout(_fixture.Config.Timeout);

        await page.GotoAsync(path);
        await page.WaitForLoadStateAsync(LoadState.NetworkIdle);

        Assert.True(
            page.Url.Contains("/login") ||
            page.Url.Contains(_fixture.Config.KeycloakUrl),
            $"Nezalogiran korisnik pristupio {path}. URL: {page.Url}");

        await page.CloseAsync();
    }

    [Fact]
    public async Task API_WithoutAuth_Returns401()
    {
        var config = _fixture.Config;

        // Playwright IAPIRequestContext — novi anonimni kontekst za API poziv
        var apiCtx = await _fixture.Playwright.APIRequest.NewContextAsync(new()
        {
            BaseURL = config.ApiUrl
        });

        var response = await apiCtx.GetAsync("/api/orders");
        Assert.Equal(401, response.Status);

        await apiCtx.DisposeAsync();
    }

    [Fact]
    public async Task AM_CannotAccess_AdminRoutes()
    {
        await using var amCtx  = await _fixture.NewAuthenticatedContextAsync("AM");
        var amPage = await amCtx.NewPageAsync();
        amPage.SetDefaultTimeout(_fixture.Config.Timeout);

        await amPage.GotoAsync("/admin/upravljanje-rolama");
        await amPage.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await amPage.WaitForTimeoutAsync(1000);

        Assert.False(
            amPage.Url.Contains("/admin/upravljanje-rolama"),
            $"AM pristupio admin ruti. URL: {amPage.Url}");
    }
}
