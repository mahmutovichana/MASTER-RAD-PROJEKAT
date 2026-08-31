namespace RBBH.TestAutomation.Api.Auth;

/// <summary>
/// Centralne korisničke poruke za auth flow.
/// Poruke prijave/lockout-a dolaze iz Keycloak teme (messages_en.properties).
/// </summary>
public static class AuthErrorMessages
{
    /// <summary>
    /// Prikazuje se na /access-denied kada autentificiran korisnik nema
    /// potrebnu rolu za pristup stranici.
    /// </summary>
    public const string AccessDenied =
        "Nemate pravo pristupa ovoj stranici. Ako mislite da je ovo greška, kontaktirajte administratora.";

    /// <summary>
    /// Prikazuje se na /greska-prijave kada OIDC prijava ne uspije na protokolarnom nivou
    /// (npr. korisnik odbije pristanak, istekla/nevažeća sesija, state mismatch).
    /// </summary>
    public const string LoginFailed =
        "Prijava nije uspjela. Pokušajte ponovo, a ako se problem ponavlja kontaktirajte administratora.";
}
