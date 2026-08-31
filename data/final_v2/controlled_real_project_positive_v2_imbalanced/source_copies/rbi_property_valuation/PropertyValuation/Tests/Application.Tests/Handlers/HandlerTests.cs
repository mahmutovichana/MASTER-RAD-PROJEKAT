// Handler unit testovi â€” klase ekvivalencije
// Svaki thin handler ima jednu klasu: "ispravna komanda â†’ delegira na servis".
// Validatori: valid-class (prolazi), invalid-class po pravilu (pada).
using FluentValidation;
using MediatR;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Abstractions;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.AccessCheck.Commands;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.AppraiserAssignment.Commands;
using RBBH.CollateralAppraisal.Application.AppraiserAssignment.Queries;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.CaDocumentReview.Commands;
using RBBH.CollateralAppraisal.Application.Common.Behaviors;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Invoice.Commands;
using RBBH.CollateralAppraisal.Application.Invoice.Queries;
using RBBH.CollateralAppraisal.Application.Opinions;
using RBBH.CollateralAppraisal.Application.Opinions.Commands;
using RBBH.CollateralAppraisal.Application.Opinions.Dtos;
using RBBH.CollateralAppraisal.Application.Opinions.Queries;
using RBBH.CollateralAppraisal.Application.OrderApproval.Commands;
using RBBH.CollateralAppraisal.Application.OrderApproval.Queries;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Commands;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Application.Orders.Queries;
using RBBH.CollateralAppraisal.Application.Orders.Requests;
using RBBH.CollateralAppraisal.Application.OriginalAppraisal.Commands;
using RBBH.CollateralAppraisal.Application.QuoteRequests.Commands;
using RBBH.CollateralAppraisal.Application.QuoteRequests.Queries;
using RBBH.CollateralAppraisal.Application.WorkflowTask.Commands;
using RBBH.CollateralAppraisal.Application.WorkflowTask.Queries;
using RBBH.CollateralAppraisal.Domain.Orders;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Handlers;

// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
// AccessCheck handlers
// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

public sealed class AccessCheckHandlerTests
{
    private readonly IAccessCheckService _svc = Substitute.For<IAccessCheckService>();

    [Fact]
    public async Task ApproveAccessCheck_DelegatesToService()
    {
        _svc.ApproveAccessAsync(1, "ok", default).Returns(Task.FromResult<CaDocumentReviewResultDto>(null!));
        await new ApproveAccessCheckCommandHandler(_svc)
            .Handle(new ApproveAccessCheckCommand(1, "ok"), default);
        await _svc.Received(1).ApproveAccessAsync(1, "ok", default);
    }

    [Fact]
    public async Task RejectAccessCheck_DelegatesToService()
    {
        _svc.RejectAccessAsync(1, "razlog", default).Returns(Task.FromResult<CaDocumentReviewResultDto>(null!));
        await new RejectAccessCheckCommandHandler(_svc)
            .Handle(new RejectAccessCheckCommand(1, "razlog"), default);
        await _svc.Received(1).RejectAccessAsync(1, "razlog", default);
    }
}

// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
// AppraiserAssignment handlers
// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

public sealed class AppraiserAssignmentHandlerTests
{
    private readonly IAppraiserAssignmentService _svc = Substitute.For<IAppraiserAssignmentService>();

    [Fact]
    public async Task AcceptByAppraiser_DelegatesToService()
    {
        _svc.AcceptByAppraiserAsync(1, default).Returns(Task.FromResult<SendToAppraiserResultDto>(null!));
        await new AcceptByAppraiserCommandHandler(_svc).Handle(new AcceptByAppraiserCommand(1), default);
        await _svc.Received(1).AcceptByAppraiserAsync(1, default);
    }

    [Fact]
    public async Task AutoSelectAppraiser_DelegatesToService()
    {
        _svc.AutoSelectAppraiserAsync(1, default).Returns(Task.FromResult<AppraiserAssignmentResultDto>(null!));
        await new AutoSelectAppraiserCommandHandler(_svc).Handle(new AutoSelectAppraiserCommand(1), default);
        await _svc.Received(1).AutoSelectAppraiserAsync(1, default);
    }

