﻿using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Documents;
using RBBH.CollateralAppraisal.Application.Documents.Dtos;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using DomainDocument = RBBH.CollateralAppraisal.Domain.Documents.Document;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Documents;

[ExcludeFromCodeCoverage]
public sealed class OrderDocumentGeneratorService : IOrderDocumentGenerator
{
    private readonly ApplicationDbContext   _db;
    private readonly IFileStorageProvider   _storage;
    private readonly ICurrentUserService    _currentUser;
    private readonly IAuditService          _audit;
    private readonly ILogger<OrderDocumentGeneratorService> _logger;

    public OrderDocumentGeneratorService(
        ApplicationDbContext db,
        IFileStorageProvider storage,
        ICurrentUserService currentUser,
        IAuditService audit,
        ILogger<OrderDocumentGeneratorService> logger)
    {
        _db          = db;
        _storage     = storage;
        _currentUser = currentUser;
        _audit       = audit;
        _logger      = logger;
    }

    public async Task<OrderDocumentGenerationResult> GenerateAsync(
        int orderId, OrderDocumentGenerationRequest request, CancellationToken ct = default)
    {
        var userId = _currentUser.IsAuthenticated ? _currentUser.UserId : null;

        var order = await _db.AppraisalOrders
            .AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == orderId, ct)
            ?? throw new NotFoundException($"Narudžba ID={orderId} nije pronaÄ‘ena.", "ORDER_NOT_FOUND");

        var protocol = await _db.OrderProtocolEntries
            .AsNoTracking()
            .FirstOrDefaultAsync(p => p.OrderId == orderId, ct)
            ?? throw new ConflictException(
                "Protokol narudžbe mora biti kreiran prije generisanja dokumenata.",
                "PROTOCOL_NOT_FOUND");

        var collateralLabel = await ResolveCodebookLabelAsync(order.CollateralTypeId, ct);
        var combinedLabel   = await ResolveCodebookLabelAsync(order.CombinedCollateralTypeId, ct);

        var narudzbenicaTypeId = await ResolveDocumentTypeIdAsync("NARUDZBENICA", ct);

        var subPath = $"appraisal-orders/{orderId}/documents";
        var generated = new List<DocumentDto>();

        // Spec (Sekcija 4): iznos naknade se ćita iz Protokola narudžbi (polje "Naknada", kolona U) i
        // pojavljuje se na više mjesta u narudžbenici — ne unosi se rućno. Ako poziv nije proslijedio iznos,
        // automatski koristimo AppraisalFee iz narudžbe da se eliminiše rućni unos i prepisivanje.
        var effectiveRequest = request with { Iznos = request.Iznos ?? order.AppraisalFee };

        var narudzbenicaDoc = await GenerateAndSaveAsync(
            order, protocol, collateralLabel, combinedLabel,
            effectiveRequest, narudzbenicaTypeId, subPath, userId,
            GenerateNarudzbenica, $"Narudzbenica_{order.OrderNumber.Replace("/", "-")}.docx", ct);
        generated.Add(narudzbenicaDoc);

        var izjavaDoc = await GenerateAndSaveAsync(
            order, protocol, collateralLabel, combinedLabel,
            effectiveRequest, narudzbenicaTypeId, subPath, userId,
            GenerateIzjava, $"Izjava_{order.OrderNumber.Replace("/", "-")}.docx", ct);
        generated.Add(izjavaDoc);

        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(order, generated, ct);

