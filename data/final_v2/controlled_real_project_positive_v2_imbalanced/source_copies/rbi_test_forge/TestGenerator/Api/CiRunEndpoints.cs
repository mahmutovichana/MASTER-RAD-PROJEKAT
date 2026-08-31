using RBBH.TestAutomation.Api.Services;
using RBBH.TestAutomation.Api.Services.ApiKeys;
using RBBH.TestAutomation.Api.Services.Ci;
using RBBH.TestAutomation.Core.Reporting;

namespace RBBH.TestAutomation.Api.Api;

public sealed record CiJobStatusResponse(
    Guid                  JobId,
    string                Status,
    string                StatusUrl,
    int                   Total,
    int                   Completed,
    string                Progress,
    double                PassRate,
    IReadOnlyList<string> FailedTests,
    DateTime              StartedAt,
    DateTime?             CompletedAt);

public static class CiRunEndpoints
{
    private static readonly TimeSpan MaxSyncWait = TimeSpan.FromMinutes(10);

    public static IEndpointRouteBuilder MapCiRunEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/run");

        group.MapPost("/group/{groupId:guid}", async (
            Guid groupId, bool? waitForCompletion,
            HttpContext http, ICiRunService ci, IApiKeyService apiKeys, ILoggerFactory lf) =>
        {
            var auth = await AuthorizeAsync(http, apiKeys, lf.CreateLogger("CiApi"));
            if (auth is not null) return auth;

            var jobId = ci.StartGroupRun(groupId);
            return await RespondAsync(jobId, waitForCompletion, http, ci);
        }).DisableAntiforgery();

        group.MapPost("/tag/{tag}", async (
            string tag, bool? waitForCompletion,
            HttpContext http, ICiRunService ci, IApiKeyService apiKeys, ILoggerFactory lf) =>
        {
            var auth = await AuthorizeAsync(http, apiKeys, lf.CreateLogger("CiApi"));
            if (auth is not null) return auth;

            var jobId = ci.StartTagRun(tag);
            if (jobId is null)
                return Results.BadRequest(new { error = $"Nepoznat tag '{tag}'. Dozvoljeni: Smoke, Regression, Full." });

            return await RespondAsync(jobId.Value, waitForCompletion, http, ci);
        }).DisableAntiforgery();

        group.MapGet("/job/{jobId:guid}/status", async (
            Guid jobId, HttpContext http, ICiRunService ci, IApiKeyService apiKeys, ILoggerFactory lf) =>
        {
            var auth = await AuthorizeAsync(http, apiKeys, lf.CreateLogger("CiApi"));
            if (auth is not null) return auth;

            var snap = ci.GetStatus(jobId);
            return snap is null
                ? Results.NotFound(new { error = "Job nije pronađen." })
                : Results.Ok(ToResponse(snap, http));
        });

        // Izvoz rezultata: junit | trx | html | json — za integraciju u Jenkins/GitLab/Azure DevOps.
        group.MapGet("/job/{jobId:guid}/report/{format}", async (
            Guid jobId, string format, HttpContext http, ICiRunService ci,
            IEnumerable<IRunReportFormatter> formatters, IApiKeyService apiKeys, ILoggerFactory lf) =>
        {
            var auth = await AuthorizeAsync(http, apiKeys, lf.CreateLogger("CiApi"));
            if (auth is not null) return auth;

            if (!ReportFormatSelector.TryResolve(format, formatters, out var fmt, out var formatter))
                return Results.BadRequest(new { error = "Format mora biti: junit, trx, html ili json." });

            var snap = ci.GetStatus(jobId);
            if (snap is null)
                return Results.NotFound(new { error = "Job nije pronađen." });

            var content = formatter.Render(CiReportMapper.ToReport(snap));

            // HTML se prikazuje inline (za pregled/dijeljenje); ostali formati se preuzimaju kao fajl.
            if (fmt != RunReportFormat.Html)
                http.Response.Headers.ContentDisposition = $"attachment; filename=\"{formatter.FileName(jobId)}\"";

            return Results.Text(content, formatter.ContentType);
        });

        // Persistirani izvještaj po runId (RunResult.Id iz baze) — preživljava restart aplikacije.
        group.MapGet("/result/{runId:guid}/report/{format}", async (
            Guid runId, string format, HttpContext http, IRunHistoryService history,
            IEnumerable<IRunReportFormatter> formatters, IApiKeyService apiKeys, ILoggerFactory lf) =>
        {
            var auth = await AuthorizeAsync(http, apiKeys, lf.CreateLogger("CiApi"));
            if (auth is not null) return auth;

            if (!ReportFormatSelector.TryResolve(format, formatters, out var fmt, out var formatter))
                return Results.BadRequest(new { error = "Format mora biti: junit, trx, html ili json." });

            var row = await history.GetRunByIdAsync(runId);
            if (row is null)
                return Results.NotFound(new { error = "Run nije pronađen." });

            var content = formatter.Render(RunReportMapper.FromHistoryRow(row));

            if (fmt != RunReportFormat.Html)
                http.Response.Headers.ContentDisposition = $"attachment; filename=\"{formatter.FileName(runId)}\"";

            return Results.Text(content, formatter.ContentType);
        });

        return app;
    }

    private static async Task<IResult?> AuthorizeAsync(
        HttpContext http, IApiKeyService apiKeys, ILogger log)
    {
        var ip = http.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        var endpoint = $"{http.Request.Method} {http.Request.Path}";

        if (!http.Request.Headers.TryGetValue("X-Api-Key", out var provided) ||
            string.IsNullOrWhiteSpace(provided.ToString()))
        {
            log.LogWarning("API poziv bez X-Api-Key headera: {Endpoint} od {IP}", endpoint, ip);
            return Results.Json(
                new { error = "X-Api-Key header je obavezan." },
                statusCode: StatusCodes.Status401Unauthorized);
        }

        var result = await apiKeys.ValidateAsync(provided.ToString()!, http.RequestAborted);
        var maskedKey = provided.ToString()![..Math.Min(8, provided.ToString()!.Length)] + "...";

        if (!result.IsValid)
        {
            log.LogWarning("Nevalidan API ključ {MaskedKey} na {Endpoint} od {IP}",
                maskedKey, endpoint, ip);
            return Results.Json(
                new { error = "Nevalidan ili istekao API ključ." },
                statusCode: StatusCodes.Status401Unauthorized);
        }

        log.LogInformation("API poziv autorizovan: ključ={MaskedKey} ({KeyName}), endpoint={Endpoint}, IP={IP}",
            maskedKey, result.KeyName, endpoint, ip);
        return null;
    }

    private static async Task<IResult> RespondAsync(Guid jobId, bool? wait, HttpContext http, ICiRunService ci)
    {
        if (wait == true)
        {
            var snap = await ci.WaitForCompletionAsync(jobId, MaxSyncWait, http.RequestAborted);
            return Results.Ok(ToResponse(snap!, http));
        }

        var running = ci.GetStatus(jobId)!;
        return Results.Json(ToResponse(running, http), statusCode: StatusCodes.Status202Accepted);
    }

    private static CiJobStatusResponse ToResponse(CiJobSnapshot s, HttpContext http)
    {
        var statusUrl = $"{http.Request.Scheme}://{http.Request.Host}/api/run/job/{s.JobId}/status";
        return new CiJobStatusResponse(
            s.JobId, s.Status.ToString(), statusUrl,
            s.Total, s.Completed, $"{s.Completed}/{s.Total}",
            s.PassRate, s.FailedTests, s.StartedAt, s.CompletedAt);
    }
}
