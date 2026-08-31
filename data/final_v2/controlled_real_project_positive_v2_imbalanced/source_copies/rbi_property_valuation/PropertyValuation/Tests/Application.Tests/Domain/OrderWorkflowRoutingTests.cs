using RBBH.CollateralAppraisal.Domain.Orders;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Domain;

public sealed class OrderWorkflowRoutingTests
{
    // ── CurrentOwnerRole ────────────────────────────────────────────────────

    [Theory]
    [InlineData(AppraisalOrderStatus.Draft, "Prodaja")]
    [InlineData(AppraisalOrderStatus.SubmittedBySales, "Kolateral administrator")]
    [InlineData(AppraisalOrderStatus.AcceptedByCA, "Kolateral administrator")]
    [InlineData(AppraisalOrderStatus.DocumentationReviewInProgress, "Kolateral administrator")]
    [InlineData(AppraisalOrderStatus.ReturnedForCorrection, "Prodaja")]
    [InlineData(AppraisalOrderStatus.CorrectionSubmitted, "Kolateral administrator")]
    [InlineData(AppraisalOrderStatus.DocumentationApproved, "Kolateral administrator")]
    [InlineData(AppraisalOrderStatus.AccessCheckRequested, "Kolateral oficir")]
    [InlineData(AppraisalOrderStatus.AccessCheckApproved, "Kolateral administrator")]
    [InlineData(AppraisalOrderStatus.AccessCheckRejected, "Kolateral administrator")]
    [InlineData(AppraisalOrderStatus.ProtocolCreated, "Kolateral administrator")]
    [InlineData(AppraisalOrderStatus.AppraiserSelected, "Kolateral administrator")]
    [InlineData(AppraisalOrderStatus.DocumentsGenerated, "Kolateral administrator")]
    [InlineData(AppraisalOrderStatus.OrderSentToAppraiser, "Vještak")]
    [InlineData(AppraisalOrderStatus.AdditionalPaymentRequested, "Kolateral administrator")]
    [InlineData(AppraisalOrderStatus.AdditionalPaymentCompleted, "Vještak")]
    [InlineData(AppraisalOrderStatus.AppraisalInProgress, "Vještak")]
    [InlineData(AppraisalOrderStatus.AppraisalReceived, "Kolateral oficir")]
    [InlineData(AppraisalOrderStatus.COApproved, "Kolateral oficir")]
    [InlineData(AppraisalOrderStatus.ReadyForProcedure, "Prodaja")]
    [InlineData(AppraisalOrderStatus.Completed, "—")]
    [InlineData(AppraisalOrderStatus.Cancelled, "—")]
    public void CurrentOwnerRole_FL_ReturnsExpected(AppraisalOrderStatus status, string expected)
    {
        var result = OrderWorkflowRouting.CurrentOwnerRole(WorkflowType.FizickaLica, status);
        Assert.Equal(expected, result);
    }

    [Theory]
    [InlineData(AppraisalOrderStatus.Draft, "Prodaja")]
    [InlineData(AppraisalOrderStatus.SubmittedBySales, "Kolateral administrator")]
    [InlineData(AppraisalOrderStatus.AccessCheckRequested, "Kolateral oficir")]
    [InlineData(AppraisalOrderStatus.OrderSentToAppraiser, "Vještak")]
    [InlineData(AppraisalOrderStatus.AppraisalReceived, "Kolateral oficir")]
    [InlineData(AppraisalOrderStatus.Completed, "—")]
    [InlineData(AppraisalOrderStatus.Cancelled, "—")]
    public void CurrentOwnerRole_PL_ReturnsExpected(AppraisalOrderStatus status, string expected)
    {
        var result = OrderWorkflowRouting.CurrentOwnerRole(WorkflowType.PravnaLica, status);
        Assert.Equal(expected, result);
    }

    [Fact]
    public void CurrentOwnerRole_NullWorkflowType_ReturnsSameAsFLBecauseOwnerDoesNotDependOnType()
    {
        foreach (var status in Enum.GetValues<AppraisalOrderStatus>())
        {
            var withNull = OrderWorkflowRouting.CurrentOwnerRole(null, status);
            var withFL = OrderWorkflowRouting.CurrentOwnerRole(WorkflowType.FizickaLica, status);
            Assert.Equal(withFL, withNull);
        }
    }

    [Fact]
    public void CurrentOwnerRole_UnknownStatus_ReturnsDash()
    {
        var result = OrderWorkflowRouting.CurrentOwnerRole(WorkflowType.FizickaLica, (AppraisalOrderStatus)9999);
        Assert.Equal("—", result);
    }

    // ── NextResponsibleRole ─────────────────────────────────────────────────

