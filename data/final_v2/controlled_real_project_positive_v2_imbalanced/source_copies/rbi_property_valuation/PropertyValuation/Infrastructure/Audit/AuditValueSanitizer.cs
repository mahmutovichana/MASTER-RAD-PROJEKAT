using System.Text.Json;
using System.Text.RegularExpressions;
using RBBH.CollateralAppraisal.Application.Audit;

namespace RBBH.CollateralAppraisal.Infrastructure.Audit;

/// <summary>
/// Serijalizuje vrijednost u JSON, zatim redaktuje osjetljiva polja i maskira PII podatke.
///
/// Dvije kategorije obrade:
///   1. Potpuna redakcija (***REDACTED***) — kriptografski materijal, tokeni, kredencijali
///   2. Parcijalno maskiranje — email, telefon (vidljivi su početak i kraj za identifikaciju)
///
/// Lista polja pokriva OWASP-preporučene kategorije tajnih podataka + bankarski PII standard.
/// </summary>
public partial class AuditValueSanitizer : IAuditValueSanitizer
{
    private static readonly JsonSerializerOptions SerializerOptions = new()
    {
        WriteIndented = false,
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
    };

    public string? Sanitize(object? value)
    {
        if (value is null)
            return null;

        string json = value is string s
            ? s
            : JsonSerializer.Serialize(value, SerializerOptions);

        // Redoslijed je bitan: parcijalno maskiranje ide POSLIJE potpune redakcije
        // kako bi se izbjeglo dvostruko procesiranje.
        json = RedactSensitiveFields(json);
        json = MaskEmailFields(json);
        json = MaskPhoneFields(json);
        json = MaskIdentifierFields(json);

        return json;
    }

    // ── Potpuna redakcija ─────────────────────────────────────────────────────

    private static string RedactSensitiveFields(string json) =>
        SensitiveFieldPattern().Replace(json, m =>
            $@"""{m.Groups[1].Value}"":""***REDACTED***""");

    // Pokriva: password, token, refreshToken, secret, apiKey, clientSecret,
    //          connectionString, authorizationHeader, privateKey, secretKey
    //          (i varijante u camelCase/PascalCase/snake_case)
    [GeneratedRegex(
        @"""(password|passwordHash|token|refreshToken|refresh_token|accessToken|access_token|" +
        @"secret|secretKey|secret_key|apiKey|api_key|clientSecret|client_secret|" +
        @"connectionString|connection_string|authorizationHeader|authorization|" +
        @"privateKey|private_key)""\s*:\s*""[^""]*""",
        RegexOptions.IgnoreCase)]
    private static partial Regex SensitiveFieldPattern();

    // ── Parcijalno maskiranje emaila ──────────────────────────────────────────

    private static string MaskEmailFields(string json) =>
        EmailFieldPattern().Replace(json, m =>
        {
            var fieldName = m.Groups[1].Value;
            var email     = m.Groups[2].Value;
            return $@"""{fieldName}"":""{MaskEmail(email)}""";
        });

    private static string MaskEmail(string email)
    {
        if (string.IsNullOrWhiteSpace(email)) return email;
        var atIdx = email.IndexOf('@');
        if (atIdx <= 0) return email;

        var local  = email[..atIdx];
        var domain = email[atIdx..];

        var visibleLocal = local.Length <= 3
            ? local[..1]
            : local[..2];

        return $"{visibleLocal}***{domain}";
    }

    // Polja koja sadrže email adresu (parcijalno maskiranje)
    [GeneratedRegex(
        @"""(email|emailAddress|email_address|userEmail|user_email|actorEmail|actor_email)""\s*:\s*""([^""@]+@[^""]+)""",
        RegexOptions.IgnoreCase)]
    private static partial Regex EmailFieldPattern();

    // ── Parcijalno maskiranje telefona ────────────────────────────────────────

    private static string MaskPhoneFields(string json) =>
        PhoneFieldPattern().Replace(json, m =>
        {
            var fieldName = m.Groups[1].Value;
            var phone     = m.Groups[2].Value;
            return $@"""{fieldName}"":""{MaskPhone(phone)}""";
        });

    private static string MaskPhone(string phone)
    {
        if (string.IsNullOrWhiteSpace(phone) || phone.Length < 6) return phone;

        // Zadržava prvih 4 i posljednjih 3 znaka: +38761***498
        var prefix = phone.Length >= 4 ? phone[..4] : phone;
        var suffix = phone.Length >= 3 ? phone[^3..] : string.Empty;
        return $"{prefix}***{suffix}";
    }

    // Polja koja sadrže telefonski broj
    [GeneratedRegex(
        @"""(phone|phoneNumber|phone_number|mobile|mobileNumber|mobile_number|tel|telefon|telefonnummer)""\s*:\s*""([^""]+)""",
        RegexOptions.IgnoreCase)]
    private static partial Regex PhoneFieldPattern();

    // ── Parcijalno maskiranje ličnog identifikatora (JMBG / PIB) ─────────────
    // GDPR / bankarska regulativa: JMBG i PIB su regulirani PII podaci.
    // Prikazuju se samo prva 2 i posljednja 2 znaka radi identifikacije u auditu.
    // Primjer: "0101985771007" → "01*********07"

    private static string MaskIdentifierFields(string json) =>
        IdentifierFieldPattern().Replace(json, m =>
        {
            var fieldName = m.Groups[1].Value;
            var identifier = m.Groups[2].Value;
            return $@"""{fieldName}"":""{MaskIdentifier(identifier)}""";
        });

    private static string MaskIdentifier(string value)
    {
        if (string.IsNullOrWhiteSpace(value) || value.Length <= 4) return value;
        var prefix = value[..2];
        var suffix = value[^2..];
        var masked = new string('*', value.Length - 4);
        return $"{prefix}{masked}{suffix}";
    }

    // Polja koja sadrže nacionalni identifikacijski broj (JMBG, PIB, MBS, OIB itd.)
    [GeneratedRegex(
        @"""(clientIdentifier|jmbg|pib|nationalId|national_id|identificationNumber|identification_number|" +
        @"taxNumber|tax_number|registrationNumber|registration_number|mbs|oib)""\s*:\s*""([^""]+)""",
        RegexOptions.IgnoreCase)]
    private static partial Regex IdentifierFieldPattern();
}
