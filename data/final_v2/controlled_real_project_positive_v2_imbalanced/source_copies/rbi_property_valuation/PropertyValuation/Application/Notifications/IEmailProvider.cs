namespace RBBH.CollateralAppraisal.Application.Notifications;

/// <summary>
/// Adapter za slanje emailova. Application sloj definiše interfejs — Infrastructure
/// implementira konkretni provider (SMTP, SendGrid, itd.).
///
/// Dev/test implementacija: <c>LogEmailProvider</c> — loguje umjesto slanja.
/// </summary>
public interface IEmailProvider
{
    Task SendAsync(EmailMessage message, CancellationToken ct = default);
}

/// <param name="ToAddress">Email adresa primaoca.</param>
/// <param name="Subject">Naslov poruke.</param>
/// <param name="Body">Tekst poruke (plain text).</param>
public sealed record EmailMessage(string ToAddress, string Subject, string Body);
