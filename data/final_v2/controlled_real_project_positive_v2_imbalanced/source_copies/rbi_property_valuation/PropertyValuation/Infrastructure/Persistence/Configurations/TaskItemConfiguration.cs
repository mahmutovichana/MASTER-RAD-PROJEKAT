using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public sealed class TaskItemConfiguration : IEntityTypeConfiguration<TaskItem>
{
    public void Configure(EntityTypeBuilder<TaskItem> builder)
    {
        builder.ToTable("task_items");
        builder.HasKey(x => x.Id);

        builder.Ignore(x => x.RowVersion);
        builder.Property(x => x.Id).HasColumnName("id");
        builder.Property(x => x.AppraisalOrderId).HasColumnName("appraisal_order_id").IsRequired();
        builder.Property(x => x.TaskType).HasColumnName("task_type").HasConversion<int>().IsRequired();
        builder.Property(x => x.Title).HasColumnName("title").HasMaxLength(300).IsRequired();
        builder.Property(x => x.Description).HasColumnName("description").HasMaxLength(2000);
        builder.Property(x => x.AssignedRole).HasColumnName("assigned_role").HasMaxLength(100);
        builder.Property(x => x.AssignedUserId).HasColumnName("assigned_user_id").HasMaxLength(100);
        builder.Property(x => x.Status).HasColumnName("status").HasConversion<int>().IsRequired();
        builder.Property(x => x.AcceptedAt).HasColumnName("accepted_at");
        builder.Property(x => x.AcceptedByUserId).HasColumnName("accepted_by_user_id").HasMaxLength(100);
        builder.Property(x => x.CompletedAt).HasColumnName("completed_at");
        builder.Property(x => x.CompletedByUserId).HasColumnName("completed_by_user_id").HasMaxLength(100);
        builder.Property(x => x.DueDate).HasColumnName("due_date");
        builder.Property(x => x.Comment).HasColumnName("comment").HasMaxLength(2000);
        builder.Property(x => x.IsLocked).HasColumnName("is_locked").IsRequired();
        builder.Property(x => x.CreatedAt).HasColumnName("created_at").IsRequired();
        builder.Property(x => x.UpdatedAt).HasColumnName("updated_at");

        builder.Property(x => x.RowVersion)
            .HasColumnName("row_version")
            .IsRowVersion();

        builder.HasQueryFilter(x => x.AppraisalOrder == null || !x.AppraisalOrder.IsDeleted);

        builder.HasIndex(x => x.AppraisalOrderId);
        builder.HasIndex(x => x.Status);
        builder.HasIndex(x => x.AssignedRole);
        builder.HasIndex(x => x.AssignedUserId);
    }
}
