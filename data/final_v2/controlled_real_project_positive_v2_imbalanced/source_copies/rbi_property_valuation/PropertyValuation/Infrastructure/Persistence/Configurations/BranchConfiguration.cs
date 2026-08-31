using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Branches;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public class BranchConfiguration : IEntityTypeConfiguration<Branch>
{
    public void Configure(EntityTypeBuilder<Branch> builder)
    {
        builder.ToTable("branches");
        builder.HasKey(x => x.Id);
        builder.Property(x => x.Id).HasColumnName("id").ValueGeneratedOnAdd();
        builder.Property(x => x.Code).HasColumnName("code").HasMaxLength(100).IsRequired();
        builder.Property(x => x.Name).HasColumnName("name").HasMaxLength(200).IsRequired();
        builder.Property(x => x.Address).HasColumnName("address").HasMaxLength(400).IsRequired();
        builder.Property(x => x.CityId).HasColumnName("city_id").IsRequired();

        builder.HasOne(x => x.City)
               .WithMany()
               .HasForeignKey(x => x.CityId)
               .OnDelete(DeleteBehavior.Restrict);

        builder.HasIndex(x => x.Code).IsUnique().HasDatabaseName("uix_branches_code");
        builder.HasIndex(x => x.CityId).HasDatabaseName("ix_branches_city_id");
    }
}