    [Fact]
    public async Task CompleteSignedDocumentImport_DelegatesToService()
    {
        _svc.CompleteSignedDocumentImportAsync(1, default).Returns(Task.FromResult<SendToAppraiserResultDto>(null!));
        await new CompleteSignedDocumentImportCommandHandler(_svc)
            .Handle(new CompleteSignedDocumentImportCommand(1), default);
        await _svc.Received(1).CompleteSignedDocumentImportAsync(1, default);
    }

    [Fact]
    public async Task ConfirmAdditionalPayment_DelegatesToService()
    {
        _svc.ConfirmAdditionalPaymentAsync(1, default).Returns(Task.FromResult<SendToAppraiserResultDto>(null!));
        await new ConfirmAdditionalPaymentCommandHandler(_svc)
            .Handle(new ConfirmAdditionalPaymentCommand(1), default);
        await _svc.Received(1).ConfirmAdditionalPaymentAsync(1, default);
    }

    [Fact]
    public async Task ManualSelectAppraiser_DelegatesToService()
    {
        _svc.ManualSelectAppraiserAsync(1, 5, default).Returns(Task.FromResult<AppraiserAssignmentResultDto>(null!));
        await new ManualSelectAppraiserCommandHandler(_svc)
            .Handle(new ManualSelectAppraiserCommand(1, 5), default);
        await _svc.Received(1).ManualSelectAppraiserAsync(1, 5, default);
    }

    [Fact]
    public async Task RejectByAppraiser_DelegatesToService()
    {
        var reason = AppraiserDeclineReason.OstaliRazlozi;
        _svc.RejectByAppraiserAsync(1, reason, null, default).Returns(Task.FromResult<SendToAppraiserResultDto>(null!));
        await new RejectByAppraiserCommandHandler(_svc)
            .Handle(new RejectByAppraiserCommand(1, reason), default);
        await _svc.Received(1).RejectByAppraiserAsync(1, reason, null, default);
    }

    [Fact]
    public async Task RequestAdditionalPayment_DelegatesToService()
    {
        _svc.RequestAdditionalPaymentAsync(1, default).Returns(Task.FromResult<SendToAppraiserResultDto>(null!));
        await new RequestAdditionalPaymentCommandHandler(_svc)
            .Handle(new RequestAdditionalPaymentCommand(1), default);
        await _svc.Received(1).RequestAdditionalPaymentAsync(1, default);
    }

    [Fact]
    public async Task SendToAppraiser_DelegatesToService()
    {
        _svc.SendToAppraiserAsync(1, default).Returns(Task.FromResult<SendToAppraiserResultDto>(null!));
        await new SendToAppraiserCommandHandler(_svc).Handle(new SendToAppraiserCommand(1), default);
        await _svc.Received(1).SendToAppraiserAsync(1, default);
    }

    [Fact]
    public async Task SubmitAppraisal_DelegatesToService()
    {
        _svc.SubmitAppraisalAsync(1, null, default).Returns(Task.FromResult<SendToAppraiserResultDto>(null!));
        await new SubmitAppraisalCommandHandler(_svc).Handle(new SubmitAppraisalCommand(1), default);
        await _svc.Received(1).SubmitAppraisalAsync(1, null, default);
    }

    [Fact]
    public async Task GetCandidatesForOrder_DelegatesToService()
    {
        IReadOnlyList<AppraiserDto> list = [];
        _svc.GetCandidatesForOrderAsync(1, default).Returns(Task.FromResult(list));
        var result = await new GetCandidatesForOrderQueryHandler(_svc)
            .Handle(new GetCandidatesForOrderQuery(1), default);
        Assert.Empty(result);
    }

