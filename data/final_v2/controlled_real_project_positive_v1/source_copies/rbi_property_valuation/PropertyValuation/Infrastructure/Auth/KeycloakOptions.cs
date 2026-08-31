namespace RBBH.CollateralAppraisal.Infrastructure.Auth;

/// <summary>
/// Konfiguracija za Keycloak JWT autentifikaciju.
/// Popuniti putem appsettings.json ili environment varijabli.
/// </summary>
[System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage]
public class KeycloakOptions
{
    public const string SectionName = "Keycloak";

    public bool Enabled { get; init; }

    // Vrijednosti se postavljaju u appsettings.Development.json (dev) ili environment varijablama (prod).
    // NIKADA ne hardkodovati secrets!
    public string Authority { get; init; } = string.Empty;
    public string Audience { get; init; } = string.Empty;
    public bool RequireHttpsMetadata { get; init; } = true;

    /// <summary>
    /// Dodatni validni issueri pored <see cref="Authority"/>.
    /// Keycloak iza split URL-a (browser=localhost, server=keycloak) izdaje tokene
    /// sa različitim "iss" zavisno od ulazne tačke; ovdje se navode svi prihvatljivi.
    /// </summary>
    public string[] ValidIssuers { get; init; } = [];
}
