namespace RBBH.CollateralAppraisal.Application.Common;

/// <summary>
/// Centralne konstante za HTTP headere koje koriste i Infrastructure i Api sloj.
/// Sprečava dupliranje magic stringova između slojeva.
/// </summary>
public static class HttpHeaders
{
    public const string CorrelationId = "X-Correlation-ID";

    /// <summary>
    /// Aktivna rola odabrana kroz /select-role mehanizam (vidi ActiveRoleState na frontend-u).
    /// Šalje ga BaseApiService na svaki zahtjev — čisto informativan header za audit log,
    /// NE koristi se za autorizaciju (ta i dalje ide isključivo preko "permission" claim-ova).
    /// </summary>
    public const string ActiveRole = "X-Active-Role";
}
