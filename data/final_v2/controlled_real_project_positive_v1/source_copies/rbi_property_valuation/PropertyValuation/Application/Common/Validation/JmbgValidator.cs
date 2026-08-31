using RBBH.CollateralAppraisal.Application.Common.Models;

namespace RBBH.CollateralAppraisal.Application.Common.Validation;

/// <summary>
/// Validacija JMBG-a (Jedinstveni matični broj građana).
/// Format: DDMMYYYRRBBBK — tačno 13 cifara, bez razmaka ili crtica.
/// Godišnji dio YYY: ≥900 → 1000+YYY (1900-1999), &lt;900 → 2000+YYY.
/// Kontrolna cifra: m = 11 − ((7(a+g)+6(b+h)+5(c+i)+4(d+j)+3(e+k)+2(f+l)) mod 11).
/// m=11 → K=0; m=10 → nema valjane K → JMBG nije validan.
/// </summary>
public static class JmbgValidator
{
    public static IReadOnlyList<ValidationFieldError> Validate(string? raw, string field = "jmbg")
    {
        if (string.IsNullOrWhiteSpace(raw))
            return [new(field, ValidationErrorCodes.RequiredJmbg, "JMBG je obavezan.")];

        var v = raw.Trim();

        if (!v.All(char.IsDigit))
            return [new(field, ValidationErrorCodes.InvalidJmbgDigitsOnly,
                "JMBG smije sadržavati samo cifre.")];

        if (v.Length != 13)
            return [new(field, ValidationErrorCodes.InvalidJmbgLength,
                "JMBG mora sadržavati tačno 13 cifara.")];

        var d = new int[13];
        for (var i = 0; i < 13; i++) d[i] = v[i] - '0';

        int day   = d[0] * 10 + d[1];
        int month = d[2] * 10 + d[3];
        int yyy   = d[4] * 100 + d[5] * 10 + d[6];
        int year  = yyy >= 900 ? 1000 + yyy : 2000 + yyy;

        if (!IsValidBirthDate(day, month, year))
            return [new(field, ValidationErrorCodes.InvalidJmbgDatePart,
                "Datum rođenja u JMBG-u nije validan.")];

        int sum = 7 * (d[0] + d[6]) + 6 * (d[1] + d[7]) +
                  5 * (d[2] + d[8]) + 4 * (d[3] + d[9]) +
                  3 * (d[4] + d[10]) + 2 * (d[5] + d[11]);
        int m = 11 - (sum % 11);

        if (m == 10 || (m == 11 ? 0 : m) != d[12])
            return [new(field, ValidationErrorCodes.InvalidJmbgChecksum,
                "Kontrolna cifra JMBG-a nije ispravna.")];

        return [];
    }

    private static bool IsValidBirthDate(int day, int month, int year)
    {
        if (year < 1900 || year > DateTime.UtcNow.Year) return false;
        try { _ = new DateTime(year, month, day); return true; }
        catch { return false; }
    }
}
