using Microsoft.Extensions.Diagnostics.HealthChecks;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Options;
using RBBH.CollateralAppraisal.Infrastructure.Storage;

namespace RBBH.CollateralAppraisal.Api.Middleware;

public sealed class FileStorageHealthCheck : IHealthCheck
{
    private readonly string _rootPath;
    private readonly long   _maxFileSizeBytes;

    public FileStorageHealthCheck(IOptions<FileStorageOptions> options, IHostEnvironment env)
    {
        var configured = options.Value.RootPath;
        _rootPath = Path.IsPathRooted(configured)
            ? configured
            : Path.Combine(env.ContentRootPath, configured);
        _maxFileSizeBytes = options.Value.MaxFileSizeBytes;
    }

    public Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context, CancellationToken ct = default)
    {
        if (!Directory.Exists(_rootPath))
            return Task.FromResult(HealthCheckResult.Unhealthy(
                $"Direktorij za skladišenje ne postoji: {_rootPath}"));

        try
        {
            var testFile = Path.Combine(_rootPath, $".hc-{Guid.NewGuid():N}");
            File.WriteAllText(testFile, "ok");
            File.Delete(testFile);
        }
        catch (Exception ex)
        {
            return Task.FromResult(HealthCheckResult.Unhealthy("Skladište nije zapisivo.", ex));
        }

        try
        {
            var drive  = new DriveInfo(Path.GetPathRoot(_rootPath) ?? _rootPath);
            var freeGb = drive.AvailableFreeSpace / (1024.0 * 1024 * 1024);
            var maxMb  = _maxFileSizeBytes / (1024 * 1024);

            return Task.FromResult(freeGb < 1.0
                ? HealthCheckResult.Degraded($"Malo slobodnog prostora: {freeGb:F1} GB. Max fajl: {maxMb} MB.")
                : HealthCheckResult.Healthy($"Skladište OK. Slobodno: {freeGb:F1} GB. Max fajl: {maxMb} MB."));
        }
        catch
        {
            return Task.FromResult(HealthCheckResult.Healthy("Skladište OK (provjera diska nije uspjela)."));
        }
    }
}
