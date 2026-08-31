using RBBH.CollateralAppraisal.Domain.Orders;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

public sealed class OrderStateMachineIntegrationTests
{
    [Fact]
    public void NonTerminalStatuses_HaveAtLeastOneOutgoingTransition()
    {
        var terminalStatuses = new[]
        {
            AppraisalOrderStatus.Completed,
            AppraisalOrderStatus.Cancelled
        };

        foreach (var status in Enum.GetValues<AppraisalOrderStatus>())
        {
            if (terminalStatuses.Contains(status)) continue;

            var hasOutgoing = Enum.GetValues<AppraisalOrderStatus>()
                .Any(target => OrderStateMachine.CanTransition(status, target));

            Assert.True(hasOutgoing,
                $"Non-terminal status {status} must have at least one outgoing transition defined.");
        }
    }

    [Fact]
    public void CompletedAndCancelled_AreTerminalStates()
    {
        foreach (var target in Enum.GetValues<AppraisalOrderStatus>())
        {
            Assert.False(OrderStateMachine.CanTransition(AppraisalOrderStatus.Completed, target),
                $"Completed should not transition to {target}");
            Assert.False(OrderStateMachine.CanTransition(AppraisalOrderStatus.Cancelled, target),
                $"Cancelled should not transition to {target}");
        }
    }

    [Fact]
    public void Draft_CanOnlyGoToSubmittedOrCancelled()
    {
        var allowed = Enum.GetValues<AppraisalOrderStatus>()
            .Where(s => OrderStateMachine.CanTransition(AppraisalOrderStatus.Draft, s))
            .ToList();

        Assert.Contains(AppraisalOrderStatus.SubmittedBySales, allowed);
        Assert.Contains(AppraisalOrderStatus.Cancelled, allowed);
        Assert.Equal(2, allowed.Count);
    }

    [Fact]
    public void FullFLWorkflow_AllTransitionsValid()
    {
        var steps = new[]
        {
            AppraisalOrderStatus.Draft,
            AppraisalOrderStatus.SubmittedBySales,
            AppraisalOrderStatus.AcceptedByCA,
            AppraisalOrderStatus.DocumentationReviewInProgress,
            AppraisalOrderStatus.DocumentationApproved,
            AppraisalOrderStatus.AppraiserSelected,
            AppraisalOrderStatus.OrderSentToAppraiser,
            AppraisalOrderStatus.AppraisalInProgress,
            AppraisalOrderStatus.AppraisalReceived,
            AppraisalOrderStatus.ReadyForProcedure,
            AppraisalOrderStatus.Completed
        };

        for (int i = 0; i < steps.Length - 1; i++)
        {
            Assert.True(
                OrderStateMachine.CanTransition(steps[i], steps[i + 1]),
                $"FL workflow: {steps[i]} → {steps[i + 1]} should be valid");
        }
    }

    [Fact]
    public void ReworkCycle_IsValid()
    {
        Assert.True(OrderStateMachine.CanTransition(
            AppraisalOrderStatus.AppraisalReceived, AppraisalOrderStatus.AppraisalReturnedForRework));
        Assert.True(OrderStateMachine.CanTransition(
            AppraisalOrderStatus.AppraisalReturnedForRework, AppraisalOrderStatus.AppraisalReceived));
    }

    [Fact]
    public void CorrectionCycle_IsValid()
    {
        Assert.True(OrderStateMachine.CanTransition(
            AppraisalOrderStatus.DocumentationReviewInProgress, AppraisalOrderStatus.ReturnedForCorrection));
        Assert.True(OrderStateMachine.CanTransition(
            AppraisalOrderStatus.ReturnedForCorrection, AppraisalOrderStatus.CorrectionSubmitted));
    }

    [Fact]
    public void AppraiserRejection_CanReselect()
    {
        Assert.True(OrderStateMachine.CanTransition(
            AppraisalOrderStatus.OrderSentToAppraiser, AppraisalOrderStatus.AppraiserRejected));
        Assert.True(OrderStateMachine.CanTransition(
            AppraisalOrderStatus.AppraiserRejected, AppraisalOrderStatus.AppraiserSelected));
    }
}
