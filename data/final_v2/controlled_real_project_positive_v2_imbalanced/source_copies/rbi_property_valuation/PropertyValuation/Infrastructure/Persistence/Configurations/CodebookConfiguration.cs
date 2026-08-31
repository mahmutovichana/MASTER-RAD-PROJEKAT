using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Codebooks;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public class CodebookConfiguration : IEntityTypeConfiguration<Codebook>
{
    public void Configure(EntityTypeBuilder<Codebook> builder)
    {
        builder.ToTable("codebooks");

        builder.HasKey(x => x.Id);
        builder.Property(x => x.Id).UseIdentityColumn();

        builder.Property(x => x.Code)
               .IsRequired()
               .HasMaxLength(100);

        builder.Property(x => x.Name)
               .IsRequired()
               .HasMaxLength(250);

        builder.Property(x => x.Description)
               .HasMaxLength(1000);

        builder.Property(x => x.Category)
               .HasMaxLength(100);

        builder.Property(x => x.IsActive)     .IsRequired();
        builder.Property(x => x.IsSystem)     .IsRequired();

        builder.Property(x => x.CreatedByUserId).HasMaxLength(128);
        builder.Property(x => x.UpdatedByUserId).HasMaxLength(128);
        builder.Property(x => x.DeletedByUserId).HasMaxLength(128);

        builder.Property(x => x.CreatedAt)
               .IsRequired()
               .HasColumnType("timestamp with time zone");
        builder.Property(x => x.UpdatedAt)
               .HasColumnType("timestamp with time zone");
        builder.Property(x => x.DeletedAt)
               .HasColumnType("timestamp with time zone");

        // Unique: Code jedinstven unutar non-deleted šifarnika
        builder.HasIndex(x => x.Code)
               .IsUnique()
               .HasFilter("\"DeletedAt\" IS NULL")
               .HasDatabaseName("uix_codebooks_code_active");

        builder.HasIndex(x => x.IsActive)
               .HasDatabaseName("ix_codebooks_is_active");

        builder.HasIndex(x => x.Category)
               .HasDatabaseName("ix_codebooks_category");

        // Soft-deleted zapisi se ne prikazuju u standardnim upitima
        builder.HasQueryFilter(x => x.DeletedAt == null);
    }
}
