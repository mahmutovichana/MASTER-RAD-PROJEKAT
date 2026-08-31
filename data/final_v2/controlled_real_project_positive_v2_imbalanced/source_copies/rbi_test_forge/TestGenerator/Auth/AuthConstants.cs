namespace RBBH.TestAutomation.Api.Auth;

/// <summary>
/// Konstante vezane za autentikaciju.
/// </summary>
public static class AuthConstants
{
    /// <summary>
    /// Period neaktivnosti (minute) nakon kojeg se korisnik automatski odjavljuje.
    /// Klijentski idle timer (JS interop) — defense in depth uz Keycloak SSO Session Idle.
    /// </summary>
    public const int IdleTimeoutMinutes = 30;
}
