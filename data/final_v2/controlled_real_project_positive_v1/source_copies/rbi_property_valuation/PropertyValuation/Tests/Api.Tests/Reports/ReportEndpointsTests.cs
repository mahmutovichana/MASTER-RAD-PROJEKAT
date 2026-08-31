using System.Net;
using RBBH.CollateralAppraisal.Api.Tests.Helpers;
using Xunit;

namespace RBBH.CollateralAppraisal.Api.Tests.Reports;

[Collection("ApiTests")]
public sealed class ReportEndpointsTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;
    public ReportEndpointsTests(ApiFactory f) => _factory = f;

    // ── GET /api/reports/concentration ───────────────────────────────────────

    [Fact]
    public async Task ConcentrationReport_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient()
            .GetAsync("/api/reports/concentration?option=1");
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task ConcentrationReport_NoPermission_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-noperm")
            .GetAsync("/api/reports/concentration?option=1");
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task ConcentrationReport_AM_Returns403()
    {
        // AM nema reports.generate permission
        var r = await _factory.CreateAuthenticatedClient("test-am")
            .GetAsync("/api/reports/concentration?option=1");
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task ConcentrationReport_Admin_Returns200WithExcelFile()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .GetAsync("/api/reports/concentration?option=1");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
        // Report vraća Excel fajl
        var contentType = r.Content.Headers.ContentType?.MediaType;
        Assert.Contains("spreadsheet", contentType ?? "", StringComparison.OrdinalIgnoreCase);
    }

    [Theory]
    [InlineData(1)]
    [InlineData(2)]
    [InlineData(3)]
    [InlineData(4)]
    [InlineData(5)]
    public async Task ConcentrationReport_AllOptions_Returns200(int option)
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .GetAsync($"/api/reports/concentration?option={option}");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    // ── GET /api/reports/timeline ─────────────────────────────────────────────

    [Fact]
    public async Task TimelineReport_Anonymous_Returns401()
    {
        var r = await _factory.CreateAnonymousClient().GetAsync("/api/reports/timeline");
        Assert.Equal(HttpStatusCode.Unauthorized, r.StatusCode);
    }

    [Fact]
    public async Task TimelineReport_NoPermission_Returns403()
    {
        var r = await _factory.CreateAuthenticatedClient("test-noperm")
            .GetAsync("/api/reports/timeline");
        Assert.Equal(HttpStatusCode.Forbidden, r.StatusCode);
    }

    [Fact]
    public async Task TimelineReport_Admin_Returns200()
    {
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .GetAsync("/api/reports/timeline");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }

    [Fact]
    public async Task TimelineReport_WithEndDate_Returns200()
    {
        var endDate = "2026-12-31";
        var r = await _factory.CreateAuthenticatedClient("test-admin")
            .GetAsync($"/api/reports/timeline?endDate={endDate}");
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
    }
}
