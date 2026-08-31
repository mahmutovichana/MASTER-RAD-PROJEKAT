using Microsoft.Playwright;
using RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;
using RBBH.CollateralAppraisal.E2E.Tests.Pages;
using Xunit;

namespace RBBH.CollateralAppraisal.E2E.Tests.Tests;

/// <summary>E2E testovi za CA/CO taskove — My Tasks dashboard.</summary>
[Collection("E2E")]
public sealed class TaskWorkflowTests : IClassFixture<PlaywrightFixture>, IAsyncLifetime
{
    private readonly PlaywrightFixture _fixture;
    private IBrowserContext _ctx  = null!;
    private IPage           _page = null!;

    public TaskWorkflowTests(PlaywrightFixture fixture) => _fixture = fixture;

    public async Task InitializeAsync()
    {
        _ctx  = await _fixture.NewAuthenticatedContextAsync("CA");
        _page = await _ctx.NewPageAsync();
        _page.SetDefaultTimeout(_fixture.Config.Timeout);
    }

    public async Task DisposeAsync() => await _ctx.DisposeAsync();

    private MyTasksPage  TasksPage  => new(_page);
    private MyOrdersPage OrdersPage => new(_page);

    [Fact]
    public async Task MyTasks_AsCA_PageLoadsSuccessfully()
    {
        await TasksPage.GotoAsync();
        await _page.WaitForLoadStateAsync(LoadState.NetworkIdle);

        Assert.True(await TasksPage.IsOnPageAsync(),
            "CA ne može pristupiti /moji-taskovi.");
    }

    [Fact]
    public async Task MyTasks_AsCA_DisplaysTasksOrEmptyState()
    {
        await TasksPage.GotoAsync();
        await _page.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await _page.WaitForTimeoutAsync(800);

        var count       = await TasksPage.GetTaskCountAsync();
        var hasEmptyMsg = await _page.GetByText("Nema aktivnih",
            new PageGetByTextOptions { Exact = false }).IsVisibleAsync();

        Assert.True(count > 0 || hasEmptyMsg,
            "My Tasks ne prikazuje ni taskove ni empty state.");
    }

    [Fact]
    public async Task MyOrders_AsCA_CanSeeAllOrders()
    {
        await OrdersPage.GotoAsync();
        await _page.WaitForLoadStateAsync(LoadState.NetworkIdle);

        Assert.True(_page.Url.Contains("/narudzbe"),
            "CA ne može pristupiti listi narudžbi.");
    }

    [Fact]
    public async Task AM_CannotAccess_AdminCodebooks()
    {
        await using var amCtx  = await _fixture.NewAuthenticatedContextAsync("AM");
        var amPage = await amCtx.NewPageAsync();
        amPage.SetDefaultTimeout(_fixture.Config.Timeout);

        await amPage.GotoAsync("/admin/sifarnici");
        await amPage.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await amPage.WaitForTimeoutAsync(1000);

        Assert.False(
            amPage.Url.Contains("/admin/sifarnici"),
            $"AM je pristupio admin stranici. URL: {amPage.Url}");
    }
}
