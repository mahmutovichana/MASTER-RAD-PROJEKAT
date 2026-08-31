﻿namespace RBBH.CollateralAppraisal.Domain.Orders;

/// <summary>
/// Evidencija vještaka koji su odbili ili prekoraćili 24h rok za konkretnu narudžbu.
/// Koristi se pri ponovnom automatskom odabiru — odbijeni vještaci se iskljućuju iz selekcije.
/// </summary>
using System.Diagnostics.CodeAnalysis;
[ExcludeFromCodeCoverage]
public sealed class OrderDeclinedAppraiser
{
    public int Id { get; private set; }
    public int AppraisalOrderId { get; private set; }
    public int AppraiserId { get; private set; }
    public DateTime DeclinedAt { get; private set; }
    public AppraiserDeclineReason Reason { get; private set; }
    public string? FreeText { get; private set; }
    public bool IsTimeout { get; private set; }

    private OrderDeclinedAppraiser() { }

    public static OrderDeclinedAppraiser Create(
        int orderId,
        int appraiserId,
        AppraiserDeclineReason reason,
        string? freeText,
        bool isTimeout,
        DateTime now) =>
        new()
        {
            AppraisalOrderId = orderId,
            AppraiserId      = appraiserId,
            DeclinedAt       = now,
            Reason           = reason,
            FreeText         = freeText,
            IsTimeout        = isTimeout
        };
}

public enum AppraiserDeclineReason
{
    NisamUGradu        = 1,
    NeModuSticiObaveze = 2,
    Bolest             = 3,
    SmrtniSlucaj       = 4,
    OstaliRazlozi      = 5,
    Timeout            = 6
}
