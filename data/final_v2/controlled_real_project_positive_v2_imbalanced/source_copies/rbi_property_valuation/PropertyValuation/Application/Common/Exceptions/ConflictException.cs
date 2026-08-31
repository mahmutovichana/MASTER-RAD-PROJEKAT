namespace RBBH.CollateralAppraisal.Application.Common.Exceptions;

/// <summary>
/// Baca se kada zahtjev krši poslovno pravilo integriteta.
/// Mapira se na HTTP 409 Conflict.
///
/// Primjeri: pokušaj uklanjanja posljednjeg administratora,
/// dodjela role koju korisnik već ima, odobravanje zapisa koji nije u ispravnom statusu.
/// </summary>
public class ConflictException : Exception
{
    /// <summary>Mašinski čitljiv kod greške (npr. "CODEBOOK_VALUE_IN_USE"). Null ako nije definisan.</summary>
    public string? ErrorCode { get; }

    public ConflictException(string message, string? errorCode = null)
        : base(message)
    {
        ErrorCode = errorCode;
    }
}
