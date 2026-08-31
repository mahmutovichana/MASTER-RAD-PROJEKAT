using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Branches;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public class CityConfiguration : IEntityTypeConfiguration<City>
{
    public void Configure(EntityTypeBuilder<City> builder)
    {
        builder.ToTable("cities");
        builder.HasKey(x => x.Id);
        builder.Property(x => x.Id).HasColumnName("id").ValueGeneratedOnAdd();
        builder.Property(x => x.Name).HasColumnName("name").HasMaxLength(100).IsRequired();

        builder.HasIndex(x => x.Name).IsUnique().HasDatabaseName("uix_cities_name");
    }
}
