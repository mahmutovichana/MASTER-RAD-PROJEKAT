using RBBH.CollateralAppraisal.Application.Common.Models;

namespace RBBH.CollateralAppraisal.Application.Common.Validation;

/// <summary>
/// Validacija naziva klijenta — razlikuje FL (fizičko lice, PersonNameValidator)
/// od PL (pravno lice, slobodniji format bez opasnih znakova).
///
/// Premješteno iz Infrastructure u Application da bi se koristilo direktno
/// u FluentValidation validatorima, eliminišući duplikaciju u servisima.
/// </summary>
public static class OrderClientNameValidator
{
    public static IReadOnlyList<ValidationFieldError> Validate(
        string? clientName, string? clientType, string field = "clientName")
    {
        if (clientType == "FL")
            return PersonNameValidator.Validate(clientName, field);

        if (string.IsNullOrWhiteSpace(clientName))
            return [new ValidationFieldError(field, ValidationErrorCodes.RequiredField,
                "Naziv firme je obavezan.")];

        var trimmed = clientName.Trim();
        if (trimmed.Length < 2 || trimmed.Length > 300)
            return [new ValidationFieldError(field, ValidationErrorCodes.InvalidFormat,
                "Naziv firme mora biti između 2 i 300 znakova.")];

        if (ContainsDangerousChars(trimmed))
            return [new ValidationFieldError(field, ValidationErrorCodes.InvalidCharacters,
                "Naziv firme sadrži nedozvoljene znakove (< > & \" ').")];

        return [];
    }

    /// <summary>Provjerava prisutnost XSS-opasnih znakova u slobodnom tekstu.</summary>
    public static bool ContainsDangerousChars(string s) =>
        s.Contains('<') || s.Contains('>') || s.Contains('&') ||
        s.Contains('"') || s.Contains('\'');
}
