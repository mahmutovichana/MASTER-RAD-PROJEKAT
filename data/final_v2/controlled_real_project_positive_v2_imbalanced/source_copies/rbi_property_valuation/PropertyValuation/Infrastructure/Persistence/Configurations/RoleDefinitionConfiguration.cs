using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Roles;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public sealed class RoleDefinitionConfiguration : IEntityTypeConfiguration<RoleDefinition>
{
    public void Configure(EntityTypeBuilder<RoleDefinition> builder)
    {
        builder.ToTable("role_definitions");
        builder.HasKey(x => x.Id);

        builder.Property(x => x.Id).HasColumnName("id");
        builder.Property(x => x.Name).HasColumnName("name").HasMaxLength(150).IsRequired();
        builder.Property(x => x.DisplayName).HasColumnName("display_name").HasMaxLength(250).IsRequired();
        builder.Property(x => x.Description).HasColumnName("description").HasMaxLength(1000);
        builder.Property(x => x.IsSystem).HasColumnName("is_system").IsRequired();
        builder.Property(x => x.IsActive).HasColumnName("is_active").IsRequired();
        builder.Property(x => x.CreatedAt).HasColumnName("created_at").IsRequired();
        builder.Property(x => x.UpdatedAt).HasColumnName("updated_at");
        builder.Property(x => x.CreatedByUserId).HasColumnName("created_by_user_id").HasMaxLength(100);
        builder.Property(x => x.UpdatedByUserId).HasColumnName("updated_by_user_id").HasMaxLength(100);
        builder.Property(x => x.DeletedAt).HasColumnName("deleted_at");
        builder.Property(x => x.DeletedByUserId).HasColumnName("deleted_by_user_id").HasMaxLength(100);

        builder.HasIndex(x => x.Name).IsUnique().HasFilter("deleted_at IS NULL");
        builder.HasIndex(x => x.IsActive);
        builder.HasIndex(x => x.IsSystem);

        builder.HasQueryFilter(x => x.DeletedAt == null);

        builder.HasMany(x => x.Permissions)
               .WithOne(x => x.RoleDefinition)
               .HasForeignKey(x => x.RoleDefinitionId)
               .OnDelete(DeleteBehavior.Cascade);
    }
}
