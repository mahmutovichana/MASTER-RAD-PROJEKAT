using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Documents;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public sealed class DocumentConfiguration : IEntityTypeConfiguration<Document>
{
    public void Configure(EntityTypeBuilder<Document> builder)
    {
        builder.ToTable("documents");
        builder.HasKey(x => x.Id);

        builder.Property(x => x.Id).HasColumnName("id");
        builder.Property(x => x.AppraisalOrderId).HasColumnName("appraisal_order_id").IsRequired();
        builder.Property(x => x.DocumentTypeId).HasColumnName("document_type_id");
        builder.Property(x => x.FileName).HasColumnName("file_name").HasMaxLength(500).IsRequired();
        builder.Property(x => x.OriginalFileName).HasColumnName("original_file_name").HasMaxLength(500).IsRequired();
        builder.Property(x => x.ContentType).HasColumnName("content_type").HasMaxLength(200);
        builder.Property(x => x.FileSize).HasColumnName("file_size").IsRequired();
        builder.Property(x => x.StoragePath).HasColumnName("storage_path").HasMaxLength(1000).IsRequired();
        builder.Property(x => x.UploadedByUserId).HasColumnName("uploaded_by_user_id").HasMaxLength(100);
        builder.Property(x => x.UploadedAt).HasColumnName("uploaded_at").IsRequired();
        builder.Property(x => x.Version).HasColumnName("version").IsRequired();
        builder.Property(x => x.PreviousVersionId).HasColumnName("previous_version_id");
        builder.Property(x => x.IsActive).HasColumnName("is_active").IsRequired();
        builder.Property(x => x.DeactivatedAt).HasColumnName("deactivated_at");
        builder.Property(x => x.DeactivatedByUserId).HasColumnName("deactivated_by_user_id").HasMaxLength(100);
        builder.Property(x => x.DeactivationReason).HasColumnName("deactivation_reason").HasMaxLength(500);
        builder.Property(x => x.IsDeleted).HasColumnName("is_deleted").IsRequired();
        builder.Property(x => x.DeletedAt).HasColumnName("deleted_at");
        builder.Property(x => x.DeletedByUserId).HasColumnName("deleted_by_user_id").HasMaxLength(100);
        builder.Property(x => x.CreatedAt).HasColumnName("created_at").IsRequired();
        builder.Property(x => x.UpdatedAt).HasColumnName("updated_at");

        builder.Property(x => x.ChangeReason).HasColumnName("change_reason").HasMaxLength(500);

        builder.HasIndex(x => x.AppraisalOrderId);
        builder.HasIndex(x => x.IsDeleted);
        builder.HasIndex(x => x.IsActive);
        builder.HasIndex(x => x.PreviousVersionId);

        builder.HasQueryFilter(x => !x.IsDeleted);
    }
}
