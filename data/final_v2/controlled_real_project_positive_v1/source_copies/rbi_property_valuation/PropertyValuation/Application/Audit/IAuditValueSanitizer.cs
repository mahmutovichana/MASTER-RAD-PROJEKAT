namespace RBBH.CollateralAppraisal.Application.Audit;

/// <summary>
/// Sanitizira osjetljive vrijednosti iz audit podataka prije serijalizacije i upisa.
/// Implementira se u Infrastructure sloju.
///
/// Implementacija prima <c>object?</c> (originalni C# objekat),
/// serijalizuje ga u JSON, uklanja/maskira osjetljiva polja i vraća
/// sanitizovani JSON string (ili null ako je input null).
///
/// Polja koja se maskiraju: password, token, refreshToken, secret,
/// apiKey, clientSecret, connectionString, authorizationHeader.
/// </summary>
public interface IAuditValueSanitizer
{
    /// <param name="value">Originalni C# objekat ili null.</param>
    /// <returns>Sanitizovani JSON string, ili null ako je <paramref name="value"/> null.</returns>
    string? Sanitize(object? value);
}
