using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public sealed class QuoteRequestConfiguration : IEntityTypeConfiguration<QuoteRequest>
{
    public void Configure(EntityTypeBuilder<QuoteRequest> builder)
    {
        builder.ToTable("quote_requests");
        builder.HasKey(x => x.Id);

        builder.Property(x => x.Id).HasColumnName("id");
        builder.Property(x => x.AppraisalOrderId).HasColumnName("appraisal_order_id").IsRequired();
        builder.Property(x => x.AppraiserId).HasColumnName("appraiser_id").IsRequired();
        builder.Property(x => x.Status).HasColumnName("status").HasConversion<int>().IsRequired();
        builder.Property(x => x.SentAt).HasColumnName("sent_at").IsRequired();
        builder.Property(x => x.Deadline).HasColumnName("deadline").IsRequired();
        builder.Property(x => x.SentByUserId).HasColumnName("sent_by_user_id").HasMaxLength(100);
        builder.Property(x => x.OfferedPrice).HasColumnName("offered_price").HasPrecision(18, 2);
        builder.Property(x => x.OfferedDays).HasColumnName("offered_days");
        builder.Property(x => x.RespondedAt).HasColumnName("responded_at");
        builder.Property(x => x.ThankYouSentAt).HasColumnName("thank_you_sent_at");
        builder.Property(x => x.CreatedAt).HasColumnName("created_at").IsRequired();
        builder.Property(x => x.UpdatedAt).HasColumnName("updated_at");

        builder.HasIndex(x => x.AppraisalOrderId);
        builder.HasIndex(x => new { x.AppraisalOrderId, x.AppraiserId }).IsUnique();
    }
}
