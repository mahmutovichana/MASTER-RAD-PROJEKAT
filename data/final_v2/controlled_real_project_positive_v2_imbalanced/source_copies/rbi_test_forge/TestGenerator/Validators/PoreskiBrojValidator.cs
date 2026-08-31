namespace RBBH.TestAutomation.Api.Validators;

public static class PoreskiBrojValidator
{
    public static IEnumerable<string> Validate(string? value, bool required = true)
    {
        if (string.IsNullOrWhiteSpace(value))
        {
            if (required)
            {
                yield return "Poreski broj je obavezan.";
            }

            yield break;
        }

        var normalized = Normalize(value);

        if (!normalized.All(char.IsDigit))
        {
            yield return "Poreski broj smije sadržavati samo cifre.";
            yield break;
        }

        if (normalized.Length < 9 || normalized.Length > 13)
        {
            yield return "Poreski broj mora imati od 9 do 13 cifara.";
        }
    }

    public static bool IsValid(string? value, bool required = true)
    {
        return !Validate(value, required).Any();
    }

    private static string Normalize(string value)
    {
        return value.Replace(" ", string.Empty).Replace("-", string.Empty).Trim();
    }
}
