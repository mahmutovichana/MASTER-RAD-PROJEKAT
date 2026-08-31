using Xunit.Abstractions;

namespace RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;

/// <summary>
/// Loguje poslovne korake testa sa vremenskim žigom i rednim brojem.
/// U DEMO_MODE dodaje kratke pauze između glavnih koraka (300-700ms)
/// da bi prezentacija bila praćljiva.
///
/// Aktivacija: E2E_DEMO_MODE=1 environment varijabla.
/// </summary>
public sealed class DemoLogger
{
    public static bool IsDemoMode =>
        Environment.GetEnvironmentVariable("E2E_DEMO_MODE") == "1";

    private readonly ITestOutputHelper? _out;
    private readonly int _totalSteps;
    private int _step;
    private DateTime _start;

    public DemoLogger(ITestOutputHelper? output, int totalSteps = 12)
    {
        _out        = output;
        _totalSteps = totalSteps;
        _start      = DateTime.Now;
    }

    public async Task StepAsync(string businessStep, int? stepNumber = null)
    {
        _step++;
        var num     = stepNumber ?? _step;
        var elapsed = (DateTime.Now - _start).TotalSeconds;
        var msg     = $"[{num:D2}/{_totalSteps}] {businessStep}  ({elapsed:F1}s)";

        _out?.WriteLine(msg);
        Console.WriteLine(msg);

        if (IsDemoMode)
            await Task.Delay(GetDemoDelay(num));
    }

    public void Warn(string message)
    {
        var msg = $"  ⚠️  {message}";
        _out?.WriteLine(msg);
        Console.WriteLine(msg);
    }

    public void Info(string message)
    {
        var msg = $"     {message}";
        _out?.WriteLine(msg);
        Console.WriteLine(msg);
    }

    public void NotImplemented(string feature, string workaround)
    {
        var msg = $"  [NOT_IMPLEMENTED] {feature}";
        var wk  = $"  [WORKAROUND]      {workaround}";
        _out?.WriteLine(msg);
        _out?.WriteLine(wk);
        Console.WriteLine(msg);
        Console.WriteLine(wk);
    }

    public void Todo(string item)
    {
        var msg = $"  [TODO] {item}";
        _out?.WriteLine(msg);
        Console.WriteLine(msg);
    }

    public void Assert(string what, string value)
    {
        var msg = $"  ✓ {what}: {value}";
        _out?.WriteLine(msg);
        Console.WriteLine(msg);
    }

    private static int GetDemoDelay(int step)
    {
        // Počeci uloga imaju malo duže pauze za "prijelaz scene"
        return step switch
        {
            1 or 4 or 7 or 10 => 700,
            _ => 400
        };
    }
}
