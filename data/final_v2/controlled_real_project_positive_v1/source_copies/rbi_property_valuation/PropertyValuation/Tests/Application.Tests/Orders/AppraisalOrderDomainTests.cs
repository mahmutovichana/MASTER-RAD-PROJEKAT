#pragma warning disable CS0618
using RBBH.CollateralAppraisal.Domain.Orders;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Orders;

public sealed class AppraisalOrderDomainTests
{
    private static AppraisalOrder MakeDraftOrder() =>
        AppraisalOrder.Create(
            orderNumber:              "PN-2026-000001",
            title:                    "Narudžba procjene za APP-stan za klijenta Test grad Sarajevo",
            clientName:               "Test Klijent",
            clientType:               "FL",
            clientIdentifier:         "1234567890123",
            contactName:              "Kontakt Osoba",
            contactPhone:             "061-123-456",
            contactEmail:             "kontakt@test.ba",
            city:                     "Sarajevo",
            branch:                   "POS_SARAJEVO_CENTAR",
            branchAddress:            "Titova 1, Sarajevo",
            propertyAddress:          "Obala 1, Sarajevo",
            collateralTypeId:         1,
            combinedCollateralTypeId: null,
            createdByUserId:          "user-1",
            createdByRole:            "AM",
            createdByName:            "Test Korisnik",
            deliveryContactName:      "Dostava Osoba",
            amRecipientName:          "AM Primalac");

    // ── Create tests ──────────────────────────────────────────────────────────

    [Fact]
    public void Create_SetsStatusToDraft()
    {
        var order = MakeDraftOrder();
        Assert.Equal(AppraisalOrderStatus.Draft, order.Status);
    }

    [Fact]
    public void Create_SetsAllRequiredFields()
    {
        var order = MakeDraftOrder();

        Assert.Equal("PN-2026-000001",   order.OrderNumber);
        Assert.Equal("Test Klijent",       order.ClientName);
        Assert.Equal("Sarajevo",           order.City);
        Assert.Equal("AM",                 order.CreatedByRole);
        Assert.False(order.IsDeleted);
    }

    [Fact]
    public void Create_WithCombinedCollateral_SetsCombinedId()
    {
        var order = AppraisalOrder.Create(
            "PN-2026-000002", "title", "Klijent", null, null,
            "Kontakt", "061-000-000", null,
            "Tuzla", "POS_TUZLA", null, null,
            collateralTypeId: 1,
            combinedCollateralTypeId: 5,
            createdByUserId: "user-2",
            createdByRole: "SM",
            createdByName: "Test Korisnik 2",
            deliveryContactName: "Dostava Osoba",
            amRecipientName: "AM Primalac");

        Assert.Equal(5, order.CombinedCollateralTypeId);
    }

    // ── Submit tests ──────────────────────────────────────────────────────────

    [Fact]
    public void Submit_ChangesStatusToSubmittedBySales()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;

        order.Submit(now);

