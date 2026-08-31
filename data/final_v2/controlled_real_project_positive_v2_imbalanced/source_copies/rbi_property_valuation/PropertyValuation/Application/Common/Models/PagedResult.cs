namespace RBBH.CollateralAppraisal.Application.Common.Models;

/// <summary>
/// Stranicirani rezultat pretrage ili listanja.
/// Vraća se iz svih endpointa koji podržavaju paginaciju.
/// </summary>
public sealed class PagedResult<T>
{
    /// <summary>Stavke na trenutnoj stranici.</summary>
    public required IReadOnlyList<T> Items { get; init; }

    /// <summary>Ukupan broj zapisa koji odgovaraju kriterijima (bez paginacije).</summary>
    public required int TotalCount { get; init; }

    /// <summary>Trenutna stranica (1-based).</summary>
    public required int Page { get; init; }

    /// <summary>Broj zapisa po stranici.</summary>
    public required int PageSize { get; init; }

    /// <summary>Ukupan broj stranica.</summary>
    public int TotalPages => PageSize > 0
        ? (int)Math.Ceiling((double)TotalCount / PageSize)
        : 0;

    public bool HasPreviousPage => Page > 1;
    public bool HasNextPage     => Page < TotalPages;

    /// <summary>Kreira prazan rezultat (nema zapisa koji odgovaraju kriterijima).</summary>
    public static PagedResult<T> Empty(int page, int pageSize) => new()
    {
        Items      = [],
        TotalCount = 0,
        Page       = page,
        PageSize   = pageSize
    };
}
