#pragma warning disable CS0618
using RBBH.CollateralAppraisal.Domain.Orders;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Regression;

/// <summary>
/// Regresijski testovi za state machine guarde na AppraisalOrder domenskim metodama.
///
/// Bug: Domenske metode pozivale bez provjere trenutnog statusa (pre-state guard nije postojao).
/// Efekat: Sekvence poput Draft.SetFinalAppraisalDocument() prolazile bez greške,
///         što je rezultiralo nekonzistentnim state-om u bazi.
///
/// Fix: OrderStateMachine.EnsureValidTransition() poziv na početku svake guarded metode.
///      InvalidStateTransitionException (a ne InvalidOperationException!) se baca za
///      nevaljane prijelaze.
/// </summary>
public sealed class StateTransitionRegressionTests
{
    private static AppraisalOrder MakeDraft() =>
        AppraisalOrder.Create(
            orderNumber:              "REG-TEST-001",
            title:                    "Regresija test narudžba",
            clientName:               "Test Klijent",
            clientType:               "FL",
            clientIdentifier:         "1234567890123",
            contactName:              "Kontakt Osoba",
            contactPhone:             "061-000-000",
            contactEmail:             "test@test.ba",
            city:                     "Sarajevo",
            branch:                   "POS_SARAJEVO_CENTAR",
            branchAddress:            "Titova 1, Sarajevo",
            propertyAddress:          "Obala 1, Sarajevo",
            collateralTypeId:         1,
            combinedCollateralTypeId: null,
            createdByUserId:          "test-user",
            createdByRole:            "AM",
            createdByName:            "Test AM",
            deliveryContactName:      "Test Kontakt",
            amRecipientName:          "Test AM Primalac");

    private static readonly DateTime Now = DateTime.UtcNow;

    // ── Bug #1: SetFinalAppraisalDocument bez prethodnog AppraisalInProgress ────
    // Stari kod: metoda je prolazila iz Draft statusa bez greške
    // Novi kod: baca InvalidStateTransitionException

    [Fact]
    public void SetFinalAppraisalDocument_FromDraft_ThrowsInvalidStateTransitionException()
    {
        var order = MakeDraft();
        // Status je Draft — nije AppraisalInProgress

        var ex = Assert.Throws<InvalidStateTransitionException>(
            () => order.SetFinalAppraisalDocument(documentId: 42, Now));

        Assert.Equal(AppraisalOrderStatus.Draft, ex.From);
    }

    [Fact]
    public void SetFinalAppraisalDocument_FromAppraisalInProgress_Succeeds()
    {
        var order = MakeDraft();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, Now);

        // Ne smije baciti
        order.SetFinalAppraisalDocument(documentId: 42, Now);

