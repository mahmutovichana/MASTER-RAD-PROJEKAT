﻿using RBBH.CollateralAppraisal.Domain.Common;

namespace RBBH.CollateralAppraisal.Domain.Documents;

/// <summary>
/// Šablon/urnek dokumenta — narudžbenica, izjava, urneci za procjenu.
/// Dostupan u kućici "Dokumentacija za pregled". Vještak ima pristup samo urnecima.
/// CO može ažurirati urneke.
/// </summary>
using System.Diagnostics.CodeAnalysis;
[ExcludeFromCodeCoverage]
public sealed class DocumentTemplate : BaseEntity
{
    public string Code { get; private set; } = null!;
    public string Name { get; private set; } = null!;
    public string? Description { get; private set; }
    public string Category { get; private set; } = null!;
    public string FileName { get; private set; } = null!;
    public string ContentType { get; private set; } = null!;
    public long FileSize { get; private set; }
    public string StoragePath { get; private set; } = null!;
    public int SortOrder { get; private set; }
    public bool IsActive { get; private set; } = true;

    /// <summary>Koje role mogu preuzeti ovaj template. Null = sve role.</summary>
    public string? AllowedRoles { get; private set; }

    private DocumentTemplate() { }

    public static DocumentTemplate Create(
        string code, string name, string? description, string category,
        string fileName, string contentType, long fileSize, string storagePath,
        int sortOrder = 0, string? allowedRoles = null)
    {
        return new DocumentTemplate
        {
            Code        = code,
            Name        = name,
            Description = description,
            Category    = category,
            FileName    = fileName,
            ContentType = contentType,
            FileSize    = fileSize,
            StoragePath = storagePath,
            SortOrder   = sortOrder,
            AllowedRoles = allowedRoles
        };
    }

    public void Update(string name, string? description, string fileName,
        string contentType, long fileSize, string storagePath, DateTime now)
    {
        Name        = name;
        Description = description;
        FileName    = fileName;
        ContentType = contentType;
        FileSize    = fileSize;
        StoragePath = storagePath;
        SetUpdatedAt(now);
    }

    public void Deactivate(DateTime now) { IsActive = false; SetUpdatedAt(now); }
}

public static class TemplateCategories
{
    public const string Workflow = "workflow";
    public const string Urnek   = "urnek";
}

public static class TemplateCodes
{
    public const string Narudzbenica  = "NARUDZBENICA";
    public const string NarudzbenicaBr = "NARUDZBENICA_BR";
    public const string Izjava        = "IZJAVA";
    public const string IzjavaSukob   = "IZJAVA_SUKOB_INTERESA";
    public const string UrnekNekretnine1 = "URNEK_NEKRETNINE_1";
    public const string UrnekNekretnine2 = "URNEK_NEKRETNINE_2";
    public const string UrnekNekretnine3 = "URNEK_NEKRETNINE_3";
    public const string UrnekNekretnine4 = "URNEK_NEKRETNINE_4";
    public const string UrnekNekretnine5 = "URNEK_NEKRETNINE_5";
    public const string UrnekNekretnine6 = "URNEK_NEKRETNINE_6";
    public const string UrnekPokretna7   = "URNEK_POKRETNA_7";
    public const string UrnekNekretnine8 = "URNEK_NEKRETNINE_8";
}
