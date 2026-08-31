namespace RBBH.CollateralAppraisal.Application.Common.Exceptions;

/// <summary>
/// Baca se kada autentificirani korisnik nema dozvolu za traženu akciju.
/// Mapira se na HTTP 403 Forbidden.
///
/// Primjeri: korisnik bez odgovarajućeg permission-a pokušava pristupiti zaštićenom resursu,
/// pokušaj uređivanja tuđeg zapisa bez administratorske dozvole.
/// </summary>
public class ForbiddenException : Exception
{
    /// <summary>Mašinski čitljiv kod greške. Null ako nije definisan.</summary>
    public string? ErrorCode { get; }

    public ForbiddenException()
        : base("You do not have permission to perform this action.") { }

    public ForbiddenException(string message, string? errorCode = null)
        : base(message)
    {
        ErrorCode = errorCode;
    }
}
