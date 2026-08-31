namespace RBBH.TestAutomation.Api.Auth;

/// <summary>
/// Konstante vezane za Keycloak OIDC autentikaciju.
/// </summary>
public static class AuthOptions
{
    /// <summary>
    /// Naziv OIDC authentication sheme. Dijeli ga Program.cs (AddOpenIdConnect),
    /// CookieOidcRefresh konfiguracija i RequestMessageHandler.
    /// </summary>
    public const string OidcScheme = "MicrosoftOidc";
}
