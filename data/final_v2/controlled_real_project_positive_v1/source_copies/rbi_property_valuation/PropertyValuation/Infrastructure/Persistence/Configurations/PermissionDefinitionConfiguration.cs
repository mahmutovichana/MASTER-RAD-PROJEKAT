using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Roles;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public sealed class PermissionDefinitionConfiguration : IEntityTypeConfiguration<PermissionDefinition>
{
    public void Configure(EntityTypeBuilder<PermissionDefinition> builder)
    {
        builder.ToTable("permission_definitions");
        builder.HasKey(x => x.Id);

        builder.Property(x => x.Id).HasColumnName("id");
        builder.Property(x => x.Code).HasColumnName("code").HasMaxLength(100).IsRequired();
        builder.Property(x => x.DisplayName).HasColumnName("display_name").HasMaxLength(250).IsRequired();
        builder.Property(x => x.Description).HasColumnName("description").HasMaxLength(1000);
        builder.Property(x => x.Module).HasColumnName("module").HasMaxLength(100).IsRequired();
        builder.Property(x => x.IsActive).HasColumnName("is_active").IsRequired();
        builder.Property(x => x.CreatedAt).HasColumnName("created_at").IsRequired();
        builder.Property(x => x.UpdatedAt).HasColumnName("updated_at");

        builder.HasIndex(x => x.Code).IsUnique();
        builder.HasIndex(x => x.Module);

        builder.HasMany(x => x.RolePermissions)
               .WithOne(x => x.PermissionDefinition)
               .HasForeignKey(x => x.PermissionDefinitionId)
               .OnDelete(DeleteBehavior.Cascade);
    }
}
