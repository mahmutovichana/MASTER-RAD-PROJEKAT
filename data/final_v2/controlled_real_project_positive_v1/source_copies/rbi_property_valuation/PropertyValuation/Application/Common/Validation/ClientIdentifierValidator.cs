using RBBH.CollateralAppraisal.Application.Common.Models;

namespace RBBH.CollateralAppraisal.Application.Common.Validation;

/// <summary>
/// Validacija identifikacionog broja klijenta. Prema specifikaciji, JMBG (13 cifara)
/// se traži uniformno i za fizička (FL) i za pravna lica (PL).
/// Delegira na <see cref="JmbgValidator"/> za potpunu validaciju (format, datum, kontrolna cifra).
/// </summary>
public static class ClientIdentifierValidator
{
    public static IReadOnlyList<ValidationFieldError> Validate(
        string? raw, string? clientType, string field = "clientIdentifier")
        => JmbgValidator.Validate(raw, field);
}
