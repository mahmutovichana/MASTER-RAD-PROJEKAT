using System.Net;
using RBBH.CollateralAppraisal.Api.Tests.Helpers;
using Xunit;

namespace RBBH.CollateralAppraisal.Api.Tests.Protocol;

[Collection("ApiTests")]
public sealed class ProtocolEndpointsTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;
    public ProtocolEndpointsTests(ApiFactory f) => _factory = f;

    // ── GET /api/protocol/orders ──────────────────────────────────────────────

    [Fact]
    public async Task GetProtocolList_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient().GetAsync("/api/protocol/orders");
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task GetProtocolList_NoPermission_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-noperm")
            .GetAsync("/api/protocol/orders");
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task GetProtocolList_WithPermission_Returns200()
    {
        // test-admin ima protocol.view permission
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .GetAsync("/api/protocol/orders");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    [Fact]
    public async Task GetProtocolList_WithPagination_Returns200()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .GetAsync("/api/protocol/orders?page=1&pageSize=5");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    // ── GET /api/protocol/orders/{orderId} ────────────────────────────────────

    [Fact]
    public async Task GetProtocolByOrder_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient().GetAsync("/api/protocol/orders/1");
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task GetProtocolByOrder_NoPermission_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-noperm")
            .GetAsync("/api/protocol/orders/1");
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task GetProtocolByOrder_NonExistent_Returns404()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .GetAsync("/api/protocol/orders/99999");
        Assert.Equal(HttpStatusCode.NotFound, r.StatusCode);
    }
}
