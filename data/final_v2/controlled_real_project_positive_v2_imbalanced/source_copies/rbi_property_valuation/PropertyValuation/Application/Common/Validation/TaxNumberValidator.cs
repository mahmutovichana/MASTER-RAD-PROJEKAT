using RBBH.CollateralAppraisal.Application.Common.Models;

namespace RBBH.CollateralAppraisal.Application.Common.Validation;

/// <summary>
/// Validacija poreznog identifikacionog broja (PIB).
/// Pravila: tačno 13 cifara, samo numerički znakovi.
/// Stripa razmake i crtice prije provjere.
/// </summary>
public static class TaxNumberValidator
{
    public static IReadOnlyList<ValidationFieldError> Validate(string? raw, string field = "poreznibroj")
    {
        if (string.IsNullOrWhiteSpace(raw))
            return [new ValidationFieldError(field, ValidationErrorCodes.RequiredTaxNumber,
                "Porezni identifikacioni broj je obavezan.")];

        var value = raw.Replace(" ", "").Replace("-", "");

        if (value.Length != 13)
            return [new ValidationFieldError(field, ValidationErrorCodes.InvalidTaxNumberLength,
                "Porezni identifikacioni broj mora sadržavati tačno 13 cifara.")];

        if (!value.All(char.IsDigit))
            return [new ValidationFieldError(field, ValidationErrorCodes.InvalidTaxNumberDigitsOnly,
                "Porezni identifikacioni broj smije sadržavati samo cifre.")];

        return [];
    }
}
