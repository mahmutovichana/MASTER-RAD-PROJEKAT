using System.Text.RegularExpressions;
using RBBH.CollateralAppraisal.Application.Common.Models;

namespace RBBH.CollateralAppraisal.Application.Common.Validation;

/// <summary>
/// Validacija imena fizičkog lica (Ime i prezime, kontakt osoba).
/// Dozvoljeno: Unicode slova (uključujući BCS digrafe Š,Đ,Č,Ć,Ž), razmaci i crtice.
/// Zabranjeno: cifre, specijalni znakovi, emoji.
/// </summary>
public static partial class PersonNameValidator
{
    public static IReadOnlyList<ValidationFieldError> Validate(
        string? raw, string field, int minLength = 2, int maxLength = 300)
    {
        if (string.IsNullOrWhiteSpace(raw))
            return [new ValidationFieldError(field, ValidationErrorCodes.RequiredField,
                "Ime je obavezno.")];

        var value = raw.Trim();

        if (value.Length < minLength || value.Length > maxLength)
            return [new ValidationFieldError(field, ValidationErrorCodes.InvalidFormat,
                $"Unos mora biti od {minLength} do {maxLength} znakova.")];

        if (!NameRegex().IsMatch(value))
            return [new ValidationFieldError(field, ValidationErrorCodes.InvalidNameFormat,
                "Ime smije sadržavati samo slova, razmake i crtice.")];

        return [];
    }

    [GeneratedRegex(@"^[\p{L}\s\-]+$")]
    private static partial Regex NameRegex();
}
