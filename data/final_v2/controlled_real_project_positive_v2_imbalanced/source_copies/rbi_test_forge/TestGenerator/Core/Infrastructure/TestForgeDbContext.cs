using Microsoft.EntityFrameworkCore;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Domain.Enums;

namespace RBBH.TestAutomation.Core.Infrastructure;

public class TestForgeDbContext(DbContextOptions<TestForgeDbContext> options) : DbContext(options)
{
    public DbSet<TestGroup> Groups => Set<TestGroup>();
    public DbSet<TestScenario> Scenarios => Set<TestScenario>();
    public DbSet<ScheduleConfig> Schedules => Set<ScheduleConfig>();
    public DbSet<RunResult> RunResults => Set<RunResult>();
    public DbSet<ApiKey> ApiKeys => Set<ApiKey>();
    public DbSet<CodeListCategory> CodeListCategories => Set<CodeListCategory>();
    public DbSet<CodeListValue> CodeListValues => Set<CodeListValue>();
    public DbSet<ApplicationAuditEntry> AuditEntries => Set<ApplicationAuditEntry>();
    public DbSet<SecurityAuditEntry> SecurityAuditEntries => Set<SecurityAuditEntry>();

    protected override void OnModelCreating(ModelBuilder b)
    {
        b.Entity<TestGroup>(e =>
        {
            e.ToTable("tf_groups");
            e.HasKey(x => x.Id);
            e.Property(x => x.Naziv).HasMaxLength(200).IsRequired();
            e.Property(x => x.Opis).HasMaxLength(2000);
            e.Property(x => x.Boja).HasMaxLength(20);
            e.Property(x => x.Tag).HasConversion<string>().HasMaxLength(20);
            e.Property(x => x.KreiranOd).HasMaxLength(100);
            e.Property(x => x.IzmjenjenOd).HasMaxLength(100);
            e.Property(x => x.NotificationConfigJson).HasColumnType("text");
            e.HasOne(x => x.ParentGroup)
                .WithMany(x => x.ChildGroups)
                .HasForeignKey(x => x.ParentGroupId)
                .OnDelete(DeleteBehavior.Restrict);
            e.HasMany(x => x.Scenarios)
                .WithOne(x => x.Group)
                .HasForeignKey(x => x.GroupId)
                .OnDelete(DeleteBehavior.Cascade);
            e.HasMany(x => x.Schedules)
                .WithOne(x => x.Group)
                .HasForeignKey(x => x.GroupId)
                .OnDelete(DeleteBehavior.Cascade);
            e.HasMany(x => x.RunResults)
                .WithOne(x => x.Group)
                .HasForeignKey(x => x.GroupId)
                .OnDelete(DeleteBehavior.Cascade);
        });

        b.Entity<TestScenario>(e =>
        {
            e.ToTable("tf_scenarios");
            e.HasKey(x => x.Id);
            e.Property(x => x.Naziv).HasMaxLength(200).IsRequired();
            e.Property(x => x.Tip).HasMaxLength(30).IsRequired();
            e.Property(x => x.Target).HasMaxLength(500);
            e.Property(x => x.KreiranOd).HasMaxLength(100);
            e.Property(x => x.RunSequentially).HasDefaultValue(false);
        });

        b.Entity<ScheduleConfig>(e =>
        {
            e.ToTable("tf_schedules");
            e.HasKey(x => x.Id);
            e.Property(x => x.CronExpression).HasMaxLength(100).IsRequired();
            e.Property(x => x.Timezone).HasMaxLength(60);
        });

        b.Entity<ApiKey>(e =>
        {
            e.ToTable("tf_api_keys");
            e.HasKey(x => x.Id);
            e.Property(x => x.Name).HasMaxLength(200).IsRequired();
            e.Property(x => x.KeyHash).HasMaxLength(128).IsRequired();
            e.Property(x => x.Prefix).HasMaxLength(12).IsRequired();
            e.Property(x => x.CreatedBy).HasMaxLength(100);
            e.HasIndex(x => x.KeyHash).IsUnique();
        });

        b.Entity<RunResult>(e =>
        {
            e.ToTable("tf_run_results");
            e.HasKey(x => x.Id);
            e.Property(x => x.State).HasConversion<string>().HasMaxLength(20);
            e.Property(x => x.TriggerType).HasConversion<string>().HasMaxLength(20);
            e.Property(x => x.OptionsJson).HasColumnType("text");
            e.Property(x => x.DetailsJson).HasColumnType("text");
        });

        b.Entity<CodeListCategory>(e =>
        {
            e.ToTable("sifarnici_kategorije");
            e.HasKey(x => x.Id);
            e.Property(x => x.Id).HasColumnName("id");
            e.Property(x => x.Name).HasColumnName("naziv").HasMaxLength(160).IsRequired();
            e.Property(x => x.Slug).HasColumnName("slug").HasMaxLength(100).IsRequired();
            e.Property(x => x.Description).HasColumnName("opis").HasMaxLength(1000);
            e.Property(x => x.Active).HasColumnName("active");
            e.Property(x => x.CreatedAt).HasColumnName("kreiran_at");
            e.HasIndex(x => x.Slug).IsUnique();
        });

        b.Entity<CodeListValue>(e =>
        {
            e.ToTable("sifarnici_vrijednosti");
            e.HasKey(x => x.Id);
            e.Property(x => x.Id).HasColumnName("id");
            e.Property(x => x.CategoryId).HasColumnName("kategorija_id");
            e.Property(x => x.Name).HasColumnName("naziv").HasMaxLength(160).IsRequired();
            e.Property(x => x.Code).HasColumnName("kod").HasMaxLength(80);
            e.Property(x => x.Order).HasColumnName("redoslijed");
            e.Property(x => x.Active).HasColumnName("active");
            e.Property(x => x.CreatedBy).HasColumnName("kreiran_od").HasMaxLength(100);
            e.Property(x => x.CreatedAt).HasColumnName("kreiran_at");
            e.Property(x => x.UpdatedBy).HasColumnName("izmjenjen_od").HasMaxLength(100);
            e.Property(x => x.UpdatedAt).HasColumnName("izmjenjen_at");
            e.HasIndex(x => new { x.CategoryId, x.Name }).IsUnique();
            e.HasOne(x => x.Category).WithMany(x => x.Values).HasForeignKey(x => x.CategoryId).OnDelete(DeleteBehavior.Cascade);
        });

        b.Entity<ApplicationAuditEntry>(e =>
        {
            e.ToTable("audit_log");
            e.HasKey(x => x.Id);
            e.Property(x => x.Id).HasColumnName("id");
            e.Property(x => x.EntityType).HasColumnName("entity_type").HasMaxLength(100);
            e.Property(x => x.EntityId).HasColumnName("entity_id");
            e.Property(x => x.Action).HasColumnName("action").HasMaxLength(30);
            e.Property(x => x.ChangedBy).HasColumnName("changed_by").HasMaxLength(100);
            e.Property(x => x.ChangedByName).HasColumnName("changed_by_name").HasMaxLength(200);
            e.Property(x => x.ChangedAt).HasColumnName("changed_at");
            e.Property(x => x.OldValues).HasColumnName("old_values");
            e.Property(x => x.NewValues).HasColumnName("new_values");
            e.HasIndex(x => new { x.EntityType, x.EntityId, x.ChangedAt });
        });

        b.Entity<SecurityAuditEntry>(e =>
        {
            e.ToTable("security_audit_log");
            e.HasKey(x => x.Id);
            e.Property(x => x.Id).HasColumnName("id").ValueGeneratedOnAdd();
            e.Property(x => x.TimestampUtc).HasColumnName("timestamp_utc");
            e.Property(x => x.EventType).HasColumnName("event_type").HasMaxLength(80);
            e.Property(x => x.Username).HasColumnName("username").HasMaxLength(150);
            e.Property(x => x.IpAddress).HasColumnName("ip_address").HasMaxLength(64);
            e.Property(x => x.FailureReason).HasColumnName("failure_reason").HasMaxLength(300);
            e.HasIndex(x => x.TimestampUtc);
        });
    }
}