    [Fact]
    public async Task GetAppraiserPackage_DelegatesToService()
    {
        _svc.GetAppraiserPackageAsync(1, default).Returns(Task.FromResult<AppraiserPackageDto>(null!));
        await new GetAppraiserPackageQueryHandler(_svc)
            .Handle(new GetAppraiserPackageQuery(1), default);
        await _svc.Received(1).GetAppraiserPackageAsync(1, default);
    }
}

// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
// CaDocumentReview handlers
// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

public sealed class CaDocumentReviewHandlerTests
{
    private readonly ICaDocumentReviewService _svc = Substitute.For<ICaDocumentReviewService>();

    [Fact]
    public async Task CompleteDocumentReview_DelegatesToService()
    {
        _svc.CompleteReviewAsync(1, default).Returns(Task.FromResult<CaDocumentReviewResultDto>(null!));
        await new CompleteDocumentReviewCommandHandler(_svc)
            .Handle(new CompleteDocumentReviewCommand(1), default);
        await _svc.Received(1).CompleteReviewAsync(1, default);
    }

    [Fact]
    public async Task RequestCorrection_DelegatesToService()
    {
        _svc.RequestCorrectionAsync(1, 2, null, default).Returns(Task.FromResult<CaDocumentReviewResultDto>(null!));
        await new RequestCorrectionCommandHandler(_svc)
            .Handle(new RequestCorrectionCommand(1, 2, null), default);
        await _svc.Received(1).RequestCorrectionAsync(1, 2, null, default);
    }

    [Fact]
    public async Task SubmitCorrection_DelegatesToService()
    {
        _svc.SubmitCorrectionAsync(1, "komentar", default).Returns(Task.FromResult<CaDocumentReviewResultDto>(null!));
        await new SubmitCorrectionCommandHandler(_svc)
            .Handle(new SubmitCorrectionCommand(1, "komentar"), default);
        await _svc.Received(1).SubmitCorrectionAsync(1, "komentar", default);
    }
}

// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
// Invoice handlers
// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

public sealed class InvoiceHandlerTests
{
    private readonly IInvoiceWorkflowService _svc = Substitute.For<IInvoiceWorkflowService>();

    [Fact]
    public async Task ConfirmInvoicePaid_DelegatesToService()
    {
        _svc.ConfirmPaidAsync(1, default).Returns(Task.FromResult<InvoiceWorkflowResultDto>(null!));
        await new ConfirmInvoicePaidCommandHandler(_svc).Handle(new ConfirmInvoicePaidCommand(1), default);
        await _svc.Received(1).ConfirmPaidAsync(1, default);
    }

    [Fact]
    public async Task SendInvoiceForPayment_DelegatesToService()
    {
        _svc.SendForPaymentAsync(1, default).Returns(Task.FromResult<InvoiceWorkflowResultDto>(null!));
        await new SendInvoiceForPaymentCommandHandler(_svc)
            .Handle(new SendInvoiceForPaymentCommand(1), default);
        await _svc.Received(1).SendForPaymentAsync(1, default);
    }

    [Fact]
    public async Task UploadInvoice_DelegatesToService()
    {
        _svc.UploadInvoiceAsync(1, 7, default).Returns(Task.FromResult<InvoiceWorkflowResultDto>(null!));
        await new UploadInvoiceCommandHandler(_svc).Handle(new UploadInvoiceCommand(1, 7), default);
        await _svc.Received(1).UploadInvoiceAsync(1, 7, default);
    }

    [Fact]
    public async Task GetInvoiceStatus_DelegatesToService()
    {
        _svc.GetStatusAsync(1, default).Returns(Task.FromResult<InvoiceStatusDto>(null!));
        await new GetInvoiceStatusQueryHandler(_svc).Handle(new GetInvoiceStatusQuery(1), default);
        await _svc.Received(1).GetStatusAsync(1, default);
    }
}

// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
// Opinions handlers
// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

public sealed class OpinionHandlerTests
{
    private readonly IOpinionService _svc = Substitute.For<IOpinionService>();

    [Fact]
    public async Task RequestOpinions_DelegatesToService()
    {
        await new RequestOpinionsCommandHandler(_svc).Handle(new RequestOpinionsCommand(1), default);
        await _svc.Received(1).RequestOpinionsAsync(1, default);
    }

