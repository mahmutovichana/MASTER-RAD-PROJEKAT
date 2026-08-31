namespace RBBH.CollateralAppraisal.Application.Codebooks.Requests;

/// <summary>
/// Request tijelo za deaktivaciju vrijednosti šifarnika.
/// Reason je opcioni ali preporučen — bilježi se u audit log i na entitetu.
/// </summary>
public sealed record DeactivateCodebookValueRequest(
    /// <summary>Razlog deaktivacije. Opcioni, bilježi se radi transparentnosti.</summary>
    string? Reason = null
);