        return new OrderDocumentGenerationResult(
            order.Id, order.OrderNumber, generated,
            $"Generisana narudžbenica i izjava za narudžbu {order.OrderNumber}.");
    }

    private async Task<DocumentDto> GenerateAndSaveAsync(
        AppraisalOrder order, OrderProtocolEntry protocol,
        string? collateralLabel, string? combinedLabel,
        OrderDocumentGenerationRequest request,
        int? documentTypeId, string subPath, string? userId,
        Func<AppraisalOrder, OrderProtocolEntry, string?, string?, OrderDocumentGenerationRequest, MemoryStream> generator,
        string fileName, CancellationToken ct)
    {
        using var docStream = generator(order, protocol, collateralLabel, combinedLabel, request);
        docStream.Position = 0;

        var storageResult = await _storage.SaveAsync(docStream, fileName, subPath, ct);

        var doc = DomainDocument.Create(
            orderId:          order.Id,
            documentTypeId:   documentTypeId,
            fileName:         fileName,
            originalFileName: fileName,
            contentType:      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            fileSize:         storageResult.FileSize,
            storagePath:      storageResult.StoragePath,
            uploadedByUserId: userId);

        _db.Documents.Add(doc);
        await _db.SaveChangesAsync(ct);

        return new DocumentDto(
            doc.Id, doc.AppraisalOrderId, doc.DocumentTypeId,
            doc.FileName, doc.OriginalFileName, doc.ContentType, doc.FileSize,
            doc.UploadedAt, doc.UploadedByUserId,
            $"/api/documents/{doc.Id}/download",
            doc.Version, doc.PreviousVersionId, doc.IsActive);
    }

    // â”€â”€ Narudžbenica â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    private static MemoryStream GenerateNarudzbenica(
        AppraisalOrder order, OrderProtocolEntry protocol,
        string? collateralLabel, string? combinedLabel,
        OrderDocumentGenerationRequest request)
    {
        var ms = new MemoryStream();
        using (var doc = WordprocessingDocument.Create(ms, WordprocessingDocumentType.Document, true))
        {
            var mainPart = doc.AddMainDocumentPart();
            mainPart.Document = new DocumentFormat.OpenXml.Wordprocessing.Document();
            var body = mainPart.Document.AppendChild(new Body());

            AddTitle(body, "NARUDŽBENICA ZA PROCJENU NEKRETNINE");
            AddEmptyLine(body);

            AddField(body, "Broj protokola", protocol.ProtocolNumber);
            AddField(body, "Datum", protocol.GeneratedAt.ToString("dd.MM.yyyy"));
            AddEmptyLine(body);

            AddSectionTitle(body, "PODACI O KLIJENTU");
            AddField(body, "Naziv klijenta", order.ClientName);
            AddField(body, "Kontakt osoba", order.ContactName);
            AddField(body, "Kontakt telefon", order.ContactPhone);
            AddField(body, "Kontakt e-mail", order.ContactEmail);
            AddField(body, "JMBG / Matićni broj", order.ClientIdentifier);
            AddEmptyLine(body);

            AddSectionTitle(body, "PODACI O NEKRETNINI");
            AddField(body, "Tip kolaterala", combinedLabel ?? collateralLabel ?? "—");
            AddField(body, "Adresa nekretnine", order.PropertyAddress);
            AddField(body, "Grad", order.PropertyCity ?? order.City);
            AddEmptyLine(body);

            AddSectionTitle(body, "PODACI O DOSTAVI");
            AddField(body, "Adresa za dostavu", order.BranchAddress ?? order.Branch);
            AddField(body, "Kontakt za dostavu", order.DeliveryContactName);
            AddField(body, "AM primalac", order.AmRecipientName);
            AddEmptyLine(body);

            var iznos = request.Iznos?.ToString("N2") ?? "________________";
            AddSectionTitle(body, "FINANSIJSKI PODACI");
            AddField(body, "Iznos procjene (KM)", iznos);
            AddField(body, "Iznos sa PDV-om (KM)", iznos);
            AddField(body, "Iznos uplate (KM)", iznos);
            AddField(body, "Ukupan iznos (KM)", iznos);
            AddEmptyLine(body);

            AddSectionTitle(body, "POSLOVNICA");
            AddField(body, "Poslovnica", order.Branch);
            AddField(body, "Adresa poslovnice", order.BranchAddress);
            AddField(body, "Inicijator narudžbe", order.CreatedByName);
            AddEmptyLine(body);
            AddEmptyLine(body);

            AddField(body, "Potpis CA", "________________________");
            AddField(body, "Datum", DateTime.UtcNow.ToString("dd.MM.yyyy"));
        }

        return ms;
    }

    // â”€â”€ Izjava â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    private static MemoryStream GenerateIzjava(
        AppraisalOrder order, OrderProtocolEntry protocol,
        string? collateralLabel, string? combinedLabel,
        OrderDocumentGenerationRequest request)
    {
        var ms = new MemoryStream();
        using (var doc = WordprocessingDocument.Create(ms, WordprocessingDocumentType.Document, true))
        {
            var mainPart = doc.AddMainDocumentPart();
            mainPart.Document = new DocumentFormat.OpenXml.Wordprocessing.Document();
            var body = mainPart.Document.AppendChild(new Body());

            AddTitle(body, "IZJAVA");
            AddEmptyLine(body);

            AddParagraph(body,
                $"U vezi narudžbe procjene nekretnine broj {protocol.ProtocolNumber}, " +
                "izjavljujem sljedeće:");
            AddEmptyLine(body);

            AddSectionTitle(body, "PODACI O NEKRETNINI");
            AddField(body, "Tip kolaterala", combinedLabel ?? collateralLabel ?? "—");
            AddField(body, "Adresa nekretnine", order.PropertyAddress);
            AddField(body, "Grad", order.PropertyCity ?? order.City);
            AddField(body, "ZK oznaka", request.ZkOznaka ?? "________________");
            AddEmptyLine(body);

            AddSectionTitle(body, "PODACI O KLIJENTU");
            AddField(body, "Naziv klijenta", order.ClientName);
            AddField(body, "JMBG / Matićni broj", order.ClientIdentifier);
            AddEmptyLine(body);

            AddParagraph(body,
                "PotvrÄ‘ujem da su gore navedeni podaci taćni i potpuni.");
            AddEmptyLine(body);
            AddEmptyLine(body);

            AddField(body, "Potpis", "________________________");
            AddField(body, "Datum", DateTime.UtcNow.ToString("dd.MM.yyyy"));
            AddField(body, "Mjesto", order.PropertyCity ?? order.City ?? "");
        }

        return ms;
    }

    // â”€â”€ OpenXml pomoćne metode â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    private static void AddTitle(Body body, string text)
    {
        var run = new Run(new Text(text));
        run.RunProperties = new RunProperties(
            new Bold(),
            new FontSize { Val = "32" });
        var para = new Paragraph(run);
        para.ParagraphProperties = new ParagraphProperties(
            new Justification { Val = JustificationValues.Center },
            new SpacingBetweenLines { After = "200" });
        body.Append(para);
    }

    private static void AddSectionTitle(Body body, string text)
    {
        var run = new Run(new Text(text));
        run.RunProperties = new RunProperties(
            new Bold(),
            new FontSize { Val = "24" },
            new Underline { Val = UnderlineValues.Single });
        var para = new Paragraph(run);
        para.ParagraphProperties = new ParagraphProperties(
            new SpacingBetweenLines { Before = "200", After = "100" });
        body.Append(para);
    }

    private static void AddField(Body body, string label, string? value)
    {
        var labelRun = new Run(new Text($"{label}: ") { Space = SpaceProcessingModeValues.Preserve });
        labelRun.RunProperties = new RunProperties(new Bold(), new FontSize { Val = "22" });

        var valueRun = new Run(new Text(value ?? "—"));
        valueRun.RunProperties = new RunProperties(new FontSize { Val = "22" });

        var para = new Paragraph(labelRun, valueRun);
        para.ParagraphProperties = new ParagraphProperties(
            new SpacingBetweenLines { After = "60" });
        body.Append(para);
    }

    private static void AddParagraph(Body body, string text)
    {
        var run = new Run(new Text(text));
        run.RunProperties = new RunProperties(new FontSize { Val = "22" });
        var para = new Paragraph(run);
        para.ParagraphProperties = new ParagraphProperties(
            new SpacingBetweenLines { After = "100" });
        body.Append(para);
    }

    private static void AddEmptyLine(Body body)
    {
        body.Append(new Paragraph());
    }

    // â”€â”€ Pomoćne metode â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    private async Task<string?> ResolveCodebookLabelAsync(int? codebookValueId, CancellationToken ct)
    {
        if (codebookValueId is null) return null;
        return await _db.CodebookValues
            .AsNoTracking()
            .Where(v => v.Id == codebookValueId.Value)
            .Select(v => v.Label)
            .FirstOrDefaultAsync(ct);
    }

    private async Task<int?> ResolveDocumentTypeIdAsync(string code, CancellationToken ct)
    {
        return await _db.CodebookValues
            .AsNoTracking()
            .Where(v => v.CodebookKey == Application.Common.Constants.CodebookKeys.DocumentTypes && v.Code == code)
            .Select(v => (int?)v.Id)
            .FirstOrDefaultAsync(ct);
    }

    private async Task RecordAuditAsync(
        AppraisalOrder order, List<DocumentDto> generated, CancellationToken ct)
    {
        try
        {
            await _audit.RecordAsync(new AuditEvent
            {
                Action            = AuditActions.DocumentUploaded,
                OperationType     = AuditOperationTypes.Create,
                Module            = AuditModules.AppraisalOrders,
                EntityType        = "AppraisalOrder",
                EntityKey         = order.Id.ToString(),
                EntityDisplayName = order.OrderNumber,
                NewValues         = new
                {
                    Action = "ORDER_DOCUMENTS_GENERATED",
                    Documents = generated.Select(d => new { d.Id, d.FileName }).ToList()
                },
                Status   = AuditStatuses.Success,
                Severity = AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Audit za generisanje dokumenata narudžbe {OrderId} nije zapisan.", order.Id);
        }
    }
}