    [Fact]
    public async Task SubmitOpinion_DelegatesToService()
    {
        var cmd = new SubmitOpinionCommand(1, OpinionType.CO, [0x01], "f.pdf", "application/pdf", null, "user-1");
        await new SubmitOpinionCommandHandler(_svc).Handle(cmd, default);
        await _svc.Received(1).SubmitOpinionAsync(
            1, OpinionType.CO, Arg.Any<Stream>(), "f.pdf", "application/pdf", null, "user-1", default);
    }

    [Fact]
    public async Task GetOpinions_DelegatesToService()
    {
        _svc.GetOpinionsAsync(1, default).Returns(Task.FromResult(new List<OpinionDto>()));
        var result = await new GetOpinionsQueryHandler(_svc).Handle(new GetOpinionsQuery(1), default);
        Assert.Empty(result);
    }
}

// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
// OrderApproval handlers
// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

public sealed class OrderApprovalHandlerTests
{
    private readonly IOrderApprovalService _svc = Substitute.For<IOrderApprovalService>();

    [Fact]
    public async Task ApproveFinalAppraisal_DelegatesToService()
    {
        _svc.ApproveFinalAppraisalAsync(1, 4, default).Returns(Task.FromResult<ApproveFinalAppraisalResultDto>(null!));
        await new ApproveFinalAppraisalCommandHandler(_svc)
            .Handle(new ApproveFinalAppraisalCommand(1, 4), default);
        await _svc.Received(1).ApproveFinalAppraisalAsync(1, 4, default);
    }

    [Fact]
    public async Task ReturnForRework_DelegatesToService()
    {
        _svc.ReturnForReworkAsync(1, "SadrÅ¾aj", "Komentar", default).Returns(Task.FromResult<ReturnForReworkResultDto>(null!));
        await new ReturnForReworkCommandHandler(_svc)
            .Handle(new ReturnForReworkCommand(1, "SadrÅ¾aj", "Komentar"), default);
        await _svc.Received(1).ReturnForReworkAsync(1, "SadrÅ¾aj", "Komentar", default);
    }

    [Fact]
    public async Task GetFinalAppraisal_DelegatesToService()
    {
        _svc.GetFinalAppraisalAsync(1, default).Returns(Task.FromResult<FinalAppraisalDto>(null!));
        await new GetFinalAppraisalQueryHandler(_svc).Handle(new GetFinalAppraisalQuery(1), default);
        await _svc.Received(1).GetFinalAppraisalAsync(1, default);
    }
}

// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
// OriginalAppraisal handlers
// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

public sealed class OriginalAppraisalHandlerTests
{
    private readonly IOriginalAppraisalService _svc = Substitute.For<IOriginalAppraisalService>();

    [Fact]
    public async Task ConfirmOriginalReceived_DelegatesToService()
    {
        _svc.ConfirmOriginalReceivedAsync(1, default).Returns(Task.FromResult<OriginalReceivedResultDto>(null!));
        await new ConfirmOriginalReceivedCommandHandler(_svc)
            .Handle(new ConfirmOriginalReceivedCommand(1), default);
        await _svc.Received(1).ConfirmOriginalReceivedAsync(1, default);
    }

    [Fact]
    public async Task SendAppraiserReminder_DelegatesToService()
    {
        _svc.SendAppraiserReminderAsync(1, default).Returns(Task.FromResult<AppraiserReminderResultDto>(null!));
        await new SendAppraiserReminderCommandHandler(_svc)
            .Handle(new SendAppraiserReminderCommand(1), default);
        await _svc.Received(1).SendAppraiserReminderAsync(1, default);
    }
}

// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
// QuoteRequests handlers
// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

public sealed class QuoteRequestsHandlerTests
{
    private readonly IQuoteRequestService _svc = Substitute.For<IQuoteRequestService>();

