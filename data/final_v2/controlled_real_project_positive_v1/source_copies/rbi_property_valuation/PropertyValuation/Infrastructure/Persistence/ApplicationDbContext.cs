using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Domain.Appraisers;
using RBBH.CollateralAppraisal.Domain.Audit;
using RBBH.CollateralAppraisal.Domain.Branches;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Domain.Documents;
using RBBH.CollateralAppraisal.Domain.Notifications;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Domain.Roles;
using RBBH.CollateralAppraisal.Infrastructure.Audit;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options) { }

    public DbSet<City>                 Cities                => Set<City>();
    public DbSet<Branch>               Branches              => Set<Branch>();
    public DbSet<AuditLog>             AuditLogs             => Set<AuditLog>();
    public DbSet<Codebook>             Codebooks             => Set<Codebook>();
    public DbSet<CodebookValue>        CodebookValues        => Set<CodebookValue>();
    public DbSet<RoleDefinition>       RoleDefinitions       => Set<RoleDefinition>();
    public DbSet<PermissionDefinition> PermissionDefinitions => Set<PermissionDefinition>();
    public DbSet<RolePermission>       RolePermissions       => Set<RolePermission>();
    public DbSet<AppraisalOrder>       AppraisalOrders       => Set<AppraisalOrder>();
    public DbSet<TaskItem>             TaskItems             => Set<TaskItem>();
    public DbSet<Document>             Documents             => Set<Document>();
    public DbSet<SharedDocument>       SharedDocuments       => Set<SharedDocument>();
    public DbSet<Notification>         Notifications         => Set<Notification>();
    public DbSet<OrderProtocolEntry>   OrderProtocolEntries  => Set<OrderProtocolEntry>();
    public DbSet<Opinion>              Opinions              => Set<Opinion>();
    public DbSet<Appraiser>                Appraisers              => Set<Appraiser>();
    public DbSet<OrderDeclinedAppraiser>   OrderDeclinedAppraisers => Set<OrderDeclinedAppraiser>();
    public DbSet<QuoteRequest>             QuoteRequests           => Set<QuoteRequest>();
    public DbSet<DocumentTemplate>         DocumentTemplates       => Set<DocumentTemplate>();
    public DbSet<AuditOutboxEntry>         AuditOutbox             => Set<AuditOutboxEntry>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
    }
}
