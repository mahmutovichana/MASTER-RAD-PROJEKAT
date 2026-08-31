using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using RBBH.CollateralAppraisal.Api.Tests.Helpers;
using Xunit;

namespace RBBH.CollateralAppraisal.Api.Tests.Notifications;

[Collection("ApiTests")]
public sealed class NotificationsEndpointsTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;
    public NotificationsEndpointsTests(ApiFactory f) => _factory = f;

    // ── GET /api/notifications/mine ───────────────────────────────────────────

    [Fact]
    public async Task GetMyNotifications_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient().GetAsync("/api/notifications/mine");
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task GetMyNotifications_NoPermission_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-noperm")
            .GetAsync("/api/notifications/mine");
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task GetMyNotifications_AM_Returns200WithPagedResult()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am")
            .GetAsync("/api/notifications/mine");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
        var body = await r.Content.ReadFromJsonAsync<JsonElement>();
        Assert.True(body.TryGetProperty("items", out _));
    }

    [Fact]
    public async Task GetMyNotifications_WithUnreadOnlyFilter_Returns200()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am")
            .GetAsync("/api/notifications/mine?unreadOnly=true&page=1&pageSize=10");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    // ── GET /api/notifications/unread-count ───────────────────────────────────

    [Fact]
    public async Task GetUnreadCount_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient().GetAsync("/api/notifications/unread-count");
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task GetUnreadCount_NoPermission_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-noperm")
            .GetAsync("/api/notifications/unread-count");
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task GetUnreadCount_AM_Returns200WithCount()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am")
            .GetAsync("/api/notifications/unread-count");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
        var body = await r.Content.ReadFromJsonAsync<JsonElement>();
        Assert.True(body.TryGetProperty("count", out var count) &&
                    count.ValueKind == JsonValueKind.Number);
    }

    // ── POST /api/notifications/{id}/read ─────────────────────────────────────

    [Fact]
    public async Task MarkRead_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient()
            .PostAsJsonAsync("/api/notifications/1/read", new { });
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task MarkRead_NoPermission_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-noperm")
            .PostAsJsonAsync("/api/notifications/1/read", new { });
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task MarkRead_NonExistent_Returns404()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am")
            .PostAsJsonAsync("/api/notifications/99999/read", new { });
        Assert.Equal(HttpStatusCode.NotFound, r.StatusCode);
    }
}