    [Fact]
    public async Task AcceptQuote_DelegatesToService()
    {
        _svc.AcceptQuoteAsync(1, 2, default).Returns(Task.FromResult<AcceptQuoteResult>(null!));
        await new AcceptQuoteCommandHandler(_svc).Handle(new AcceptQuoteCommand(1, 2), default);
        await _svc.Received(1).AcceptQuoteAsync(1, 2, default);
    }

    [Fact]
    public async Task SendQuoteRequests_DelegatesToService()
    {
        var deadline = DateTime.UtcNow.AddDays(3);
        _svc.SendQuoteRequestsAsync(1, Arg.Any<SendQuoteRequestsInput>(), default)
            .Returns(Task.FromResult<SendQuoteRequestsResult>(null!));
        await new SendQuoteRequestsCommandHandler(_svc)
            .Handle(new SendQuoteRequestsCommand(1, [5, 6], deadline), default);
        await _svc.Received(1).SendQuoteRequestsAsync(1, Arg.Any<SendQuoteRequestsInput>(), default);
    }

    [Fact]
    public async Task SendThankYou_DelegatesToService()
    {
        _svc.SendThankYouAsync(1, default).Returns(Task.FromResult<SendThankYouResult>(null!));
        await new SendThankYouCommandHandler(_svc).Handle(new SendThankYouCommand(1), default);
        await _svc.Received(1).SendThankYouAsync(1, default);
    }

    [Fact]
    public async Task GetQuoteRequests_DelegatesToService()
    {
        IReadOnlyList<QuoteRequestDto> list = [];
        _svc.GetByOrderAsync(1, default).Returns(Task.FromResult(list));
        var result = await new GetQuoteRequestsQueryHandler(_svc)
            .Handle(new GetQuoteRequestsQuery(1), default);
        Assert.Empty(result);
    }
}

// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
// WorkflowTask handlers
// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

public sealed class WorkflowTaskHandlerTests
{
    private readonly IWorkflowTaskService _svc = Substitute.For<IWorkflowTaskService>();

    [Fact]
    public async Task AcceptTask_DelegatesToService()
    {
        _svc.AcceptTaskAsync(1, default).Returns(Task.FromResult<WorkflowTaskDto>(null!));
        await new AcceptTaskCommandHandler(_svc).Handle(new AcceptTaskCommand(1), default);
        await _svc.Received(1).AcceptTaskAsync(1, default);
    }

    [Fact]
    public async Task CompleteTask_DelegatesToService()
    {
        _svc.CompleteTaskAsync(1, "ok", default).Returns(Task.FromResult<WorkflowTaskDto>(null!));
        await new CompleteTaskCommandHandler(_svc).Handle(new CompleteTaskCommand(1, "ok"), default);
        await _svc.Received(1).CompleteTaskAsync(1, "ok", default);
    }

    [Fact]
    public async Task GetMyTasks_DelegatesToService()
    {
        var paged = new PagedResult<WorkflowTaskDto> { Items = [], TotalCount = 0, Page = 1, PageSize = 20 };
        _svc.GetMyTasksAsync(1, 20, default).Returns(Task.FromResult(paged));
        var result = await new GetMyTasksQueryHandler(_svc).Handle(new GetMyTasksQuery(1, 20), default);
        Assert.Equal(0, result.TotalCount);
    }
}

// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
// Orders â€” handlers koji nisu pokriti Api.Tests-om
// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

public sealed class OrdersExtraHandlerTests
{
    private readonly IAppraisalOrderService _orderSvc = Substitute.For<IAppraisalOrderService>();
    private readonly IOrderQueryService     _querySvc = Substitute.For<IOrderQueryService>();

    [Fact]
    public async Task CancelOrder_DelegatesToService()
    {
        await new CancelOrderCommandHandler(_orderSvc).Handle(new CancelOrderCommand(1), default);
        await _orderSvc.Received(1).CancelAsync(1, default);
    }

