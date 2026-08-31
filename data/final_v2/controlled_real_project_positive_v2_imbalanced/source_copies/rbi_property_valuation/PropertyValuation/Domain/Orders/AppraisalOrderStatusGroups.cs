﻿namespace RBBH.CollateralAppraisal.Domain.Orders;

/// <summary>
/// Grupe statusa narudžbe procjene koje se koriste u poslovnim pravilima (Faza C — odabir vještaka).
/// </summary>
using System.Diagnostics.CodeAnalysis;
[ExcludeFromCodeCoverage]
public static class AppraisalOrderStatusGroups
{
    /// <summary>
    /// Statusi koji se raćunaju kao "aktivna dodjela vještaku" — koristi se za limit
    /// broja paralelnih procjena po vještaku (Individual&lt;2, Firm&lt;5) i za prikaz
    /// "broj aktivnih procjena" u admin listi vještaka.
    /// </summary>
    public static readonly List<AppraisalOrderStatus> ActiveAppraisalStatuses =
    [
        AppraisalOrderStatus.AppraiserSelected,
        AppraisalOrderStatus.DocumentsGenerated,
        AppraisalOrderStatus.OrderSentToAppraiser,
        AppraisalOrderStatus.AdditionalPaymentRequested,
        AppraisalOrderStatus.AdditionalPaymentCompleted,
        AppraisalOrderStatus.AppraisalInProgress,
        AppraisalOrderStatus.AppraisalReceived,
        AppraisalOrderStatus.COApproved
    ];
}
