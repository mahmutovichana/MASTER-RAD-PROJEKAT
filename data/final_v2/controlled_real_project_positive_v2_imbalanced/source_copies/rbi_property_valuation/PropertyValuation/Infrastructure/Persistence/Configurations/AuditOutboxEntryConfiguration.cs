using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Infrastructure.Audit;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public sealed class AuditOutboxEntryConfiguration : IEntityTypeConfiguration<AuditOutboxEntry>
{
    public void Configure(EntityTypeBuilder<AuditOutboxEntry> builder)
    {
        builder.ToTable("AuditOutbox");
        builder.HasKey(e => e.Id);
        builder.Property(e => e.Id).UseIdentityColumn();
        builder.Property(e => e.Payload).IsRequired().HasColumnType("nvarchar(max)");
        builder.Property(e => e.CreatedAt).IsRequired();
        builder.Property(e => e.ProcessedAt);

        // Indeks za polling worker — samo neprocesirani zapisi, sortirani po vremenu.
        builder.HasIndex(e => new { e.ProcessedAt, e.CreatedAt })
               .HasFilter("[ProcessedAt] IS NULL")
               .HasDatabaseName("IX_AuditOutbox_Unprocessed");
    }
}