    [Fact]
    public async Task CreateDraftOrder_DelegatesToService()
    {
        _orderSvc.CreateDraftAsync(null, default).Returns(Task.FromResult<AppraisalOrderDto>(null!));
        await new CreateDraftOrderCommandHandler(_orderSvc).Handle(new CreateDraftOrderCommand(), default);
        await _orderSvc.Received(1).CreateDraftAsync(null, default);
    }

    [Fact]
    public async Task SubmitOrder_DelegatesToService()
    {
        _orderSvc.SubmitAsync(1, default).Returns(Task.FromResult<AppraisalOrderDto>(null!));
        await new SubmitOrderCommandHandler(_orderSvc).Handle(new SubmitOrderCommand(1), default);
        await _orderSvc.Received(1).SubmitAsync(1, default);
    }

    [Fact]
    public async Task UpdateDraftOrder_DelegatesToService()
    {
        var req = new UpdateOrderRequest(null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null);
        _orderSvc.UpdateDraftAsync(1, req, false, default).Returns(Task.FromResult<AppraisalOrderDto>(null!));
        await new UpdateDraftOrderCommandHandler(_orderSvc)
            .Handle(new UpdateDraftOrderCommand(1, req, false), default);
        await _orderSvc.Received(1).UpdateDraftAsync(1, req, false, default);
    }

    [Fact]
    public async Task GetOrderDetail_DelegatesToService()
    {
        _querySvc.GetByIdAsync(1, default).Returns(Task.FromResult<AppraisalOrderDetailDto>(null!));
        await new GetOrderDetailQueryHandler(_querySvc).Handle(new GetOrderDetailQuery(1), default);
        await _querySvc.Received(1).GetByIdAsync(1, default);
    }

    [Fact]
    public async Task GetOrderSummary_DelegatesToService()
    {
        _querySvc.GetSummaryAsync(default).Returns(Task.FromResult<OrderSummaryDto>(null!));
        await new GetOrderSummaryQueryHandler(_querySvc).Handle(new GetOrderSummaryQuery(), default);
        await _querySvc.Received(1).GetSummaryAsync(default);
    }
}

// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
// Validators â€” klase ekvivalencije
// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

public sealed class ValidatorTests
{
    // â”€â”€ RejectAccessCheckCommandValidator â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    [Fact]
    public void RejectAccessCheck_Valid_Passes()
    {
        var r = new RejectAccessCheckCommandValidator().Validate(new RejectAccessCheckCommand(1, "razlog"));
        Assert.True(r.IsValid);
    }

    [Fact]
    public void RejectAccessCheck_AllInvalid_Fails()
    {
        var r = new RejectAccessCheckCommandValidator().Validate(new RejectAccessCheckCommand(0, ""));
        Assert.False(r.IsValid);
        Assert.Contains(r.Errors, e => e.PropertyName == "OrderId");
        Assert.Contains(r.Errors, e => e.PropertyName == "Comment");
    }

    [Fact]
    public void RejectAccessCheck_CommentTooLong_Fails()
    {
        var r = new RejectAccessCheckCommandValidator().Validate(
            new RejectAccessCheckCommand(1, new string('x', 2001)));
        Assert.False(r.IsValid);
        Assert.Contains(r.Errors, e => e.PropertyName == "Comment");
    }

    // â”€â”€ ManualSelectAppraiserCommandValidator â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    [Fact]
    public void ManualSelectAppraiser_Valid_Passes()
        => Assert.True(new ManualSelectAppraiserCommandValidator()
            .Validate(new ManualSelectAppraiserCommand(1, 5)).IsValid);

    [Fact]
    public void ManualSelectAppraiser_ZeroIds_Fails()
    {
        var r = new ManualSelectAppraiserCommandValidator().Validate(new ManualSelectAppraiserCommand(0, 0));
        Assert.False(r.IsValid);
        Assert.Equal(2, r.Errors.Count);
    }

    // â”€â”€ RejectByAppraiserCommandValidator â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    [Fact]
    public void RejectByAppraiser_Valid_Passes()
        => Assert.True(new RejectByAppraiserCommandValidator()
            .Validate(new RejectByAppraiserCommand(1, AppraiserDeclineReason.OstaliRazlozi)).IsValid);