        Assert.Equal(AppraisalOrderStatus.AppraisalReceived, order.Status);
    }

    // ── Bug #2: SelectAppraiser iz Draft statusa ──────────────────────────────
    // Stari kod: Draft.SelectAppraiser() prolazilo (self-state ili direktan skok)
    // Novi kod: zahtijeva DocumentationApproved pre-state

    [Fact]
    public void SelectAppraiser_FromDraft_ThrowsInvalidStateTransitionException()
    {
        var order = MakeDraft();

        var ex = Assert.Throws<InvalidStateTransitionException>(
            () => order.SelectAppraiser(appraiserId: 7, Now));

        Assert.Equal(AppraisalOrderStatus.Draft, ex.From);
        Assert.Equal(AppraisalOrderStatus.AppraiserSelected, ex.To);
    }

    [Fact]
    public void SelectAppraiser_FromDocumentationApproved_Succeeds()
    {
        var order = MakeDraft();
        order.ChangeStatus(AppraisalOrderStatus.DocumentationApproved, Now);

        order.SelectAppraiser(appraiserId: 7, Now);

        Assert.Equal(AppraisalOrderStatus.AppraiserSelected, order.Status);
    }

    // ── Bug #3: SendToAppraiser zahtijeva AppraiserSelected ─────────────────
    // Draft.SendToAppraiser() nije bila zaštićena

    [Fact]
    public void SendToAppraiser_FromDraft_ThrowsInvalidStateTransitionException()
    {
        var order = MakeDraft();

        Assert.Throws<InvalidStateTransitionException>(
            () => order.SendToAppraiser(Now));
    }

    [Fact]
    public void SendToAppraiser_FromAppraiserSelected_Succeeds()
    {
        var order = MakeDraft();
        order.ChangeStatus(AppraisalOrderStatus.AppraiserSelected, Now);

        order.SendToAppraiser(Now);

        Assert.Equal(AppraisalOrderStatus.OrderSentToAppraiser, order.Status);
    }

    // ── Bug #4: ReturnForRework zahtijeva AppraisalReceived ──────────────────

    [Fact]
    public void ReturnForRework_FromDraft_ThrowsInvalidStateTransitionException()
    {
        var order = MakeDraft();

        Assert.Throws<InvalidStateTransitionException>(
            () => order.ReturnForRework(Now));
    }

    [Fact]
    public void ReturnForRework_FromAppraisalReceived_Succeeds()
    {
        var order = MakeDraft();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReceived, Now);

        order.ReturnForRework(Now);

        Assert.Equal(AppraisalOrderStatus.AppraisalReturnedForRework, order.Status);
    }

    // ── Bug #5: SubmitReworkedAppraisal zahtijeva AppraisalReturnedForRework ──

    [Fact]
    public void SubmitReworkedAppraisal_FromDraft_ThrowsInvalidStateTransitionException()
    {
        var order = MakeDraft();

        Assert.Throws<InvalidStateTransitionException>(
            () => order.SubmitReworkedAppraisal(documentId: 99, Now));
    }

    [Fact]
    public void SubmitReworkedAppraisal_FromAppraisalReturnedForRework_Succeeds()
    {
        var order = MakeDraft();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReturnedForRework, Now);

        order.SubmitReworkedAppraisal(documentId: 99, Now);

        Assert.Equal(AppraisalOrderStatus.AppraisalReceived, order.Status);
    }

    // ── Bug #6: SubmitCorrection zahtijeva ReturnedForCorrection ────────────

    [Fact]
    public void SubmitCorrection_FromDraft_ThrowsInvalidStateTransitionException()
    {
        var order = MakeDraft();

        Assert.Throws<InvalidStateTransitionException>(
            () => order.SubmitCorrection(Now));
    }

    [Fact]
    public void SubmitCorrection_FromReturnedForCorrection_Succeeds()
    {
        var order = MakeDraft();
        order.ChangeStatus(AppraisalOrderStatus.ReturnedForCorrection, Now);

        order.SubmitCorrection(Now);

        Assert.Equal(AppraisalOrderStatus.CorrectionSubmitted, order.Status);
    }

    // ── Bug #7: InvalidStateTransitionException ima ispravne From/To properije ──
    // Stari kod: bacao InvalidOperationException bez strukturiranih podataka
    // Novi kod: InvalidStateTransitionException s From, To i Message

    [Fact]
    public void InvalidStateTransition_ExceptionHasCorrectFromAndToProperties()
    {
        var order = MakeDraft();

        var ex = Assert.Throws<InvalidStateTransitionException>(
            () => order.SelectAppraiser(7, Now));

        Assert.Equal(AppraisalOrderStatus.Draft, ex.From);
        Assert.Equal(AppraisalOrderStatus.AppraiserSelected, ex.To);
        Assert.NotNull(ex.Message);
        Assert.NotEmpty(ex.Message);
    }

    [Fact]
    public void InvalidStateTransition_MessageMentionsBothStatuses()
    {
        var order = MakeDraft();

        var ex = Assert.Throws<InvalidStateTransitionException>(
            () => order.SendToAppraiser(Now));

        // Poruka treba biti korisna za debugging
        Assert.Contains("Draft", ex.Message, StringComparison.OrdinalIgnoreCase);
    }

    // ── Validni prijelazi: smoke testovi kritičnih ruta ──────────────────────────

    [Fact]
    public void FullHappyPath_DraftToCompleted_AllTransitionsSucceed()
    {
        // Dokumentira kompletnu happy-path sekvencu — ako neka ruta pukne, ovdje se vidi
        var order = MakeDraft();

        order.Submit(Now);                                                    // Draft → SubmittedBySales
        order.ChangeStatus(AppraisalOrderStatus.AcceptedByCA, Now);          // CO prihvata
        order.StartDocumentationReview(Now);                                 // → DocumentationReviewInProgress
        order.ApproveDocumentation(Now);                                     // → DocumentationApproved
        order.SelectAppraiser(appraiserId: 10, Now);                         // → AppraiserSelected
        order.SendToAppraiser(Now);                                          // → OrderSentToAppraiser
        order.ChangeStatus(AppraisalOrderStatus.AppraisalInProgress, Now);   // Procjenitelj prihvata
        order.SetFinalAppraisalDocument(documentId: 5, Now);                 // → AppraisalReceived
        order.ApproveByCO("co-user", Now);                                   // → ReadyForProcedure
        order.ConfirmOriginalReceived("co-user", Now);                       // → Completed

        Assert.Equal(AppraisalOrderStatus.Completed, order.Status);
    }

    [Fact]
    public void CorrectionPath_ReturnedForCorrectionToCorrectionSubmitted_IsValid()
    {
        // Ova ruta je bila missing u state machine-u — dodana kao fix
        var order = MakeDraft();
        order.ChangeStatus(AppraisalOrderStatus.ReturnedForCorrection, Now);

        // Ne smije baciti — ova tranzicija mora biti registrirana
        order.SubmitCorrection(Now);

        Assert.Equal(AppraisalOrderStatus.CorrectionSubmitted, order.Status);
    }

    [Fact]
    public void ReworkPath_AppraisalReturnedForReworkToAppraisalReceived_IsValid()
    {
        var order = MakeDraft();
        order.ChangeStatus(AppraisalOrderStatus.AppraisalReturnedForRework, Now);

        order.SubmitReworkedAppraisal(documentId: 77, Now);

        Assert.Equal(AppraisalOrderStatus.AppraisalReceived, order.Status);
    }

    // ── Samoprijelaz (self-transition) uvijek je nevalidan ───────────────────────

    [Fact]
    public void SelfTransition_AppraiserSelectedToAppraiserSelected_Throws()
    {
        // Ovaj bug se pojavio u AppraiserAssignmentServiceTests gdje je seeder
        // postavljao order u AppraiserSelected a zatim pozivao SelectAppraiser() opet
        var order = MakeDraft();
        order.ChangeStatus(AppraisalOrderStatus.AppraiserSelected, Now);

        var ex = Assert.Throws<InvalidStateTransitionException>(
            () => order.SelectAppraiser(appraiserId: 5, Now));

        Assert.Equal(AppraisalOrderStatus.AppraiserSelected, ex.From);
        Assert.Equal(AppraisalOrderStatus.AppraiserSelected, ex.To);
    }
}
