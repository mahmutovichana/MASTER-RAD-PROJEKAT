using RBBH.CollateralAppraisal.Application.Common.Models;

namespace RBBH.CollateralAppraisal.Application.Common.Exceptions;

/// <summary>
/// Validacijska greška — baca se kada unos ne ispunjava pravila.
/// Mapira se na 400 Bad Request u GlobalExceptionHandler-u.
///
/// Preporučeni konstruktor za nove validatore: ValidationException(IReadOnlyList&lt;ValidationFieldError&gt;)
/// Stariji konstruktori ostavljeni za backward compatibility.
/// </summary>
public class ValidationException : Exception
{
    /// <summary>Stari format: field → poruke[]. Backward compatibility.</summary>
    public IDictionary<string, string[]> Errors { get; }

    /// <summary>
    /// Novi format: lista grešaka po poljima s code i message.
    /// Ako postoji, GlobalExceptionHandler šalje "fieldErrors" umjesto "errors".
    /// </summary>
    public IReadOnlyList<ValidationFieldError>? FieldErrors { get; }

    public ValidationException()
        : base("One or more validation failures have occurred.")
    {
        Errors = new Dictionary<string, string[]>();
    }

    public ValidationException(IDictionary<string, string[]> errors)
        : base("One or more validation failures have occurred.")
    {
        Errors = errors;
    }

    public ValidationException(string field, string error)
        : base("One or more validation failures have occurred.")
    {
        Errors = new Dictionary<string, string[]> { { field, [error] } };
    }

    /// <summary>
    /// Preporučeni konstruktor za strukturirane greške s error codom po polju.
    /// Primjer:
    /// throw new ValidationException([
    ///     new ValidationFieldError("jmbg", ValidationErrorCodes.InvalidJmbgFormat,
    ///         "JMBG mora sadržavati tačno 13 cifara.")
    /// ]);
    /// </summary>
    public ValidationException(IReadOnlyList<ValidationFieldError> fieldErrors)
        : base("One or more validation failures have occurred.")
    {
        Errors      = new Dictionary<string, string[]>();
        FieldErrors = fieldErrors;
    }
}