    [Fact]
    public void RejectByAppraiser_InvalidOrderId_Fails()
    {
        var r = new RejectByAppraiserCommandValidator()
            .Validate(new RejectByAppraiserCommand(0, AppraiserDeclineReason.Bolest));
        Assert.False(r.IsValid);
        Assert.Contains(r.Errors, e => e.PropertyName == "OrderId");
    }

    [Fact]
    public void RejectByAppraiser_InvalidEnum_Fails()
    {
        var r = new RejectByAppraiserCommandValidator()
            .Validate(new RejectByAppraiserCommand(1, (AppraiserDeclineReason)999));
        Assert.False(r.IsValid);
        Assert.Contains(r.Errors, e => e.PropertyName == "Reason");
    }

    // â”€â”€ RequestCorrectionCommandValidator â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    [Fact]
    public void RequestCorrection_Valid_Passes()
        => Assert.True(new RequestCorrectionCommandValidator()
            .Validate(new RequestCorrectionCommand(1, 2, null)).IsValid);

    [Fact]
    public void RequestCorrection_ZeroIds_Fails()
    {
        var r = new RequestCorrectionCommandValidator().Validate(new RequestCorrectionCommand(0, 0, null));
        Assert.False(r.IsValid);
        Assert.Equal(2, r.Errors.Count);
    }

    // â”€â”€ ApproveFinalAppraisalCommandValidator â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    [Fact]
    public void ApproveFinalAppraisal_NullRating_Passes()
        => Assert.True(new ApproveFinalAppraisalCommandValidator()
            .Validate(new ApproveFinalAppraisalCommand(1, null)).IsValid);

    [Fact]
    public void ApproveFinalAppraisal_ValidRating_Passes()
        => Assert.True(new ApproveFinalAppraisalCommandValidator()
            .Validate(new ApproveFinalAppraisalCommand(1, 3)).IsValid);

    [Fact]
    public void ApproveFinalAppraisal_ZeroOrderId_Fails()
        => Assert.False(new ApproveFinalAppraisalCommandValidator()
            .Validate(new ApproveFinalAppraisalCommand(0, null)).IsValid);

    [Fact]
    public void ApproveFinalAppraisal_RatingOutOfRange_Fails()
    {
        // ocjena 6 â€” izvan klase [1-5]
        var r = new ApproveFinalAppraisalCommandValidator()
            .Validate(new ApproveFinalAppraisalCommand(1, 6));
        Assert.False(r.IsValid);
    }

    // â”€â”€ ReturnForReworkCommandValidator â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    [Fact]
    public void ReturnForRework_Valid_Passes()
        => Assert.True(new ReturnForReworkCommandValidator()
            .Validate(new ReturnForReworkCommand(1, "SadrÅ¾aj", "Komentar")).IsValid);

    [Fact]
    public void ReturnForRework_AllEmpty_Fails()
    {
        var r = new ReturnForReworkCommandValidator().Validate(new ReturnForReworkCommand(0, "", ""));
        Assert.False(r.IsValid);
        Assert.Equal(3, r.Errors.Count);
    }

    [Fact]
    public void ReturnForRework_CommentTooLong_Fails()
    {
        var r = new ReturnForReworkCommandValidator()
            .Validate(new ReturnForReworkCommand(1, "SadrÅ¾aj", new string('x', 2001)));
        Assert.False(r.IsValid);
        Assert.Contains(r.Errors, e => e.PropertyName == "Comment");
    }

    // â”€â”€ SendQuoteRequestsCommandValidator â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    [Fact]
    public void SendQuoteRequests_Valid_Passes()
        => Assert.True(new SendQuoteRequestsCommandValidator()
            .Validate(new SendQuoteRequestsCommand(1, [5, 6], DateTime.UtcNow.AddDays(1))).IsValid);

