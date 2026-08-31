using System.Diagnostics;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace E2ETests.Fixtures;

public sealed class AppFixture : IAsyncLifetime
{
    private Process? _apiProcess;
    private Process? _webProcess;
    private readonly StringBuilder _output = new();
    public string BaseUrl { get; private set; } = "";
    public string ApiBaseUrl { get; private set; } = "";

    public async Task InitializeAsync()
    {
        var root = FindRepositoryRoot();
        var apiPort = GetFreePort();
        var webPort = GetFreePort();
        ApiBaseUrl = $"http://127.0.0.1:{apiPort}";
        BaseUrl = $"http://127.0.0.1:{webPort}";

        _apiProcess = Start("dotnet", Path.Combine(root, "TestGenerator"),
            ["run", "--project", "TestGenerator.csproj", "--no-launch-profile", "--no-restore"],
            new Dictionary<string, string>
            {
                ["ASPNETCORE_URLS"] = ApiBaseUrl,
                ["ASPNETCORE_ENVIRONMENT"] = "Development",
                ["DOTNET_ENVIRONMENT"] = "Development",
                ["MockAuth__Enabled"] = "true",
                ["MockAuth__ActiveUser"] = "qaengineer1"
            });
        await WaitForReady($"{ApiBaseUrl}/health/live", TimeSpan.FromSeconds(120), _apiProcess);

        _webProcess = Start("cmd.exe", Path.Combine(root, "src", "Web"),
            ["/d", "/s", "/c", "pnpm.cmd dev"],
            new Dictionary<string, string>
            {
                ["WEB_PORT"] = webPort.ToString(),
                ["API_PROXY_TARGET"] = ApiBaseUrl
            });
        await WaitForReady(BaseUrl, TimeSpan.FromSeconds(120), _webProcess);
    }

    public Task DisposeAsync()
    {
        Stop(_webProcess); Stop(_apiProcess); return Task.CompletedTask;
    }

    private Process Start(string command, string workingDirectory, IReadOnlyList<string> arguments, IReadOnlyDictionary<string, string> environment)
    {
        var process = new Process { StartInfo = new ProcessStartInfo(command) { WorkingDirectory = workingDirectory, RedirectStandardOutput = true, RedirectStandardError = true, UseShellExecute = false } };
        foreach (var argument in arguments) process.StartInfo.ArgumentList.Add(argument);
        foreach (var (key, value) in environment) process.StartInfo.Environment[key] = value;
        process.OutputDataReceived += (_, e) => { if (e.Data is not null) _output.AppendLine(e.Data); };
        process.ErrorDataReceived += (_, e) => { if (e.Data is not null) _output.AppendLine(e.Data); };
        process.Start(); process.BeginOutputReadLine(); process.BeginErrorReadLine(); return process;
    }

    private async Task WaitForReady(string url, TimeSpan timeout, Process process)
    {
        using var http = new HttpClient(new HttpClientHandler { AllowAutoRedirect = false });
        var deadline = DateTime.UtcNow + timeout;
        while (DateTime.UtcNow < deadline)
        {
            if (process.HasExited) throw new InvalidOperationException($"Proces je završen kodom {process.ExitCode}.\n{_output}");
            try { if ((await http.GetAsync(url)).StatusCode is >= HttpStatusCode.OK and < HttpStatusCode.BadRequest) return; } catch { }
            await Task.Delay(500);
        }
        throw new TimeoutException($"Aplikacija nije spremna na {url}.\n{_output}");
    }

    private static void Stop(Process? process)
    {
        if (process is { HasExited: false }) { process.Kill(entireProcessTree: true); process.WaitForExit(5000); }
        process?.Dispose();
    }

    private static int GetFreePort()
    {
        using var listener = new TcpListener(IPAddress.Loopback, 0); listener.Start();
        var port = ((IPEndPoint)listener.LocalEndpoint).Port; listener.Stop(); return port;
    }

    private static string FindRepositoryRoot()
    {
        var directory = new DirectoryInfo(AppContext.BaseDirectory);
        while (directory is not null)
        {
            if (File.Exists(Path.Combine(directory.FullName, "TestGenerator", "TestGenerator.csproj"))) return directory.FullName;
            directory = directory.Parent;
        }
        throw new InvalidOperationException($"Nije pronađen korijen repozitorija iz {AppContext.BaseDirectory}.");
    }
}
