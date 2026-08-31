namespace RBBH.CollateralAppraisal.Application.Reports.Dtos;

/// <summary>
/// Parametri za filter zakašnjelih procjena.
/// Filter: narudžba kod vještaka (OrderSentToAppraiserAt) > MinBusinessDaysOverdue radnih dana.
/// </summary>
public sealed record AppraiserReminderRequest(
    int?  AppraiserId         = null,  // opcionalni filter po vještaku
    int   MinBusinessDaysOverdue = 5,  // default: 5 radnih dana (spec)
    int   Page                = 1,
    int   PageSize            = 50);
