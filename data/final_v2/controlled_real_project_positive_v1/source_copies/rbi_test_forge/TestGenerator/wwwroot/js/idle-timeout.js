// Idle timeout — sluša korisničke događaje i javlja .NET-u.
// MainLayout poziva idleTimeout.start(dotNetRef) pri prvom renderu i
// idleTimeout.stop() pri dispose-u. Debounce sprječava previše interop poziva.
window.idleTimeout = (function () {
    let dotNetRef = null;
    let debounceTimer = null;

    const events = ['mousedown', 'keydown', 'scroll', 'touchstart'];

    function onActivity() {
        // Debounce: najviše 1 poziv prema .NET-u po sekundi.
        if (debounceTimer) clearTimeout(debounceTimer);
        debounceTimer = setTimeout(function () {
            if (dotNetRef) {
                dotNetRef.invokeMethodAsync('OnUserActivity');
            }
        }, 1000);
    }

    return {
        start: function (dotNetReference) {
            dotNetRef = dotNetReference;
            events.forEach(function (evt) {
                document.addEventListener(evt, onActivity, { passive: true });
            });
        },
        stop: function () {
            dotNetRef = null;
            if (debounceTimer) clearTimeout(debounceTimer);
            events.forEach(function (evt) {
                document.removeEventListener(evt, onActivity);
            });
        }
    };
})();
