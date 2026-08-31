using System.Text.RegularExpressions;
using RBBH.CollateralAppraisal.Application.Common.Models;

namespace RBBH.CollateralAppraisal.Application.Common.Validation;

/// <summary>
/// Validacija telefonskog broja (BiH format).
/// Prihvata: +387XXXXXXXX ili 0XXXXXXXX (9 cifara nakon vodeće nule).
/// Razmaci, crtice i zagrade se uklanjaju prije provjere.
/// </summary>
public static partial class PhoneNumberValidator
{
    public static IReadOnlyList<ValidationFieldError> Validate(string? raw, string field = "contactPhone")
    {
        if (string.IsNullOrWhiteSpace(raw))
            return [new ValidationFieldError(field, ValidationErrorCodes.RequiredField,
                "Telefon je obavezan.")];

        var normalized = NormalizeChars().Replace(raw.Trim(), "");

        if (!PhoneRegex().IsMatch(normalized))
            return [new ValidationFieldError(field, ValidationErrorCodes.InvalidPhoneFormat,
                "Neispravan format telefonskog broja.")];

        return [];
    }

    /// <summary>Uklanja razmake, crtice i zagrade (zadržava cifre i vodeći '+').</summary>
    [GeneratedRegex(@"[\s\-\(\)]")]
    private static partial Regex NormalizeChars();

    [GeneratedRegex(@"^(?:\+387|0)\d{8}$")]
    private static partial Regex PhoneRegex();
}
