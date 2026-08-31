namespace RBBH.CollateralAppraisal.Application.Common.CQRS;

/// <summary>
/// Opt-in interface za komande koje trebaju automatski audit log putem AuditBehavior-a.
///
/// KADA implementirati:
///   • Samo na komandama čiji handleri DIREKTNO implementuju logiku (ne delegiraju na servis).
///   • Ako komanda delegira na servis koji već poziva IAuditService interno, NE implementovati
///     ovaj interfejs — servis već audira s bogatijim kontekstom (EntityDisplayName, OldValues).
///
/// Trenutno stanje: nijedna komanda ne implementuje ovaj interfejs jer svi handleri
/// delegiraju na servise koji sami audiraju. Koristiti za buduće handlere koji logiku
/// implementiraju direktno bez posredničkog servisa.
/// </summary>
public interface IAuditableCommand
{
    string AuditAction         { get; }
    string AuditEntityType     { get; }
    string? AuditEntityKey     { get; }
    string AuditModule         { get; }
    string AuditOperationType  { get; }
    string AuditSeverity       { get; }
}
