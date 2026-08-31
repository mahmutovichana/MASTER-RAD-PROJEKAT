using RBBH.CollateralAppraisal.Domain.Common;

namespace RBBH.CollateralAppraisal.Domain.Orders;


/// <summary>
/// Task / kućica vezana za narudžbu procjene.
/// Svaki korak workflowa kreira task koji se dodjeljuje roli ili korisniku.
/// Prihvatanje je ekskluzivno — jedan korisnik zaključava task (IsLocked).
/// </summary>
public sealed class TaskItem : BaseEntity, IConcurrencyAware
{
    public uint RowVersion { get; private set; }
    public int AppraisalOrderId { get; private set; }
    public AppraisalOrder? AppraisalOrder { get; private set; }  // Navigation property
    public TaskItemType TaskType { get; private set; }
    public string Title { get; private set; } = null!;
    public string? Description { get; private set; }

    // ── Dodjela ────────────────────────────────────────────────────────────
    public string? AssignedRole { get; private set; }
    public string? AssignedUserId { get; private set; }

    // ── Status ─────────────────────────────────────────────────────────────
    public TaskItemStatus Status { get; private set; }

    // ── Vremenski žig ──────────────────────────────────────────────────────
    public DateTime? AcceptedAt { get; private set; }
    public string? AcceptedByUserId { get; private set; }
    public DateTime? CompletedAt { get; private set; }
    public string? CompletedByUserId { get; private set; }
    public DateTime? DueDate { get; private set; }

    // ── Komentar ───────────────────────────────────────────────────────────
    public string? Comment { get; private set; }

    // ── Zaključan (drugi korisnik ga je prihvatio) ─────────────────────────
    public bool IsLocked { get; private set; }

    private TaskItem() { }

    public static TaskItem Create(
        int orderId,
        TaskItemType type,
        string title,
        string? description,
        string? assignedRole,
        DateTime? dueDate = null,
        string? assignedUserId = null)
    {
        return new TaskItem
        {
            AppraisalOrderId = orderId,
            TaskType         = type,
            Title            = title,
            Description      = description,
            AssignedRole     = assignedRole,
            AssignedUserId   = assignedUserId,
            Status           = TaskItemStatus.Open,
            DueDate          = dueDate
        };
    }

    public void Accept(string userId, DateTime now)
    {
        Status           = TaskItemStatus.Accepted;
        AcceptedByUserId = userId;
        AcceptedAt       = now;
        AssignedUserId   = userId;
        IsLocked         = true;
        SetUpdatedAt(now);
    }

    public void Complete(string userId, string? comment, DateTime now)
    {
        Status            = TaskItemStatus.Completed;
        CompletedByUserId = userId;
        CompletedAt       = now;
        Comment           = comment;
        SetUpdatedAt(now);
    }

    public void Return(string? comment, DateTime now)
    {
        Status   = TaskItemStatus.Returned;
        Comment  = comment;
        IsLocked = false;
        SetUpdatedAt(now);
    }

    public void Cancel(DateTime now)
    {
        Status = TaskItemStatus.Cancelled;
        SetUpdatedAt(now);
    }
}

public enum TaskItemStatus
{
    Open       = 0,
    Accepted   = 1,
    InProgress = 2,
    Completed  = 3,
    Returned   = 4,
    Cancelled  = 5
}

public enum TaskItemType
{
    AcceptCAOrder             = 1,
    ReviewDocumentation       = 2,
    ReturnForCorrection       = 3,
    CorrectDocumentation      = 4,
    AccessCheckCO             = 5,
    FillMandatoryCAFields     = 6,
    GenerateProtocol          = 7,
    GenerateOrderDocuments    = 8,
    SelectAppraiser           = 9,
    SendOrderToAppraiser      = 10,
    AdditionalPayment         = 11,
    UploadFinalAppraisal      = 12,
    ApproveFinalAppraisal     = 13,
    ConfirmOriginalReceived   = 14,
    RequestOpinion            = 15,
    SubmitOpinion             = 16,
    SendThankYou              = 17,
    UploadInvoice             = 18,
    SendInvoiceForPayment     = 19,
    ConfirmInvoicePaid        = 20,
    AppraiserRejected         = 21,
    ReworkAppraisal           = 22,
    ImportSignedDocuments     = 23,
    AcceptAppraiserOrder      = 24,
    ConfirmAdditionalPayment  = 25,
    DeliverOriginalToOffice   = 26
}