    [Theory]
    [InlineData(AppraisalOrderStatus.Draft, "Kolateral administrator")]
    [InlineData(AppraisalOrderStatus.SubmittedBySales, "Kolateral administrator")]
    [InlineData(AppraisalOrderStatus.AcceptedByCA, "Kolateral administrator")]
    [InlineData(AppraisalOrderStatus.DocumentationReviewInProgress, "Vještak")]
    [InlineData(AppraisalOrderStatus.ReturnedForCorrection, "Prodaja")]
    [InlineData(AppraisalOrderStatus.CorrectionSubmitted, "Kolateral administrator")]
    [InlineData(AppraisalOrderStatus.DocumentationApproved, "Vještak")]
    [InlineData(AppraisalOrderStatus.AccessCheckRequested, "Kolateral oficir")]
    [InlineData(AppraisalOrderStatus.AccessCheckApproved, "Vještak")]
    [InlineData(AppraisalOrderStatus.AccessCheckRejected, "Prodaja")]
    [InlineData(AppraisalOrderStatus.ProtocolCreated, "Vještak")]
    [InlineData(AppraisalOrderStatus.AppraiserSelected, "Vještak")]
    [InlineData(AppraisalOrderStatus.DocumentsGenerated, "Vještak")]
    [InlineData(AppraisalOrderStatus.OrderSentToAppraiser, "Kolateral oficir")]
    [InlineData(AppraisalOrderStatus.AdditionalPaymentRequested, "Vještak")]
    [InlineData(AppraisalOrderStatus.AdditionalPaymentCompleted, "Kolateral oficir")]
    [InlineData(AppraisalOrderStatus.AppraisalInProgress, "Kolateral oficir")]
    [InlineData(AppraisalOrderStatus.AppraisalReceived, "Kolateral oficir")]
    [InlineData(AppraisalOrderStatus.COApproved, "Prodaja")]
    [InlineData(AppraisalOrderStatus.ReadyForProcedure, "Prodaja")]
    [InlineData(AppraisalOrderStatus.Completed, "—")]
    [InlineData(AppraisalOrderStatus.Cancelled, "—")]
    public void NextResponsibleRole_FL_ReturnsExpected(AppraisalOrderStatus status, string expected)
    {
        var result = OrderWorkflowRouting.NextResponsibleRole(WorkflowType.FizickaLica, status);
        Assert.Equal(expected, result);
    }

    [Theory]
    [InlineData(AppraisalOrderStatus.DocumentationReviewInProgress, "Kolateral oficir")]
    [InlineData(AppraisalOrderStatus.DocumentationApproved, "Kolateral oficir")]
    public void NextResponsibleRole_PL_RoutesThroughCO(AppraisalOrderStatus status, string expected)
    {
        var result = OrderWorkflowRouting.NextResponsibleRole(WorkflowType.PravnaLica, status);
        Assert.Equal(expected, result);
    }

    [Fact]
    public void NextResponsibleRole_FL_vs_PL_DiffersOnlyForDocReviewAndApproved()
    {
        var flDocReview = OrderWorkflowRouting.NextResponsibleRole(
            WorkflowType.FizickaLica, AppraisalOrderStatus.DocumentationReviewInProgress);
        var plDocReview = OrderWorkflowRouting.NextResponsibleRole(
            WorkflowType.PravnaLica, AppraisalOrderStatus.DocumentationReviewInProgress);
        Assert.NotEqual(flDocReview, plDocReview);
        Assert.Equal("Vještak", flDocReview);
        Assert.Equal("Kolateral oficir", plDocReview);

        var flDocApproved = OrderWorkflowRouting.NextResponsibleRole(
            WorkflowType.FizickaLica, AppraisalOrderStatus.DocumentationApproved);
        var plDocApproved = OrderWorkflowRouting.NextResponsibleRole(
            WorkflowType.PravnaLica, AppraisalOrderStatus.DocumentationApproved);
        Assert.NotEqual(flDocApproved, plDocApproved);
        Assert.Equal("Vještak", flDocApproved);
        Assert.Equal("Kolateral oficir", plDocApproved);
    }

    [Fact]
    public void NextResponsibleRole_NullWorkflowType_DefaultsToFL()
    {
        var docReviewNull = OrderWorkflowRouting.NextResponsibleRole(
            null, AppraisalOrderStatus.DocumentationReviewInProgress);
        var docReviewFL = OrderWorkflowRouting.NextResponsibleRole(
            WorkflowType.FizickaLica, AppraisalOrderStatus.DocumentationReviewInProgress);
        Assert.Equal(docReviewFL, docReviewNull);

        var docApprovedNull = OrderWorkflowRouting.NextResponsibleRole(
            null, AppraisalOrderStatus.DocumentationApproved);
        var docApprovedFL = OrderWorkflowRouting.NextResponsibleRole(
            WorkflowType.FizickaLica, AppraisalOrderStatus.DocumentationApproved);
        Assert.Equal(docApprovedFL, docApprovedNull);
    }

