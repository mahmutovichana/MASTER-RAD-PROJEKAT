using RBBH.CollateralAppraisal.Application.Common.Interfaces;

namespace RBBH.CollateralAppraisal.Application.Tests.Helpers;

/// <summary>
/// Deterministička implementacija IClock za testove.
/// Podrazumijevano vraća 2026-01-15 10:00:00 UTC — stabilno i ​​razumljivo u assert porukama.
/// Može se podesiti na lijepu testnu vrijednost ili promijeniti via AdvanceBy().
/// </summary>
public sealed class FakeClock : IClock
{
    private DateTime _current;

    public FakeClock(DateTime? fixedTime = null)
    {
        _current = fixedTime ?? new DateTime(2026, 1, 15, 10, 0, 0, DateTimeKind.Utc);
    }

    public DateTime UtcNow => _current;

    public void AdvanceBy(TimeSpan span) => _current = _current.Add(span);
    public void SetTo(DateTime time) => _current = DateTime.SpecifyKind(time, DateTimeKind.Utc);
}
