using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public sealed class OrderDeclinedAppraiserConfiguration : IEntityTypeConfiguration<OrderDeclinedAppraiser>
{
    public void Configure(EntityTypeBuilder<OrderDeclinedAppraiser> builder)
    {
        builder.ToTable("order_declined_appraisers");

        builder.HasKey(x => x.Id);
        builder.Property(x => x.Id).HasColumnName("id").ValueGeneratedOnAdd();

        builder.Property(x => x.AppraisalOrderId).HasColumnName("appraisal_order_id").IsRequired();
        builder.Property(x => x.AppraiserId).HasColumnName("appraiser_id").IsRequired();
        builder.Property(x => x.DeclinedAt).HasColumnName("declined_at").IsRequired();
        builder.Property(x => x.Reason).HasColumnName("reason").IsRequired();
        builder.Property(x => x.FreeText).HasColumnName("free_text").HasMaxLength(1000);
        builder.Property(x => x.IsTimeout).HasColumnName("is_timeout").IsRequired();

        builder.HasIndex(x => x.AppraisalOrderId).HasDatabaseName("ix_order_declined_appraisers_order_id");
        builder.HasIndex(x => new { x.AppraisalOrderId, x.AppraiserId })
               .HasDatabaseName("ix_order_declined_appraisers_order_appraiser");
    }
}
