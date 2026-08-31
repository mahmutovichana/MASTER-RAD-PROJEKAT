using MudBlazor;

namespace RBBH.TestAutomation.Api.Services;

/// <summary>
/// Tanki wrapper nad ISnackbar — osigurava konzistentno trajanje i poziciju toast poruka u cijeloj aplikaciji.
/// Success: 3s, Warning: 5s, Error: ostaje dok korisnik ne zatvori.
/// </summary>
public sealed class ToastService(ISnackbar snackbar)
{
    public void Success(string message) =>
        snackbar.Add(message, Severity.Success, cfg => cfg.VisibleStateDuration = 3000);

    public void Info(string message) =>
        snackbar.Add(message, Severity.Info, cfg => cfg.VisibleStateDuration = 4000);

    public void Warning(string message) =>
        snackbar.Add(message, Severity.Warning, cfg => cfg.VisibleStateDuration = 5000);

    public void Error(string message) =>
        snackbar.Add(message, Severity.Error, cfg =>
        {
            cfg.VisibleStateDuration = int.MaxValue;
            cfg.ShowCloseIcon = true;
        });
}
