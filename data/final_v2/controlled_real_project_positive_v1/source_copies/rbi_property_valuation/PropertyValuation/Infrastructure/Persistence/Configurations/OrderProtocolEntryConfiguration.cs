using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public sealed class OrderProtocolEntryConfiguration : IEntityTypeConfiguration<OrderProtocolEntry>
{
    public void Configure(EntityTypeBuilder<OrderProtocolEntry> builder)
    {
        builder.ToTable("order_protocol_entries");
        builder.HasKey(x => x.Id);

        builder.Property(x => x.Id).HasColumnName("id");
        builder.Property(x => x.OrderId).HasColumnName("order_id").IsRequired();
        builder.Property(x => x.ProtocolNumber).HasColumnName("protocol_number").HasMaxLength(20).IsRequired();
        builder.Property(x => x.ProtocolYear).HasColumnName("protocol_year").IsRequired();
        builder.Property(x => x.ProtocolSequence).HasColumnName("protocol_sequence").IsRequired();
        builder.Property(x => x.GeneratedAt).HasColumnName("generated_at").IsRequired();
        builder.Property(x => x.GeneratedByUserId).HasColumnName("generated_by_user_id").HasMaxLength(100).IsRequired();
        builder.Property(x => x.Status).HasColumnName("status").HasConversion<int>().IsRequired();
        builder.Property(x => x.CreatedAt).HasColumnName("created_at").IsRequired();
        builder.Property(x => x.UpdatedAt).HasColumnName("updated_at");

        // Query filter usklađen sa AppraisalOrder.IsDeleted (rješava EF model-validation upozorenje)
        builder.HasQueryFilter(x => x.Order == null || !x.Order.IsDeleted);

        // Restrict (ne Cascade) — protokolni broj je zvanični dokument, ne briše se zajedno s narudžbom
        builder.HasOne(x => x.Order)
               .WithMany()
               .HasForeignKey(x => x.OrderId)
               .OnDelete(DeleteBehavior.Restrict);

        // Jedan protokol per narudžba
        builder.HasIndex(x => x.OrderId).IsUnique();
        builder.HasIndex(x => x.ProtocolNumber).IsUnique();
        builder.HasIndex(x => new { x.ProtocolYear, x.ProtocolSequence }).IsUnique();
        builder.HasIndex(x => x.ProtocolYear);
    }
}
