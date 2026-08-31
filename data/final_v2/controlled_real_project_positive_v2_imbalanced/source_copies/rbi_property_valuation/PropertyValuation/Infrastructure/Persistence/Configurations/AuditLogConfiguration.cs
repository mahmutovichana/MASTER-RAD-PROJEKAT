using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Audit;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public class AuditLogConfiguration : IEntityTypeConfiguration<AuditLog>
{
    public void Configure(EntityTypeBuilder<AuditLog> builder)
    {
        builder.ToTable("audit_logs");

        builder.HasKey(x => x.Id);
        builder.Property(x => x.Id).UseIdentityColumn();

        // ── Timestamp ────────────────────────────────────────────────────────
        builder.Property(x => x.TimestampUtc)
               .IsRequired()
               .HasColumnType("datetime2");

        // ── Akter ────────────────────────────────────────────────────────────
        builder.Property(x => x.ActorUserId)   .IsRequired().HasMaxLength(128);
        builder.Property(x => x.ActorUsername)  .IsRequired().HasMaxLength(256);
        builder.Property(x => x.ActorEmail)     .HasMaxLength(256);
        builder.Property(x => x.ActorFullName)  .HasMaxLength(256);
        builder.Property(x => x.ActorRole)      .HasMaxLength(128);
        builder.Property(x => x.ActiveRole)     .HasMaxLength(128);

        // ── Šta se desilo ────────────────────────────────────────────────────
        builder.Property(x => x.Action)        .IsRequired().HasMaxLength(128);
        builder.Property(x => x.OperationType) .IsRequired().HasMaxLength(64);
        builder.Property(x => x.Module)        .IsRequired().HasMaxLength(64);

        // ── Izvor podataka ───────────────────────────────────────────────────
        builder.Property(x => x.SourceSystem)        .HasMaxLength(128);
        builder.Property(x => x.SourceConnectionName).HasMaxLength(256);
        builder.Property(x => x.SourceDatabase)      .HasMaxLength(128);
        builder.Property(x => x.SourceSchema)        .HasMaxLength(64);
        builder.Property(x => x.SourceTable)         .HasMaxLength(256);

        // ── Entitet ──────────────────────────────────────────────────────────
        builder.Property(x => x.EntityType)       .IsRequired().HasMaxLength(128);
        builder.Property(x => x.EntityKey)        .HasMaxLength(256);
        builder.Property(x => x.EntityDisplayName).HasMaxLength(512);

        // JSON se u SQL Serveru čuva kao nvarchar(max); aplikacijski ugovor ostaje isti.
        builder.Property(x => x.OldValuesJson)    .HasColumnType("nvarchar(max)");
        builder.Property(x => x.NewValuesJson)    .HasColumnType("nvarchar(max)");
        builder.Property(x => x.ChangedFieldsJson).HasColumnType("nvarchar(max)");

        // ── Ishod ─────────────────────────────────────────────────────────────
        builder.Property(x => x.Status)  .IsRequired().HasMaxLength(64);
        builder.Property(x => x.Severity).IsRequired().HasMaxLength(32);
        builder.Property(x => x.Reason)  .HasMaxLength(1024);

        // ── Integracija ───────────────────────────────────────────────────────
        builder.Property(x => x.IntegrationDirection)  .HasMaxLength(16);
        builder.Property(x => x.ExternalRequestId)     .HasMaxLength(256);
        builder.Property(x => x.ExternalResponseStatus).HasMaxLength(64);

        // ── HTTP kontekst ─────────────────────────────────────────────────────
        builder.Property(x => x.CorrelationId).HasMaxLength(64);
        builder.Property(x => x.RequestPath)  .HasMaxLength(1024);
        builder.Property(x => x.HttpMethod)   .HasMaxLength(10);
        builder.Property(x => x.IpAddress)    .HasMaxLength(64);
        builder.Property(x => x.UserAgent)    .HasMaxLength(512);

        // ── Indeksi (9) ───────────────────────────────────────────────────────
        builder.HasIndex(x => x.TimestampUtc)
               .HasDatabaseName("ix_audit_logs_timestamp_utc");

        builder.HasIndex(x => x.ActorUserId)
               .HasDatabaseName("ix_audit_logs_actor_user_id");

        builder.HasIndex(x => x.ActiveRole)
               .HasDatabaseName("ix_audit_logs_active_role");

        builder.HasIndex(x => x.Action)
               .HasDatabaseName("ix_audit_logs_action");

        builder.HasIndex(x => x.Module)
               .HasDatabaseName("ix_audit_logs_module");

        builder.HasIndex(x => new { x.EntityType, x.EntityKey })
               .HasDatabaseName("ix_audit_logs_entity_type_key");

        builder.HasIndex(x => x.CorrelationId)
               .HasDatabaseName("ix_audit_logs_correlation_id");

        builder.HasIndex(x => x.Status)
               .HasDatabaseName("ix_audit_logs_status");

        builder.HasIndex(x => x.Severity)
               .HasDatabaseName("ix_audit_logs_severity");

        builder.HasIndex(x => x.SourceSystem)
               .HasDatabaseName("ix_audit_logs_source_system");
    }
}
