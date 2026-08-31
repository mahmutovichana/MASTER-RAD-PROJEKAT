namespace RBBH.CollateralAppraisal.Infrastructure.Auth;

/// <summary>
/// Konfiguracija za Keycloak Admin REST API.
/// Primarni pristup: client_credentials (service account) — zahtijeva manage-realm rolu na service accountu.
/// Koristi isključivo client_credentials service account tok.
/// Secretove i lozinke postaviti putem environment varijabli — NIKADA ne hardkodovati!
/// </summary>
[System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage]
public class KeycloakAdminOptions
{
    public const string SectionName = "KeycloakAdmin";

    public string BaseUrl { get; set; } = string.Empty;
    public string Realm { get; set; } = string.Empty;
    public string ClientId { get; init; } = string.Empty;
    public string ClientSecret { get; init; } = string.Empty;

}
