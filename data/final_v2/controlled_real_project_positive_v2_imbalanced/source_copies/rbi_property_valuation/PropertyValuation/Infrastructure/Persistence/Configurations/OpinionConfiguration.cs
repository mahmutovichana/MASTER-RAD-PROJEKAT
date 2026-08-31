using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public sealed class OpinionConfiguration : IEntityTypeConfiguration<Opinion>
{
    public void Configure(EntityTypeBuilder<Opinion> builder)
    {
        builder.ToTable("order_opinions");
        builder.HasKey(x => x.Id);

        builder.Property(x => x.Id).HasColumnName("id");
        builder.Property(x => x.AppraisalOrderId).HasColumnName("appraisal_order_id").IsRequired();
        builder.Property(x => x.OpinionType).HasColumnName("opinion_type").HasConversion<int>().IsRequired();
        builder.Property(x => x.Status).HasColumnName("status").HasConversion<int>().IsRequired();
        builder.Property(x => x.DocumentId).HasColumnName("document_id");
        builder.Property(x => x.ImportedByUserId).HasColumnName("imported_by_user_id").HasMaxLength(100);
        builder.Property(x => x.ImportedAt).HasColumnName("imported_at");
        builder.Property(x => x.Comment).HasColumnName("comment").HasMaxLength(2000);
        builder.Property(x => x.CreatedAt).HasColumnName("created_at").IsRequired();
        builder.Property(x => x.UpdatedAt).HasColumnName("updated_at");

        builder.HasIndex(x => x.AppraisalOrderId);
        builder.HasIndex(x => new { x.AppraisalOrderId, x.OpinionType }).IsUnique();
    }
}
