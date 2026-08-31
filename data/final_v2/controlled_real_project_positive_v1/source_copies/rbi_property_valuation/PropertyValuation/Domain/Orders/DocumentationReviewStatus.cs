namespace RBBH.CollateralAppraisal.Domain.Orders;

/// <summary>
/// Status pregleda dokumentacije od strane CA.
/// Vrijednosti se mapiraju na bazu kao bosanski nazivi radi konzistentnosti
/// s postojećim podacima.
/// </summary>
public enum DocumentationReviewStatus
{
    NijePregledano = 0,
    UToku          = 1,
    Vraceno        = 2,
    Odobreno       = 3
}
