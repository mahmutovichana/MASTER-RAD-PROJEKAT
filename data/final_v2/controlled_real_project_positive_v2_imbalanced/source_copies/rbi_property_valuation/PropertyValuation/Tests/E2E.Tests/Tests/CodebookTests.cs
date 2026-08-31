using Microsoft.Playwright;
using RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;
using RBBH.CollateralAppraisal.E2E.Tests.Pages;
using Xunit;

namespace RBBH.CollateralAppraisal.E2E.Tests.Tests;

/// <summary>E2E testovi za upravljanje šifarnicima (Admin).</summary>
[Collection("E2E")]
public sealed class CodebookTests : IClassFixture<PlaywrightFixture>, IAsyncLifetime
{
    private readonly PlaywrightFixture _fixture;
    private IBrowserContext _ctx  = null!;
    private IPage           _page = null!;

    public CodebookTests(PlaywrightFixture fixture) => _fixture = fixture;

    public async Task InitializeAsync()
    {
        _ctx  = await _fixture.NewAuthenticatedContextAsync("Admin");
        _page = await _ctx.NewPageAsync();
        _page.SetDefaultTimeout(_fixture.Config.Timeout);
    }

    public async Task DisposeAsync() => await _ctx.DisposeAsync();

    private CodebookPage Codebooks => new(_page);

    [Fact]
    public async Task Codebooks_AdminCanAccessPage()
    {
        await Codebooks.GotoAsync();
        await _page.WaitForLoadStateAsync(LoadState.NetworkIdle);

        Assert.True(await Codebooks.IsOnPageAsync(),
            "Admin ne može pristupiti /admin/sifarnici.");
    }

    [Fact]
    public async Task Codebooks_PageDisplaysExistingCodebooks()
    {
        await Codebooks.GotoAsync();
        await _page.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await _page.WaitForTimeoutAsync(500);

        var count = await Codebooks.GetCodebookCountAsync();
        Assert.True(count > 0,
            "Lista šifarnika je prazna — provjeri CodebookSeeder.");
    }

    [Fact]
    public async Task Codebooks_AM_CannotAccessAdminPage()
    {
        await using var amCtx  = await _fixture.NewAuthenticatedContextAsync("AM");
        var amPage = await amCtx.NewPageAsync();
        amPage.SetDefaultTimeout(_fixture.Config.Timeout);

        await amPage.GotoAsync("/admin/sifarnici");
        await amPage.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await amPage.WaitForTimeoutAsync(1000);

        Assert.False(
            amPage.Url.Contains("/admin/sifarnici"),
            $"AM je pristupio admin/sifarnici. URL: {amPage.Url}");
    }
}
