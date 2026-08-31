namespace RBBH.CollateralAppraisal.Application.Common.Models;

/// <summary>
/// Greška vezana za jedno polje u validacijskom odgovoru.
/// Koristi se u ValidationException.FieldErrors i serijalizuje kao "fieldErrors" u ProblemDetails response-u.
///
/// Primjer JSON:
/// { "field": "jmbg", "code": "INVALID_JMBG_FORMAT", "message": "JMBG mora sadržavati tačno 13 cifara." }
/// </summary>
/// <param name="Field">Naziv polja (camelCase, npr. "jmbg", "poreznibroj", "ime").</param>
/// <param name="Code">Stabilan error code za mapiranje na frontend. Koristiti konstante iz ValidationErrorCodes.</param>
/// <param name="Message">Poruka za prikaz korisniku (na jeziku projekta).</param>
public sealed record ValidationFieldError(
    string Field,
    string Code,
    string Message
);
