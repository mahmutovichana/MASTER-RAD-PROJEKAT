namespace RBBH.CollateralAppraisal.Application.Common.Interfaces;

/// <summary>
/// Apstrakcija za sistemsko vrijeme. Omogućava determinističko testiranje
/// svake logike koja zavisi od DateTime.UtcNow (SLA rokovi, timeout prozori, audit timestampi).
/// </summary>
public interface IClock
{
    DateTime UtcNow { get; }
}
