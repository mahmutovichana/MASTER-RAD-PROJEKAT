using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

/// <summary>
/// Zajednički mapper AppraisalOrder domenskog entiteta na AppraisalOrderDto.
/// Ekstrahovan iz AppraisalOrderService (I-1 refactoring) da bi ga mogli koristiti
/// i OrderCreateService i OrderSubmitService bez dupliranja.
/// </summary>
internal static class OrderDtoMapper
{
    public static AppraisalOrderDto ToDto(
        AppraisalOrder order,
        ICurrentUserService currentUser,
        string?  collateralLabel,
        string?  combinedLabel,
        string?  protocolNumber = null)
    {
        var isOwner = order.CreatedByUserId == currentUser.UserId;
        var isDraft = order.Status == AppraisalOrderStatus.Draft;

        bool HasPerm(string p) => currentUser.Permissions.Contains(p, StringComparer.OrdinalIgnoreCase);

        var canRejectOrder = HasPerm(AppPermissions.OrdersAccept)
            && order.Status is AppraisalOrderStatus.OrderSentToAppraiser
                             or AppraisalOrderStatus.AppraisalInProgress;

        var canAdminRejectOrder = HasPerm(AppPermissions.OrdersSendToAppraiser)
            && order.Status is AppraisalOrderStatus.OrderSentToAppraiser
                             or AppraisalOrderStatus.AppraisalInProgress;

        var canRequestAdditionalPayment = HasPerm(AppPermissions.OrdersAccept)
            && order.Status is AppraisalOrderStatus.OrderSentToAppraiser
                             or AppraisalOrderStatus.AppraisalInProgress;

        var canCompleteAdditionalPayment = HasPerm(AppPermissions.OrdersSendToAppraiser)
            && order.Status == AppraisalOrderStatus.AdditionalPaymentRequested;

        var canAcceptOrder = HasPerm(AppPermissions.OrdersAccept)
            && order.Status == AppraisalOrderStatus.OrderSentToAppraiser;

        return new AppraisalOrderDto(
            order.Id,
            order.OrderNumber,
            order.Title,
            order.Status.ToString(),
            (int)order.Status,
            order.WorkflowType?.ToString(),
            OrderWorkflowRouting.CurrentOwnerRole(order.EffectiveWorkflowType, order.Status),
            OrderWorkflowRouting.NextResponsibleRole(order.EffectiveWorkflowType, order.Status),
            order.ClientName,
            order.ClientType,
            order.ClientIdentifier,
            order.CollateralTypeId,
            collateralLabel,
            order.CombinedCollateralTypeId,
            combinedLabel,
            order.City,
            order.PropertyAddress,
            order.PropertyCity,
            order.Branch,
            order.BranchAddress,
            order.ContactName,
            order.ContactPhone,
            order.ContactEmail,
            order.DeliveryContactName,
            order.AmRecipientName,
            order.CreatedByUserId,
            order.CreatedByRole,
            order.CreatedByName,
            order.CreatedAt,
            order.UpdatedAt,
            order.SubmittedAt,
            order.InternalNote,
            order.RequestReceivedAt,
            order.RequestSentAt,
            order.SquareMetersCommercial,
            order.SquareMetersResidential,
            AppraisalFee: order.AppraisalFee,
            CollateralStatus: order.CollateralStatus,
            ProtocolNumber: protocolNumber,
            InvoiceWorkflowStatus: order.InvoiceStatus.ToString(),
            InvoiceUploadedByName: order.InvoiceUploadedByName,
            InvoiceUploadedAt: order.InvoiceUploadedAt,
            InvoiceSentForPaymentByName: order.InvoiceSentForPaymentByName,
            InvoiceSentForPaymentAt: order.InvoiceSentForPaymentAt,
            InvoicePaidByName: order.InvoicePaidByName,
            InvoicePaidAt: order.InvoicePaidAt,
            InvoiceDocumentId: order.InvoiceDocumentId,
            Capabilities: new OrderCapabilitiesDto(
                CanEdit:                      isOwner && isDraft,
                CanSubmit:                    isOwner && isDraft,
                CanCancel:                    isOwner && isDraft,
                CanRejectOrder:               canRejectOrder,
                CanRequestAdditionalPayment:  canRequestAdditionalPayment,
                CanCompleteAdditionalPayment: canCompleteAdditionalPayment,
                CanAcceptOrder:               canAcceptOrder,
                CanAdminRejectOrder:          canAdminRejectOrder
            ),
            order.AcceptedByCAUserId,
            order.AcceptedAt
        );
    }
}
