using RBBH.CollateralAppraisal.Domain.Orders;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

public sealed class OrderStateMachineTests
{
    [Theory]
    [InlineData(AppraisalOrderStatus.Draft, AppraisalOrderStatus.SubmittedBySales, true)]
    [InlineData(AppraisalOrderStatus.Draft, AppraisalOrderStatus.Cancelled, true)]
    [InlineData(AppraisalOrderStatus.Draft, AppraisalOrderStatus.Completed, false)]
    [InlineData(AppraisalOrderStatus.SubmittedBySales, AppraisalOrderStatus.AcceptedByCA, true)]
    [InlineData(AppraisalOrderStatus.SubmittedBySales, AppraisalOrderStatus.Completed, false)]
    [InlineData(AppraisalOrderStatus.AcceptedByCA, AppraisalOrderStatus.DocumentationReviewInProgress, true)]
    [InlineData(AppraisalOrderStatus.DocumentationReviewInProgress, AppraisalOrderStatus.ReturnedForCorrection, true)]
    [InlineData(AppraisalOrderStatus.DocumentationReviewInProgress, AppraisalOrderStatus.DocumentationApproved, true)]
    [InlineData(AppraisalOrderStatus.DocumentationReviewInProgress, AppraisalOrderStatus.AccessCheckRequested, true)]
    [InlineData(AppraisalOrderStatus.AppraisalReceived, AppraisalOrderStatus.ReadyForProcedure, true)]
    [InlineData(AppraisalOrderStatus.AppraisalReceived, AppraisalOrderStatus.AppraisalReturnedForRework, true)]
    [InlineData(AppraisalOrderStatus.AppraisalReturnedForRework, AppraisalOrderStatus.AppraisalReceived, true)]
    [InlineData(AppraisalOrderStatus.ReadyForProcedure, AppraisalOrderStatus.Completed, true)]
    [InlineData(AppraisalOrderStatus.Completed, AppraisalOrderStatus.Draft, false)]
    [InlineData(AppraisalOrderStatus.Cancelled, AppraisalOrderStatus.Draft, false)]
    [InlineData(AppraisalOrderStatus.OrderSentToAppraiser, AppraisalOrderStatus.AppraisalInProgress, true)]
    [InlineData(AppraisalOrderStatus.OrderSentToAppraiser, AppraisalOrderStatus.AppraiserRejected, true)]
    // Additional transitions
    [InlineData(AppraisalOrderStatus.SubmittedBySales, AppraisalOrderStatus.Cancelled, true)]
    [InlineData(AppraisalOrderStatus.ReturnedForCorrection, AppraisalOrderStatus.CorrectionSubmitted, true)]
    [InlineData(AppraisalOrderStatus.ReturnedForCorrection, AppraisalOrderStatus.Cancelled, true)]
    [InlineData(AppraisalOrderStatus.CorrectionSubmitted, AppraisalOrderStatus.DocumentationReviewInProgress, true)]
    [InlineData(AppraisalOrderStatus.CorrectionSubmitted, AppraisalOrderStatus.AcceptedByCA, true)]
    [InlineData(AppraisalOrderStatus.DocumentationApproved, AppraisalOrderStatus.AccessCheckRequested, true)]
    [InlineData(AppraisalOrderStatus.DocumentationApproved, AppraisalOrderStatus.ProtocolCreated, true)]
    [InlineData(AppraisalOrderStatus.DocumentationApproved, AppraisalOrderStatus.AppraiserSelected, true)]
    [InlineData(AppraisalOrderStatus.AccessCheckRequested, AppraisalOrderStatus.AccessCheckApproved, true)]
    [InlineData(AppraisalOrderStatus.AccessCheckRequested, AppraisalOrderStatus.AccessCheckRejected, true)]
    [InlineData(AppraisalOrderStatus.AccessCheckApproved, AppraisalOrderStatus.ProtocolCreated, true)]
    [InlineData(AppraisalOrderStatus.AccessCheckApproved, AppraisalOrderStatus.AppraiserSelected, true)]
    [InlineData(AppraisalOrderStatus.AccessCheckRejected, AppraisalOrderStatus.DocumentationReviewInProgress, true)]
    [InlineData(AppraisalOrderStatus.AccessCheckRejected, AppraisalOrderStatus.ReturnedForCorrection, true)]
    [InlineData(AppraisalOrderStatus.ProtocolCreated, AppraisalOrderStatus.AppraiserSelected, true)]
    [InlineData(AppraisalOrderStatus.AppraiserSelected, AppraisalOrderStatus.DocumentsGenerated, true)]
    [InlineData(AppraisalOrderStatus.AppraiserSelected, AppraisalOrderStatus.OrderSentToAppraiser, true)]
    [InlineData(AppraisalOrderStatus.DocumentsGenerated, AppraisalOrderStatus.OrderSentToAppraiser, true)]
    [InlineData(AppraisalOrderStatus.OrderSentToAppraiser, AppraisalOrderStatus.AdditionalPaymentRequested, true)]
    [InlineData(AppraisalOrderStatus.AppraiserRejected, AppraisalOrderStatus.AppraiserSelected, true)]
    [InlineData(AppraisalOrderStatus.AppraiserRejected, AppraisalOrderStatus.AccessCheckApproved, true)]
    [InlineData(AppraisalOrderStatus.AppraiserRejected, AppraisalOrderStatus.DocumentationApproved, true)]
    [InlineData(AppraisalOrderStatus.AdditionalPaymentRequested, AppraisalOrderStatus.AdditionalPaymentCompleted, true)]
    [InlineData(AppraisalOrderStatus.AdditionalPaymentCompleted, AppraisalOrderStatus.AppraisalInProgress, true)]
    [InlineData(AppraisalOrderStatus.AdditionalPaymentCompleted, AppraisalOrderStatus.OrderSentToAppraiser, true)]
    [InlineData(AppraisalOrderStatus.AppraisalInProgress, AppraisalOrderStatus.AppraisalReceived, true)]
    [InlineData(AppraisalOrderStatus.AppraisalInProgress, AppraisalOrderStatus.AdditionalPaymentRequested, true)]
    [InlineData(AppraisalOrderStatus.AppraisalReceived, AppraisalOrderStatus.COApproved, true)]
    [InlineData(AppraisalOrderStatus.COApproved, AppraisalOrderStatus.ReadyForProcedure, true)]
    // OriginalReceived (160) uklonjen: ReadyForProcedure → Completed direktno
    [InlineData(AppraisalOrderStatus.ReadyForProcedure, AppraisalOrderStatus.Completed, true)]
    // Forbidden transitions
    [InlineData(AppraisalOrderStatus.Draft, AppraisalOrderStatus.AppraisalInProgress, false)]
    [InlineData(AppraisalOrderStatus.AppraisalReceived, AppraisalOrderStatus.Draft, false)]
    [InlineData(AppraisalOrderStatus.ReadyForProcedure, AppraisalOrderStatus.Draft, false)]
    public void CanTransition_ReturnsExpected(AppraisalOrderStatus from, AppraisalOrderStatus to, bool expected)
    {
        Assert.Equal(expected, OrderStateMachine.CanTransition(from, to));
    }

    [Fact]
    public void EnsureValidTransition_InvalidTransition_Throws()
    {
        Assert.Throws<InvalidStateTransitionException>(
            () => OrderStateMachine.EnsureValidTransition(
                AppraisalOrderStatus.Draft, AppraisalOrderStatus.Completed));
    }

    [Fact]
    public void EnsureValidTransition_ValidTransition_DoesNotThrow()
    {
        var ex = Record.Exception(
            () => OrderStateMachine.EnsureValidTransition(
                AppraisalOrderStatus.Draft, AppraisalOrderStatus.SubmittedBySales));
        Assert.Null(ex);
    }

    [Fact]
    public void Completed_HasNoOutgoingTransitions()
    {
        Assert.False(OrderStateMachine.CanTransition(AppraisalOrderStatus.Completed, AppraisalOrderStatus.Draft));
        Assert.False(OrderStateMachine.CanTransition(AppraisalOrderStatus.Completed, AppraisalOrderStatus.SubmittedBySales));
    }

    [Fact]
    public void Cancelled_HasNoOutgoingTransitions()
    {
        Assert.False(OrderStateMachine.CanTransition(AppraisalOrderStatus.Cancelled, AppraisalOrderStatus.Draft));
    }
}