    [Fact]
    public void NextResponsibleRole_UnknownStatus_ReturnsDash()
    {
        var result = OrderWorkflowRouting.NextResponsibleRole(WorkflowType.FizickaLica, (AppraisalOrderStatus)9999);
        Assert.Equal("—", result);
    }

    [Theory]
    [InlineData(AppraisalOrderStatus.Draft)]
    [InlineData(AppraisalOrderStatus.SubmittedBySales)]
    [InlineData(AppraisalOrderStatus.AcceptedByCA)]
    [InlineData(AppraisalOrderStatus.ReturnedForCorrection)]
    [InlineData(AppraisalOrderStatus.CorrectionSubmitted)]
    [InlineData(AppraisalOrderStatus.AccessCheckRequested)]
    [InlineData(AppraisalOrderStatus.AccessCheckApproved)]
    [InlineData(AppraisalOrderStatus.AccessCheckRejected)]
    [InlineData(AppraisalOrderStatus.ProtocolCreated)]
    [InlineData(AppraisalOrderStatus.AppraiserSelected)]
    [InlineData(AppraisalOrderStatus.DocumentsGenerated)]
    [InlineData(AppraisalOrderStatus.OrderSentToAppraiser)]
    [InlineData(AppraisalOrderStatus.AdditionalPaymentRequested)]
    [InlineData(AppraisalOrderStatus.AdditionalPaymentCompleted)]
    [InlineData(AppraisalOrderStatus.AppraisalInProgress)]
    [InlineData(AppraisalOrderStatus.AppraisalReceived)]
    [InlineData(AppraisalOrderStatus.COApproved)]
    [InlineData(AppraisalOrderStatus.ReadyForProcedure)]
    [InlineData(AppraisalOrderStatus.Completed)]
    [InlineData(AppraisalOrderStatus.Cancelled)]
    public void NextResponsibleRole_NonBranchingStatuses_SameForFLAndPL(AppraisalOrderStatus status)
    {
        if (status == AppraisalOrderStatus.DocumentationReviewInProgress ||
            status == AppraisalOrderStatus.DocumentationApproved)
            return;

        var fl = OrderWorkflowRouting.NextResponsibleRole(WorkflowType.FizickaLica, status);
        var pl = OrderWorkflowRouting.NextResponsibleRole(WorkflowType.PravnaLica, status);
        Assert.Equal(fl, pl);
    }

    // ── Constants ────────────────────────────────────────────────────────────

    [Fact]
    public void Constants_AreExpectedValues()
    {
        Assert.Equal("Prodaja", OrderWorkflowRouting.Prodaja);
        Assert.Equal("Kolateral administrator", OrderWorkflowRouting.CA);
        Assert.Equal("Kolateral oficir", OrderWorkflowRouting.CO);
        Assert.Equal("Vještak", OrderWorkflowRouting.Vjestak);
    }

    // ── Terminal statuses ────────────────────────────────────────────────────

    [Theory]
    [InlineData(AppraisalOrderStatus.Completed)]
    [InlineData(AppraisalOrderStatus.Cancelled)]
    public void TerminalStatuses_ReturnDashForBothOwnerAndNext(AppraisalOrderStatus status)
    {
        Assert.Equal("—", OrderWorkflowRouting.CurrentOwnerRole(WorkflowType.FizickaLica, status));
        Assert.Equal("—", OrderWorkflowRouting.CurrentOwnerRole(WorkflowType.PravnaLica, status));
        Assert.Equal("—", OrderWorkflowRouting.NextResponsibleRole(WorkflowType.FizickaLica, status));
        Assert.Equal("—", OrderWorkflowRouting.NextResponsibleRole(WorkflowType.PravnaLica, status));
    }

    // ── Every enum value is covered ──────────────────────────────────────────

    [Fact]
    public void CurrentOwnerRole_CoversAllDefinedStatuses()
    {
        foreach (var status in Enum.GetValues<AppraisalOrderStatus>())
        {
            var result = OrderWorkflowRouting.CurrentOwnerRole(WorkflowType.FizickaLica, status);
            Assert.False(string.IsNullOrEmpty(result));
        }
    }

    [Fact]
    public void NextResponsibleRole_CoversAllDefinedStatuses()
    {
        foreach (var status in Enum.GetValues<AppraisalOrderStatus>())
        {
            var result = OrderWorkflowRouting.NextResponsibleRole(WorkflowType.FizickaLica, status);
            Assert.False(string.IsNullOrEmpty(result));
        }
    }
}
