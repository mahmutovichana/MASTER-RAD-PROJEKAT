namespace RBBH.CollateralAppraisal.Application.Audit;

/// <summary>
/// Moduli aplikacije koji generišu audit događaje.
/// Pokriva: US1 Login, US2 Role Management, US3 Validacije/Sigurnost, US4 Sifarnici i buduće module.
/// </summary>
public static class AuditModules
{
    public const string Users            = "Users";
    public const string Roles            = "Roles";
    public const string Security         = "Security";
    public const string Codebooks        = "Codebooks";
    public const string AppraisalOrders  = "AppraisalOrders";
    public const string Documents        = "Documents";
    public const string System           = "System";
}
