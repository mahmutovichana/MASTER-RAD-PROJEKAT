namespace RBBH.CollateralAppraisal.Domain.Common;

public abstract class BaseEntity
{
    public int Id { get; protected set; }
    // NAPOMENA: DateTime.UtcNow je svjesna kompromisna odluka — entiteti se kreiraju
    // posrednim instanciranjem (EF, seeder, factory). IClock ovdje nije moguć bez
    // destruktivnih promjena konstruktora svih entiteta. Factory metode primaju 'now'
    // parametar za timestamp-osjetljive operacije (vidi Document.Create, QuoteRequest.Create).
    public DateTime CreatedAt { get; protected set; } = DateTime.UtcNow;
    public DateTime? UpdatedAt { get; protected set; }

    public void SetUpdatedAt(DateTime updatedAt) => UpdatedAt = updatedAt;
}

/// <summary>
/// Interfejs za entitete koji koriste optimistic concurrency (RowVersion).
/// Samo AppraisalOrder i TaskItem implementiraju ovo — ostali entiteti ne trebaju.
/// </summary>
public interface IConcurrencyAware
{
    uint RowVersion { get; }
}
