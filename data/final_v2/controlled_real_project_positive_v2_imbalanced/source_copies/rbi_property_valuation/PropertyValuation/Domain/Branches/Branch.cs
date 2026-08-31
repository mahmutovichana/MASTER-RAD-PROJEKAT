using RBBH.CollateralAppraisal.Domain.Common;

namespace RBBH.CollateralAppraisal.Domain.Branches;

public sealed class Branch : BaseEntity
{
    public string Code    { get; private set; } = null!;  // npr. "POS_SARAJEVO_CENTAR"
    public string Name    { get; private set; } = null!;  // prikazni naziv
    public string Address { get; private set; } = null!;  // puna adresa
    public int    CityId  { get; private set; }

    public City City { get; private set; } = null!;

    private Branch() { }

    public static Branch Create(string code, string name, string address, int cityId)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(code);
        ArgumentException.ThrowIfNullOrWhiteSpace(name);
        ArgumentException.ThrowIfNullOrWhiteSpace(address);
        return new Branch
        {
            Code    = code.Trim().ToUpperInvariant(),
            Name    = name.Trim(),
            Address = address.Trim(),
            CityId  = cityId
        };
    }

    public void Update(string name, string address, int cityId)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(name);
        ArgumentException.ThrowIfNullOrWhiteSpace(address);
        Name    = name.Trim();
        Address = address.Trim();
        CityId  = cityId;
    }
}
