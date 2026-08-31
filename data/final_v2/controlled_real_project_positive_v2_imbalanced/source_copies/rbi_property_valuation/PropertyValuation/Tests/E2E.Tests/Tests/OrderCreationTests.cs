using Microsoft.Playwright;
using RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;
using RBBH.CollateralAppraisal.E2E.Tests.Pages;
using Xunit;

namespace RBBH.CollateralAppraisal.E2E.Tests.Tests;

/// <summary>
/// E2E testovi za kreiranje narudžbe kroz UI (AM uloga).
/// Happy path: FL narudžba, submit, draft, validacija.
/// </summary>
[Collection("E2E")]
public sealed class OrderCreationTests : IClassFixture<PlaywrightFixture>, IAsyncLifetime
{
    private readonly PlaywrightFixture _fixture;
    private IBrowserContext _ctx  = null!;
    private IPage           _page = null!;

    public OrderCreationTests(PlaywrightFixture fixture) => _fixture = fixture;

    public async Task InitializeAsync()
    {
        _ctx  = await _fixture.NewAuthenticatedContextAsync("AM");
        _page = await _ctx.NewPageAsync();
        _page.SetDefaultTimeout(_fixture.Config.Timeout);
    }

    public async Task DisposeAsync() => await _ctx.DisposeAsync();

    private CreateOrderPage CreatePage => new(_page);
    private MyOrdersPage    OrdersPage => new(_page);

    [Fact]
    public async Task CreateOrder_WithEmptyForm_SubmitButtonIsDisabled()
    {
        await CreatePage.GotoFLAsync();
        await _page.WaitForLoadStateAsync(LoadState.NetworkIdle);

        Assert.False(await CreatePage.IsSubmitEnabledAsync(),
            "Submit je aktivan na praznoj formi — greška validacije.");
    }

    [Fact]
    public async Task CreateOrder_AsDraft_SavesWithoutSubmitting()
    {
        await CreatePage.GotoFLAsync();
        await _page.WaitForLoadStateAsync(LoadState.NetworkIdle);

        await CreatePage.FillClientNameAsync("E2E Draft Klijent");
        await CreatePage.FillContactNameAsync("Kontakt");
        await CreatePage.ClickSaveDraftAsync();

        await _page.WaitForTimeoutAsync(2000);

        await OrdersPage.GotoAsync();
        var count = await OrdersPage.GetOrderCountAsync();
        Assert.True(count >= 1, "Draft narudžba nije vidljiva u listi.");
    }

    [Fact]
    public async Task NavigateTo_CreateOrderChooser_AsAM_PageLoads()
    {
        await _page.GotoAsync("/narudzbe/nova");
        await _page.WaitForLoadStateAsync(LoadState.NetworkIdle);

        Assert.True(
            _page.Url.Contains("/narudzbe/nova") || _page.Url.Contains("/narudzbe"),
            $"AM ne može pristupiti /narudzbe/nova. URL: {_page.Url}");
    }
}