        Assert.Equal(AppraisalOrderStatus.SubmittedBySales, order.Status);
        Assert.Equal(now, order.SubmittedAt);
    }

    [Fact]
    public void Submit_SetsUpdatedAt()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;

        order.Submit(now);

        Assert.Equal(now, order.UpdatedAt);
    }

    // ── UpdateDraft tests ─────────────────────────────────────────────────────

    [Fact]
    public void UpdateDraft_ChangesTitle()
    {
        var order   = MakeDraftOrder();
        var newTitle = "Novi naslov";
        var now     = DateTime.UtcNow;

        order.UpdateDraft(
            newTitle, "Novi Klijent", null, null,
            null, null, null,
            "Mostar", null, null, null,
            1, null,
            null, null, now);

        Assert.Equal(newTitle,     order.Title);
        Assert.Equal("Novi Klijent", order.ClientName);
        Assert.Equal("Mostar",     order.City);
    }

    // ── SoftDelete tests ──────────────────────────────────────────────────────

    [Fact]
    public void SoftDelete_SetsIsDeletedAndDeletedAt()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;

        order.SoftDelete("user-1", now);

        Assert.True(order.IsDeleted);
        Assert.Equal(now,      order.DeletedAt);
        Assert.Equal("user-1", order.DeletedByUserId);
    }

    // ── State machine tests ───────────────────────────────────────────────────

    [Fact]
    public void AcceptByCA_ChangesStatusToAcceptedByCA()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;
        order.Submit(now);

        order.AcceptByCA("ca-user-1", "Test CA", now);

        Assert.Equal(AppraisalOrderStatus.AcceptedByCA, order.Status);
        Assert.Equal("ca-user-1", order.AcceptedByCAUserId);
        Assert.Equal("Test CA", order.AcceptedByCAName);
        Assert.Equal(DocumentationReviewStatus.NijePregledano, order.DocumentationReviewStatus);
    }

    // ── Misc setters ──────────────────────────────────────────────────────────

    [Fact]
    public void UpdateTitle_ChangesTitleAndUpdatedAt()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;

        order.UpdateTitle("Novi naslov narudžbe", now);

        Assert.Equal("Novi naslov narudžbe", order.Title);
        Assert.Equal(now, order.UpdatedAt);
    }

    [Fact]
    public void ChangeStatus_ChangesStatusAndUpdatedAt()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;

        order.ChangeStatus(AppraisalOrderStatus.ProtocolCreated, now);

        Assert.Equal(AppraisalOrderStatus.ProtocolCreated, order.Status);
        Assert.Equal(now, order.UpdatedAt);
    }

    [Fact]
    public void SetInternalNote_SetsNoteAndUpdatedAt()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;

        order.SetInternalNote("Interna napomena", now);

        Assert.Equal("Interna napomena", order.InternalNote);
        Assert.Equal(now, order.UpdatedAt);
    }

    // ── CO odobrenje finalne procjene (US 93/94) ────────────────────────────────

    [Fact]
    public void SetFinalAppraisalDocument_SetsDocumentIdAndStatus()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, now);

        order.SetFinalAppraisalDocument(documentId: 42, now);

        Assert.Equal(42, order.FinalAppraisalDocumentId);
        Assert.Equal(AppraisalOrderStatus.AppraisalReceived, order.Status);
        Assert.Equal(now, order.UpdatedAt);
    }

    [Fact]
    public void ApproveByCO_SetsApprovalFieldsAndStatus()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, now);

        order.ApproveByCO("co-user-1", now);

        Assert.Equal(now,        order.CoApprovedAt);
        Assert.Equal("co-user-1", order.CoApprovedByUserId);
        Assert.Equal(now,        order.ReadyForProcedureAt);
        Assert.Equal(AppraisalOrderStatus.ReadyForProcedure, order.Status);
        Assert.Equal(now,        order.UpdatedAt);
    }

    [Fact]
    public void ConfirmOriginalReceived_SetsReceivedFieldsAndStatus()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;
        order.ChangeStatus(AppraisalOrderStatus.ReadyForProcedure, now);

        order.ConfirmOriginalReceived("user-1", now);

        Assert.Equal(now,      order.OriginalReceivedAt);
        Assert.Equal("user-1", order.OriginalReceivedByUserId);
        Assert.Equal(AppraisalOrderStatus.Completed, order.Status);
        Assert.Equal(now,      order.UpdatedAt);
    }

    [Fact]
    public void RecordAppraiserReminder_IncrementsCountAndSetsLastSentAt()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;

        order.RecordAppraiserReminder(now);

        Assert.Equal(1,   order.AppraiserReminderCount);
        Assert.Equal(now, order.AppraiserReminderLastSentAt);
        Assert.Equal(now, order.UpdatedAt);

        order.RecordAppraiserReminder(now.AddMinutes(1));

        Assert.Equal(2, order.AppraiserReminderCount);
        Assert.Equal(now.AddMinutes(1), order.AppraiserReminderLastSentAt);
    }

    [Fact]
    public void MarkOpinionsCompleted_SetsOpinionsCompletedAt()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;

        order.MarkOpinionsCompleted(now);

        Assert.Equal(now, order.OpinionsCompletedAt);
        Assert.Equal(now, order.UpdatedAt);
    }

    [Fact]
    public void SendToAppraiser_SetsOrderSentToAppraiserAt()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;
        order.ChangeStatus(AppraisalOrderStatus.AppraiserSelected, now);

        order.SendToAppraiser(now);

        Assert.Equal(AppraisalOrderStatus.OrderSentToAppraiser, order.Status);
        Assert.Equal(now, order.OrderSentToAppraiserAt);
    }

    [Fact]
    public void ReturnForRework_SetsCorrectionRequestedAt()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, now);

        order.ReturnForRework(now);

        Assert.Equal(AppraisalOrderStatus.AppraisalReturnedForRework, order.Status);
        Assert.Equal(now, order.CorrectionRequestedAt);
        Assert.Null(order.FinalAppraisalDocumentId);
    }

    [Fact]
    public void SubmitReworkedAppraisal_SetsCorrectedAppraisalReceivedAt()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReturnedForRework, now);

        order.SubmitReworkedAppraisal(42, now);

        Assert.Equal(AppraisalOrderStatus.AppraisalReceived, order.Status);
        Assert.Equal(42, order.FinalAppraisalDocumentId);
        Assert.Equal(now, order.CorrectedAppraisalReceivedAt);
    }

    [Fact]
    public void SetFinalAppraisalDocument_SetsAppraisalDeliveredToCoAt()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, now);

        order.SetFinalAppraisalDocument(99, now);

        Assert.Equal(99, order.FinalAppraisalDocumentId);
        Assert.Equal(now, order.AppraisalDeliveredToCoAt);
    }

    [Fact]
    public void SubmitCorrection_SetsDocumentationSupplementAt()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;
        order.ChangeStatus(AppraisalOrderStatus.ReturnedForCorrection, now);

        order.SubmitCorrection(now);

        Assert.Equal(AppraisalOrderStatus.CorrectionSubmitted, order.Status);
        Assert.Equal(now, order.DocumentationSupplementAt);
    }

    [Fact]
    public void SetAppraisalFee_StoresValue()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;

        order.SetAppraisalFee(350.50m, now);

        Assert.Equal(350.50m, order.AppraisalFee);
    }

    [Fact]
    public void SetCollateralStatus_StoresValue()
    {
        var order = MakeDraftOrder();
        var now   = DateTime.UtcNow;

        order.SetCollateralStatus("Novoponudjeni", now);

        Assert.Equal("Novoponudjeni", order.CollateralStatus);
    }
}
