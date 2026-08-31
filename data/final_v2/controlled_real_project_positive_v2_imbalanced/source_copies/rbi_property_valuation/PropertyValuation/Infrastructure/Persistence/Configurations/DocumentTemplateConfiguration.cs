using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Documents;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public sealed class DocumentTemplateConfiguration : IEntityTypeConfiguration<DocumentTemplate>
{
    public void Configure(EntityTypeBuilder<DocumentTemplate> builder)
    {
        builder.ToTable("document_templates");
        builder.HasKey(x => x.Id);

        builder.Property(x => x.Id).HasColumnName("id");
        builder.Property(x => x.Code).HasColumnName("code").HasMaxLength(100).IsRequired();
        builder.Property(x => x.Name).HasColumnName("name").HasMaxLength(300).IsRequired();
        builder.Property(x => x.Description).HasColumnName("description").HasMaxLength(1000);
        builder.Property(x => x.Category).HasColumnName("category").HasMaxLength(50).IsRequired();
        builder.Property(x => x.FileName).HasColumnName("file_name").HasMaxLength(300).IsRequired();
        builder.Property(x => x.ContentType).HasColumnName("content_type").HasMaxLength(100).IsRequired();
        builder.Property(x => x.FileSize).HasColumnName("file_size").IsRequired();
        builder.Property(x => x.StoragePath).HasColumnName("storage_path").HasMaxLength(500).IsRequired();
        builder.Property(x => x.SortOrder).HasColumnName("sort_order").IsRequired();
        builder.Property(x => x.IsActive).HasColumnName("is_active").IsRequired().HasDefaultValue(true);
        builder.Property(x => x.AllowedRoles).HasColumnName("allowed_roles").HasMaxLength(500);
        builder.Property(x => x.CreatedAt).HasColumnName("created_at").IsRequired();
        builder.Property(x => x.UpdatedAt).HasColumnName("updated_at");

        builder.HasIndex(x => x.Code).IsUnique();
        builder.HasIndex(x => x.Category);
    }
}
