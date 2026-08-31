using System.Globalization;
using System.Text;

namespace RBBH.TestAutomation.Api.Validators;

public static class ValidatorExtensions
{
    public static IEnumerable<string> Required(string? value, string fieldName)
    {
        if (string.IsNullOrWhiteSpace(value))
        {
            yield return $"{fieldName} je obavezno.";
        }
    }

    public static bool ContainsNormalized(
        this string? value,
        string? searchTerm,
        CompareOptions compareOptions = CompareOptions.IgnoreCase | CompareOptions.IgnoreNonSpace
    )
    {
        if (string.IsNullOrWhiteSpace(searchTerm))
        {
            return true;
        }

        if (string.IsNullOrWhiteSpace(value))
        {
            return false;
        }

        var culture = CultureInfo.GetCultureInfo("bs-BA");
        return culture.CompareInfo.IndexOf(value, searchTerm, compareOptions) >= 0
            || RemoveDiacritics(value)
                .Contains(RemoveDiacritics(searchTerm), StringComparison.OrdinalIgnoreCase);
    }

    private static string RemoveDiacritics(string value)
    {
        var normalized = value.Normalize(NormalizationForm.FormD);
        var builder = new StringBuilder(normalized.Length);

        foreach (var character in normalized)
        {
            if (CharUnicodeInfo.GetUnicodeCategory(character) != UnicodeCategory.NonSpacingMark)
            {
                builder.Append(NormalizeBosnianCharacter(character));
            }
        }

        return builder.ToString().Normalize(NormalizationForm.FormC);
    }

    private static string NormalizeBosnianCharacter(char character)
    {
        return character switch
        {
            'Đ' => "Dj",
            'đ' => "dj",
            _ => character.ToString(),
        };
    }
}
