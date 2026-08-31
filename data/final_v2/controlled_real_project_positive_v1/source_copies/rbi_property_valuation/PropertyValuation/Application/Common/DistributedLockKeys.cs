namespace RBBH.CollateralAppraisal.Application.Common;

/// <summary>
/// Fiksni integer ključevi za SQL Server advisory lockove.
/// Stabilni konstantni ID-evi garantuju da isti lock prepoznaju svi čvorovi klastera.
/// </summary>
public static class DistributedLockKeys
{
    public const long AppraiserUploadTimeout     = 1001L;
    public const long AppraiserAcceptanceTimeout = 1002L;
    public const long AuditOutboxProcessor       = 1003L;
}
