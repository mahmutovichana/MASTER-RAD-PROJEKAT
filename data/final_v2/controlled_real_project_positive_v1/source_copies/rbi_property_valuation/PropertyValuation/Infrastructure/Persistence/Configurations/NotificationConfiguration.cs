using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Notifications;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public sealed class NotificationConfiguration : IEntityTypeConfiguration<Notification>
{
    public void Configure(EntityTypeBuilder<Notification> builder)
    {
        builder.ToTable("notifications");
        builder.HasKey(x => x.Id);

        builder.Property(x => x.Id).HasColumnName("id");
        builder.Property(x => x.RecipientUserId).HasColumnName("recipient_user_id").HasMaxLength(128);
        builder.Property(x => x.RecipientRole).HasColumnName("recipient_role").HasMaxLength(128);
        builder.Property(x => x.Channel).HasColumnName("channel").HasConversion<int>().IsRequired();
        builder.Property(x => x.Subject).HasColumnName("subject").HasMaxLength(256).IsRequired();
        builder.Property(x => x.Message).HasColumnName("message").IsRequired();
        builder.Property(x => x.Status).HasColumnName("status").HasConversion<int>().IsRequired();
        builder.Property(x => x.SentAt).HasColumnName("sent_at");
        builder.Property(x => x.RetryCount).HasColumnName("retry_count").IsRequired().HasDefaultValue(0);
        builder.Property(x => x.ErrorMessage).HasColumnName("error_message");
        builder.Property(x => x.RelatedEntityType).HasColumnName("related_entity_type").HasMaxLength(128);
        builder.Property(x => x.RelatedEntityId).HasColumnName("related_entity_id").HasMaxLength(128);
        builder.Property(x => x.IsRead).HasColumnName("is_read").IsRequired().HasDefaultValue(false);
        builder.Property(x => x.ReadAt).HasColumnName("read_at");
        builder.Property(x => x.CreatedAt).HasColumnName("created_at").IsRequired();
        builder.Property(x => x.UpdatedAt).HasColumnName("updated_at");

        builder.Property(x => x.DeduplicationKey).HasColumnName("deduplication_key").HasMaxLength(512);

        builder.HasIndex(x => x.RecipientUserId);
        builder.HasIndex(x => x.Status);
        builder.HasIndex(x => new { x.RecipientUserId, x.IsRead });
        builder.HasIndex(x => x.DeduplicationKey);
    }
}
