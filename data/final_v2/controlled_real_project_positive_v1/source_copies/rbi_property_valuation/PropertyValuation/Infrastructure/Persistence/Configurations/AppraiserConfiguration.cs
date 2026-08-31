using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RBBH.CollateralAppraisal.Domain.Appraisers;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

public sealed class AppraiserConfiguration : IEntityTypeConfiguration<Appraiser>
{
    public void Configure(EntityTypeBuilder<Appraiser> builder)
    {
        builder.ToTable("appraisers");
        builder.HasKey(x => x.Id);

        builder.Property(x => x.Id).HasColumnName("id");
        builder.Property(x => x.Name).HasColumnName("name").HasMaxLength(300).IsRequired();
        builder.Property(x => x.City).HasColumnName("city").HasMaxLength(100);
        builder.Property(x => x.LegalForm).HasColumnName("legal_form").HasConversion<int>().IsRequired();
        builder.Property(x => x.ClientScope).HasColumnName("client_scope").HasConversion<int>().IsRequired();
        builder.Property(x => x.SupportedPropertyTypes).HasColumnName("supported_property_types").HasMaxLength(500);
        builder.Property(x => x.SupportedCities).HasColumnName("supported_cities").HasMaxLength(4000);
        builder.Property(x => x.IsOnLeave).HasColumnName("is_on_leave").IsRequired().HasDefaultValue(false);
        builder.Property(x => x.IsBlacklisted).HasColumnName("is_blacklisted").IsRequired().HasDefaultValue(false);
        builder.Property(x => x.ContactEmail).HasColumnName("contact_email").HasMaxLength(200);
        builder.Property(x => x.ContactPhone).HasColumnName("contact_phone").HasMaxLength(50);
        builder.Property(x => x.Notes).HasColumnName("notes").HasMaxLength(2000);
        builder.Property(x => x.IsActive).HasColumnName("is_active").IsRequired().HasDefaultValue(true);
        builder.Property(x => x.CreatedAt).HasColumnName("created_at").IsRequired();
        builder.Property(x => x.UpdatedAt).HasColumnName("updated_at");

        builder.HasIndex(x => x.City);
        builder.HasIndex(x => x.IsActive);
        builder.HasIndex(x => x.IsOnLeave);
        builder.Property(x => x.SupportedCities).HasColumnName("supported_cities").HasMaxLength(2000);
        builder.Property(x => x.SupportedPropertyTypes).HasColumnName("supported_property_types").HasMaxLength(2000);

        builder.HasIndex(x => x.IsBlacklisted);
    }
}
