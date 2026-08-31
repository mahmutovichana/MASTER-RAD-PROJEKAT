using System.Diagnostics;
using System.Text;
using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Api.Services.Scenarios;

namespace RBBH.TestAutomation.Api.Services.Run;

/// <summary>
/// Izvrsava test scenarije uzivo iz aplikacije (HTTP) i vraca prolaz/pad.
/// </summary>
public interface IScenarioRunner
{
    Task<ScenarioRunResult> RunAsync(ScenarioDto scenario, RunConfigDto config, CancellationToken ct = default);
}

public sealed class ScenarioRunner(IHttpClientFactory httpFactory) : IScenarioRunner
{
    public async Task<ScenarioRunResult> RunAsync(
        ScenarioDto scenario, RunConfigDto config, CancellationToken ct = default)
    {
        if (scenario.Tip != TipScenarija.Rest || scenario.Rest is null)
            return new ScenarioRunResult(scenario.Id, scenario.Naziv, ScenarioRunStatus.Skipped,
                null, null, 0, "UI scenariji se jos ne izvrsavaju iz aplikacije.", null, null);

        var rest = scenario.Rest;
        var sw = Stopwatch.StartNew();
        string? requestDetails = null;

        try
        {
            using var client = httpFactory.CreateClient("ScenarioRunner");
            using var request = BuildRequest(rest, config);
            requestDetails = BuildRequestDetails(request);
            using var response = await client.SendAsync(request, ct);
            sw.Stop();

            var actual = (int)response.StatusCode;
            var body = await response.Content.ReadAsStringAsync(ct);
            var responseDetails = $"HTTP {actual}\n{TrimForStorage(body)}";

            if (actual != rest.OcekivaniStatus)
                return Fail(scenario, actual, rest.OcekivaniStatus, sw.ElapsedMilliseconds,
                    $"Ocekivan status {rest.OcekivaniStatus}, dobijen {actual}.", requestDetails, responseDetails);

            foreach (var a in rest.ResponseAsserti)
            {
                if (!JsonPathEvaluator.TryEvaluate(body, a.JsonPutanja, out var value))
                    return Fail(scenario, actual, rest.OcekivaniStatus, sw.ElapsedMilliseconds,
                        $"Putanja '{a.JsonPutanja}' nije pronadjena u odgovoru.", requestDetails, responseDetails);

                if (!string.Equals(value, a.OcekivanaVrijednost, StringComparison.Ordinal))
                    return Fail(scenario, actual, rest.OcekivaniStatus, sw.ElapsedMilliseconds,
                        $"'{a.JsonPutanja}': ocekivano '{a.OcekivanaVrijednost}', dobijeno '{value}'.",
                        requestDetails, responseDetails);
            }

            return new ScenarioRunResult(scenario.Id, scenario.Naziv, ScenarioRunStatus.Passed,
                actual, rest.OcekivaniStatus, sw.ElapsedMilliseconds, null, requestDetails, responseDetails);
        }
        catch (OperationCanceledException)
        {
            throw;
        }
        catch (Exception ex)
        {
            sw.Stop();
            return Fail(scenario, null, rest.OcekivaniStatus, sw.ElapsedMilliseconds,
                $"Greska pri izvrsavanju: {ex.Message}",
                requestDetails,
                $"HTTP response nije primljen.\n{ex.GetType().Name}: {ex.Message}");
        }
    }

    private static ScenarioRunResult Fail(
        ScenarioDto s, int? actual, int expected, long ms, string reason, string? request, string? response) =>
        new(s.Id, s.Naziv, ScenarioRunStatus.Failed, actual, expected, ms, reason, request, response);

    private static HttpRequestMessage BuildRequest(RestScenarioDto rest, RunConfigDto config)
    {
        var url = ScenarioVariableResolver.Resolve(rest.Url, config);

        var method = rest.Metoda switch
        {
            HttpMetoda.Get    => HttpMethod.Get,
            HttpMetoda.Post   => HttpMethod.Post,
            HttpMetoda.Put    => HttpMethod.Put,
            HttpMetoda.Patch  => HttpMethod.Patch,
            HttpMetoda.Delete => HttpMethod.Delete,
            _                 => HttpMethod.Get,
        };

        var request = new HttpRequestMessage(method, url);

        string? contentType = null;
        var requestHeaders = new List<HeaderDto>();
        foreach (var h in rest.Headeri)
        {
            var val = ScenarioVariableResolver.Resolve(h.Vrijednost, config);
            if (string.Equals(h.Kljuc, "Content-Type", StringComparison.OrdinalIgnoreCase))
                contentType = val;
            else
                requestHeaders.Add(new HeaderDto(h.Kljuc, val));
        }

        if (rest.RequestBody is not null)
            request.Content = new StringContent(
                ScenarioVariableResolver.Resolve(rest.RequestBody, config),
                Encoding.UTF8,
                contentType ?? "application/json");

        foreach (var h in requestHeaders)
            request.Headers.TryAddWithoutValidation(h.Kljuc, h.Vrijednost);

        return request;
    }

    private static string BuildRequestDetails(HttpRequestMessage request)
    {
        var body = request.Content is null ? "" : request.Content.ReadAsStringAsync().GetAwaiter().GetResult();
        return $"{request.Method} {request.RequestUri}\n{TrimForStorage(body)}";
    }

    private static string TrimForStorage(string value)
    {
        const int max = 4000;
        return value.Length <= max ? value : value[..max] + "\n... skraceno ...";
    }
}
