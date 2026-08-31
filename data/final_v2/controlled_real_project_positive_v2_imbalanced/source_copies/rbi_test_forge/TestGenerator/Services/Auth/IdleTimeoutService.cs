namespace RBBH.TestAutomation.Api.Services.Auth;

/// <summary>
/// Per-circuit timer koji prati zadnju korisničku aktivnost.
///
/// Registracija: Scoped — jedna instanca po SignalR konekciji (korisničkoj sesiji),
/// jer idle timeout je vezan za konkretan circuit, ne globalno.
///
/// Tok: MainLayout pozove Start() pri prvom renderu i RecordActivity() na svaki
/// korisnički događaj koji stigne iz JS-a (mousedown/keydown/scroll). Ako prođe
/// <c>timeout</c> bez aktivnosti → izvrši se onTimeout callback (logout).
///
/// Ograničenje: ako padne SignalR konekcija ili JS interop, timer ne radi —
/// zato je dopuna Keycloak server-side SSO Session Idle (defense in depth).
/// </summary>
public sealed class IdleTimeoutService : IDisposable
{
    private Timer? _timer;
    private Func<Task>? _onTimeout;
    private TimeSpan _timeout;

    /// <summary>
    /// Pokreće idle timer. onTimeout se poziva kada istekne period bez aktivnosti.
    /// </summary>
    public void Start(TimeSpan timeout, Func<Task> onTimeout)
    {
        _timeout = timeout;
        _onTimeout = onTimeout;
        ResetTimer();
    }

    /// <summary>Poziva se iz JS-a (preko [JSInvokable]) pri svakom korisničkom događaju.</summary>
    public void RecordActivity() => ResetTimer();

    private void ResetTimer()
    {
        if (_onTimeout is null) return;

        _timer?.Dispose();
        _timer = new Timer(async _ =>
        {
            // Timer callback je async void — neuhvaćen izuzetak iz onTimeout (npr. logout
            // nad zatvorenim circuitom) bi inače bio neobservan i mogao srušiti proces.
            // Server-side Keycloak SSO Session Idle je backstop, pa je sigurno progutati.
            try
            {
                if (_onTimeout is { } onTimeout)
                    await onTimeout();
            }
            catch
            {
                // namjerno progutano — vidi komentar iznad (defense in depth)
            }
        }, null, _timeout, Timeout.InfiniteTimeSpan);
    }

    public void Dispose() => _timer?.Dispose();
}
