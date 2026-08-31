using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using RBBH.CollateralAppraisal.Api.Tests.Helpers;
using Xunit;

namespace RBBH.CollateralAppraisal.Api.Tests.Tasks;

[Collection("ApiTests")]
public sealed class WorkflowTaskEndpointsTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;
    public WorkflowTaskEndpointsTests(ApiFactory f) => _factory = f;

    // ── GET /api/tasks/my ─────────────────────────────────────────────────────

    [Fact]
    public async Task GetMyTasks_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient().GetAsync("/api/tasks/my");
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task GetMyTasks_NoPermission_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-noperm").GetAsync("/api/tasks/my");
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task GetMyTasks_AM_Returns200WithEmptyList()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am").GetAsync("/api/tasks/my");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
        var body = await r.Content.ReadFromJsonAsync<JsonElement>();
        // Fresh DB — nema taskova
        Assert.True(body.TryGetProperty("items", out var items) &&
                    items.ValueKind == JsonValueKind.Array);
    }

    [Fact]
    public async Task GetMyTasks_WithPagination_Returns200()
    {
        var r = await _factory.CreateAuthenticatedClient("test-am")
            .GetAsync("/api/tasks/my?page=1&pageSize=5");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    // ── POST /api/tasks/{id}/accept ───────────────────────────────────────────

    [Fact]
    public async Task AcceptTask_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient()
            .PostAsJsonAsync("/api/tasks/1/accept", new { });
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task AcceptTask_NoPermission_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-noperm")
            .PostAsJsonAsync("/api/tasks/1/accept", new { });
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task AcceptTask_NonExistentId_Returns404()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .PostAsJsonAsync("/api/tasks/99999/accept", new { });
        Assert.Equal(HttpStatusCode.NotFound, r.StatusCode);
    }

    // ── POST /api/tasks/{id}/complete ─────────────────────────────────────────

    [Fact]
    public async Task CompleteTask_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient()
            .PostAsJsonAsync("/api/tasks/1/complete", new { comment = "Done" });
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task CompleteTask_NoPermission_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-noperm")
            .PostAsJsonAsync("/api/tasks/1/complete", new { comment = "Done" });
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task CompleteTask_NonExistentId_Returns404()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .PostAsJsonAsync("/api/tasks/99999/complete", new { comment = "Done" });
        Assert.Equal(HttpStatusCode.NotFound, r.StatusCode);
    }
}
