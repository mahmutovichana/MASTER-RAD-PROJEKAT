using Hangfire.Common;
using Hangfire.States;
using Hangfire.Storage;

namespace RBBH.TestAutomation.Api.Jobs;

/// <summary>
/// Retention politika za Hangfire jobove: uspješni se čuvaju 7 dana,
/// neuspjeli (Failed/Deleted) 30 dana radi analize. Primjenjuje se globalno
/// preko <c>UseFilter</c> u registraciji Hangfire-a.
/// </summary>
public sealed class RetentionPolicyAttribute : JobFilterAttribute, IApplyStateFilter
{
    private static readonly TimeSpan SuccessRetention = TimeSpan.FromDays(7);
    private static readonly TimeSpan FailureRetention = TimeSpan.FromDays(30);

    public void OnStateApplied(ApplyStateContext context, IWriteOnlyTransaction transaction)
    {
        var state = context.NewState.Name;

        if (state == SucceededState.StateName)
            context.JobExpirationTimeout = SuccessRetention;
        else if (state == FailedState.StateName || state == DeletedState.StateName)
            context.JobExpirationTimeout = FailureRetention;
    }

    public void OnStateUnapplied(ApplyStateContext context, IWriteOnlyTransaction transaction)
    {
        // Bez akcije — retention se postavlja samo pri ulasku u finalno stanje.
    }
}
