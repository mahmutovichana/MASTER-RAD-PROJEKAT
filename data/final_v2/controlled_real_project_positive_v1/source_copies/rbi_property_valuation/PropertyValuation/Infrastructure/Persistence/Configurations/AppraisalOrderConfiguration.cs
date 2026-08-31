using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Appraisers;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public sealed class AppraisalOrderConfiguration : IEntityTypeConfiguration<AppraisalOrder>
{
    public void Configure(EntityTypeBuilder<AppraisalOrder> builder)
    {
        builder.ToTable("appraisal_orders");
        builder.HasKey(x => x.Id);

        // RowVersion se trenutno ne perzistira; konkurentnost se kontroliše kroz servisni sloj.
        builder.Ignore(x => x.RowVersion);

        builder.Property(x => x.Id).HasColumnName("id");
        builder.Property(x => x.OrderNumber).HasColumnName("order_number").HasMaxLength(50).IsRequired();
        builder.Property(x => x.Title).HasColumnName("title").HasMaxLength(500).IsRequired();
        builder.Property(x => x.Status).HasColumnName("status").HasConversion<int>().IsRequired();
        builder.Property(x => x.WorkflowType).HasColumnName("workflow_type");
        builder.Property(x => x.ClientName).HasColumnName("client_name").HasMaxLength(300).IsRequired();
        builder.Property(x => x.ClientType).HasColumnName("client_type").HasMaxLength(50);
        builder.Property(x => x.ClientIdentifier).HasColumnName("client_identifier").HasMaxLength(50);
        builder.Property(x => x.ContactName).HasColumnName("contact_name").HasMaxLength(300);
        builder.Property(x => x.ContactPhone).HasColumnName("contact_phone").HasMaxLength(50);
        builder.Property(x => x.ContactEmail).HasColumnName("contact_email").HasMaxLength(200);
        builder.Property(x => x.Branch).HasColumnName("branch").HasMaxLength(200);
        builder.Property(x => x.BranchAddress).HasColumnName("branch_address").HasMaxLength(400);
        builder.Property(x => x.City).HasColumnName("city").HasMaxLength(100);
        builder.Property(x => x.CityId).HasColumnName("city_id");
        builder.Property(x => x.BranchId).HasColumnName("branch_id");
        builder.Property(x => x.CollateralTypeId).HasColumnName("collateral_type_id");
        builder.Property(x => x.CombinedCollateralTypeId).HasColumnName("combined_collateral_type_id");
        builder.Property(x => x.PropertyAddress).HasColumnName("property_address").HasMaxLength(500);
        builder.Property(x => x.PropertyCity).HasColumnName("property_city").HasMaxLength(150);
        builder.Property(x => x.CreatedByUserId).HasColumnName("created_by_user_id").HasMaxLength(100);
        builder.Property(x => x.CreatedByRole).HasColumnName("created_by_role").HasMaxLength(100);
        builder.Property(x => x.CreatedByName).HasColumnName("created_by_name").HasMaxLength(300);
        builder.Property(x => x.CreatedByEmail).HasColumnName("created_by_email").HasMaxLength(200);
        builder.Property(x => x.DeliveryContactName).HasColumnName("delivery_contact_name").HasMaxLength(300);
        builder.Property(x => x.AmRecipientName).HasColumnName("am_recipient_name").HasMaxLength(300);
        builder.Property(x => x.AcceptedByCAUserId).HasColumnName("accepted_by_ca_user_id").HasMaxLength(100);
        builder.Property(x => x.AcceptedByCAName).HasColumnName("accepted_by_ca_name").HasMaxLength(300);
        builder.Property(x => x.AcceptedAt).HasColumnName("accepted_at");
        builder.Property(x => x.SubmittedAt).HasColumnName("submitted_at");
        builder.Property(x => x.DocumentationReviewStatus)
            .HasColumnName("documentation_review_status")
            .HasMaxLength(30)
            .HasConversion<string?>(
                v => v.HasValue ? DocumentationReviewStatusConverter.ToDbValue(v.Value) : null,
                v => v != null ? DocumentationReviewStatusConverter.FromDbValue(v) : null);
        builder.Property(x => x.AppraiserId).HasColumnName("appraiser_id");
        builder.Property(x => x.InternalNote).HasColumnName("internal_note").HasMaxLength(2000);
        builder.Property(x => x.IsDeleted).HasColumnName("is_deleted").IsRequired();
        builder.Property(x => x.DeletedAt).HasColumnName("deleted_at");
        builder.Property(x => x.DeletedByUserId).HasColumnName("deleted_by_user_id").HasMaxLength(100);
        builder.Property(x => x.CreatedAt).HasColumnName("created_at").IsRequired();
        builder.Property(x => x.UpdatedAt).HasColumnName("updated_at");
        builder.Property(x => x.PaymentConsentStatus).HasColumnName("payment_consent_status").HasMaxLength(100);

        // ── Finalna procjena / odobrenje CO (US 93) ──────────────────────
        builder.Property(x => x.FinalAppraisalDocumentId).HasColumnName("final_appraisal_document_id");
        builder.Property(x => x.CoApprovedAt).HasColumnName("co_approved_at");
        builder.Property(x => x.CoApprovedByUserId).HasColumnName("co_approved_by_user_id").HasMaxLength(100);
        builder.Property(x => x.ReadyForProcedureAt).HasColumnName("ready_for_procedure_at");

        // ── Original procjene u poslovnici (US 93) ───────────────────────
        builder.Property(x => x.OriginalReceivedAt).HasColumnName("original_received_at");
        builder.Property(x => x.OriginalReceivedByUserId).HasColumnName("original_received_by_user_id").HasMaxLength(100);
        builder.Property(x => x.CorrectionCount).HasColumnName("correction_count").IsRequired().HasDefaultValue(0);
        builder.Property(x => x.AppraiserReminderCount).HasColumnName("appraiser_reminder_count").IsRequired().HasDefaultValue(0);
        builder.Property(x => x.AppraiserReminderLastSentAt).HasColumnName("appraiser_reminder_last_sent_at");


        // ── Mišljenja CO i Pravne službe (US 94) ─────────────────────────
        builder.Property(x => x.OpinionsCompletedAt).HasColumnName("opinions_completed_at");

        // ── Prodaja — datum prijema/slanja ────────────────────────────────
        builder.Property(x => x.RequestReceivedAt).HasColumnName("request_received_at");
        builder.Property(x => x.RequestSentAt).HasColumnName("request_sent_at");

        // ── Faktura (CA) ──────────────────────────────────────────────────
        builder.Property(x => x.InvoiceSentDate).HasColumnName("invoice_sent_date");
        builder.Property(x => x.InvoiceReceivedDate).HasColumnName("invoice_received_date");

        // ── Faktura workflow ──────────────────────────────────────────────
        builder.Property(x => x.InvoiceStatus).HasColumnName("invoice_status").HasConversion<int>().IsRequired().HasDefaultValue(InvoiceWorkflowStatus.None);
        builder.Property(x => x.InvoiceDocumentId).HasColumnName("invoice_document_id");
        builder.Property(x => x.InvoiceUploadedByUserId).HasColumnName("invoice_uploaded_by_user_id").HasMaxLength(100);
        builder.Property(x => x.InvoiceUploadedByName).HasColumnName("invoice_uploaded_by_name").HasMaxLength(300);
        builder.Property(x => x.InvoiceUploadedAt).HasColumnName("invoice_uploaded_at");
        builder.Property(x => x.InvoiceSentForPaymentByUserId).HasColumnName("invoice_sent_for_payment_by_user_id").HasMaxLength(100);
        builder.Property(x => x.InvoiceSentForPaymentByName).HasColumnName("invoice_sent_for_payment_by_name").HasMaxLength(300);
        builder.Property(x => x.InvoiceSentForPaymentAt).HasColumnName("invoice_sent_for_payment_at");
        builder.Property(x => x.InvoicePaidByUserId).HasColumnName("invoice_paid_by_user_id").HasMaxLength(100);
        builder.Property(x => x.InvoicePaidByName).HasColumnName("invoice_paid_by_name").HasMaxLength(300);
        builder.Property(x => x.InvoicePaidAt).HasColumnName("invoice_paid_at");

        // ── Procjena / vještak ────────────────────────────────────────────
        builder.Property(x => x.AppraiserVisitDate).HasColumnName("appraiser_visit_date");
        builder.Property(x => x.AppraiserRating).HasColumnName("appraiser_rating");
        builder.Property(x => x.EsgCertificate).HasColumnName("esg_certificate").HasMaxLength(50);

        // ── CO pregled dokumentacije ──────────────────────────────────────
        builder.Property(x => x.CoDocumentationReviewStartedAt).HasColumnName("co_documentation_review_started_at");
        builder.Property(x => x.CoOpinionSentToAmAt).HasColumnName("co_opinion_sent_to_am_at");

        // ── Protokol polja (spec DIO_2) ───────────────────────────────────
        builder.Property(x => x.AppraisalFee).HasColumnName("appraisal_fee");
        builder.Property(x => x.CollateralStatus).HasColumnName("collateral_status").HasMaxLength(100);
        builder.Property(x => x.OrderSentToAppraiserAt).HasColumnName("order_sent_to_appraiser_at");
        builder.Property(x => x.SignedDocumentsReceivedAt).HasColumnName("signed_documents_received_at");
        builder.Property(x => x.DocumentationSupplementAt).HasColumnName("documentation_supplement_at");
        builder.Property(x => x.AppraisalDeliveredToCoAt).HasColumnName("appraisal_delivered_to_co_at");
        builder.Property(x => x.CorrectionRequestedAt).HasColumnName("correction_requested_at");
        builder.Property(x => x.CorrectedAppraisalReceivedAt).HasColumnName("corrected_appraisal_received_at");

        // ── PL-specifična polja (m² poslovnog/stambenog dijela) ──────────────
        builder.Property(x => x.SquareMetersCommercial).HasColumnName("square_meters_commercial");
        builder.Property(x => x.SquareMetersResidential).HasColumnName("square_meters_residential");

        builder.HasIndex(x => x.OrderNumber).IsUnique();
        builder.HasIndex(x => x.Status);
        builder.HasIndex(x => x.CreatedByUserId);
        builder.HasIndex(x => x.IsDeleted);
        builder.HasIndex(x => x.AppraiserId);
        builder.HasIndex(x => x.City);
        builder.HasIndex(x => new { x.Status, x.City });
        builder.HasIndex(x => new { x.AppraiserId, x.Status });

        // ── Optimizacioni indeksi (dodate radi performansi MyOrders query-ja i date-range filtera)
        builder.HasIndex(x => new { x.CreatedByUserId, x.IsDeleted })
            .HasDatabaseName("ix_orders_owner_deleted");
        builder.HasIndex(x => new { x.CreatedByUserId, x.Status })
            .HasDatabaseName("ix_orders_owner_status");
        builder.HasIndex(x => x.CreatedAt)
            .HasDatabaseName("ix_orders_created_at");

        // ── Vještak (Faza C) — nullable FK, bez navigation property na ovoj strani ──
        builder.HasOne<Appraiser>()
            .WithMany()
            .HasForeignKey(x => x.AppraiserId)
            .OnDelete(DeleteBehavior.SetNull);

        builder.HasQueryFilter(x => !x.IsDeleted);
    }
}
