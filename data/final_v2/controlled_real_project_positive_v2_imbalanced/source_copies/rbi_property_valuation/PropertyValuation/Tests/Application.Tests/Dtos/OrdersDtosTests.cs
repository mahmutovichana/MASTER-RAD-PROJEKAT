using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Requests;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Dtos;

public sealed class OrdersDtosTests
{
    [Fact]
    public void AppraisalOrderDto_StoresAllProperties()
    {
        var dto = new AppraisalOrderDto(
            Id: 1,
            OrderNumber: "PN-2026-000001",
            Title: "Naslov",
            Status: "Draft",
            StatusCode: 0,
            WorkflowType: null,
            CurrentOwnerRole: null,
            NextResponsibleRole: null,
            ClientName: "Klijent",
            ClientType: "FL",
            ClientIdentifier: "1234567890123",
            CollateralTypeId: 1,
            CollateralTypeLabel: "Stan",
            CombinedCollateralTypeId: null,
            CombinedCollateralTypeLabel: null,
            City: "Sarajevo",
            PropertyAddress: "Adresa 1",
            PropertyCity: null,
            Branch: "POS_SARAJEVO_CENTAR",
            BranchAddress: "Titova 1",
            ContactName: "Kontakt",
            ContactPhone: "061-123-456",
            ContactEmail: "kontakt@test.ba",
            DeliveryContactName: "Dostava",
            AmRecipientName: "AM Primalac",
            CreatedByUserId: "user-1",
            CreatedByRole: "AM",
            CreatedByName: "Korisnik",
            CreatedAt: new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc),
            UpdatedAt: null,
            SubmittedAt: null,
            InternalNote: null,
            RequestReceivedAt: null,
            RequestSentAt: null,
            SquareMetersCommercial: null,
            SquareMetersResidential: null,
            Capabilities: new OrderCapabilitiesDto(CanEdit: true, CanSubmit: true, CanCancel: false),
            AcceptedByCAUserId: "ca-user-1",
            AcceptedAt: new DateTime(2026, 6, 2, 0, 0, 0, DateTimeKind.Utc));


