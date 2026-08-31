using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Codebooks;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public sealed class CodebookValueConfiguration : IEntityTypeConfiguration<CodebookValue>
{
    public void Configure(EntityTypeBuilder<CodebookValue> builder)
    {
        builder.ToTable("codebook_values");

        builder.HasKey(x => x.Id);
        builder.Property(x => x.Id).UseIdentityColumn();

        builder.Property(x => x.CodebookKey)
               .HasMaxLength(100)
               .IsRequired();

        builder.Property(x => x.Code)
               .HasMaxLength(100)
               .IsRequired();

        builder.Property(x => x.Label)
               .HasMaxLength(300)
               .IsRequired();

        builder.Property(x => x.Description)
               .HasMaxLength(1000);

        builder.Property(x => x.CreatedByUserId)
               .HasMaxLength(100);

        builder.Property(x => x.UpdatedByUserId)
               .HasMaxLength(100);

        builder.Property(x => x.DeactivatedByUserId)
               .HasMaxLength(100);

        builder.Property(x => x.DeactivationReason)
               .HasMaxLength(500);

        builder.Property(x => x.DeletedByUserId)
               .HasMaxLength(100);

        // Globalni query filter — soft-deleted zapisi su nevidljivi u standardnim upitima
        builder.HasQueryFilter(x => x.DeletedAt == null);

        // Jedinstvenost Code-a unutar CodebookKey-a — samo za neobrisane vrijednosti (parcijalni indeks)
        builder.HasIndex(x => new { x.CodebookKey, x.Code })
               .IsUnique()
               .HasFilter("\"DeletedAt\" IS NULL")
               .HasDatabaseName("uix_codebook_values_key_code_active");

        // Indeks za dropdown upit: WHERE codebook_key = 'X' AND is_active = true
        builder.HasIndex(x => new { x.CodebookKey, x.IsActive })
               .HasDatabaseName("ix_codebook_values_key_active");

        // Indeks za admin pregled po codebookKey
        builder.HasIndex(x => x.CodebookKey)
               .HasDatabaseName("ix_codebook_values_key");
    }
}
