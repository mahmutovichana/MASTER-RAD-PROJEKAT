namespace RBBH.CollateralAppraisal.Application.Codebooks;

/// <summary>
/// Mašinski čitljivi kodovi grešaka za šifarnike.
/// Uključuju se u ProblemDetails.Extensions["errorCode"] kako bi frontend
/// mogao prikazati odgovarajuće upozorenje bez parsiranja poruke.
/// </summary>
public static class CodebookErrorCodes
{
    public const string ValueNotFound                = "CODEBOOK_VALUE_NOT_FOUND";
    public const string KeyMismatch                  = "CODEBOOK_KEY_MISMATCH";
    public const string ValueAlreadyInactive         = "CODEBOOK_VALUE_ALREADY_INACTIVE";
    public const string ValueAlreadyActive           = "CODEBOOK_VALUE_ALREADY_ACTIVE";
    public const string ValueAlreadyDeleted          = "CODEBOOK_VALUE_ALREADY_DELETED";
    public const string ValueInUse                   = "CODEBOOK_VALUE_IN_USE";
    public const string SystemLocked                 = "CODEBOOK_VALUE_SYSTEM_LOCKED";
    public const string CriticalLocked               = "CODEBOOK_VALUE_CRITICAL_LOCKED";
    public const string DeleteNotAllowed             = "CODEBOOK_VALUE_DELETE_NOT_ALLOWED";
    public const string DeactivationNotAllowed       = "CODEBOOK_VALUE_DEACTIVATION_NOT_ALLOWED";
    public const string UsageCheckFailed             = "CODEBOOK_USAGE_CHECK_FAILED";
    public const string CacheInvalidationFailed      = "CODEBOOK_CACHE_INVALIDATION_FAILED";
    public const string InactiveForNewRecord         = "CODEBOOK_VALUE_INACTIVE_FOR_NEW_RECORD";
    public const string ManagePermissionRequired     = "CODEBOOK_MANAGE_PERMISSION_REQUIRED";
    public const string CodebookKeyUnknown           = "CODEBOOK_KEY_UNKNOWN";
    public const string CodeInUseCannotChange        = "CODEBOOK_VALUE_CODE_IN_USE_CANNOT_CHANGE";
    public const string DuplicateCode               = "CODEBOOK_VALUE_DUPLICATE_CODE";

    // ── Codebook (container) greške ───────────────────────────────────────────
    public const string CodebookNotFound             = "CODEBOOK_NOT_FOUND";
    public const string CodebookDuplicateCode        = "CODEBOOK_DUPLICATE_CODE";
    public const string CodebookSystemLocked         = "CODEBOOK_SYSTEM_LOCKED";
    public const string CodebookAlreadyInactive      = "CODEBOOK_ALREADY_INACTIVE";
    public const string CodebookAlreadyActive        = "CODEBOOK_ALREADY_ACTIVE";
    public const string CodebookHasActiveValues      = "CODEBOOK_HAS_ACTIVE_VALUES";
}
