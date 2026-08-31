using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Roles;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public sealed class RolePermissionConfiguration : IEntityTypeConfiguration<RolePermission>
{
    public void Configure(EntityTypeBuilder<RolePermission> builder)
    {
        builder.ToTable("role_permissions");
        builder.HasKey(x => new { x.RoleDefinitionId, x.PermissionDefinitionId });

        builder.Property(x => x.RoleDefinitionId).HasColumnName("role_definition_id");
        builder.Property(x => x.PermissionDefinitionId).HasColumnName("permission_definition_id");
        builder.Property(x => x.CreatedAt).HasColumnName("created_at").IsRequired();
        builder.Property(x => x.CreatedByUserId).HasColumnName("created_by_user_id").HasMaxLength(100);

        // Query filter usklađen sa RoleDefinition.DeletedAt (rješava EF model-validation upozorenje)
        builder.HasQueryFilter(x => x.RoleDefinition.DeletedAt == null);

        builder.HasIndex(x => x.RoleDefinitionId);
        builder.HasIndex(x => x.PermissionDefinitionId);
    }
}