    [Fact]
    public void SendQuoteRequests_EmptyList_Fails()
    {
        var r = new SendQuoteRequestsCommandValidator()
            .Validate(new SendQuoteRequestsCommand(1, [], DateTime.UtcNow.AddDays(1)));
        Assert.False(r.IsValid);
        Assert.Contains(r.Errors, e => e.PropertyName == "AppraiserIds");
    }

    [Fact]
    public void SendQuoteRequests_DeadlineInPast_Fails()
    {
        var r = new SendQuoteRequestsCommandValidator()
            .Validate(new SendQuoteRequestsCommand(1, [5], DateTime.UtcNow.AddDays(-1)));
        Assert.False(r.IsValid);
        Assert.Contains(r.Errors, e => e.PropertyName == "Deadline");
    }

    [Fact]
    public void SendQuoteRequests_InvalidAppraiserId_Fails()
    {
        var r = new SendQuoteRequestsCommandValidator()
            .Validate(new SendQuoteRequestsCommand(1, [0], DateTime.UtcNow.AddDays(1)));
        Assert.False(r.IsValid);
        Assert.Contains(r.Errors, e => e.PropertyName == "AppraiserIds");
    }

    // â”€â”€ UpdateDraftOrderCommandValidator â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    private static UpdateOrderRequest EmptyRequest()
        => new(null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null);

    [Fact]
    public void UpdateDraftOrder_Valid_Passes()
        => Assert.True(new UpdateDraftOrderCommandValidator()
            .Validate(new UpdateDraftOrderCommand(1, EmptyRequest())).IsValid);

    [Fact]
    public void UpdateDraftOrder_ZeroOrderId_Fails()
        => Assert.False(new UpdateDraftOrderCommandValidator()
            .Validate(new UpdateDraftOrderCommand(0, EmptyRequest())).IsValid);

    [Fact]
    public void UpdateDraftOrder_ClientNameTooLong_Fails()
    {
        var r = new UpdateDraftOrderCommandValidator().Validate(
            new UpdateDraftOrderCommand(1,
                new UpdateOrderRequest(new string('x', 301), null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null)));
        Assert.False(r.IsValid);
        Assert.Contains(r.Errors, e => e.PropertyName.Contains("clientName", StringComparison.OrdinalIgnoreCase));
    }
}

// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
// AuditBehavior â€” pokriva audit putanju (IAuditableCommand branch)
// â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

file sealed record FakeCmd : IRequest<string>;

file sealed record AuditCmd : IRequest<string>, IAuditableCommand
{
    public string AuditAction        => "TestAction";
    public string AuditEntityType    => "TestEntity";
    public string? AuditEntityKey    => "1";
    public string AuditModule        => "Tests";
    public string AuditOperationType => "Create";
    public string AuditSeverity      => "Low";
}

public sealed class AuditBehaviorTests
{
    private readonly IAuditService _audit = Substitute.For<IAuditService>();

    [Fact]
    public async Task NonAuditableCommand_SkipsAudit()
    {
        var behavior = new AuditBehavior<FakeCmd, string>(_audit, NullLogger<AuditBehavior<FakeCmd, string>>.Instance);
        var result = await behavior.Handle(new FakeCmd(), () => Task.FromResult("ok"), default);
        Assert.Equal("ok", result);
        await _audit.DidNotReceive().RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task AuditableCommand_RecordsAuditAfterHandler()
    {
        var behavior = new AuditBehavior<AuditCmd, string>(_audit, NullLogger<AuditBehavior<AuditCmd, string>>.Instance);
        var result = await behavior.Handle(new AuditCmd(), () => Task.FromResult("done"), default);
        Assert.Equal("done", result);
        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == "TestAction"), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task AuditableCommand_AuditThrows_LogsAndReturnsResult()
    {
        _audit.RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>())
              .Returns(Task.FromException(new InvalidOperationException("db down")));
        var behavior = new AuditBehavior<AuditCmd, string>(_audit, NullLogger<AuditBehavior<AuditCmd, string>>.Instance);
        var result = await behavior.Handle(new AuditCmd(), () => Task.FromResult("safe"), default);
        Assert.Equal("safe", result);
    }
}
