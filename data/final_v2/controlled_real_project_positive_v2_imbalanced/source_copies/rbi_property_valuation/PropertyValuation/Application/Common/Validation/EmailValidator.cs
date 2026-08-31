using System.Text.RegularExpressions;
using RBBH.CollateralAppraisal.Application.Common.Models;

namespace RBBH.CollateralAppraisal.Application.Common.Validation;

/// <summary>Validacija formata email adrese (opcionalno polje).</summary>
public static partial class EmailValidator
{
    public static IReadOnlyList<ValidationFieldError> Validate(string? raw, string field = "contactEmail")
    {
        if (string.IsNullOrWhiteSpace(raw))
            return [];

        var value = raw.Trim();

        if (!EmailRegex().IsMatch(value))
            return [new ValidationFieldError(field, ValidationErrorCodes.InvalidEmailFormat,
                "Email adresa nije ispravnog formata.")];

        if (value.Length > 200)
            return [new ValidationFieldError(field, ValidationErrorCodes.MaxLengthExceeded,
                "Email ne smije biti duži od 200 znakova.")];

        return [];
    }

    [GeneratedRegex(@"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")]
    private static partial Regex EmailRegex();
}