        Assert.Equal(1, dto.Id);
        Assert.Equal("PN-2026-000001", dto.OrderNumber);
        Assert.Equal("Draft", dto.Status);
        Assert.True(dto.Capabilities.CanEdit);
        Assert.True(dto.Capabilities.CanSubmit);
        Assert.False(dto.Capabilities.CanCancel);
        Assert.Equal("ca-user-1", dto.AcceptedByCAUserId);
        Assert.Equal(new DateTime(2026, 6, 2, 0, 0, 0, DateTimeKind.Utc), dto.AcceptedAt);
    }

    [Fact]
    public void AppraisalOrderListItemDto_StoresAllProperties()
    {
        var dto = new AppraisalOrderListItemDto(
            Id: 1,
            OrderNumber: "PN-2026-000001",
            Title: "Naslov",
            Status: "Draft",
            StatusCode: 0,
            WorkflowType: null,
            ClientName: "Klijent",
            CollateralTypeLabel: "Stan",
            CombinedCollateralTypeLabel: null,
            City: "Sarajevo",
            CreatedByRole: "AM",
            CreatedAt: new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc),
            SubmittedAt: null,
            Branch: "POS_SARAJEVO_CENTAR",
            UpdatedAt: null);

        Assert.Equal("PN-2026-000001", dto.OrderNumber);
        Assert.Equal("Klijent", dto.ClientName);
        Assert.Equal("Sarajevo", dto.City);
    }

    [Fact]
    public void OrderSummaryDto_StoresCounts()
    {
        var dto = new OrderSummaryDto(Total: 10, Draft: 2, SubmittedBySales: 3, InProgress: 4, Completed: 1, Cancelled: 0);

        Assert.Equal(10, dto.Total);
        Assert.Equal(2,  dto.Draft);
        Assert.Equal(3,  dto.SubmittedBySales);
        Assert.Equal(4,  dto.InProgress);
        Assert.Equal(1,  dto.Completed);
        Assert.Equal(0,  dto.Cancelled);
    }

    [Fact]
    public void ProtocolEntryDto_StoresAllProperties()
    {
        var dto = new ProtocolEntryDto(
            Id: 1,
            OrderId: 5,
            OrderNumber: "PN-2026-000005",
            OrderTitle: "Naslov",
            ProtocolNumber: "2026/00001",
            ProtocolYear: 2026,
            ProtocolSequence: 1,
            Status: "Active",
            GeneratedAt: new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc),
            GeneratedByUserId: "user-1",
            ClientName: "Klijent",
            City: "Sarajevo",
            Branch: "POS_SARAJEVO_CENTAR",
            OrderStatus: "ProtocolCreated",
            OrderStatusCode: 80,
            CollateralTypeLabel: "Stan",
            CombinedCollateralTypeLabel: null,
            ClientType: "FL",
            ClientIdentifier: "1234567890123",
            ContactName: "Kontakt",
            ContactPhone: "061-123-456",
            PropertyAddress: "Adresa 1",
            BranchAddress: "Titova 1",
            CreatedByName: "Korisnik",
            CreatedByRole: "AM",
            DeliveryContactName: "Dostava",
            AmRecipientName: "AM Primalac");

        Assert.Equal("2026/00001", dto.ProtocolNumber);
        Assert.Equal(2026, dto.ProtocolYear);
        Assert.Equal(1,    dto.ProtocolSequence);
        Assert.Equal("Active", dto.Status);
        Assert.Equal("Klijent", dto.ClientName);
    }

    [Fact]
    public void WorkflowTaskDto_StoresAllProperties()
    {
        var dto = new WorkflowTaskDto(
            Id: 1,
            OrderId: 5,
            OrderNumber: "PN-2026-000005",
            OrderTitle: "Naslov",
            TaskType: "AcceptCAOrder",
            TaskTypeCode: 1,
            Title: "Prihvati narudžbu",
            Description: "opis",
            AssignedRole: "CA",
            AssignedUserId: null,
            Status: "Open",
            StatusCode: 0,
            IsLocked: false,
            DueDate: null,
            AcceptedAt: null,
            AcceptedByUserId: null,
            CompletedAt: null,
            CompletedByUserId: null,
            Comment: null,
            CreatedAt: new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc));

        Assert.Equal("AcceptCAOrder", dto.TaskType);
        Assert.Equal("Open",          dto.Status);
        Assert.False(dto.IsLocked);
    }

    [Fact]
    public void FinalAppraisalDto_StoresAllProperties()
    {
        var dto = new FinalAppraisalDto(
            OrderId: 5,
            DocumentId: 42,
            OriginalFileName: "procjena.pdf",
            ContentType: "application/pdf",
            FileSize: 1024,
            UploadedAt: new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc),
            UploadedByUserId: "user-1",
            DownloadUrl: "/api/orders/5/final-appraisal");

        Assert.Equal(5,  dto.OrderId);
        Assert.Equal(42, dto.DocumentId);
        Assert.Equal("procjena.pdf", dto.OriginalFileName);
    }

    [Fact]
    public void ApproveFinalAppraisalResultDto_StoresAllProperties()
    {
        var now = new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc);

        var dto = new ApproveFinalAppraisalResultDto(
            OrderId: 5,
            OrderNumber: "PN-2026-000005",
            Status: "ReadyForProcedure",
            CoApprovedAt: now,
            CoApprovedByUserId: "co-user-1",
            ReadyForProcedureAt: now,
            FinalAppraisalDocumentId: 42,
            DownloadUrl: "/api/orders/5/final-appraisal",
            NotificationSent: true,
            Message: "Odobreno");

        Assert.Equal("ReadyForProcedure", dto.Status);
        Assert.True(dto.NotificationSent);
        Assert.Equal("co-user-1", dto.CoApprovedByUserId);
    }

    [Fact]
    public void CreateOrderRequest_StoresAllProperties()
    {
        var request = new CreateOrderRequest(
            ClientName: "Klijent",
            ClientType: "FL",
            ClientIdentifier: "1234567890123",
            CollateralTypeId: 1,
            CombinedCollateralTypeId: null,
            City: "Sarajevo",
            PropertyAddress: "Adresa 1",
            Branch: "POS_SARAJEVO_CENTAR",
            BranchAddress: "Titova 1",
            ContactName: "Kontakt",
            ContactPhone: "061-123-456",
            ContactEmail: "kontakt@test.ba",
            InternalNote: null,
            DeliveryContactName: "Dostava",
            AmRecipientName: "AM Primalac");

        Assert.Equal("Klijent",  request.ClientName);
        Assert.Equal(1,          request.CollateralTypeId);
        Assert.Equal("Sarajevo", request.City);
    }

    [Fact]
    public void UpdateOrderRequest_AllowsOptionalContactFields()
    {
        var request = new UpdateOrderRequest(
            ClientName: "Klijent",
            ClientType: null,
            ClientIdentifier: null,
            CollateralTypeId: null,
            CombinedCollateralTypeId: null,
            City: null,
            PropertyAddress: null,
            Branch: null,
            BranchAddress: null,
            ContactName: null,
            ContactPhone: null,
            ContactEmail: null,
            InternalNote: null);

        Assert.Equal("Klijent", request.ClientName);
        Assert.Null(request.DeliveryContactName);
        Assert.Null(request.AmRecipientName);
    }

    [Fact]
    public void OrderListRequest_DefaultsApplyExpectedPagingAndSort()
    {
        var request = new OrderListRequest();

        Assert.Equal(1,    request.Page);
        Assert.Equal(20,   request.PageSize);
        Assert.True(request.SortDescending);
        Assert.Null(request.Search);
        Assert.Null(request.Status);
    }

    [Fact]
    public void OrderDetailCapabilitiesDto_StoresAllFlags()
    {
        var capabilities = new OrderDetailCapabilitiesDto(
            CanEdit: true,
            CanSubmit: true,
            CanCancel: false,
            CanApproveFinal: true,
            CanDownloadFinal: false,
            CanConfirmOriginal: true,
            CanRemindAppraiser: false,
            CanRequestCorrection: true,
            CanCompleteReview: false,
            CanSubmitCorrection: true,
            CanAccessCheck: false,
            CanSelectAppraiser: true,
            CanSendToAppraiser: false);

        Assert.True(capabilities.CanEdit);
        Assert.True(capabilities.CanSubmit);
        Assert.False(capabilities.CanCancel);
        Assert.True(capabilities.CanApproveFinal);
        Assert.False(capabilities.CanDownloadFinal);
        Assert.True(capabilities.CanConfirmOriginal);
        Assert.False(capabilities.CanRemindAppraiser);
        Assert.True(capabilities.CanRequestCorrection);
        Assert.False(capabilities.CanCompleteReview);
        Assert.True(capabilities.CanSubmitCorrection);
        Assert.False(capabilities.CanAccessCheck);
        Assert.True(capabilities.CanSelectAppraiser);
        Assert.False(capabilities.CanSendToAppraiser);
    }

    [Fact]
    public void AppraisalOrderDetailDto_StoresAllProperties()
    {
        var now = DateTime.UtcNow;
        var capabilities = new OrderDetailCapabilitiesDto(
            true, true, false, true, false, true, false, true, false, true, false, true, false);

        var dto = new AppraisalOrderDetailDto(
            Id: 1,
            OrderNumber: "PN-2026-000001",
            Title: "Naslov",
            Status: "Draft",
            StatusCode: 0,
            WorkflowType: null,
            CurrentOwnerRole: null,
            NextResponsibleRole: null,
            ClientName: "Klijent",
            ClientType: "FL",
            ClientIdentifier: "0101985100129",
            CollateralTypeId: 10,
            CollateralTypeLabel: "Stan",
            CombinedCollateralTypeId: null,
            CombinedCollateralTypeLabel: null,
            City: "Sarajevo",
            PropertyAddress: "Ulica 1",
            PropertyCity: null,
            Branch: "Centar",
            BranchAddress: "Adresa centra",
            ContactName: "Kontakt",
            ContactPhone: "+38761123456",
            ContactEmail: "kontakt@test.ba",
            CreatedByUserId: "user-1",
            CreatedByRole: "Unosnik",
            CreatedAt: now,
            UpdatedAt: now,
            SubmittedAt: null,
            InternalNote: "Napomena",
            CoApprovedByName: null,
            CoApprovedAt: null,
            OriginalReceivedByName: null,
            OriginalReceivedAt: null,
            AppraiserReminderCount: 2,
            AppraiserReminderLastSentAt: now,
            CorrectionReason: null,
            CorrectionComment: null,
            AccessCheckComment: null,
            AppraiserId: null,
            AppraiserName: null,
            AppraiserCity: null,
            InvoiceSentDate: null,
            InvoiceReceivedDate: null,
            AppraiserVisitDate: null,
            AppraiserRating: null,
            EsgCertificate: null,
            InvoiceWorkflowStatus: null,
            InvoiceUploadedByName: null,
            InvoiceUploadedAt: null,
            InvoiceSentForPaymentByName: null,
            InvoiceSentForPaymentAt: null,
            InvoicePaidByName: null,
            InvoicePaidAt: null,
            InvoiceDocumentId: null,
            AppraisalFee: null,
            CollateralStatus: null,
            ProtocolNumber: null,
            OrderSentToAppraiserAt: null,
            SignedDocumentsReceivedAt: null,
            AppraisalDeliveredToCoAt: null,
            CorrectionRequestedAt: null,
            CorrectedAppraisalReceivedAt: null,
            ReadyForProcedureAt: null,
            AcceptedByCAName: "Test CA",
            DocumentationReviewStatus: "Nije pregledano",
            CreatedByName: "Korisnik",
            Capabilities: capabilities);

        Assert.Equal(1, dto.Id);
        Assert.Equal("PN-2026-000001", dto.OrderNumber);
        Assert.Equal("FL", dto.ClientType);
        Assert.Equal("Stan", dto.CollateralTypeLabel);
        Assert.Equal(2, dto.AppraiserReminderCount);
        Assert.Equal(now, dto.AppraiserReminderLastSentAt);
        Assert.Same(capabilities, dto.Capabilities);
    }

    [Fact]
    public void OriginalReceivedResultDto_StoresAllProperties()
    {
        var now = DateTime.UtcNow;

        var dto = new OriginalReceivedResultDto(
            OrderId: 5,
            OrderNumber: "PN-2026-000005",
            Status: "InProgress",
            OriginalReceivedAt: now,
            OriginalReceivedByUserId: "user-2",
            NotificationsSent: true,
            Message: "Original primljen.");

        Assert.Equal(5, dto.OrderId);
        Assert.Equal("PN-2026-000005", dto.OrderNumber);
        Assert.Equal("InProgress", dto.Status);
        Assert.Equal(now, dto.OriginalReceivedAt);
        Assert.Equal("user-2", dto.OriginalReceivedByUserId);
        Assert.True(dto.NotificationsSent);
        Assert.Equal("Original primljen.", dto.Message);
    }

    // ── AppraisalOrderDetailDto extended coverage ──────────────────────────────

    [Fact]
    public void AppraisalOrderDetailDto_DefaultParameters_HaveExpectedValues()
    {
        var now = DateTime.UtcNow;
        var capabilities = new OrderDetailCapabilitiesDto(
            false, false, false, false, false, false, false, false, false, false, false, false, false);

        var dto = new AppraisalOrderDetailDto(
            Id: 2,
            OrderNumber: "PN-2026-000002",
            Title: "Naslov 2",
            Status: "SubmittedBySales",
            StatusCode: 10,
            WorkflowType: "FizickaLica",
            CurrentOwnerRole: "CA",
            NextResponsibleRole: "CO",
            ClientName: "Klijent 2",
            ClientType: "PL",
            ClientIdentifier: "4200000000000",
            CollateralTypeId: 20,
            CollateralTypeLabel: "Poslovni prostor",
            CombinedCollateralTypeId: 30,
            CombinedCollateralTypeLabel: "Kombinovano",
            City: "Mostar",
            PropertyAddress: "Ulica 2",
            PropertyCity: "Mostar",
            Branch: "POS_MOSTAR",
            BranchAddress: "Adresa Mostar",
            ContactName: "Kontakt 2",
            ContactPhone: "+38762999888",
            ContactEmail: "kontakt2@test.ba",
            CreatedByUserId: "user-2",
            CreatedByRole: "SM",
            CreatedAt: now,
            UpdatedAt: now,
            SubmittedAt: now,
            InternalNote: null,
            CoApprovedByName: "CO Korisnik",
            CoApprovedAt: now,
            OriginalReceivedByName: "Original Korisnik",
            OriginalReceivedAt: now,
            AppraiserReminderCount: 0,
            AppraiserReminderLastSentAt: null,
            CorrectionReason: "Greska",
            CorrectionComment: "Ispravite tabelu",
            AccessCheckComment: "Provjera pristupa OK",
            AppraiserId: 10,
            AppraiserName: "Vjestak Petar",
            AppraiserCity: "Tuzla",
            InvoiceSentDate: now,
            InvoiceReceivedDate: now,
            AppraiserVisitDate: now,
            AppraiserRating: 5,
            EsgCertificate: "A+",
            InvoiceWorkflowStatus: "Uploaded",
            InvoiceUploadedByName: "CA Korisnik",
            InvoiceUploadedAt: now,
            InvoiceSentForPaymentByName: "Finansije",
            InvoiceSentForPaymentAt: now,
            InvoicePaidByName: "Blagajna",
            InvoicePaidAt: now,
            InvoiceDocumentId: 100,
            AppraisalFee: 1500.00m,
            CollateralStatus: "Aktivan",
            ProtocolNumber: "2026/00042",
            OrderSentToAppraiserAt: now,
            SignedDocumentsReceivedAt: now,
            AppraisalDeliveredToCoAt: now,
            CorrectionRequestedAt: now,
            CorrectedAppraisalReceivedAt: now,
            ReadyForProcedureAt: now,
            Capabilities: capabilities);

        // Default parameters should be null when not specified
        Assert.Null(dto.AcceptedByCAName);
        Assert.Null(dto.DocumentationReviewStatus);
        Assert.Null(dto.CreatedByName);
    }

    [Fact]
    public void AppraisalOrderDetailDto_ExplicitDefaultParams_StoreValues()
    {
        var now = DateTime.UtcNow;
        var capabilities = new OrderDetailCapabilitiesDto(
            true, true, true, true, true, true, true, true, true, true, true, true, true);

        var dto = new AppraisalOrderDetailDto(
            Id: 3,
            OrderNumber: "PN-2026-000003",
            Title: "T",
            Status: "Completed",
            StatusCode: 100,
            WorkflowType: null,
            CurrentOwnerRole: null,
            NextResponsibleRole: null,
            ClientName: "K",
            ClientType: null,
            ClientIdentifier: null,
            CollateralTypeId: null,
            CollateralTypeLabel: null,
            CombinedCollateralTypeId: null,
            CombinedCollateralTypeLabel: null,
            City: null,
            PropertyAddress: null,
            PropertyCity: null,
            Branch: null,
            BranchAddress: null,
            ContactName: null,
            ContactPhone: null,
            ContactEmail: null,
            CreatedByUserId: null,
            CreatedByRole: null,
            CreatedAt: now,
            UpdatedAt: null,
            SubmittedAt: null,
            InternalNote: null,
            CoApprovedByName: null,
            CoApprovedAt: null,
            OriginalReceivedByName: null,
            OriginalReceivedAt: null,
            AppraiserReminderCount: 0,
            AppraiserReminderLastSentAt: null,
            CorrectionReason: null,
            CorrectionComment: null,
            AccessCheckComment: null,
            AppraiserId: null,
            AppraiserName: null,
            AppraiserCity: null,
            InvoiceSentDate: null,
            InvoiceReceivedDate: null,
            AppraiserVisitDate: null,
            AppraiserRating: null,
            EsgCertificate: null,
            InvoiceWorkflowStatus: null,
            InvoiceUploadedByName: null,
            InvoiceUploadedAt: null,
            InvoiceSentForPaymentByName: null,
            InvoiceSentForPaymentAt: null,
            InvoicePaidByName: null,
            InvoicePaidAt: null,
            InvoiceDocumentId: null,
            AppraisalFee: null,
            CollateralStatus: null,
            ProtocolNumber: null,
            OrderSentToAppraiserAt: null,
            SignedDocumentsReceivedAt: null,
            AppraisalDeliveredToCoAt: null,
            CorrectionRequestedAt: null,
            CorrectedAppraisalReceivedAt: null,
            ReadyForProcedureAt: null,
            AcceptedByCAName: "CA Korisnik",
            DocumentationReviewStatus: "Odobreno",
            CreatedByName: "Ivan",
            Capabilities: capabilities);

        Assert.Equal("CA Korisnik", dto.AcceptedByCAName);
        Assert.Equal("Odobreno", dto.DocumentationReviewStatus);
        Assert.Equal("Ivan", dto.CreatedByName);
        Assert.Equal(100, dto.StatusCode);
        Assert.Equal("Completed", dto.Status);
    }

    [Fact]
    public void AppraisalOrderDetailDto_AllNullableFields_StoreNullCorrectly()
    {
        var now = DateTime.UtcNow;
        var capabilities = new OrderDetailCapabilitiesDto(
            false, false, false, false, false, false, false, false, false, false, false, false, false);

        var dto = new AppraisalOrderDetailDto(
            Id: 4, OrderNumber: "PN-2026-000004", Title: "T", Status: "Draft", StatusCode: 0,
            WorkflowType: null, CurrentOwnerRole: null, NextResponsibleRole: null,
            ClientName: "K", ClientType: null, ClientIdentifier: null,
            CollateralTypeId: null, CollateralTypeLabel: null,
            CombinedCollateralTypeId: null, CombinedCollateralTypeLabel: null,
            City: null, PropertyAddress: null, PropertyCity: null,
            Branch: null, BranchAddress: null, ContactName: null, ContactPhone: null, ContactEmail: null,
            CreatedByUserId: null, CreatedByRole: null, CreatedAt: now, UpdatedAt: null, SubmittedAt: null,
            InternalNote: null, CoApprovedByName: null, CoApprovedAt: null,
            OriginalReceivedByName: null, OriginalReceivedAt: null,
            AppraiserReminderCount: 0, AppraiserReminderLastSentAt: null,
            CorrectionReason: null, CorrectionComment: null, AccessCheckComment: null,
            AppraiserId: null, AppraiserName: null, AppraiserCity: null,
            InvoiceSentDate: null, InvoiceReceivedDate: null, AppraiserVisitDate: null,
            AppraiserRating: null, EsgCertificate: null,
            InvoiceWorkflowStatus: null, InvoiceUploadedByName: null, InvoiceUploadedAt: null,
            InvoiceSentForPaymentByName: null, InvoiceSentForPaymentAt: null,
            InvoicePaidByName: null, InvoicePaidAt: null, InvoiceDocumentId: null,
            AppraisalFee: null, CollateralStatus: null, ProtocolNumber: null,
            OrderSentToAppraiserAt: null, SignedDocumentsReceivedAt: null,
            AppraisalDeliveredToCoAt: null, CorrectionRequestedAt: null,
            CorrectedAppraisalReceivedAt: null, ReadyForProcedureAt: null,
            Capabilities: capabilities);

        Assert.Null(dto.WorkflowType);
        Assert.Null(dto.CurrentOwnerRole);
        Assert.Null(dto.NextResponsibleRole);
        Assert.Null(dto.ClientType);
        Assert.Null(dto.ClientIdentifier);
        Assert.Null(dto.CollateralTypeId);
        Assert.Null(dto.CollateralTypeLabel);
        Assert.Null(dto.CombinedCollateralTypeId);
        Assert.Null(dto.CombinedCollateralTypeLabel);
        Assert.Null(dto.City);
        Assert.Null(dto.PropertyAddress);
        Assert.Null(dto.PropertyCity);
        Assert.Null(dto.Branch);
        Assert.Null(dto.BranchAddress);
        Assert.Null(dto.ContactName);
        Assert.Null(dto.ContactPhone);
        Assert.Null(dto.ContactEmail);
        Assert.Null(dto.CreatedByUserId);
        Assert.Null(dto.CreatedByRole);
        Assert.Null(dto.UpdatedAt);
        Assert.Null(dto.SubmittedAt);
        Assert.Null(dto.InternalNote);
        Assert.Null(dto.CoApprovedByName);
        Assert.Null(dto.CoApprovedAt);
        Assert.Null(dto.OriginalReceivedByName);
        Assert.Null(dto.OriginalReceivedAt);
        Assert.Null(dto.AppraiserReminderLastSentAt);
        Assert.Null(dto.CorrectionReason);
        Assert.Null(dto.CorrectionComment);
        Assert.Null(dto.AccessCheckComment);
        Assert.Null(dto.AppraiserId);
        Assert.Null(dto.AppraiserName);
        Assert.Null(dto.AppraiserCity);
        Assert.Null(dto.InvoiceSentDate);
        Assert.Null(dto.InvoiceReceivedDate);
        Assert.Null(dto.AppraiserVisitDate);
        Assert.Null(dto.AppraiserRating);
        Assert.Null(dto.EsgCertificate);
        Assert.Null(dto.InvoiceWorkflowStatus);
        Assert.Null(dto.InvoiceUploadedByName);
        Assert.Null(dto.InvoiceUploadedAt);
        Assert.Null(dto.InvoiceSentForPaymentByName);
        Assert.Null(dto.InvoiceSentForPaymentAt);
        Assert.Null(dto.InvoicePaidByName);
        Assert.Null(dto.InvoicePaidAt);
        Assert.Null(dto.InvoiceDocumentId);
        Assert.Null(dto.AppraisalFee);
        Assert.Null(dto.CollateralStatus);
        Assert.Null(dto.ProtocolNumber);
        Assert.Null(dto.OrderSentToAppraiserAt);
        Assert.Null(dto.SignedDocumentsReceivedAt);
        Assert.Null(dto.AppraisalDeliveredToCoAt);
        Assert.Null(dto.CorrectionRequestedAt);
        Assert.Null(dto.CorrectedAppraisalReceivedAt);
        Assert.Null(dto.ReadyForProcedureAt);
        Assert.Equal(0, dto.AppraiserReminderCount);
    }

    [Fact]
    public void AppraisalOrderDetailDto_AllPopulatedFields_StoreValuesCorrectly()
    {
        var now = new DateTime(2026, 6, 10, 12, 0, 0, DateTimeKind.Utc);
        var capabilities = new OrderDetailCapabilitiesDto(
            true, true, true, true, true, true, true, true, true, true, true, true, true);

        var dto = new AppraisalOrderDetailDto(
            Id: 99, OrderNumber: "PN-2026-000099", Title: "Full", Status: "InProgress", StatusCode: 50,
            WorkflowType: "PravnaLica", CurrentOwnerRole: "CA", NextResponsibleRole: "CO",
            ClientName: "Firma d.o.o.", ClientType: "PL", ClientIdentifier: "4200000000000",
            CollateralTypeId: 5, CollateralTypeLabel: "Zemljiste",
            CombinedCollateralTypeId: 6, CombinedCollateralTypeLabel: "Kombinovano",
            City: "Banja Luka", PropertyAddress: "Ulica 99", PropertyCity: "Banja Luka",
            Branch: "POS_BANJA_LUKA", BranchAddress: "Adresa BL",
            ContactName: "Kontakt Full", ContactPhone: "+38765111222", ContactEmail: "full@test.ba",
            CreatedByUserId: "user-99", CreatedByRole: "UB",
            CreatedAt: now, UpdatedAt: now, SubmittedAt: now,
            InternalNote: "Interni komentar",
            CoApprovedByName: "CO Odobritelj", CoApprovedAt: now,
            OriginalReceivedByName: "Primatelj", OriginalReceivedAt: now,
            AppraiserReminderCount: 3, AppraiserReminderLastSentAt: now,
            CorrectionReason: "Greska u tabeli", CorrectionComment: "Molimo ispravite",
            AccessCheckComment: "OK",
            AppraiserId: 42, AppraiserName: "Vjestak Marko", AppraiserCity: "Zenica",
            InvoiceSentDate: now, InvoiceReceivedDate: now, AppraiserVisitDate: now,
            AppraiserRating: 4, EsgCertificate: "B",
            InvoiceWorkflowStatus: "Paid", InvoiceUploadedByName: "Upload user",
            InvoiceUploadedAt: now, InvoiceSentForPaymentByName: "Payment user",
            InvoiceSentForPaymentAt: now, InvoicePaidByName: "Paid user", InvoicePaidAt: now,
            InvoiceDocumentId: 200, AppraisalFee: 2500.50m,
            CollateralStatus: "Aktivan", ProtocolNumber: "2026/00099",
            OrderSentToAppraiserAt: now, SignedDocumentsReceivedAt: now,
            AppraisalDeliveredToCoAt: now, CorrectionRequestedAt: now,
            CorrectedAppraisalReceivedAt: now, ReadyForProcedureAt: now,
            AcceptedByCAName: "CA Accept", DocumentationReviewStatus: "Pregledano",
            CreatedByName: "Kreator", Capabilities: capabilities);

        Assert.Equal(99, dto.Id);
        Assert.Equal("PN-2026-000099", dto.OrderNumber);
        Assert.Equal("Full", dto.Title);
        Assert.Equal("InProgress", dto.Status);
        Assert.Equal(50, dto.StatusCode);
        Assert.Equal("PravnaLica", dto.WorkflowType);
        Assert.Equal("CA", dto.CurrentOwnerRole);
        Assert.Equal("CO", dto.NextResponsibleRole);
        Assert.Equal("Firma d.o.o.", dto.ClientName);
        Assert.Equal("PL", dto.ClientType);
        Assert.Equal("4200000000000", dto.ClientIdentifier);
        Assert.Equal(5, dto.CollateralTypeId);
        Assert.Equal("Zemljiste", dto.CollateralTypeLabel);
        Assert.Equal(6, dto.CombinedCollateralTypeId);
        Assert.Equal("Kombinovano", dto.CombinedCollateralTypeLabel);
        Assert.Equal("Banja Luka", dto.City);
        Assert.Equal("Ulica 99", dto.PropertyAddress);
        Assert.Equal("Banja Luka", dto.PropertyCity);
        Assert.Equal("POS_BANJA_LUKA", dto.Branch);
        Assert.Equal("Adresa BL", dto.BranchAddress);
        Assert.Equal("Kontakt Full", dto.ContactName);
        Assert.Equal("+38765111222", dto.ContactPhone);
        Assert.Equal("full@test.ba", dto.ContactEmail);
        Assert.Equal("user-99", dto.CreatedByUserId);
        Assert.Equal("UB", dto.CreatedByRole);
        Assert.Equal(now, dto.CreatedAt);
        Assert.Equal(now, dto.UpdatedAt);
        Assert.Equal(now, dto.SubmittedAt);
        Assert.Equal("Interni komentar", dto.InternalNote);
        Assert.Equal("CO Odobritelj", dto.CoApprovedByName);
        Assert.Equal(now, dto.CoApprovedAt);
        Assert.Equal("Primatelj", dto.OriginalReceivedByName);
        Assert.Equal(now, dto.OriginalReceivedAt);
        Assert.Equal(3, dto.AppraiserReminderCount);
        Assert.Equal(now, dto.AppraiserReminderLastSentAt);
        Assert.Equal("Greska u tabeli", dto.CorrectionReason);
        Assert.Equal("Molimo ispravite", dto.CorrectionComment);
        Assert.Equal("OK", dto.AccessCheckComment);
        Assert.Equal(42, dto.AppraiserId);
        Assert.Equal("Vjestak Marko", dto.AppraiserName);
        Assert.Equal("Zenica", dto.AppraiserCity);
        Assert.Equal(now, dto.InvoiceSentDate);
        Assert.Equal(now, dto.InvoiceReceivedDate);
        Assert.Equal(now, dto.AppraiserVisitDate);
        Assert.Equal(4, dto.AppraiserRating);
        Assert.Equal("B", dto.EsgCertificate);
        Assert.Equal("Paid", dto.InvoiceWorkflowStatus);
        Assert.Equal("Upload user", dto.InvoiceUploadedByName);
        Assert.Equal(now, dto.InvoiceUploadedAt);
        Assert.Equal("Payment user", dto.InvoiceSentForPaymentByName);
        Assert.Equal(now, dto.InvoiceSentForPaymentAt);
        Assert.Equal("Paid user", dto.InvoicePaidByName);
        Assert.Equal(now, dto.InvoicePaidAt);
        Assert.Equal(200, dto.InvoiceDocumentId);
        Assert.Equal(2500.50m, dto.AppraisalFee);
        Assert.Equal("Aktivan", dto.CollateralStatus);
        Assert.Equal("2026/00099", dto.ProtocolNumber);
        Assert.Equal(now, dto.OrderSentToAppraiserAt);
        Assert.Equal(now, dto.SignedDocumentsReceivedAt);
        Assert.Equal(now, dto.AppraisalDeliveredToCoAt);
        Assert.Equal(now, dto.CorrectionRequestedAt);
        Assert.Equal(now, dto.CorrectedAppraisalReceivedAt);
        Assert.Equal(now, dto.ReadyForProcedureAt);
        Assert.Equal("CA Accept", dto.AcceptedByCAName);
        Assert.Equal("Pregledano", dto.DocumentationReviewStatus);
        Assert.Equal("Kreator", dto.CreatedByName);
    }

    // ── OrderDetailCapabilitiesDto extended coverage ───────────────────────────

    [Fact]
    public void OrderDetailCapabilitiesDto_DefaultParameters_AllFalse()
    {
        var capabilities = new OrderDetailCapabilitiesDto(
            CanEdit: false, CanSubmit: false, CanCancel: false,
            CanApproveFinal: false, CanDownloadFinal: false, CanConfirmOriginal: false,
            CanRemindAppraiser: false, CanRequestCorrection: false, CanCompleteReview: false,
            CanSubmitCorrection: false, CanAccessCheck: false,
            CanSelectAppraiser: false, CanSendToAppraiser: false);

        // Defaulted parameters should be false
        Assert.False(capabilities.CanRequestAdditionalPayment);
        Assert.False(capabilities.CanCompleteAdditionalPayment);
        Assert.False(capabilities.CanGenerateDocuments);
        Assert.False(capabilities.CanSendQuoteRequests);
        Assert.False(capabilities.CanSendThankYou);
        Assert.False(capabilities.CanUploadInvoice);
        Assert.False(capabilities.CanSendInvoiceForPayment);
        Assert.False(capabilities.CanConfirmInvoicePaid);
        Assert.False(capabilities.CanRejectOrder);
        Assert.False(capabilities.CanReturnForRework);
    }

    [Fact]
    public void OrderDetailCapabilitiesDto_ExplicitDefaultParams_StoreTrue()
    {
        var capabilities = new OrderDetailCapabilitiesDto(
            CanEdit: false, CanSubmit: false, CanCancel: false,
            CanApproveFinal: false, CanDownloadFinal: false, CanConfirmOriginal: false,
            CanRemindAppraiser: false, CanRequestCorrection: false, CanCompleteReview: false,
            CanSubmitCorrection: false, CanAccessCheck: false,
            CanSelectAppraiser: false, CanSendToAppraiser: false,
            CanRequestAdditionalPayment: true,
            CanCompleteAdditionalPayment: true,
            CanGenerateDocuments: true,
            CanSendQuoteRequests: true,
            CanSendThankYou: true,
            CanUploadInvoice: true,
            CanSendInvoiceForPayment: true,
            CanConfirmInvoicePaid: true,
            CanRejectOrder: true,
            CanReturnForRework: true);

        Assert.True(capabilities.CanRequestAdditionalPayment);
        Assert.True(capabilities.CanCompleteAdditionalPayment);
        Assert.True(capabilities.CanGenerateDocuments);
        Assert.True(capabilities.CanSendQuoteRequests);
        Assert.True(capabilities.CanSendThankYou);
        Assert.True(capabilities.CanUploadInvoice);
        Assert.True(capabilities.CanSendInvoiceForPayment);
        Assert.True(capabilities.CanConfirmInvoicePaid);
        Assert.True(capabilities.CanRejectOrder);
        Assert.True(capabilities.CanReturnForRework);
    }

    // ── AppraisalOrderDto extended coverage ────────────────────────────────────

    [Fact]
    public void AppraisalOrderDto_DefaultParameters_HaveExpectedValues()
    {
        var dto = new AppraisalOrderDto(
            Id: 10, OrderNumber: "PN-2026-000010", Title: "T", Status: "Draft", StatusCode: 0,
            WorkflowType: null, CurrentOwnerRole: null, NextResponsibleRole: null,
            ClientName: "K", ClientType: null, ClientIdentifier: null,
            CollateralTypeId: null, CollateralTypeLabel: null,
            CombinedCollateralTypeId: null, CombinedCollateralTypeLabel: null,
            City: null, PropertyAddress: null, PropertyCity: null,
            Branch: null, BranchAddress: null,
            ContactName: null, ContactPhone: null, ContactEmail: null,
            DeliveryContactName: null, AmRecipientName: null,
            CreatedByUserId: null, CreatedByRole: null, CreatedByName: null,
            CreatedAt: DateTime.UtcNow, UpdatedAt: null, SubmittedAt: null,
            InternalNote: null, RequestReceivedAt: null, RequestSentAt: null,
            SquareMetersCommercial: null, SquareMetersResidential: null);

        Assert.Null(dto.AppraisalFee);
        Assert.Null(dto.CollateralStatus);
        Assert.Null(dto.ProtocolNumber);
        Assert.Null(dto.InvoiceWorkflowStatus);
        Assert.Null(dto.InvoiceUploadedByName);
        Assert.Null(dto.InvoiceUploadedAt);
        Assert.Null(dto.InvoiceSentForPaymentByName);
        Assert.Null(dto.InvoiceSentForPaymentAt);
        Assert.Null(dto.InvoicePaidByName);
        Assert.Null(dto.InvoicePaidAt);
        Assert.Null(dto.InvoiceDocumentId);
        Assert.Null(dto.AcceptedByCAUserId);
        Assert.Null(dto.AcceptedAt);
    }

    [Fact]
    public void AppraisalOrderDto_AllOptionalFieldsPopulated_StoreValues()
    {
        var now = new DateTime(2026, 6, 15, 10, 0, 0, DateTimeKind.Utc);

        var dto = new AppraisalOrderDto(
            Id: 20, OrderNumber: "PN-2026-000020", Title: "Full", Status: "InProgress", StatusCode: 50,
            WorkflowType: "PravnaLica", CurrentOwnerRole: "CA", NextResponsibleRole: "CO",
            ClientName: "Firma d.o.o.", ClientType: "PL", ClientIdentifier: "4200000000000",
            CollateralTypeId: 5, CollateralTypeLabel: "Stan",
            CombinedCollateralTypeId: 6, CombinedCollateralTypeLabel: "Kombinovano",
            City: "Sarajevo", PropertyAddress: "Adresa 20", PropertyCity: "Sarajevo",
            Branch: "POS_CENTAR", BranchAddress: "Titova 1",
            ContactName: "Kontakt", ContactPhone: "061-111-222", ContactEmail: "k@test.ba",
            DeliveryContactName: "Dostava", AmRecipientName: "AM Prim",
            CreatedByUserId: "user-20", CreatedByRole: "AM", CreatedByName: "Kreator",
            CreatedAt: now, UpdatedAt: now, SubmittedAt: now,
            InternalNote: "Napomena", RequestReceivedAt: now, RequestSentAt: now,
            SquareMetersCommercial: 120.5m, SquareMetersResidential: 85.0m,
            AppraisalFee: 3000.00m, CollateralStatus: "Aktivan", ProtocolNumber: "2026/00020",
            InvoiceWorkflowStatus: "Paid", InvoiceUploadedByName: "Uploader",
            InvoiceUploadedAt: now, InvoiceSentForPaymentByName: "Sender",
            InvoiceSentForPaymentAt: now, InvoicePaidByName: "Payer", InvoicePaidAt: now,
            InvoiceDocumentId: 50,
            Capabilities: new OrderCapabilitiesDto(CanEdit: false, CanSubmit: false, CanCancel: true),
            AcceptedByCAUserId: "ca-user-20", AcceptedAt: now);

        Assert.Equal(3000.00m, dto.AppraisalFee);
        Assert.Equal("Aktivan", dto.CollateralStatus);
        Assert.Equal("2026/00020", dto.ProtocolNumber);
        Assert.Equal("Paid", dto.InvoiceWorkflowStatus);
        Assert.Equal("Uploader", dto.InvoiceUploadedByName);
        Assert.Equal(now, dto.InvoiceUploadedAt);
        Assert.Equal("Sender", dto.InvoiceSentForPaymentByName);
        Assert.Equal(now, dto.InvoiceSentForPaymentAt);
        Assert.Equal("Payer", dto.InvoicePaidByName);
        Assert.Equal(now, dto.InvoicePaidAt);
        Assert.Equal(50, dto.InvoiceDocumentId);
        Assert.Equal("ca-user-20", dto.AcceptedByCAUserId);
        Assert.Equal(now, dto.AcceptedAt);
        Assert.Equal(120.5m, dto.SquareMetersCommercial);
        Assert.Equal(85.0m, dto.SquareMetersResidential);
        Assert.Equal("Dostava", dto.DeliveryContactName);
        Assert.Equal("AM Prim", dto.AmRecipientName);
        Assert.Equal(now, dto.RequestReceivedAt);
        Assert.Equal(now, dto.RequestSentAt);
        Assert.Equal("Napomena", dto.InternalNote);
        Assert.False(dto.Capabilities.CanEdit);
        Assert.True(dto.Capabilities.CanCancel);
    }

    // ── WorkflowTaskDto extended coverage ──────────────────────────────────────

    [Fact]
    public void WorkflowTaskDto_AllFieldsPopulated_StoresCorrectValues()
    {
        var created = new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc);
        var accepted = new DateTime(2026, 6, 2, 0, 0, 0, DateTimeKind.Utc);
        var completed = new DateTime(2026, 6, 3, 0, 0, 0, DateTimeKind.Utc);
        var due = new DateTime(2026, 6, 10, 0, 0, 0, DateTimeKind.Utc);

        var dto = new WorkflowTaskDto(
            Id: 10, OrderId: 20, OrderNumber: "PN-2026-000020", OrderTitle: "Naslov",
            TaskType: "ReviewDocuments", TaskTypeCode: 5,
            Title: "Pregledaj dokumentaciju", Description: "Detaljan opis zadatka",
            AssignedRole: "CO", AssignedUserId: "co-user-1",
            Status: "Completed", StatusCode: 2, IsLocked: true,
            DueDate: due, AcceptedAt: accepted, AcceptedByUserId: "co-user-1",
            CompletedAt: completed, CompletedByUserId: "co-user-1",
            Comment: "Sve OK", CreatedAt: created);

        Assert.Equal(10, dto.Id);
        Assert.Equal(20, dto.OrderId);
        Assert.Equal("PN-2026-000020", dto.OrderNumber);
        Assert.Equal("Naslov", dto.OrderTitle);
        Assert.Equal("ReviewDocuments", dto.TaskType);
        Assert.Equal(5, dto.TaskTypeCode);
        Assert.Equal("Pregledaj dokumentaciju", dto.Title);
        Assert.Equal("Detaljan opis zadatka", dto.Description);
        Assert.Equal("CO", dto.AssignedRole);
        Assert.Equal("co-user-1", dto.AssignedUserId);
        Assert.Equal("Completed", dto.Status);
        Assert.Equal(2, dto.StatusCode);
        Assert.True(dto.IsLocked);
        Assert.Equal(due, dto.DueDate);
        Assert.Equal(accepted, dto.AcceptedAt);
        Assert.Equal("co-user-1", dto.AcceptedByUserId);
        Assert.Equal(completed, dto.CompletedAt);
        Assert.Equal("co-user-1", dto.CompletedByUserId);
        Assert.Equal("Sve OK", dto.Comment);
        Assert.Equal(created, dto.CreatedAt);
    }

    [Fact]
    public void WorkflowTaskDto_NullOptionalFields_StoreNullCorrectly()
    {
        var now = DateTime.UtcNow;

        var dto = new WorkflowTaskDto(
            Id: 1, OrderId: 1, OrderNumber: "PN-2026-000001", OrderTitle: null,
            TaskType: "AcceptCAOrder", TaskTypeCode: 0,
            Title: "Prihvati", Description: null,
            AssignedRole: null, AssignedUserId: null,
            Status: "Open", StatusCode: 0, IsLocked: false,
            DueDate: null, AcceptedAt: null, AcceptedByUserId: null,
            CompletedAt: null, CompletedByUserId: null,
            Comment: null, CreatedAt: now);

        Assert.Null(dto.OrderTitle);
        Assert.Null(dto.Description);
        Assert.Null(dto.AssignedRole);
        Assert.Null(dto.AssignedUserId);
        Assert.Null(dto.DueDate);
        Assert.Null(dto.AcceptedAt);
        Assert.Null(dto.AcceptedByUserId);
        Assert.Null(dto.CompletedAt);
        Assert.Null(dto.CompletedByUserId);
        Assert.Null(dto.Comment);
    }

    // ── CaDocumentReviewDtos coverage ──────────────────────────────────────────

    [Fact]
    public void RequestCorrectionRequest_StoresReasonCodeIdAndComment()
    {
        var request = new RequestCorrectionRequest(ReasonCodeId: 3, Comment: "Nedostaje tabela");

        Assert.Equal(3, request.ReasonCodeId);
        Assert.Equal("Nedostaje tabela", request.Comment);
    }

    [Fact]
    public void RequestCorrectionRequest_NullComment_StoresNull()
    {
        var request = new RequestCorrectionRequest(ReasonCodeId: 1, Comment: null);

        Assert.Equal(1, request.ReasonCodeId);
        Assert.Null(request.Comment);
    }

    [Fact]
    public void SubmitCorrectionRequest_StoresComment()
    {
        var request = new SubmitCorrectionRequest(Comment: "Ispravljena tabela");

        Assert.Equal("Ispravljena tabela", request.Comment);
    }

    [Fact]
    public void SubmitCorrectionRequest_NullComment_StoresNull()
    {
        var request = new SubmitCorrectionRequest(Comment: null);

        Assert.Null(request.Comment);
    }

    [Fact]
    public void CaDocumentReviewResultDto_StoresAllProperties()
    {
        var dto = new CaDocumentReviewResultDto(
            OrderId: 5,
            OrderNumber: "PN-2026-000005",
            Status: "CorrectionRequested",
            StatusCode: 60,
            NotificationSent: true,
            Message: "Korekcija zatrazena");

        Assert.Equal(5, dto.OrderId);
        Assert.Equal("PN-2026-000005", dto.OrderNumber);
        Assert.Equal("CorrectionRequested", dto.Status);
        Assert.Equal(60, dto.StatusCode);
        Assert.True(dto.NotificationSent);
        Assert.Equal("Korekcija zatrazena", dto.Message);
    }

    [Fact]
    public void CaDocumentReviewResultDto_NotificationNotSent_StoresFalse()
    {
        var dto = new CaDocumentReviewResultDto(
            OrderId: 1, OrderNumber: "PN-2026-000001",
            Status: "ReviewCompleted", StatusCode: 70,
            NotificationSent: false, Message: "Pregled zavrsen");

        Assert.False(dto.NotificationSent);
    }

    // ── ApproveFinalAppraisalResultDto extended coverage ───────────────────────

    [Fact]
    public void ApproveFinalAppraisalResultDto_AllProperties_StoredCorrectly()
    {
        var approvedAt = new DateTime(2026, 6, 5, 14, 30, 0, DateTimeKind.Utc);
        var readyAt = new DateTime(2026, 6, 5, 14, 31, 0, DateTimeKind.Utc);

        var dto = new ApproveFinalAppraisalResultDto(
            OrderId: 10,
            OrderNumber: "PN-2026-000010",
            Status: "ReadyForProcedure",
            CoApprovedAt: approvedAt,
            CoApprovedByUserId: "co-user-5",
            ReadyForProcedureAt: readyAt,
            FinalAppraisalDocumentId: 100,
            DownloadUrl: "/api/orders/10/final-appraisal",
            NotificationSent: false,
            Message: "Nije poslana notifikacija");

        Assert.Equal(10, dto.OrderId);
        Assert.Equal("PN-2026-000010", dto.OrderNumber);
        Assert.Equal("ReadyForProcedure", dto.Status);
        Assert.Equal(approvedAt, dto.CoApprovedAt);
        Assert.Equal("co-user-5", dto.CoApprovedByUserId);
        Assert.Equal(readyAt, dto.ReadyForProcedureAt);
        Assert.Equal(100, dto.FinalAppraisalDocumentId);
        Assert.Equal("/api/orders/10/final-appraisal", dto.DownloadUrl);
        Assert.False(dto.NotificationSent);
        Assert.Equal("Nije poslana notifikacija", dto.Message);
    }

    // ── FinalAppraisalDto extended coverage ────────────────────────────────────

    [Fact]
    public void FinalAppraisalDto_AllFieldsPopulated_StoresCorrectValues()
    {
        var uploaded = new DateTime(2026, 6, 1, 8, 0, 0, DateTimeKind.Utc);

        var dto = new FinalAppraisalDto(
            OrderId: 15,
            DocumentId: 200,
            OriginalFileName: "final_procjena_v2.pdf",
            ContentType: "application/pdf",
            FileSize: 2048576,
            UploadedAt: uploaded,
            UploadedByUserId: "ca-user-3",
            DownloadUrl: "/api/orders/15/final-appraisal");

        Assert.Equal(15, dto.OrderId);
        Assert.Equal(200, dto.DocumentId);
        Assert.Equal("final_procjena_v2.pdf", dto.OriginalFileName);
        Assert.Equal("application/pdf", dto.ContentType);
        Assert.Equal(2048576, dto.FileSize);
        Assert.Equal(uploaded, dto.UploadedAt);
        Assert.Equal("ca-user-3", dto.UploadedByUserId);
        Assert.Equal("/api/orders/15/final-appraisal", dto.DownloadUrl);
    }

    [Fact]
    public void FinalAppraisalDto_NullOptionalFields_StoresNull()
    {
        var dto = new FinalAppraisalDto(
            OrderId: 1,
            DocumentId: 1,
            OriginalFileName: "file.pdf",
            ContentType: null,
            FileSize: 0,
            UploadedAt: DateTime.UtcNow,
            UploadedByUserId: null,
            DownloadUrl: "/api/orders/1/final-appraisal");

        Assert.Null(dto.ContentType);
        Assert.Null(dto.UploadedByUserId);
        Assert.Equal(0, dto.FileSize);
    }

    // ── ProtocolEntryDto extended coverage ─────────────────────────────────────

    [Fact]
    public void ProtocolEntryDto_DefaultParameters_HaveExpectedValues()
    {
        var now = DateTime.UtcNow;

        var dto = new ProtocolEntryDto(
            Id: 1, OrderId: 5, OrderNumber: "PN-2026-000005", OrderTitle: "Naslov",
            ProtocolNumber: "2026/00001", ProtocolYear: 2026, ProtocolSequence: 1,
            Status: "Active", GeneratedAt: now, GeneratedByUserId: "user-1",
            ClientName: "Klijent", City: "Sarajevo", Branch: "POS_SARAJEVO",
            OrderStatus: "ProtocolCreated", OrderStatusCode: 80,
            CollateralTypeLabel: "Stan", CombinedCollateralTypeLabel: null,
            ClientType: "FL", ClientIdentifier: "1234567890123",
            ContactName: "Kontakt", ContactPhone: "061-123-456",
            PropertyAddress: "Adresa 1", BranchAddress: "Titova 1",
            CreatedByName: "Korisnik", CreatedByRole: "AM",
            DeliveryContactName: "Dostava", AmRecipientName: "AM Primalac");

        // All default parameters should be null
        Assert.Null(dto.RequestReceivedAt);
        Assert.Null(dto.RequestSentAt);
        Assert.Null(dto.InvoiceSentDate);
        Assert.Null(dto.InvoiceReceivedDate);
        Assert.Null(dto.PaymentConsentStatus);
        Assert.Null(dto.CoApprovalComment);
        Assert.Null(dto.AppraiserName);
        Assert.Null(dto.AppraiserRating);
        Assert.Null(dto.EsgCertificate);
        Assert.Null(dto.AppraiserVisitDate);
        Assert.Null(dto.AppraisalFee);
        Assert.Null(dto.CollateralStatus);
        Assert.Null(dto.SubmittedAt);
        Assert.Null(dto.OrderSentToAppraiserAt);
        Assert.Null(dto.SignedDocumentsReceivedAt);
        Assert.Null(dto.DocumentationSupplementAt);
        Assert.Null(dto.CoApprovedAt);
        Assert.Null(dto.AppraisalDeliveredToCoAt);
        Assert.Null(dto.CorrectionRequestedAt);
        Assert.Null(dto.CorrectedAppraisalReceivedAt);
        Assert.Null(dto.ReadyForProcedureAt);
        Assert.Null(dto.OriginalReceivedAt);
        Assert.Null(dto.CoApprovedByUserId);
        Assert.Null(dto.AcceptedByCAName);
        Assert.Null(dto.DocumentationReviewStatus);
    }

    [Fact]
    public void ProtocolEntryDto_AllFieldsPopulated_StoresCorrectValues()
    {
        var now = new DateTime(2026, 6, 10, 12, 0, 0, DateTimeKind.Utc);

        var dto = new ProtocolEntryDto(
            Id: 99, OrderId: 50, OrderNumber: "PN-2026-000050", OrderTitle: "Full Proto",
            ProtocolNumber: "2026/00099", ProtocolYear: 2026, ProtocolSequence: 99,
            Status: "Active", GeneratedAt: now, GeneratedByUserId: "user-99",
            ClientName: "Firma d.o.o.", City: "Mostar", Branch: "POS_MOSTAR",
            OrderStatus: "Completed", OrderStatusCode: 100,
            CollateralTypeLabel: "Poslovni prostor", CombinedCollateralTypeLabel: "Kombinovano",
            ClientType: "PL", ClientIdentifier: "4200000000000",
            ContactName: "Kontakt Full", ContactPhone: "+38762999888",
            PropertyAddress: "Ulica 99", BranchAddress: "Adresa Mostar",
            CreatedByName: "Kreator", CreatedByRole: "SM",
            DeliveryContactName: "Dostava Full", AmRecipientName: "AM Full",
            RequestReceivedAt: now, RequestSentAt: now,
            InvoiceSentDate: now, InvoiceReceivedDate: now,
            PaymentConsentStatus: "Approved",
            CoApprovalComment: "Odobreno bez primjedbi",
            AppraiserName: "Vjestak Petar", AppraiserRating: 5,
            EsgCertificate: "A+", AppraiserVisitDate: now,
            AppraisalFee: 5000.00m, CollateralStatus: "Aktivan",
            SubmittedAt: now, OrderSentToAppraiserAt: now,
            SignedDocumentsReceivedAt: now, DocumentationSupplementAt: now,
            CoApprovedAt: now, AppraisalDeliveredToCoAt: now,
            CorrectionRequestedAt: now, CorrectedAppraisalReceivedAt: now,
            ReadyForProcedureAt: now, OriginalReceivedAt: now,
            CoApprovedByUserId: "co-user-1",
            AcceptedByCAName: "CA Korisnik",
            DocumentationReviewStatus: "Pregledano");

        Assert.Equal(99, dto.Id);
        Assert.Equal(50, dto.OrderId);
        Assert.Equal("PN-2026-000050", dto.OrderNumber);
        Assert.Equal("Full Proto", dto.OrderTitle);
        Assert.Equal("2026/00099", dto.ProtocolNumber);
        Assert.Equal(2026, dto.ProtocolYear);
        Assert.Equal(99, dto.ProtocolSequence);
        Assert.Equal("PL", dto.ClientType);
        Assert.Equal("4200000000000", dto.ClientIdentifier);
        Assert.Equal("Kontakt Full", dto.ContactName);
        Assert.Equal("+38762999888", dto.ContactPhone);
        Assert.Equal("Ulica 99", dto.PropertyAddress);
        Assert.Equal("Adresa Mostar", dto.BranchAddress);
        Assert.Equal("Kreator", dto.CreatedByName);
        Assert.Equal("SM", dto.CreatedByRole);
        Assert.Equal("Dostava Full", dto.DeliveryContactName);
        Assert.Equal("AM Full", dto.AmRecipientName);
        Assert.Equal(now, dto.RequestReceivedAt);
        Assert.Equal(now, dto.RequestSentAt);
        Assert.Equal(now, dto.InvoiceSentDate);
        Assert.Equal(now, dto.InvoiceReceivedDate);
        Assert.Equal("Approved", dto.PaymentConsentStatus);
        Assert.Equal("Odobreno bez primjedbi", dto.CoApprovalComment);
        Assert.Equal("Vjestak Petar", dto.AppraiserName);
        Assert.Equal(5, dto.AppraiserRating);
        Assert.Equal("A+", dto.EsgCertificate);
        Assert.Equal(now, dto.AppraiserVisitDate);
        Assert.Equal(5000.00m, dto.AppraisalFee);
        Assert.Equal("Aktivan", dto.CollateralStatus);
        Assert.Equal(now, dto.SubmittedAt);
        Assert.Equal(now, dto.OrderSentToAppraiserAt);
        Assert.Equal(now, dto.SignedDocumentsReceivedAt);
        Assert.Equal(now, dto.DocumentationSupplementAt);
        Assert.Equal(now, dto.CoApprovedAt);
        Assert.Equal(now, dto.AppraisalDeliveredToCoAt);
        Assert.Equal(now, dto.CorrectionRequestedAt);
        Assert.Equal(now, dto.CorrectedAppraisalReceivedAt);
        Assert.Equal(now, dto.ReadyForProcedureAt);
        Assert.Equal(now, dto.OriginalReceivedAt);
        Assert.Equal("co-user-1", dto.CoApprovedByUserId);
        Assert.Equal("CA Korisnik", dto.AcceptedByCAName);
        Assert.Equal("Pregledano", dto.DocumentationReviewStatus);
        Assert.Equal("Kombinovano", dto.CombinedCollateralTypeLabel);
        Assert.Equal("Poslovni prostor", dto.CollateralTypeLabel);
        Assert.Equal(100, dto.OrderStatusCode);
        Assert.Equal("Completed", dto.OrderStatus);
    }

    // ── AppraisalOrderListItemDto extended coverage ───────────────────────────

    [Fact]
    public void AppraisalOrderListItemDto_AllFieldsPopulated_StoresCorrectValues()
    {
        var created = new DateTime(2026, 6, 1, 0, 0, 0, DateTimeKind.Utc);
        var submitted = new DateTime(2026, 6, 2, 0, 0, 0, DateTimeKind.Utc);
        var updated = new DateTime(2026, 6, 3, 0, 0, 0, DateTimeKind.Utc);

        var dto = new AppraisalOrderListItemDto(
            Id: 42, OrderNumber: "PN-2026-000042", Title: "Lista stavka",
            Status: "InProgress", StatusCode: 50,
            WorkflowType: "FizickaLica", ClientName: "Klijent Lista",
            CollateralTypeLabel: "Kuca", CombinedCollateralTypeLabel: "Kuca+Garaza",
            City: "Tuzla", CreatedByRole: "UB",
            CreatedAt: created, SubmittedAt: submitted,
            Branch: "POS_TUZLA", UpdatedAt: updated);

        Assert.Equal(42, dto.Id);
        Assert.Equal("PN-2026-000042", dto.OrderNumber);
        Assert.Equal("Lista stavka", dto.Title);
        Assert.Equal("InProgress", dto.Status);
        Assert.Equal(50, dto.StatusCode);
        Assert.Equal("FizickaLica", dto.WorkflowType);
        Assert.Equal("Klijent Lista", dto.ClientName);
        Assert.Equal("Kuca", dto.CollateralTypeLabel);
        Assert.Equal("Kuca+Garaza", dto.CombinedCollateralTypeLabel);
        Assert.Equal("Tuzla", dto.City);
        Assert.Equal("UB", dto.CreatedByRole);
        Assert.Equal(created, dto.CreatedAt);
        Assert.Equal(submitted, dto.SubmittedAt);
        Assert.Equal("POS_TUZLA", dto.Branch);
        Assert.Equal(updated, dto.UpdatedAt);
    }

    [Fact]
    public void AppraisalOrderListItemDto_NullOptionalFields_StoreNull()
    {
        var dto = new AppraisalOrderListItemDto(
            Id: 1, OrderNumber: "PN-2026-000001", Title: "T",
            Status: "Draft", StatusCode: 0,
            WorkflowType: null, ClientName: "K",
            CollateralTypeLabel: null, CombinedCollateralTypeLabel: null,
            City: null, CreatedByRole: null,
            CreatedAt: DateTime.UtcNow, SubmittedAt: null,
            Branch: null, UpdatedAt: null);

        Assert.Null(dto.WorkflowType);
        Assert.Null(dto.CollateralTypeLabel);
        Assert.Null(dto.CombinedCollateralTypeLabel);
        Assert.Null(dto.City);
        Assert.Null(dto.CreatedByRole);
        Assert.Null(dto.SubmittedAt);
        Assert.Null(dto.Branch);
        Assert.Null(dto.UpdatedAt);
    }

    // ── OrderCapabilitiesDto coverage ──────────────────────────────────────────

    [Theory]
    [InlineData(true, true, true)]
    [InlineData(false, false, false)]
    [InlineData(true, false, true)]
    [InlineData(false, true, false)]
    public void OrderCapabilitiesDto_StoresAllFlagCombinations(bool canEdit, bool canSubmit, bool canCancel)
    {
        var dto = new OrderCapabilitiesDto(CanEdit: canEdit, CanSubmit: canSubmit, CanCancel: canCancel);

        Assert.Equal(canEdit, dto.CanEdit);
        Assert.Equal(canSubmit, dto.CanSubmit);
        Assert.Equal(canCancel, dto.CanCancel);
    }

    // ── OrderSummaryDto edge cases ─────────────────────────────────────────────

    [Fact]
    public void OrderSummaryDto_ZeroCounts_StoresAllZeros()
    {
        var dto = new OrderSummaryDto(Total: 0, Draft: 0, SubmittedBySales: 0, InProgress: 0, Completed: 0, Cancelled: 0);

        Assert.Equal(0, dto.Total);
        Assert.Equal(0, dto.Draft);
        Assert.Equal(0, dto.SubmittedBySales);
        Assert.Equal(0, dto.InProgress);
        Assert.Equal(0, dto.Completed);
        Assert.Equal(0, dto.Cancelled);
    }
}
