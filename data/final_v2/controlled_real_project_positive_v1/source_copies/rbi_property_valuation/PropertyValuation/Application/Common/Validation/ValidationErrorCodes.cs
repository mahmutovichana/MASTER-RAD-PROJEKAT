namespace RBBH.CollateralAppraisal.Application.Common.Validation;

/// <summary>
/// Centralizirani stabilni error kodovi za validacijske greške.
/// Frontend koristi ove kodove za mapiranje na prikaz.
/// QA koristi ove kodove za verifikaciju odgovora.
///
/// Format: UPPER_SNAKE_CASE, opisuje ŠTA JE POGREŠNO.
/// Nikad mijenjati postojeće vrijednosti — to je breaking change za frontend i QA.
/// </summary>
public static class ValidationErrorCodes
{
    // ── Opšti validacijski kodovi ──────────────────────────────────────────────
    public const string ValidationError          = "VALIDATION_ERROR";
    public const string RequiredField            = "REQUIRED_FIELD";
    public const string InvalidFormat            = "INVALID_FORMAT";
    public const string InvalidInput             = "INVALID_INPUT";
    public const string ValueNotAllowed          = "VALUE_NOT_ALLOWED";
    public const string MaxLengthExceeded        = "MAX_LENGTH_EXCEEDED";
    public const string MinLengthNotMet          = "MIN_LENGTH_NOT_MET";
    public const string InvalidCharacters        = "INVALID_CHARACTERS";
    public const string UnsupportedCharacters    = "UNSUPPORTED_CHARACTERS";
    public const string InvalidCodeFormat        = "INVALID_CODE_FORMAT";

    // ── JMBG ──────────────────────────────────────────────────────────────────
    public const string RequiredJmbg             = "REQUIRED_JMBG";
    public const string InvalidJmbgFormat        = "INVALID_JMBG_FORMAT";
    public const string InvalidJmbgLength        = "INVALID_JMBG_LENGTH";
    public const string InvalidJmbgDigitsOnly    = "INVALID_JMBG_DIGITS_ONLY";
    public const string InvalidJmbgDatePart      = "INVALID_JMBG_DATE_PART";
    public const string InvalidJmbgChecksum      = "INVALID_JMBG_CHECKSUM";

    // ── Porezni broj ──────────────────────────────────────────────────────────
    public const string RequiredTaxNumber        = "REQUIRED_TAX_NUMBER";
    public const string InvalidTaxNumberFormat   = "INVALID_TAX_NUMBER_FORMAT";
    public const string InvalidTaxNumberLength   = "INVALID_TAX_NUMBER_LENGTH";
    public const string InvalidTaxNumberDigitsOnly = "INVALID_TAX_NUMBER_DIGITS_ONLY";

    // ── Matični broj firme — neaktivno, FL i PL koriste JMBG (vidi gore) ────────
    public const string RequiredCompanyId            = "REQUIRED_COMPANY_ID";
    public const string InvalidCompanyIdLength       = "INVALID_COMPANY_ID_LENGTH";
    public const string InvalidCompanyIdDigitsOnly   = "INVALID_COMPANY_ID_DIGITS_ONLY";

    // ── Ime / naziv ───────────────────────────────────────────────────────────
    public const string InvalidNameFormat        = "INVALID_NAME_FORMAT";

    // ── Telefon ───────────────────────────────────────────────────────────────
    public const string InvalidPhoneFormat       = "INVALID_PHONE_FORMAT";

    // ── Email ─────────────────────────────────────────────────────────────────
    public const string InvalidEmailFormat       = "INVALID_EMAIL_FORMAT";

    // ── Tip klijenta ──────────────────────────────────────────────────────────
    public const string RequiredClientType       = "REQUIRED_CLIENT_TYPE";

    // ── Kolateral ─────────────────────────────────────────────────────────────
    public const string InvalidCombinedCollateralBase = "INVALID_COMBINED_COLLATERAL_BASE";

    // ── Datumi ────────────────────────────────────────────────────────────────
    public const string InvalidDateRange         = "INVALID_DATE_RANGE";

    // ── Grad / Poslovnica ─────────────────────────────────────────────────────
    public const string InvalidBranchForCity     = "INVALID_BRANCH_FOR_CITY";

    // ── Pretraga ──────────────────────────────────────────────────────────────
    public const string InvalidSearchQuery       = "INVALID_SEARCH_QUERY";
    public const string SearchQueryTooLong       = "SEARCH_QUERY_TOO_LONG";
}
