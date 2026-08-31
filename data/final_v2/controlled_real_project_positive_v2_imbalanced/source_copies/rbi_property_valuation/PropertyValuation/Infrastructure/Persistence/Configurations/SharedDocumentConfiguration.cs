using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Documents;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public sealed class SharedDocumentConfiguration : IEntityTypeConfiguration<SharedDocument>
{
    public void Configure(EntityTypeBuilder<SharedDocument> builder)
    {
        builder.ToTable("shared_documents");
        builder.HasKey(x => x.Id);

        builder.Property(x => x.Id).HasColumnName("id");
        builder.Property(x => x.Title).HasColumnName("title").HasMaxLength(300).IsRequired();
        builder.Property(x => x.Category).HasColumnName("category").HasMaxLength(100).IsRequired();
        builder.Property(x => x.FileName).HasColumnName("file_name").HasMaxLength(500).IsRequired();
        builder.Property(x => x.OriginalFileName).HasColumnName("original_file_name").HasMaxLength(500).IsRequired();
        builder.Property(x => x.ContentType).HasColumnName("content_type").HasMaxLength(200);
        builder.Property(x => x.FileSize).HasColumnName("file_size").IsRequired();
        builder.Property(x => x.StoragePath).HasColumnName("storage_path").HasMaxLength(1000).IsRequired();
        builder.Property(x => x.UploadedByUserId).HasColumnName("uploaded_by_user_id").HasMaxLength(100);
        builder.Property(x => x.UploadedAt).HasColumnName("uploaded_at").IsRequired();
        builder.Property(x => x.IsActive).HasColumnName("is_active").IsRequired();
        builder.Property(x => x.DeactivatedAt).HasColumnName("deactivated_at");
        builder.Property(x => x.DeactivatedByUserId).HasColumnName("deactivated_by_user_id").HasMaxLength(100);
        builder.Property(x => x.CreatedAt).HasColumnName("created_at").IsRequired();
        builder.Property(x => x.UpdatedAt).HasColumnName("updated_at");

        builder.HasIndex(x => x.Category);
        builder.HasIndex(x => x.IsActive);
    }
}
