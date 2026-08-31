namespace RBBH.TestAutomation.Api.Validators;

public static class JmbgValidator
{
    public static IEnumerable<string> Validate(string? value, bool required = true)
    {
        if (string.IsNullOrWhiteSpace(value))
        {
            if (required)
            {
                yield return "JMBG je obavezan.";
            }

            yield break;
        }

        var normalized = value.Trim();

        if (!normalized.All(char.IsDigit))
        {
            yield return "JMBG smije sadržavati samo cifre.";
            yield break;
        }

        if (normalized.Length != 13)
        {
            yield return "JMBG mora imati tačno 13 cifara.";
            yield break;
        }

        if (!IsChecksumValid(normalized))
        {
            yield return "JMBG nije ispravan.";
        }
    }

    public static bool IsValid(string? value, bool required = true)
    {
        return !Validate(value, required).Any();
    }

    private static bool IsChecksumValid(string jmbg)
    {
        var digits = jmbg.Select(c => c - '0').ToArray();

        var remainder =
            (
                7 * (digits[0] + digits[6])
                + 6 * (digits[1] + digits[7])
                + 5 * (digits[2] + digits[8])
                + 4 * (digits[3] + digits[9])
                + 3 * (digits[4] + digits[10])
                + 2 * (digits[5] + digits[11])
            )
            % 11;

        var checksum = 11 - remainder;

        if (checksum == 10)
        {
            return false;
        }

        if (checksum == 11)
        {
            checksum = 0;
        }

        return digits[12] == checksum;
    }
}
