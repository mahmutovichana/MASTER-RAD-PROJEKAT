namespace RBBH.CollateralAppraisal.Application.Audit;

/// <summary>
/// Tip operacije — opisuje PRIRODU izmjene, ne poslovni kontekst.
/// Koristi se zajedno s AuditActions za precizno filtriranje.
/// Npr. Action = ORDER_ASSIGNED_BY_SYSTEM, OperationType = Assign.
/// </summary>
public static class AuditOperationTypes
{
    public const string Create       = "Create";
    public const string Read         = "Read";
    public const string Update       = "Update";
    public const string Delete       = "Delete";
    public const string Assign       = "Assign";
    public const string Remove       = "Remove";
    public const string Approve      = "Approve";
    public const string Reject       = "Reject";
    public const string Cancel       = "Cancel";
    public const string Sync         = "Sync";
    public const string Import       = "Import";
    public const string Export       = "Export";
    public const string Process      = "Process";
    public const string AccessDenied = "AccessDenied";
    public const string Login        = "Login";
    public const string Logout       = "Logout";
}
